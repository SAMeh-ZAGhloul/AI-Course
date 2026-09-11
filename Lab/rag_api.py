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

# --- Bilingual: optional multilingual embedding model ---------------------
# Default keeps all-MiniLM-L6-v2 (no rebuild needed). To upgrade semantic
# Arabic search, set EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2,
# delete ./chroma_db and re-run etl_pipeline.py. etl_pipeline.py reads the
# same env var so both sides stay in sync.
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "").strip() or None


def _make_embedding_function():
    if EMBEDDING_MODEL:
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
        return SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    return embedding_functions.DefaultEmbeddingFunction()

ef = _make_embedding_function()
client = chromadb.PersistentClient(path=CHROMA_DIR, settings=_CHROMA_SETTINGS)
col = client.get_or_create_collection("gold_chunks", embedding_function=ef,
                                      metadata={"hnsw:space": "cosine"})

app = FastAPI(title="L03 RAG Endpoint", version="1.1-bilingual")
_cache = []  # [(question, answer)] — demo-grade semantic cache


# ---------------- Bilingual helpers (AR/EN) -------------------------------
import re as _re

_AR_RE = _re.compile(r"[\u0600-\u06FF]")

# Small offline AR->EN glossary so retrieval works even without an LLM key.
AR_TO_EN_GLOSSARY = {
    "قانون حماية البيانات الشخصية": "Personal Data Protection Law PDPL data privacy consent DPIA ROPA",
    "حماية البيانات": "data protection privacy",
    "البيانات الشخصية": "personal data",
    "الخصوصية": "privacy",
    "الموافقة": "consent",
    "ملفات تعريف الارتباط": "cookies consent",
    "تقييم أثر حماية البيانات": "data protection impact assessment DPIA",
    "ما هو": "what is",
    "ما هي": "what is",
    "اشرح": "explain",
    "عرف": "define",
    "المعمارية": "architecture",
    "المتدرجة": "medallion",
    "الطبقات": "layers",
    "التقسيم": "chunking",
    "التكراري": "recursive",
    "النصوص": "text",
    "الاسترجاع": "retrieval",
    "التقييم": "evaluation",
}

AR_ABBREV = {
    "PDPL": "Personal Data Protection Law PDPL",
    "DPIA": "Data Protection Impact Assessment DPIA",
    "ROPA": "Record of Processing Activities ROPA",
    "GDPR": "General Data Protection Regulation GDPR",
}


def detect_lang(text):
    """'ar' if Arabic chars present, else 'en'."""
    return "ar" if _AR_RE.search(text or "") else "en"


def local_ar_to_en(text):
    """Offline glossary-based AR->EN keyword expansion for retrieval."""
    out = text
    for ar, en in AR_TO_EN_GLOSSARY.items():
        if ar in out:
            out = out.replace(ar, " " + en + " ")
    for abbr, exp in AR_ABBREV.items():
        if _re.search(r"\b" + abbr + r"\b", out, _re.IGNORECASE):
            out += " " + exp
    return _re.sub(r"\s+", " ", out).strip()


def llm_translate(text, target="en"):
    """Translate via configured generator. Returns '' on failure (offline-safe)."""
    try:
        if GENERATOR == "openai" and not os.getenv("OPENAI_API_KEY"):
            return ""
        if GENERATOR != "openai" and not os.getenv("OPENROUTER_API_KEY"):
            return ""
        goal = ("English. Reply with ONLY the translation."
                if target == "en" else
                "Modern Standard Arabic. Reply with ONLY the translation.")
        sys_prompt = "You are a translator. Translate the user text to " + goal
        if GENERATOR == "openai":
            from openai import OpenAI
            out = OpenAI().chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "system", "content": sys_prompt},
                          {"role": "user", "content": text}])
            return out.choices[0].message.content.strip()
        import requests
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", timeout=60,
            headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"],
                     "Content-Type": "application/json"},
            json={"model": OPENROUTER_MODEL,
                  "messages": [{"role": "system", "content": sys_prompt},
                               {"role": "user", "content": text}]})
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return ""


def retrieval_queries(question, lang):
    """Ordered query variants for dense search (original + expansions)."""
    variants = [question]
    if lang == "ar":
        local = local_ar_to_en(question)
        if local and local != question:
            variants.append(local)
        llm_en = llm_translate(question, target="en")
        if llm_en and llm_en not in variants:
            variants.append(llm_en)
    elif "PDPL" in (question or "").upper():
        exp = local_ar_to_en(question)
        if exp != question:
            variants.append(exp)
    out, seen = [], set()
    for v in variants:
        if v and v not in seen:
            seen.add(v)
            out.append(v)
    return out


def retrieve(query, k=None):
    k = min(k or TOP_K, col.count())
    if k == 0:
        return []
    lang = detect_lang(query)
    best, seen_ids = [], set()
    for variant in retrieval_queries(query, lang):
        res = col.query(query_texts=[variant], n_results=k)
        for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0],
                                   res["distances"][0]):
            score = 1 - dist  # cosine distance -> similarity
            if score >= MIN_SCORE:
                key = (meta["doc"], doc[:80])
                if key not in seen_ids:
                    seen_ids.add(key)
                    best.append({"text": doc, "source": meta["doc"],
                                 "score": round(score, 3)})
    best.sort(key=lambda h: -h["score"])
    if len(best) < k:
        # offline keyword fallback: catches abbreviations (PDPL/DPIA/ROPA)
        # that dense MiniLM may miss, esp. for Arabic queries.
        try:
            got = col.get(include=["documents", "metadatas"])
            ids = got.get("ids", [])
            toks = [t for t in _re.findall(r"[A-Za-z]{2,}|[\u0600-\u06FF]{3,}",
                                           " ".join(retrieval_queries(query, lang)).upper())]
            stop = {"WHAT", "THE", "AND", "FOR", "WITH", "FROM", "WITH", "QUE",
                    "EST", "WHAT", "هو", "هي", "في", "على", "إلى"}
            toks = [t for t in toks if t not in stop and len(t) > 2]
            scored = []
            for cid, doc, meta in zip(ids, got["documents"], got["metadatas"]):
                key = (meta["doc"], doc[:80])
                if key in seen_ids or not toks:
                    continue
                up = doc.upper()
                hits = sum(1 for t in toks if t in up)
                if hits:
                    scored.append((hits, {"text": doc, "source": meta["doc"],
                                          "score": round(0.21 + 0.05 * hits, 3)}))
            scored.sort(key=lambda x: -x[0])
            for _, h in scored[:max(0, k - len(best))]:
                best.append(h)
        except Exception:
            pass
    return best[:k]


def generate(question, hits):
    context = "\n\n".join(f"[{i+1}] {h['text']} (source: {h['source']})"
                          for i, h in enumerate(hits))
    lang = detect_lang(question)
    lang_rule = ("Answer in Modern Standard Arabic (same language as the question)."
                 if lang == "ar" else
                 "Answer in English (same language as the question).")
    prompt = ("""You are a grounded assistant. Answer ONLY from the context below.
Cite sources as [1], [2]... If the answer is not in the context, say you don't know
(in the user's language).
""" + lang_rule + "\n\nContext:\n" + context + f"\n\nQuestion: {question}\nAnswer:")
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
