# -*- coding: utf-8 -*-
"""Content data for Module 02 updated decks (bilingual AR/EN)."""

DECKS = {
    "V06": {
        "title_ar": "أساسيات البيانات",
        "title_en": "Data Fundamentals",
        "slides": [
            ("خريطة المسار / Roadmap", [
                ("رحلة الوحدة: البيانات → التخزين → الخصائص → الفهارس المتجهية → التصنيف → الحوكمة → MLOps → المختبر.",
                 "Module journey: data → storage → features → vector indexes → labeling → governance → MLOps → lab."),
                ("شريحة الخريطة تمنح المتعلم الصورة الكاملة من اليوم الأول.",
                 "This roadmap gives learners the full picture from day one."),
            ]),
            ("أنواع البيانات / Data Types", [
                ("بيانات مهيكلة (جداول)، شبه مهيكلة (JSON/XML)، غير مهيكلة (نصوص، صور، صوت).",
                 "Structured (tables), semi-structured (JSON/XML), unstructured (text, images, audio)."),
                ("اختيار النوع يحدد أدوات التخزين والمعالجة المناسبة.",
                 "The data type determines the right storage and processing tools."),
            ]),
            ("التنسيقات / Formats", [
                ("CSV للتبادل البسيط، JSON للواجهات البرمجية، Parquet وAvro للتحليلات والأنابيب.",
                 "CSV for simple exchange, JSON for APIs, Parquet and Avro for analytics and pipelines."),
                ("التنسيقات العمودية (Parquet) تقلل الحجم وتسرّع القراءة التحليلية.",
                 "Columnar formats (Parquet) reduce size and speed up analytical reads."),
            ]),
            ("أنابيب ETL / ELT", [
                ("ETL: التحويل قبل التحميل؛ ELT: التحميل أولاً ثم التحويل داخل المنصة المستهدفة.",
                 "ETL: transform before loading; ELT: load first, transform inside the target platform."),
                ("ELT هو النمط السائد في بيئات Lakehouse الحديثة.",
                 "ELT is the dominant pattern in modern lakehouse environments."),
            ]),
            ("مقارنة أنماط المعالجة / Processing Patterns", [
                ("المعمارية المتدرِّجة Medallion (Lakehouse): Bronze خام → Silver منقَّى → Gold جاهز للتحليل؛ إدارة مركزية؛ الأنسب للتحليلات وخطوط AI/ML/RAG.",
                 "Medallion (Lakehouse): raw Bronze → cleansed Silver → analytics-ready Gold; central ownership; best for analytics and AI/ML/RAG pipelines."),
                ("مستودع البيانات: ETL/ELT → Staging → المستودع → أسواق البيانات؛ حوكمة مركزية؛ الأنسب للتقارير وذكاء الأعمال.",
                 "Data warehouse: ETL/ELT → staging → warehouse → data marts; central governance; best for reporting and BI."),
                ("شبكة البيانات Data Mesh: ملكية لامركزية بالمجالات؛ منتجات بيانات بعقود (مخطط، أمان، SLA) وكتالوج موحد؛ الأنسب للمؤسسات الكبيرة.",
                 "Data mesh: decentralized domain ownership; data products with contracts (schema, security, SLA) and a unified catalog; best for large organizations."),
            ]),
            ("جدول المقارنة السريع / Quick Comparison", [
                ("المعايير: الفكرة الجوهرية / تدفق البيانات / مالك البيانات / حالة الاستخدام المثلى / نمط الحوكمة.",
                 "Criteria: core idea / data flow / data ownership / best use case / governance style."),
                ("Medallion: فريق هندسة مركزي — المستودع: فرق BI — Data Mesh: فرق المجالات.",
                 "Medallion: central data engineering — warehouse: BI teams — data mesh: domain teams."),
            ]),
        ],
        "quiz": [
            ("ما الفرق الجوهري بين ETL وELT؟",
             "What is the key difference between ETL and ELT?",
             "ETL يحوّل قبل التحميل؛ ELT يحمّل أولاً ثم يحوّل داخل المنصة الهدف.",
             "ETL transforms before loading; ELT loads first and transforms inside the target platform."),
            ("أين تُستخدم طبقة Gold في المعمارية المتدرِّجة؟",
             "Where is the Gold layer used in the Medallion architecture?",
             "تجميعات على مستوى الأعمال جاهزة للتحليل.",
             "Business-level aggregates that are analytics-ready."),
            ("أي نمط يناسب مؤسسة كبيرة بفرق مستقلة وملكية لامركزية؟",
             "Which pattern suits a large organization with independent, decentralized teams?",
             "شبكة البيانات Data Mesh.",
             "Data mesh."),
            ("ما التنسيق الأنسب للتحليلات عالية الأداء ولماذا؟",
             "Which format suits high-performance analytics and why?",
             "Parquet — تنسيق عمودي يقلل الحجم ويسرّع القراءة.",
             "Parquet — columnar, smaller and faster for analytical reads."),
        ],
        "reading": [
            ("توثيق Databricks — المعمارية المتدرِّجة Medallion.", "Databricks docs — Medallion architecture."),
            ("مقالات Data Mesh — Zhamak Dehghani.", "Data Mesh articles — Zhamak Dehghani."),
            ("توثيق Apache Parquet.", "Apache Parquet documentation."),
        ],
    },
}

DECKS.update({
    "V07": {
        "title_ar": "المستودعات والبحيرات ومعمارية Lakehouse",
        "title_en": "Warehouses, Data Lakes & Lakehouse",
        "slides": [
            ("المستودع مقابل البحيرة / Warehouse vs Lake", [
                ("المستودع: مخطط عند الكتابة، SQL سريع، بيانات مهيكلة فقط.",
                 "Warehouse: schema-on-write, fast SQL, structured data only."),
                ("البحيرة: مخطط عند القراءة، كل التنسيقات، تكلفة تخزين منخفضة.",
                 "Lake: schema-on-read, any format, low-cost storage."),
            ]),
            ("معمارية Lakehouse / Lakehouse", [
                ("تجمع مرونة البحيرة وأداء المستودع في منصة واحدة (Delta Lake, Iceberg, Hudi).",
                 "Combines lake flexibility with warehouse performance (Delta Lake, Iceberg, Hudi)."),
                ("طبقات معاملات ACID وفهرسة وحوكمة فوق تخزين الكائنات.",
                 "ACID transactions, indexing, and governance layers over object storage."),
            ]),
            ("منتجات البيانات وعقودها / Data Products & Contracts", [
                ("منتج البيانات: مجموعة بيانات موثوقة موثّقة قابلة للاكتشاف تُدار كمنتج حقيقي.",
                 "Data product: a trusted, documented, discoverable dataset managed like a product."),
                ("عقد البيانات: المخطط والأمان ومستوى الخدمة SLA — وحدة التسليم الحديثة.",
                 "Data contract: schema + security + SLA — the modern delivery unit."),
            ]),
            ("متى تختار كل نموذج؟ / When to Choose Which", [
                ("فريق مركزي وتحليلات → Medallion على Lakehouse؛ تقارير صارمة → مستودع؛ مؤسسة كبيرة بفرق مستقلة → Data Mesh.",
                 "Central team + analytics → Medallion; strict BI → warehouse; large independent teams → data mesh."),
            ]),
            ("ربط بالمقرر / Course Tie-in", [
                ("مسار عملي: Bronze → Silver → Gold ينتهي في فهرس متجهي يغذّي تطبيق RAG (مختبر L03).",
                 "Hands-on path: Bronze → Silver → Gold ending in a vector index feeding a RAG app (lab L03)."),
            ]),
        ],
        "quiz": [
            ("ما معنى «مخطط عند القراءة»؟",
             "What does 'schema-on-read' mean?",
             "لا يُفرض المخطط عند الكتابة بل عند القراءة — سمة البحيرات.",
             "Schema is enforced at read time, not write time — a lake trait."),
            ("ما مكونات عقد البيانات الثلاثة؟",
             "What are the three components of a data contract?",
             "المخطط، الأمان، مستوى الخدمة SLA.",
             "Schema, security, and SLA."),
            ("ماذا يضيف Lakehouse عن البحيرة المجردة؟",
             "What does a lakehouse add over a raw lake?",
             "معاملات ACID وأداء SQL وحوكمة.",
             "ACID transactions, SQL performance, and governance."),
        ],
        "reading": [
            ("توثيق Delta Lake وApache Iceberg.", "Delta Lake and Apache Iceberg docs."),
            ("مقالات Data Contracts (Chad Sanderson).", "Data contracts articles (Chad Sanderson)."),
        ],
    },
})

DECKS.update({
    "V08": {
        "title_ar": "هندسة الخصائص ومخازنها",
        "title_en": "Feature Engineering & Feature Stores",
        "slides": [
            ("هندسة الخصائص / Feature Engineering", [
                ("تحويل البيانات الخام إلى ميزات ذات معنى تدعم تدريب النماذج وخدمتها.",
                 "Turning raw data into meaningful features supporting model training and serving."),
                ("أمثلة: التجميعات الزمنية، الترميز، التطبيع.",
                 "Examples: time-window aggregates, encoding, normalization."),
            ]),
            ("مخازن الخصائص / Feature Stores", [
                ("Feast وTecton وHopsworks: تعريف الميزة مرة واحدة وإعادة استخدامها في التدريب والخدمة.",
                 "Feast, Tecton, Hopsworks: define features once, reuse for training and serving."),
                ("تمنع انحراف الميزات بين التدريب والإنتاج.",
                 "They prevent feature skew between training and production."),
            ]),
            ("اتساق Offline/Online / Consistency", [
                ("Offline للتدريب التاريخي؛ Online لخدمة منخفضة الكمون (ميلي ثانية).",
                 "Offline for historical training; online for low-latency (ms) serving."),
                ("اتساق القيم بين البيئتين شرط لصحة النموذج في الإنتاج.",
                 "Value consistency across stores is essential for production correctness."),
            ]),
            ("الربط بالتطبيقات الوكيلة / Agentic Applications", [
                ("الوكلاء يحتاجون ميزات لحظية متسقة لقرارات التخصيص والمخاطر والتوجيه.",
                 "Agents need consistent real-time features for personalization, risk, and routing."),
                ("مخزن الخصائص هو «مصدر الحقيقة» للميزات أمام أي وكيل ذكي.",
                 "The feature store is the single source of truth behind any agent."),
            ]),
        ],
        "quiz": [
            ("ما المشكلة التي يحلها مخزن الخصائص؟",
             "What problem does a feature store solve?",
             "انحراف الميزات بين التدريب والخدمة وتكرار العمل.",
             "Feature skew between training/serving and duplicated work."),
            ("فرّق بين المخزن Offline وOnline.",
             "Differentiate offline vs online stores.",
             "Offline للتدريب التاريخي؛ Online لخدمة فورية منخفضة الكمون.",
             "Offline for historical training; online for low-latency serving."),
            ("اذكر أداتين لمخازن الخصائص.",
             "Name two feature-store tools.",
             "Feast وHopsworks (أو Tecton).",
             "Feast and Hopsworks (or Tecton)."),
        ],
        "reading": [
            ("توثيق Feast.", "Feast documentation."),
            ("توثيق Hopsworks Feature Store.", "Hopsworks feature store docs."),
        ],
    },
})

DECKS.update({
    "V09": {
        "title_ar": "قواعد البيانات المتجهية + RAG التطبيقي",
        "title_en": "Vector Databases + Applied RAG",
        "slides": [
            ("قواعد البيانات المتجهية / Vector Databases", [
                ("تخزين التمثيلات المتجهية (Embeddings) والبحث فيها بالتشابه: Pinecone، Weaviate، pgvector، ChromaDB.",
                 "Store embeddings and search by similarity: Pinecone, Weaviate, pgvector, ChromaDB."),
                ("فهرس HNSW يمنح بحثًا تقريبيًا سريعًا (ANN) بكفاءة عالية.",
                 "HNSW index provides fast approximate nearest-neighbor (ANN) search."),
            ]),
            ("1) الفهرسة: استراتيجيات التقسيم / Indexing: Chunking", [
                ("ثابت الحجم: أبسطها مع تداخل لكنه يقطع الجُمل. دلالي: تجميع حسب تشابه الكوساينس، حساس للعتبة.",
                 "Fixed-size: simplest with overlap but breaks sentences. Semantic: cosine grouping, threshold-sensitive."),
                ("تكراري (الموصى به افتراضيًا): فصل بالفقرات ثم تقسيم ما تجاوز الحد. بحسب البنية: العناوين. بالنموذج اللغوي: الأدق والأغلى.",
                 "Recursive (recommended default): split by paragraphs then oversized chunks. Structure-based: headings. LLM-based: most accurate, most expensive."),
            ]),
            ("2) الاسترجاع / Retrieval", [
                ("بحث هجين: كثيف (Dense) + متناثر (BM25) يغطي المعنى والكلمات المفتاحية معًا.",
                 "Hybrid search: dense + sparse (BM25) covers meaning and keywords."),
                ("إعادة ترتيب Cross-encoder وتحويل الاستعلام Multi-Query يرفعان دقة النتائج.",
                 "Cross-encoder reranking and multi-query transformation improve precision."),
            ]),
            ("3) التوليد / Generation", [
                ("موجِّه مقيَّد بالمصادر المسترجعة (Grounded Prompting) مع الاستشهاد: «أجب فقط من السياق المرفق».",
                 "Grounded prompting strictly on retrieved sources with citations: 'answer only from the provided context'."),
            ]),
            ("4) التقييم + 5) التحسين / Evaluation + Optimization", [
                ("مثلث RAG: الوفاء (Faithfulness)، ملاءمة الإجابة (Answer Relevancy)، دقة السياق (Context Precision) — بإطار RAGAS.",
                 "RAG triad: faithfulness, answer relevancy, context precision — measured with RAGAS."),
                ("التحسين: تخزين دلالي مؤقت، توجيه الطلبات بين النماذج، ومراقبة مستمرة.",
                 "Optimization: semantic caching, model routing, continuous monitoring."),
            ]),
            ("الأخطاء الشائعة / Common Pitfalls", [
                ("تقسيم يكسر الجداول أو الأكواد؛ إهمال إعادة الترتيب فيضيع الأكثر ملاءمة.",
                 "Chunking that breaks tables/code; skipping reranking loses the most relevant hits."),
                ("غياب تقييم الوفاء فيسمح بالهلوسة؛ استرجاع أعلى-ك دون حد أدنى للدرجة.",
                 "No faithfulness evaluation allows hallucination; top-k without a score floor."),
            ]),
        ],
        "quiz": [
            ("ما استراتيجية التقسيم الموصى بها افتراضيًا؟",
             "Which chunking strategy is the recommended default?",
             "التقسيم التكراري Recursive Chunking.",
             "Recursive chunking."),
            ("لماذا نجمع البحث الكثيف مع BM25؟",
             "Why combine dense search with BM25?",
             "الكثيف يفهم المعنى وBM25 يطابق الكلمات النادرة حرفيًا.",
             "Dense captures meaning; BM25 matches rare exact keywords."),
            ("ما مكونات مثلث تقييم RAG الثلاثة؟",
             "Name the three parts of the RAG evaluation triad.",
             "الوفاء، ملاءمة الإجابة، دقة السياق.",
             "Faithfulness, answer relevancy, context precision."),
            ("ما وظيفة إعادة الترتيب Cross-encoder؟",
             "What does cross-encoder reranking do?",
             "يعيد ترتيب المرشحين بنموذج أدق لرفع ملاءمة النتائج.",
             "Re-scores candidates with a more accurate model."),
            ("كيف يقلل التخزين الدلالي المؤقت التكلفة؟",
             "How does semantic caching cut cost?",
             "يعيد استخدام إجابات الأسئلة المشابهة بدل استدعاء النموذج كل مرة.",
             "Reuses answers for similar questions."),
        ],
        "reading": [
            ("Daily Dose of DS — استراتيجيات تقسيم RAG.", "Daily Dose of DS — RAG chunking strategies."),
            ("توثيق RAGAS لإطار التقييم.", "RAGAS evaluation framework docs."),
            ("توثيق ChromaDB والفهرسة HNSW.", "ChromaDB docs and HNSW indexing."),
        ],
    },
})

DECKS.update({
    "V10": {
        "title_ar": "تصنيف البيانات على نطاق واسع",
        "title_en": "Labeling at Scale",
        "slides": [
            ("لماذا التصنيف؟ / Why Labeling?", [
                ("جودة التصنيفات تحدد سقف أداء أي نموذج تعلّم مُوجَّه.",
                 "Label quality caps the performance of any supervised model."),
            ]),
            ("الأدوات / Tools", [
                ("Label Studio للتعددية، Roboflow للرؤية الحاسوبية، Scale AI للتوسع المؤسسي.",
                 "Label Studio for versatility, Roboflow for vision, Scale AI for enterprise scale."),
            ]),
            ("التصنيف بمساعدة LLM / LLM-assisted Labeling", [
                ("نموذج لغوي يقترح التصنيفات مبدئيًا لتسريع العملية وخفض التكلفة.",
                 "An LLM pre-labels examples to speed up the process and cut cost."),
                ("التحقق البشري (Human-in-the-loop) إلزامي قبل القبول، مع قياس اتفاق النموذج مع البشر.",
                 "Human-in-the-loop validation is mandatory before acceptance, measuring human–model agreement."),
            ]),
        ],
        "quiz": [
            ("لماذا لا نعتمد تصنيفات LLM مباشرة دون مراجعة؟",
             "Why not accept LLM labels directly without review?",
             "لأن النموذج قد يخطئ أو يتحيز — التحقق البشري يضمن الجودة.",
             "The model can err or be biased — human validation guarantees quality."),
            ("أي أداة تناسب مشاريع الرؤية الحاسوبية؟",
             "Which tool fits computer-vision projects?",
             "Roboflow.",
             "Roboflow."),
        ],
        "reading": [
            ("توثيق Label Studio.", "Label Studio docs."),
            ("توثيق Roboflow.", "Roboflow docs."),
        ],
    },
})

DECKS.update({
    "V11": {
        "title_ar": "حوكمة البيانات وسلسلة العهدة والفهرسة",
        "title_en": "Data Governance, Lineage & Cataloging",
        "slides": [
            ("الحوكمة والفهرسة / Governance & Cataloging", [
                ("سلسلة العهدة (Lineage) تتبع أصل البيانات وتحولاتها؛ الفهرسة تجعلها قابلة للاكتشاف.",
                 "Lineage traces data origin and transformations; cataloging makes it discoverable."),
                ("أدوات: Apache Atlas، Collibra، DataHub.",
                 "Tools: Apache Atlas, Collibra, DataHub."),
            ]),
            ("المعمارية المرجعية للذكاء التوليدي (1/2) / GenAI Reference Architecture (1/2)", [
                ("أ. بوابة منصة GenAI: نافذة موحدة بكتالوج حلول ومحفظة POC → MVP → PROD موثقة.",
                 "A. Portal: unified pane of glass with a solution catalog and documented POC → MVP → PROD portfolio."),
                ("ب. الأتمتة والامتثال: خطوط CI/CD ببوابات تحكم آلية وموافقات مرحلية وفق DevSecOps.",
                 "B. Automation & compliance: CI/CD with automated control gates and stage-gate approvals (DevSecOps)."),
            ]),
            ("المعمارية المرجعية للذكاء التوليدي (2/2) / GenAI Reference Architecture (2/2)", [
                ("ج. الخدمات المشتركة: بوابة AI موحدة، مكتبة موجِّهات، خدمة التغذية الراجعة، قاعدة تدقيق LLM، حواجز حماية Guardrails.",
                 "C. Shared services: unified AI gateway, prompt library, feedback service, LLM audit database, guardrails."),
                ("د. الحوكمة والمراقبة: أمن البيانات، الذكاء المسؤول (تدقيق التحيّز والهلوسة)، وإدارة التكاليف FinOps.",
                 "D. Governance & monitoring: data security, responsible AI (bias/hallucination audits), FinOps."),
            ]),
        ],
        "quiz": [
            ("ما وظيفة بوابة AI الموحدة (AI Gateway)؟",
             "What does a unified AI gateway do?",
             "نقطة دخول موحدة تفرض المصادقة والحدود والتسجيل على كل الاستدعاءات.",
             "A single entry point enforcing auth, limits, and logging for all calls."),
            ("لماذا نحتاج قاعدة تدقيق لنماذج LLM؟",
             "Why keep an LLM audit database?",
             "لتتبع الموجِّهات والإجابات والامتثال والتحقيق في الحوادث.",
             "To trace prompts/answers for compliance and investigation."),
            ("ما دور CI/CD في حوكمة GenAI؟",
             "What is CI/CD's role in GenAI governance?",
             "بوابات تحكم وموافقات مرحلية آلية قبل الإنتاج.",
             "Automated control gates and approvals before production."),
        ],
        "reading": [
            ("توثيق DataHub وApache Atlas.", "DataHub and Apache Atlas docs."),
            ("المعمارية المرجعية للذكاء التوليدي — McKinsey.", "GenAI reference architecture — McKinsey."),
        ],
    },
})

DECKS.update({
    "V12": {
        "title_ar": "أساسيات MLOps + تمهيد للمختبر",
        "title_en": "MLOps Fundamentals + Lab Prelude",
        "slides": [
            ("MLOps والأدوات / MLOps & Tools", [
                ("MLflow لتتبع التجارب والنماذج، Kubeflow لأتمتة الخطوط، DVC لإصدارات البيانات.",
                 "MLflow for tracking, Kubeflow for pipeline automation, DVC for data versioning."),
            ]),
            ("تمييز المفاهيم / Concept Distinctions", [
                ("LLM: يرمّز النص ويتنبأ بالرموز التالية. الذكاء التوليدي: يولّد محتوى جديدًا (نص/صورة/صوت).",
                 "LLM: predicts next tokens. Generative AI: generates new content (text/image/audio)."),
                ("الوكلاء: يكشفون النية ويستدعون الأدوات. الأنظمة الوكيلة: تخطيط ذاتي وتنفيذ متعدد الخطوات مع تقييم للنتائج.",
                 "Agents: detect intent and call tools. Agentic AI: self-directed multi-step planning with outcome evaluation."),
            ]),
            ("RAG الوكيلي / Agentic RAG", [
                ("يجمع البحث المتجهي وجلب البيانات عبر الواجهات في عملية متعددة الخطوات، بذاكرة محدَّثة وتحقق من النتائج قبل التسليم.",
                 "Combines vector search and API fetching in multi-step flows, with refreshed memory and verification before delivery."),
            ]),
            ("التكلفة والأداء عمليًا / Practical Cost & Performance", [
                ("التضمين (Embedding) أقل تكلفة بمرتبة كاملة من التوليد (Generation) — الاسترجاع أرخص من التوليد.",
                 "Embedding costs an order of magnitude less than generation — retrieval is cheaper than generation."),
                ("التخزين الدلالي المؤقت يخفض الكمون والتكلفة؛ توجيه الطلبات يرسل المهام البسيطة لنماذج أصغر أرخص.",
                 "Semantic caching cuts latency and cost; routing sends easy tasks to smaller, cheaper models."),
                ("قاعدة FinOps: قِس التكلفة لكل طلب (per-request) قبل التوسع.",
                 "FinOps rule: measure per-request cost before scaling."),
            ]),
            ("تمهيد للمختبر L03 / Lab Prelude", [
                ("المختبر: خط محلي خفيف — Python venv + SQLite مدمجة (Bronze/Silver) + ChromaDB (Gold) — دون Docker، بنقطة نهاية FastAPI على المسار /query.",
                 "The lab: lightweight local pipeline — Python venv + built-in SQLite (Bronze/Silver) + ChromaDB (Gold) — no Docker, ending in a FastAPI /query endpoint."),
            ]),
        ],
        "quiz": [
            ("فرّق بين AI Agent وAgentic AI.",
             "Differentiate an AI agent from agentic AI.",
             "الوكيل يستجيب ويستدعي أدوات؛ الوكيلي يخطط ذاتيًا وينفذ خطوات متعددة ويتكيف.",
             "An agent responds and calls tools; agentic AI self-plans multi-step execution."),
            ("ما أرخص: تضمين أم توليد؟",
             "Which is cheaper: embedding or generation?",
             "التضمين — أقل بتكلفة مرتبة كاملة.",
             "Embedding — roughly an order of magnitude cheaper."),
            ("ما أدوات تتبع التجارب وإصدارات البيانات؟",
             "Which tools track experiments and version data?",
             "MLflow للتتبع وDVC لإصدارات البيانات.",
             "MLflow for tracking, DVC for data versioning."),
        ],
        "reading": [
            ("توثيق MLflow وDVC.", "MLflow and DVC docs."),
            ("دليل تجهيز البيئة للمختبر L03.", "L03 Environment Setup Guide."),
        ],
    },
})

