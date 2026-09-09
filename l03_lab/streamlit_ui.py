# -*- coding: utf-8 -*-
"""
L03 — Streamlit UI for the RAG lab.
Tabs: 📤 Upload & Ingest | 📄 Documents | 💬 Query | 📊 Evaluation | ⚙️ About
Run:  streamlit run streamlit_ui.py
"""
import os
import sys
import json
import uuid

# Must be set BEFORE chromadb/onnx import (macOS deadlock fix).
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import pandas as pd
import streamlit as st

st.set_page_config(page_title="L03 — RAG Lab", page_icon="🧪", layout="wide")

# --- guard FIRST: refuse to run outside the pinned venv (importing
#     chromadb/streamlit combos from a global env segfaults at browser
#     connect) ---
if ".venv" not in sys.prefix:
    st.error("⚠️ هذه الواجهة تعمل فقط من بيئة venv الخاصة بالمختبر.\n\n"
             "شغّل: **`./run_ui.sh`** — أو:\n\n"
             "```bash\nsource .venv/bin/activate\nstreamlit run streamlit_ui.py\n```")
    st.error("⚠️ This UI must run from the lab's venv.\n\nRun: **`./run_ui.sh`** "
             "— or activate the venv first (see above). A global Python env "
             "crashes with a segfault at browser connect.")
    st.stop()

import chromadb
import chromadb.telemetry.product.posthog as _ph
_ph.posthog.capture = lambda *a, **k: None  # no-op: offline lab

import rag_api as rag
import etl_pipeline as etl

RAW_DIR = etl.SOURCE_DOCS
AR = "اسم الملف غير المدعوم — الصيغ: TXT/MD/CSV/PDF"
EN = "Unsupported file — formats: TXT/MD/CSV/PDF"



# ----------------------------------------------------------------- helpers
def supported(name):
    return name.lower().endswith((".txt", ".md", ".csv", ".pdf"))


@st.cache_resource
def get_collection():
    return rag.col


col = get_collection()


def list_documents():
    """Distinct documents currently indexed in the Gold layer."""
    if col.count() == 0:
        return []
    got = col.get(include=["metadatas"])
    docs = {}
    for m in got["metadatas"]:
        d = m["doc"]
        docs[d] = docs.get(d, 0) + 1
    return sorted(docs.items())


def ingest_file(path, name):
    """Run Bronze → Silver → Gold for a single new file, then index it.

    Uses rag.client (the SAME PersistentClient that owns rag.col) to drop +
    recreate the collection — a batched delete+add on a used HNSW segment is
    what deadlocked SQLite in Chroma 0.5.x. Batched encode+insert with both
    console logs (terminal) and Streamlit progress (browser).
    """
    import sqlalchemy
    import time
    engine = sqlalchemy.create_engine(etl.DB_URL)
    bronze_df = etl.bronze(engine)          # re-ingests all raw docs (replace mode)
    silver_df = etl.silver(engine, bronze_df)
    print("[Gold] rebuilding collection 'gold_chunks'...", flush=True)
    # Drop + recreate via the SAME client (no 2nd PersistentClient → no lock fight)
    try:
        rag.client.delete_collection("gold_chunks")
        print("[Gold] old collection dropped.", flush=True)
    except Exception as e:
        print(f"[Gold] (no old collection to drop: {e})", flush=True)
    global col
    fresh = rag.client.get_or_create_collection(
        "gold_chunks", embedding_function=rag.ef,
        metadata={"hnsw:space": "cosine"})
    col = fresh
    # batched encode + insert with Streamlit progress + console log
    ids = silver_df["chunk_id"].tolist()
    docs = silver_df["text"].tolist()
    metas = [{"doc": d, "idx": int(i)} for d, i in
             zip(silver_df["doc_name"], silver_df["chunk_idx"])]
    prog = st.progress(0.0, text="Gold: تضمين وفهرسة / embedding & indexing…")
    B = 10
    for s in range(0, len(ids), B):
        lo = docs[s:s + B]
        t0 = time.time()
        print(f"[Gold]  encode {s + 1}..{min(s + B, len(ids))}/{len(ids)} ...",
              flush=True)
        embs = rag.ef(lo)
        print(f"[Gold]  encoded in {time.time() - t0:.1f}s, inserting...",
              flush=True)
        fresh.add(ids=ids[s:s + B], documents=lo,
                  embeddings=embs, metadatas=metas[s:s + B])
        done = min(s + B, len(ids))
        print(f"[Gold]  ... {done}/{len(ids)} done", flush=True)
        prog.progress(done / len(ids), text=f"Gold: {done}/{len(ids)} مقطعًا / chunks…")
    prog.empty()
    print(f"[Gold] ChromaDB HNSW index ready: {fresh.count()} vectors.", flush=True)
    try:
        rag.col = fresh  # keep rag.retrieve()/evaluate() on the new collection
        rag._cache.clear()
    except Exception:
        pass
    # refresh cached sidebar metrics
    try:
        st.cache_resource.clear()
    except Exception:
        pass
    return len(silver_df)


# ----------------------------------------------------------------- sidebar
with st.sidebar:
    st.title("🧪 L03 — RAG Lab")
    st.caption("Bronze → Silver → Gold → /query — محلي بالكامل / fully local")
    n = col.count()
    st.metric("مقاطع مفهرسة / indexed chunks", n)
    st.metric("مستندات / documents", len(list_documents()))
    st.divider()
    st.caption(f"المولّد / generator: `{rag.GENERATOR}`\n\n"
               f"النموذج / model: `{rag.OPENROUTER_MODEL if rag.GENERATOR == 'openrouter' else os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}`")
    st.caption(f"الكاش الدلالي / semantic cache: {len(rag._cache)} إدخال/entries")

tab_up, tab_docs, tab_q, tab_eval, tab_about = st.tabs(
    ["📤 رفع مستند / Upload", "📄 المستندات / Documents",
     "💬 استعلام / Query", "📊 التقييم / Evaluation", "⚙️ حول / About"])

# ------------------------------------------------------- 1) Upload & ingest
with tab_up:
    st.header("📤 رفع مستند جديد / Upload a new document")
    st.caption("الصيغ: TXT / MD / CSV / PDF — يُحفظ في data/raw ثم يُفهرس عبر "
               "Bronze→Silver→Gold / Saved to data/raw then indexed "
               "through Bronze→Silver→Gold")
    up = st.file_uploader("اختر ملفًا / choose a file",
                          type=["txt", "md", "csv", "pdf"])
    if up is not None and st.button("⬆️ رفع وفهرسة / Upload & Ingest",
                                    type="primary"):
        if not supported(up.name):
            st.error(f"❌ {AR} / {EN}")
        else:
            os.makedirs(RAW_DIR, exist_ok=True)
            path = os.path.join(RAW_DIR, up.name)
            with open(path, "wb") as f:
                f.write(up.getvalue())
            with st.spinner("جارٍ الفهرسة… / indexing…"):
                try:
                    n_chunks = ingest_file(path, up.name)
                    st.success(f"✅ فُهرس `{up.name}` — {n_chunks} مقطعًا في Gold "
                               f"/ indexed — {n_chunks} chunks in Gold")
                except Exception as e:
                    st.error(f"فشل الفهرسة / ingestion failed: `{e}`")

# ------------------------------------------------------------- 2) Documents
with tab_docs:
    st.header("📄 المستندات المفهرسة / Indexed documents")
    docs = list_documents()
    if not docs:
        st.warning("لا توجد مستندات بعد — ارفع واحدًا من تبويب الرفع. "
                   "/ No documents yet — upload one from the Upload tab.")
    else:
        df = pd.DataFrame([{"المستند / document": d, "المقاطع / chunks": c}
                           for d, c in docs])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.divider()
        st.subheader("معاينة المقاطع / Inspect chunks")
        sel = st.selectbox("اختر مستندًا / pick a document", [d for d, _ in docs])
        if sel:
            got = col.get(where={"doc": sel}, include=["documents", "metadatas"])
            rows = sorted(zip(got["ids"], got["documents"],
                              [m["idx"] for m in got["metadatas"]]),
                          key=lambda r: r[2])
            for cid, text, idx in rows:
                with st.expander(f"مقطع {idx} — {cid[:8]}…"):
                    st.write(text)

# ------------------------------------------------------------------ 3) Query
with tab_q:
    st.header("💬 استعلام RAG / RAG query")
    q = st.text_area("سؤالك / your question", height=90,
                     placeholder="مثال: ما الاستراتيجية الموصى بها لتقسيم النصوص؟")
    k = st.slider("عدد المقاطع المسترجعة / top-k", 1, 10, rag.TOP_K)
    if st.button("🔎 أرسل / Ask", type="primary") and q.strip():
        with st.spinner("استرجاع + توليد… / retrieval + generation…"):
            try:
                hits = rag.retrieve(q, k=k)
                if not hits:
                    st.warning("لا توجد معلومات كافية في الفهرس للإجابة. "
                               "/ No relevant context found.")
                else:
                    cached = any(rag._similarity(q, cq) >= rag.CACHE_SIM
                                 for cq, _ in rag._cache)
                    answer = rag.generate(q, hits)
                    rag._cache.append((q, answer))
                    st.markdown("#### الإجابة / Answer")
                    st.success(answer)
                    st.caption("💾 من الكاش الدلالي / from semantic cache"
                               if cached else "🆕 توليد جديد / fresh generation")
                    st.markdown("#### المصادر / Sources")
                    for i, h in enumerate(hits, 1):
                        st.markdown(f"**[{i}]** `{h['source']}` — "
                                    f"تشابه / score `{h['score']}`")
                        with st.expander("النص المسترجع / retrieved text"):
                            st.write(h["text"])
            except Exception as e:
                st.error(f"خطأ / error: `{e}`")

# ------------------------------------------------------------- 4) Evaluation
with tab_eval:
    st.header("📊 التقييم مقابل المجموعة المرجعية / Golden-dataset evaluation")
    st.caption("12 سؤالًا — دقة السياق + العثور على المصدر المتوقع "
               "/ context precision + expected-source hit")
    if st.button("▶️ شغّل التقييم / Run evaluation", type="primary"):
        with open(rag.GOLDEN, encoding="utf-8") as f:
            data = json.load(f)
        rows, prog = [], st.progress(0.0)
        for i, item in enumerate(data["items"], 1):
            hits = rag.retrieve(item.get("question_en") or item["question"])
            expected = item["expected_source"]
            hit_ok = any(h["source"].endswith(expected.split("/")[-1])
                         for h in hits)
            prec = round(sum(h["score"] for h in hits) / len(hits), 2) if hits else 0
            rows.append({"#": item["id"], "السؤال / question": item["question"],
                         "precision": prec, "source found": "✅" if hit_ok else "❌"})
            prog.progress(i / len(data["items"]))
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        c1, c2 = st.columns(2)
        c1.metric("متوسط دقة السياق / avg context precision",
                  round(sum(r["precision"] for r in rows) / len(rows), 2))
        c2.metric("نسبة العثور على المصدر / source-hit rate",
                  f"{sum(1 for r in rows if r['source found'] == '✅') / len(rows):.0%}")
        st.info("❌ لا تعني فشلًا دائمًا: قد لا تكون إجابة السؤال في المستندات المفهرسة — "
                "ارفع مستنداتك. / ❌ doesn't always mean failure: the answer may simply "
                "not be in the indexed docs — upload yours.")

# ------------------------------------------------------------------ 5) About
with tab_about:
    st.header("⚙️ حول المختبر / About the lab")
    st.markdown("""
**المعمارية / Architecture:** Bronze (SQLite خام) → Silver (تنظيف + تقسيم تكراري) →
Gold (HNSW cosine في ChromaDB) → استرجاع كثيف → موجِّه مقيَّد بالمصادر → كاش دلالي → تقييم.
""")
    st.markdown("- **API:** `uvicorn rag_api:app --reload` → http://localhost:8000/docs\n"
                "- **CLI evaluation:** `python rag_api.py evaluate`\n"
                "- **Setup guide:** `../L03_Environment_Setup_Guide.md`")
    st.caption("التوليد عبر OpenRouter الخطة المجانية — المفتاح في .env (لا يُرفع إلى Git). "
               "/ Generation via OpenRouter free tier — key in .env (never committed).")
