# -*- coding: utf-8 -*-
"""
L03 — Mini ETL pipeline: Bronze → Silver → Gold (local, no Docker).
- Bronze: raw documents stored unmodified in SQLite (built into Python).
- Silver: cleaned, deduplicated, recursively chunked.
- Gold: embeddings + HNSW vector index in local ChromaDB.

Run:  python etl_pipeline.py
"""
import os
import json
import logging
import re
import uuid

import pandas as pd
from sqlalchemy import create_engine, text

from rapidfuzz import fuzz

import chromadb
import chromadb.telemetry.product.posthog as _ph
_ph.posthog.capture = lambda *a, **k: None  # no-op: offline lab, no telemetry
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# ONNX/tokenizers deadlock fix on macOS (M1/M2): single-thread + no fork parallelism.
# Must be set before onnxruntime does heavy work.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

# pypdf logs one "Ignoring wrong pointing object ... (offset 0)" line per malformed
# cross-reference entry it recovers from (common in PowerPoint-exported PDFs). These
# are harmless recovery notices, not failures — but they flood stderr, so silence them.
logging.getLogger("pypdf._reader").setLevel(logging.ERROR)

DB_URL = os.getenv("DB_URL", "sqlite:///./l03_lab.db")  # SQLite: built into Python
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")
SOURCE_DOCS = os.getenv("SOURCE_DOCS", "./data/raw")

# ---------------------------------------------------------------- Bronze
def bronze(engine):
    """Ingest raw documents (txt/md/pdf/csv) unmodified."""
    rows = []
    os.makedirs(SOURCE_DOCS, exist_ok=True)
    for name in sorted(os.listdir(SOURCE_DOCS)):
        path = os.path.join(SOURCE_DOCS, name)
        if not os.path.isfile(path):
            continue
        if name.lower().endswith((".txt", ".md", ".csv")):
            with open(path, encoding="utf-8", errors="ignore") as f:
                content = f.read()
        elif name.lower().endswith(".pdf"):
            from pypdf import PdfReader
            content = "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)
        else:
            continue
        rows.append({"doc_id": str(uuid.uuid4()), "name": name,
                     "content": content, "ts": pd.Timestamp.utcnow()})
    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit(
            f"[Bronze] لا توجد مستندات في {SOURCE_DOCS} — أضف ملفات txt/md/csv/pdf ثم أعد التشغيل.\n"
            f"[Bronze] No documents found in {SOURCE_DOCS} — add .txt/.md/.csv/.pdf files and re-run."
        )
    df.to_sql("bronze_docs", engine, if_exists="replace", index=False)
    print(f"[Bronze] {len(df)} raw documents stored unmodified.")
    return df


# ---------------------------------------------------------------- Silver
def recursive_chunk(text_, chunk_size=500, overlap=50):
    """Recursive chunking (recommended default): paragraphs → sentences → hard split."""
    if len(text_) <= chunk_size:
        return [text_]
    chunks, current = [], ""
    for para in re.split(r"\n\s*\n", text_):          # 1) paragraphs
        if len(current) + len(para) <= chunk_size:
            current += para + "\n\n"
            continue
        for sent in re.split(r"(?<=[.!?؟])\s+", para):  # 2) sentences
            if len(current) + len(sent) > chunk_size:
                if current:
                    chunks.append(current.strip())
                current = current[-overlap:] if overlap else ""
            current += sent + " "
        chunks.append(current.strip())
        current = ""
    if current.strip():
        chunks.append(current.strip())
    return [c for c in chunks if c]


def silver(engine, bronze_df):
    """Clean, normalize, deduplicate, then recursively chunk."""
    docs = bronze_df.drop_duplicates(subset=["content"]).copy()
    docs["content"] = (docs["content"]
                       .str.replace(r"\r", "", regex=True)
                       .str.replace(r"[ \t]+", " ", regex=True)
                       .str.strip())
    rows = []
    for _, r in docs.iterrows():
        for i, chunk in enumerate(recursive_chunk(r["content"])):
            rows.append({"chunk_id": str(uuid.uuid4()), "doc_name": r["name"],
                         "chunk_idx": i, "text": chunk})
    # near-duplicate chunk removal (fuzzy)
    seen, kept = [], []
    for row in rows:
        if all(fuzz.ratio(row["text"], s["text"]) < 95 for s in seen):
            seen.append(row)
            kept.append(row)
    df = pd.DataFrame(kept)
    df.to_sql("silver_chunks", engine, if_exists="replace", index=False)
    print(f"[Silver] {len(df)} clean chunks ({len(rows) - len(kept)} near-duplicates removed).")
    return df


# ---------------------------------------------------------------- Gold
def gold(silver_df, batch_size=10, progress_cb=None):
    """Embeddings + HNSW index in local ChromaDB (persisted to ./chroma_db).

    Embeddings are computed explicitly (not inside col.add) so a freeze
    can be attributed to encoding vs. sqlite/HNSW insert.
    progress_cb(done:int, total:int) is called after each batch (for Streamlit).
    """
    import time
    import traceback
    print("[Gold] starting... (loading embedding model)", flush=True)
    try:
        client = chromadb.PersistentClient(path=CHROMA_DIR,
                                           settings=Settings(anonymized_telemetry=False))
        print("[Gold] chroma client ready.", flush=True)
        _emb_name = os.getenv("EMBEDDING_MODEL", "").strip() or None
        if _emb_name:
            from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
            ef = SentenceTransformerEmbeddingFunction(model_name=_emb_name)
        else:
            ef = embedding_functions.DefaultEmbeddingFunction()  # local MiniLM (all-MiniLM-L6-v2)
        print("[Gold] embedding function loaded.", flush=True)
        try:
            _probe = ef(["hello"])
            print(f"[Gold] model warm-up OK (dim={len(_probe[0])}).", flush=True)
        except Exception as e:
            print(f"[Gold] ERROR loading embedding model: {e}", flush=True)
            print("[Gold] Hint: first run downloads ~80MB (all-MiniLM-L6-v2) from HuggingFace.",
                  flush=True)
            traceback.print_exc()
            raise SystemExit(1)
        # NOTE: must match rag_api.py collection name ("gold_chunks")
        col = client.get_or_create_collection("gold_chunks",
                                              embedding_function=ef,
                                              metadata={"hnsw:space": "cosine"})
        print(f"[Gold] collection 'gold_chunks' count before insert: {col.count()}", flush=True)
        if col.count() == 0:
            ids = silver_df["chunk_id"].tolist()
            docs = silver_df["text"].tolist()
            metas = [{"doc": d, "idx": int(i)} for d, i in
                     zip(silver_df["doc_name"], silver_df["chunk_idx"])]
            print(f"[Gold] encoding {len(ids)} docs in batches of {batch_size}...",
                  flush=True)
            for s in range(0, len(ids), batch_size):
                lo_docs = docs[s:s + batch_size]
                t0 = time.time()
                print(f"[Gold]  encode {s + 1}..{min(s + batch_size, len(ids))}/{len(ids)} ...",
                      flush=True)
                embs = ef(lo_docs)  # hang here = onnx/tokenizers deadlock
                print(f"[Gold]  encoded in {time.time() - t0:.1f}s, inserting...",
                      flush=True)
                col.add(ids=ids[s:s + batch_size],
                        documents=lo_docs,
                        embeddings=embs,
                        metadatas=metas[s:s + batch_size])
                done = min(s + batch_size, len(ids))
                print(f"[Gold]  ... {done}/{len(ids)} done",
                      flush=True)
                if progress_cb is not None:
                    progress_cb(done, len(ids))
        else:
            print("[Gold] collection already populated — skipping insert "
                  "(delete ./chroma_db to force rebuild).", flush=True)
        print(f"[Gold] ChromaDB HNSW index ready: {col.count()} vectors.", flush=True)
    except SystemExit:
        raise
    except Exception:
        print("[Gold] FAILED with exception:", flush=True)
        traceback.print_exc()
        raise


def main():
    engine = create_engine(DB_URL)
    bronze_df = bronze(engine)
    silver_df = silver(engine, bronze_df)
    gold(silver_df)
    print("ETL complete → run: uvicorn rag_api:app --reload")


if __name__ == "__main__":
    main()
