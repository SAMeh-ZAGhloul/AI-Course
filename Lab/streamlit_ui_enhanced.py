# -*- coding: utf-8 -*-
"""
L03 — Enhanced Educational Streamlit UI for the RAG Lab.
Visually explains all RAG steps: Bronze→Silver→Gold→Retrieval→Generation→Evaluation.
Tabs: 🎓 Educational Flow | 📤 Upload | 📄 Documents | 💬 Query | 📊 Evaluation | ⚙️ About

Run:  streamlit run streamlit_ui_enhanced.py
"""
import os
import sys
import json
import uuid
import time

# Must be set BEFORE chromadb/onnx import (macOS deadlock fix).
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="L03 — RAG Lab Educational", page_icon="🎓", layout="wide")

# --- guard FIRST: refuse to run outside the pinned venv ---
if ".venv" not in sys.prefix:
    st.error("⚠️ هذه الواجهة تعمل فقط من بيئة venv الخاصة بالمختبر.\n\n"
             "شغّل: **`./run_ui.sh`** — أو:\n\n"
             "```bash\nsource .venv/bin/activate\nstreamlit run streamlit_ui_enhanced.py\n```")
    st.error("⚠️ This UI must run from the lab's venv.\n\nRun: **`./run_ui.sh`** "
             "— or activate the venv first. A global Python env crashes with a segfault.")
    st.stop()

import chromadb
import chromadb.telemetry.product.posthog as _ph
_ph.posthog.capture = lambda *a, **k: None  # no-op: offline lab

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
    st.warning("⚠️ Plotly not installed — visualization will be limited. "
               "Install with: pip install plotly")

try:
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

import rag_api as rag
import etl_pipeline as etl

RAW_DIR = etl.SOURCE_DOCS
AR = "اسم الملف غير المدعوم — الصيغ: TXT/MD/CSV/PDF"
EN = "Unsupported file — formats: TXT/MD/CSV/PDF"

# ================================================================= HELPERS
def supported(name):
    return name.lower().endswith((".txt", ".md", ".csv", ".pdf"))


@st.cache_resource
def get_collection():
    return rag.col


col = get_collection()


def list_documents():
    """Distinct documents currently indexed."""
    if col.count() == 0:
        return []
    got = col.get(include=["metadatas"])
    docs = {}
    for m in got["metadatas"]:
        d = m["doc"]
        docs[d] = docs.get(d, 0) + 1
    return sorted(docs.items())


def get_embeddings(texts):
    """Get embeddings for a list of texts."""
    return rag.ef(texts)


def get_all_chunk_embeddings():
    """Retrieve all chunk embeddings from ChromaDB."""
    if col.count() == 0:
        return np.array([]), []
    got = col.get(include=["embeddings", "documents", "metadatas"])
    if len(got["embeddings"]) == 0:
        return np.array([]), []
    return np.array(got["embeddings"]), got["documents"]


def ingest_file(path, name):
    """Run Bronze → Silver → Gold for a single new file."""
    import sqlalchemy
    engine = sqlalchemy.create_engine(etl.DB_URL)
    bronze_df = etl.bronze(engine)
    silver_df = etl.silver(engine, bronze_df)
    print("[Gold] rebuilding collection 'gold_chunks'...", flush=True)
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
        rag.col = fresh
        rag._cache.clear()
    except Exception:
        pass
    try:
        st.cache_resource.clear()
    except Exception:
        pass
    return len(silver_df)


def create_etl_flow_diagram():
    """Create a visual ETL flow diagram."""
    if not HAS_PLOTLY:
        st.info("📊 Plotly required for diagram. Install: `pip install plotly`")
        return
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("🗄️ Bronze<br>(Raw Documents)", 
                       "🧹 Silver<br>(Cleaned & Chunked)", 
                       "🏅 Gold<br>(Indexed Embeddings)"),
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]]
    )
    
    col_count = col.count()
    if col_count == 0:
        docs_count = 0
    else:
        docs_count = len(list_documents())
    
    # Add indicators for each layer
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=docs_count,
            title="Documents",
            number={"font": {"size": 40}},
            domain={"x": [0, 0.33], "y": [0, 1]}
        ),
        row=1, col=1
    )
    
    # Try to get chunk info from database
    try:
        import sqlalchemy
        engine = sqlalchemy.create_engine(etl.DB_URL)
        with engine.connect() as conn:
            try:
                result = conn.execute(sqlalchemy.text("SELECT COUNT(*) as cnt FROM silver_chunks"))
                silver_count = result.fetchone()[0] if result.fetchone() else 0
            except:
                silver_count = 0
    except:
        silver_count = col_count
    
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=silver_count,
            title="Chunks",
            number={"font": {"size": 40}},
            domain={"x": [0.33, 0.66], "y": [0, 1]}
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=col_count,
            title="Indexed Vectors",
            number={"font": {"size": 40}},
            domain={"x": [0.66, 1], "y": [0, 1]}
        ),
        row=1, col=3
    )
    
    fig.update_layout(height=300, showlegend=False, margin=dict(t=100, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)


def create_embedding_visualization():
    """Visualize embeddings using PCA or t-SNE."""
    if col.count() == 0:
        st.warning("No chunks indexed yet. Upload a document first.")
        return
    
    if not HAS_SKLEARN:
        st.info("🔬 scikit-learn required for embedding visualization. Install: `pip install scikit-learn`")
        return
    
    with st.spinner("⏳ Computing embedding projection (this may take a moment)…"):
        embeddings, docs = get_all_chunk_embeddings()
        
        if len(embeddings) == 0:
            st.warning("No embeddings available.")
            return
        
        # Use PCA for faster dimensionality reduction
        if len(embeddings) > 1:
            pca = PCA(n_components=2)
            projected = pca.fit_transform(embeddings)
        else:
            projected = embeddings[:, :2] if embeddings.shape[1] >= 2 else np.column_stack([embeddings[:, 0], np.zeros(len(embeddings))])
        
        # Create color map by document
        doc_names = []
        colors = []
        color_map = {}
        color_palette = px.colors.qualitative.Set1
        
        for meta_idx, doc_text in enumerate(docs):
            doc_names.append(doc_text[:50] + "..." if len(doc_text) > 50 else doc_text)
        
        df_viz = pd.DataFrame({
            "x": projected[:, 0],
            "y": projected[:, 1],
            "text": doc_names,
            "idx": range(len(docs))
        })
        
        fig = px.scatter(
            df_viz,
            x="x", y="y",
            hover_data={"text": True, "idx": True, "x": ":.3f", "y": ":.3f"},
            labels={"x": f"PC1 / Dim 1", "y": f"PC2 / Dim 2"},
            title="📊 Chunk Embedding Space (PCA Projection)",
            height=500
        )
        fig.update_traces(marker=dict(size=8, opacity=0.7))
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"📌 {len(embeddings)} chunks visualized in 2D space using PCA dimensionality reduction")


def create_retrieval_visualization(query, hits):
    """Visualize query retrieval with similarity scores."""
    if not hits or not HAS_PLOTLY:
        return
    
    # Get embeddings
    query_emb = np.array(rag.ef([query])[0])
    
    # Sort by score
    hits_sorted = sorted(hits, key=lambda h: h["score"], reverse=True)
    
    fig = go.Figure()
    
    # Add bar chart for similarity scores
    fig.add_trace(go.Bar(
        x=[f"[{i+1}]" for i in range(len(hits_sorted))],
        y=[h["score"] for h in hits_sorted],
        text=[f"{h['score']:.3f}" for h in hits_sorted],
        textposition="auto",
        marker=dict(
            color=[h["score"] for h in hits_sorted],
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Similarity")
        ),
        hovertext=[h["source"] for h in hits_sorted],
        hoverinfo="text+y"
    ))
    
    fig.update_layout(
        title="🔍 Retrieval Similarity Scores",
        xaxis_title="Retrieved Chunk",
        yaxis_title="Cosine Similarity",
        height=350,
        showlegend=False,
        margin=dict(b=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_rag_flow_diagram():
    """Create a step-by-step RAG flow diagram."""
    if not HAS_PLOTLY:
        return
    
    steps = [
        ("1️⃣ User Query", "text input"),
        ("2️⃣ Embedding", "convert to vector"),
        ("3️⃣ HNSW Search", "cosine similarity"),
        ("4️⃣ Top-K Retrieval", "retrieve top 5"),
        ("5️⃣ Build Context", "format chunks"),
        ("6️⃣ Generate Answer", "LLM with grounding"),
        ("7️⃣ Add Citations", "cite sources"),
        ("8️⃣ Cache Check", "reuse if similar"),
    ]
    
    fig = go.Figure()
    
    y_pos = np.arange(len(steps))
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", 
              "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E2"]
    
    for i, (step, desc) in enumerate(steps):
        fig.add_trace(go.Bar(
            y=[step],
            x=[1],
            orientation="h",
            marker=dict(color=colors[i]),
            text=desc,
            textposition="inside",
            textfont=dict(size=11),
            name=step,
            hovertemplate=f"<b>{step}</b><br>{desc}<extra></extra>"
        ))
    
    fig.update_layout(
        title="🔄 RAG Pipeline Steps",
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=True),
        height=500,
        showlegend=False,
        margin=dict(l=150),
        barmode="overlay"
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ================================================================= SIDEBAR
with st.sidebar:
    st.title("🎓 L03 — RAG Lab\nEducational Edition")
    st.caption("Bronze → Silver → Gold → RAG Pipeline")
    st.caption("محلي بالكامل / fully local, no Docker")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📄 Docs", len(list_documents()))
    with col2:
        st.metric("📊 Chunks", col.count())
    
    st.divider()
    
    st.subheader("🧰 Pipeline Config")
    st.caption(f"**Generator:** `{rag.GENERATOR}`")
    if rag.GENERATOR == "openrouter":
        model_name = rag.OPENROUTER_MODEL.split("/")[-1][:20]
        st.caption(f"**Model:** `{model_name}`")
    st.caption(f"**Embedding:** all-MiniLM-L6-v2 (384-dim)")
    st.caption(f"**Index:** HNSW Cosine")
    st.caption(f"**Cache Entries:** {len(rag._cache)}")
    
    st.divider()
    st.caption("📚 **Educational Resources:**")
    st.caption("- [RAGAS Evaluation](https://docs.ragas.io/)")
    st.caption("- [ChromaDB Docs](https://docs.trychroma.com/)")
    st.caption("- [RAG Fundamentals](https://python.langchain.com/docs/modules/data_connection/)")


# ================================================================= TABS
tabs = st.tabs([
    "🎓 Educational Flow",
    "📤 Upload & Ingest",
    "📄 Documents",
    "💬 Query",
    "📊 Evaluation",
    "⚙️ About"
])

# ================= TAB 0: EDUCATIONAL FLOW
with tabs[0]:
    st.header("🎓 RAG Pipeline — Visual Explanation")
    st.write("Explore each step of the Retrieval-Augmented Generation pipeline interactively.")
    
    flow_view = st.radio(
        "Select a view:",
        ["ETL Overview", "Embedding Space", "RAG Pipeline", "Full Flow"],
        horizontal=True
    )
    
    st.divider()
    
    if flow_view == "ETL Overview":
        st.subheader("📊 ETL Layers: Bronze → Silver → Gold")
        st.write("""
        - **Bronze (🗄️)**: Raw documents stored unmodified in SQLite
        - **Silver (🧹)**: Documents cleaned, normalized, recursively chunked (500 chars, 50 overlap)
        - **Gold (🏅)**: Chunks embedded and indexed in ChromaDB with HNSW (cosine distance)
        """)
        create_etl_flow_diagram()
        
        st.subheader("📝 ETL Process Details")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.expander("🗄️ Bronze Layer", expanded=True):
                st.write("""
                **What happens:**
                - Read TXT, MD, CSV, PDF files
                - Store content unmodified
                - No transformations
                
                **Output:**
                - SQLite table: `bronze_docs`
                - Columns: doc_id, name, content, ts
                """)
        
        with col2:
            with st.expander("🧹 Silver Layer", expanded=True):
                st.write("""
                **What happens:**
                - Remove exact duplicates
                - Normalize whitespace
                - **Recursive Chunking:**
                  1. Split by paragraphs
                  2. Split by sentences
                  3. Hard split if oversized
                - Remove fuzzy duplicates (95%+ similarity)
                
                **Output:**
                - SQLite table: `silver_chunks`
                - Columns: chunk_id, doc_name, chunk_idx, text
                """)
        
        with col3:
            with st.expander("🏅 Gold Layer", expanded=True):
                st.write("""
                **What happens:**
                - Convert chunks to embeddings
                - Use all-MiniLM-L6-v2 (384-dim)
                - Build HNSW index (cosine space)
                - Persist to ChromaDB
                
                **Output:**
                - ChromaDB collection: `gold_chunks`
                - Metadata: doc name, chunk index
                - Ready for dense search
                """)
    
    elif flow_view == "Embedding Space":
        st.subheader("🔬 Chunk Embedding Visualization")
        st.write("See how chunks are positioned in embedding space. Similar chunks cluster together.")
        create_embedding_visualization()
        st.caption("""
        **What to notice:**
        - Chunks from the same document often cluster
        - Similar semantic content appears near each other
        - This is why HNSW retrieval works well
        """)
    
    elif flow_view == "RAG Pipeline":
        st.subheader("🔄 RAG Pipeline Steps")
        st.write("From user question to grounded answer with citations.")
        create_rag_flow_diagram()
        
        st.subheader("📋 Step Breakdown")
        with st.expander("1️⃣ User Query", expanded=False):
            st.write("User enters a natural language question.")
        with st.expander("2️⃣ Embedding", expanded=False):
            st.write("Convert query to 384-dimensional embedding using all-MiniLM-L6-v2.")
        with st.expander("3️⃣ HNSW Search", expanded=False):
            st.write("Compute cosine similarity between query and all chunk embeddings.")
        with st.expander("4️⃣ Top-K Retrieval", expanded=False):
            st.write("Return top 5 most similar chunks with similarity score ≥ 0.2.")
        with st.expander("5️⃣ Build Context", expanded=False):
            st.write("Format retrieved chunks as: `[1] text (source: filename)` for each hit.")
        with st.expander("6️⃣ Generate Answer", expanded=False):
            st.write("Send grounded prompt to LLM (OpenRouter/OpenAI) with context and instructions to cite sources.")
        with st.expander("7️⃣ Add Citations", expanded=False):
            st.write("Model adds citations like [1], [2]... and says 'I don't know' if context insufficient.")
        with st.expander("8️⃣ Cache Check", expanded=False):
            st.write("Semantic cache: if new question is 92%+ similar to last question, reuse cached answer.")
    
    elif flow_view == "Full Flow":
        st.subheader("🔀 Complete RAG Architecture")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("""
            ## Data Flow
            
            1. **Input** → Document upload
            2. **Bronze** → Raw storage (SQLite)
            3. **Silver** → Cleaning + chunking
            4. **Gold** → Embeddings + index
            5. **Query** → User question
            6. **Retrieve** → Dense search
            7. **Generate** → LLM output
            8. **Cache** → Store answers
            9. **Evaluate** → Benchmark
            """)
        
        with col2:
            st.write("""
            ## Key Concepts
            
            **Embeddings**: Convert text to 384-dim vectors
            
            **HNSW Index**: Fast approximate nearest neighbor search
            
            **Grounding**: Use retrieved context to constrain generation
            
            **Citations**: [1] for first source, [2] for second, etc.
            
            **Semantic Cache**: Reuse for similar questions (92%+ similarity)
            
            **Evaluation Metrics**:
            - Context Precision: avg similarity of retrieved chunks
            - Expected Source Found: did answer source appear in top-k?
            """)
        
        st.divider()
        create_etl_flow_diagram()
        st.divider()
        create_rag_flow_diagram()

# ================= TAB 1: UPLOAD
with tabs[1]:
    st.header("📤 Upload & Index a New Document")
    st.write("""
    Upload a document (TXT, MD, CSV, or PDF) to ingest it through the ETL pipeline.
    The system will:
    1. 🗄️ Store raw content in **Bronze**
    2. 🧹 Clean and chunk in **Silver**
    3. 🏅 Embed and index in **Gold**
    """)
    
    up = st.file_uploader("Choose a file (TXT/MD/CSV/PDF)",
                          type=["txt", "md", "csv", "pdf"])
    
    if up is not None:
        st.info(f"📄 Selected: `{up.name}` ({up.size} bytes)")
        
        if st.button("⬆️ Upload & Ingest Through Pipeline", type="primary", use_container_width=True):
            if not supported(up.name):
                st.error(f"❌ {AR} / {EN}")
            else:
                os.makedirs(RAW_DIR, exist_ok=True)
                path = os.path.join(RAW_DIR, up.name)
                with open(path, "wb") as f:
                    f.write(up.getvalue())
                
                with st.spinner("🔄 Running ETL pipeline…"):
                    try:
                        n_chunks = ingest_file(path, up.name)
                        st.success(f"""
                        ✅ **Success!** Document indexed
                        
                        - 📝 Document: `{up.name}`
                        - 📊 Chunks created: `{n_chunks}`
                        - 🏅 Indexed in Gold layer
                        
                        View it in the **📄 Documents** tab.
                        """)
                    except Exception as e:
                        st.error(f"❌ Ingestion failed: `{e}`")

# ================= TAB 2: DOCUMENTS
with tabs[2]:
    st.header("📄 Indexed Documents")
    docs = list_documents()
    
    if not docs:
        st.warning("📭 No documents indexed yet. Upload one from the **📤 Upload** tab.")
    else:
        st.subheader(f"📚 {len(docs)} Document(s) Indexed")
        
        # Summary table
        df = pd.DataFrame([{
            "📄 Document": d,
            "📊 Chunks": c,
            "Avg Size": "~500 chars"
        } for d, c in docs])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("🔍 Inspect Chunks")
        
        sel = st.selectbox("Select a document:", [d for d, _ in docs], key="doc_select")
        if sel:
            got = col.get(where={"doc": sel}, include=["documents", "metadatas"])
            rows = sorted(zip(got["ids"], got["documents"],
                              [m["idx"] for m in got["metadatas"]]),
                          key=lambda r: r[2])
            
            st.info(f"📋 **{len(rows)} chunks** from `{sel}`")
            
            for cid, text, idx in rows:
                with st.expander(f"📍 Chunk #{idx} — {cid[:12]}…", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(text)
                    with col2:
                        st.metric("Length", f"{len(text)} chars")
                        st.caption(f"ID: {cid[:20]}…")

# ================= TAB 3: QUERY
with tabs[3]:
    st.header("💬 Query the RAG System")
    st.write("Ask a question and see retrieval + generation in action.")
    
    q = st.text_area(
        "Your question:",
        height=80,
        placeholder="E.g., What are the Medallion architecture layers?",
        key="query_input"
    )
    
    col1, col2 = st.columns([2, 1])
    with col1:
        k = st.slider("Retrieved chunks (top-k)", 1, 10, rag.TOP_K)
    with col2:
        show_steps = st.checkbox("Show steps", value=True)
    
    if st.button("🔎 Search & Generate", type="primary", use_container_width=True) and q.strip():
        with st.spinner("⏳ Processing…"):
            try:
                # Step 1: Retrieve
                if show_steps:
                    st.info("📍 **Step 1: Retrieval** — Finding relevant chunks…")
                
                hits = rag.retrieve(q, k=k)
                
                if not hits:
                    st.warning("⚠️ No relevant chunks found. Try adding more documents.")
                else:
                    if show_steps:
                        st.success(f"✅ Retrieved {len(hits)} chunks")
                    
                    # Visualize retrieval
                    with st.expander("📊 Retrieval Similarity Scores", expanded=True):
                        create_retrieval_visualization(q, hits)
                    
                    # Step 2: Generate
                    if show_steps:
                        st.info("🤖 **Step 2: Generation** — Creating grounded answer…")
                    
                    with st.spinner("Generating…"):
                        answer = rag.generate(q, hits)
                        rag._cache.append((q, answer))
                    
                    if show_steps:
                        st.success("✅ Answer generated")
                    
                    # Display results
                    st.divider()
                    st.subheader("🎯 Answer")
                    st.success(answer)
                    
                    # Cache status
                    cached = any(rag._similarity(q, cq) >= rag.CACHE_SIM
                                for cq, _ in rag._cache)
                    if cached:
                        st.caption("💾 From semantic cache (92%+ similarity)")
                    else:
                        st.caption("🆕 Fresh generation")
                    
                    # Sources
                    st.subheader("📚 Retrieved Sources")
                    for i, h in enumerate(hits, 1):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**[{i}]** from `{h['source']}`")
                        with col2:
                            st.metric("Similarity", f"{h['score']:.3f}")
                        
                        with st.expander("View chunk text"):
                            st.write(h["text"])
                    
            except Exception as e:
                st.error(f"❌ Error: `{e}`")

# ================= TAB 4: EVALUATION
with tabs[4]:
    st.header("📊 Evaluation Against Golden Dataset")
    st.write("Benchmark your RAG system against 12 reference questions.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.caption("**Metrics:**")
        st.caption("- **Context Precision** ≈ average similarity of retrieved chunks")
        st.caption("- **Expected Source Found** = whether the benchmark's expected source appeared in results")
    with col2:
        st.caption("**Golden Dataset:**")
        st.caption("- 12 bilingual Q&A pairs")
        st.caption("- AR/EN questions and references")
        st.caption("- Expected source document name")
    
    if st.button("▶️ Run Evaluation", type="primary", use_container_width=True):
        with open(rag.GOLDEN, encoding="utf-8") as f:
            data = json.load(f)
        
        rows, prog = [], st.progress(0.0, text="Evaluating…")
        
        for i, item in enumerate(data["items"], 1):
            hits = rag.retrieve(item.get("question_en") or item["question"])
            expected = item["expected_source"]
            hit_ok = any(h["source"].endswith(expected.split("/")[-1])
                        for h in hits) if expected != "NOT_IN_CORPUS" else False
            prec = round(sum(h["score"] for h in hits) / len(hits), 2) if hits else 0
            
            rows.append({
                "#": item["id"],
                "سؤال / Question": item["question"][:40] + "…",
                "Precision": prec,
                "Source Found": "✅" if hit_ok else "❌"
            })
            prog.progress(i / len(data["items"]), text=f"Evaluating ({i}/{len(data['items'])})")
        
        prog.empty()
        
        st.divider()
        st.subheader("📈 Results")
        
        df_results = pd.DataFrame(rows)
        st.dataframe(df_results, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        
        avg_precision = round(sum(r["Precision"] for r in rows) / len(rows), 3)
        hit_rate = sum(1 for r in rows if r["Source Found"] == "✅") / len(rows)
        
        with col1:
            st.metric("📊 Avg Context Precision", f"{avg_precision:.3f}", 
                     delta="Higher is better" if avg_precision > 0.5 else "Needs improvement")
        
        with col2:
            st.metric("🎯 Expected Source Hit Rate", f"{hit_rate:.0%}",
                     delta="Higher is better" if hit_rate > 0.5 else "Needs improvement")
        
        with col3:
            st.metric("📚 Passing Questions", f"{sum(1 for r in rows if r['Source Found'] == '✅')}/{len(rows)}")
        
        st.divider()
        st.info("""
        **Interpretation:**
        - ✅ means the expected source appeared in top-k results
        - ❌ typically means the answer isn't covered by indexed documents
        - Upload more relevant documents to improve ✅ rates
        - Higher precision scores indicate better retrieval quality
        """)

# ================= TAB 5: ABOUT
with tabs[5]:
    st.header("⚙️ About L03 Educational RAG Lab")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎓 Learning Outcomes")
        st.write("""
        Students will understand:
        
        - **Bronze→Silver→Gold**: 3-tier data architecture
        - **Recursive Chunking**: Best practice for splitting
        - **Embeddings & HNSW**: Dense vector search
        - **Grounded Prompting**: Using context to constrain LLMs
        - **Citation Tracking**: Linking answers to sources
        - **Semantic Caching**: Efficient prompt reuse
        - **RAG Evaluation**: Benchmarking with golden datasets
        """)
    
    with col2:
        st.subheader("🔧 Technical Stack")
        st.write("""
        - **SQLite** — Bronze & Silver layers
        - **ChromaDB** — Gold layer (HNSW index)
        - **all-MiniLM-L6-v2** — Embeddings (384-dim)
        - **FastAPI** — `/query` endpoint
        - **Streamlit** — Educational UI
        - **OpenRouter** — LLM (free tier)
        - **Python 3.10+** — Language
        - **No Docker** — Local development
        """)
    
    st.divider()
    st.subheader("📚 Resources")
    
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        **RAG Fundamentals**
        - [LangChain Docs](https://python.langchain.com/docs/modules/data_connection/)
        - [Ollama](https://ollama.ai/) (local LLM)
        """)
    
    with cols[1]:
        st.markdown("""
        **Vector Search**
        - [ChromaDB](https://docs.trychroma.com/)
        - [HNSW](https://github.com/nmslib/hnswlib)
        - [Embeddings](https://huggingface.co/sentence-transformers/)
        """)
    
    with cols[2]:
        st.markdown("""
        **Evaluation**
        - [RAGAS](https://docs.ragas.io/)
        - [RAG Triad](https://arxiv.org/abs/2402.10318)
        - [Context Precision](https://docs.ragas.io/concepts/metrics/context_precision)
        """)
    
    st.divider()
    st.subheader("🚀 Quick Commands")
    
    st.code("""
# Run ETL pipeline
python -u etl_pipeline.py

# Run FastAPI backend
uvicorn rag_api:app --reload

# Evaluate against golden dataset
python rag_api.py evaluate

# Run this educational UI
streamlit run streamlit_ui_enhanced.py
    """, language="bash")
    
    st.divider()
    st.subheader("📝 File Structure")
    st.write("""
    - `etl_pipeline.py` — Bronze→Silver→Gold pipeline
    - `rag_api.py` — FastAPI /query endpoint + evaluation
    - `streamlit_ui.py` — Original UI (5 basic tabs)
    - `streamlit_ui_enhanced.py` — **This enhanced educational UI**
    - `golden_dataset.json` — 12 reference Q&A pairs
    - `l03_lab.db` — SQLite database
    - `chroma_db/` — ChromaDB persistent storage
    - `data/raw/` — Source documents (add yours here)
    """)
    
    st.divider()
    st.caption("🧪 L03 Live Lab — Module 02 (Data Engineering for AI) / الوحدة الثانية")
    st.caption("Bilingual (AR/EN) / ثنائية اللغة")
