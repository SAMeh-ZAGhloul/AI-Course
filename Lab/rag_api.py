# -*- coding: utf-8 -*-
"""
L03 — RAG endpoint (FastAPI /query), fully local & lightweight.
Retrieval: dense search (ChromaDB HNSW) + keyword fallback.
Generation: grounded prompt (OpenRouter free tier by default, OpenAI optional).
Optimization: simple semantic cache (cosine similarity on past questions).
Evaluation: `python rag_api.py evaluate` scores the golden dataset.

Run:  uvicorn rag_api:app --reload
"""
import os
import json

import chromadb
import chromadb.telemetry.product.posthog as _ph
_ph.posthog.capture = lambda *a, **k: None  # no-op: offline lab, no telemetry
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from fastapi import FastAPI
from pydantic import BaseModel

CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")
_CHROMA_SETTINGS = Settings(anonymized_telemetry=False)  # silence telemetry noise

# --- load .env (if present) so students don't need manual exports ---
_ENV = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_ENV):
    with open(_ENV, encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

GENERATOR = os.getenv("GENERATOR", "openrouter")  # "openrouter" | "openai"
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")
GOLDEN = os.getenv("GOLDEN", "./golden_dataset.json")
TOP_K, MIN_SCORE, CACHE_SIM = 5, 0.2, 0.92

ef = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path=CHROMA_DIR, settings=_CHROMA_SETTINGS)
col = client.get_or_create_collection("gold_chunks", embedding_function=ef,
                                      metadata={"hnsw:space": "cosine"})

app = FastAPI(title="L03 RAG Endpoint", version="1.0")
_cache = []  # [(question, answer)] — demo-grade semantic cache


def retrieve(query, k=None):
    k = min(k or TOP_K, col.count())
    if k == 0:
        return []
    res = col.query(query_texts=[query], n_results=k)
    hits = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0],
                               res["distances"][0]):
        score = 1 - dist  # cosine distance → similarity
        if score >= MIN_SCORE:
            hits.append({"text": doc, "source": meta["doc"], "score": round(score, 3)})
    return hits


def generate(question, hits):
    context = "\n\n".join(f"[{i+1}] {h['text']} (source: {h['source']})"
                          for i, h in enumerate(hits))
    prompt = ("""You are a grounded assistant. Answer ONLY from the context below.
Cite sources as [1], [2]... If the answer is not in the context, say you don't know.

Context:
""" + context + f"\n\nQuestion: {question}\nAnswer:")
    if GENERATOR == "openai":
        from openai import OpenAI
        out = OpenAI().chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}])
        return out.choices[0].message.content.strip()
    # OpenRouter (OpenAI-compatible API, free-tier models available)
    import requests
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions", timeout=120,
        headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
                 "Content-Type": "application/json"},
        json={"model": OPENROUTER_MODEL,
              "messages": [{"role": "user", "content": prompt}]})
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


class Query(BaseModel):
    question: str


@app.post("/query")
def query(q: Query):
    # semantic cache: reuse answers to very similar past questions
    if _cache:
        cache_q, cache_a = _cache[-1]
        if _similarity(q.question, cache_q) >= CACHE_SIM:
            return {"answer": cache_a, "cached": True, "sources": []}
    hits = retrieve(q.question)
    if not hits:
        return {"answer": "لا توجد معلومات كافية في الفهرس للإجابة. / No relevant context found.",
                "cached": False, "sources": []}
    answer = generate(q.question, hits)
    _cache.append((q.question, answer))
    return {"answer": answer, "cached": False, "sources": hits}


def _similarity(a, b):
    qe, be = (ef([a])[0], ef([b])[0])
    dot = sum(x * y for x, y in zip(qe, be))
    return dot / ((sum(x * x for x in qe) ** .5) * (sum(x * x for x in be) ** .5))


# -------- evaluation against the golden dataset (RAG-triad-style spot check)
def evaluate():
    with open(GOLDEN, encoding="utf-8") as f:
        data = json.load(f)
    print(f"Evaluating {len(data['items'])} golden questions...\n")
    for item in data["items"]:
        # MiniLM is English-centric: retrieve with the English question when available
        hits = retrieve(item.get("question_en") or item["question"])
        expected = item["expected_source"]
        hit_ok = any(h["source"].endswith(expected.split("/")[-1]) for h in hits)
        prec = round(sum(h["score"] for h in hits) / len(hits), 2) if hits else 0
        print(f"{item['id']:>2}. context_precision≈{prec} "
              f"expected_source_found={hit_ok}  {item['question'][:50]}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "evaluate":
        evaluate()
    else:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
