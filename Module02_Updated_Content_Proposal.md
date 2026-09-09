# Module 02 — المحتوى المحدَّث (اقتراح للمراجعة قبل تعديل ملفات PPTX)
# Module 02 — Updated Course Content (Proposal for review before touching PPTX files)

**مصادر التحديث:** الإطارات المرجعية المرفقة + أفضل الممارسات المنشورة (Daily Dose of DS — استراتيجيات التقسيم في RAG، معمارية McKinsey المرجعية لـ GenAI، مثلث تقييم RAG).
**Sources:** Attached reference infographics + published best practices (Daily Dose of DS — RAG chunking strategies, McKinsey GenAI reference architecture, the RAG evaluation triad).

---

## V06 — أساسيات البيانات (تحديث)
## V06 — Data Fundamentals (Update)

**الشرائح الحالية:** أنواع البيانات، التنسيقات، مسارات ETL/ELT.
**Current slides:** data types, formats, ETL/ELT pipelines.

**التحديث المقترح:** إثراء شريحة المسارات (أو إضافة شريحة) بمقارنة أنماط معالجة البيانات الثلاثة:
**Proposed update:** enrich the pipelines slide (or add one) comparing the three data-processing patterns:

- **المعمارية المتدرِّجة Medallion (Lakehouse):** بيانات خام غير قابلة للتغيير في طبقة Bronze → بيانات منقَّاة ومنظَّمة في Silver → تجميعات على مستوى الأعمال جاهزة للتحليل في Gold. تُدار عادةً بفريق هندسة بيانات مركزي، وتتم الحوكمة عبر تحسين الجودة بين الطبقات. الأنسب لبيئات Lakehouse والتحليلات وخطوط بيانات الذكاء الاصطناعي (AI/ML/RAG).
- **Medallion architecture (Lakehouse):** raw immutable data in Bronze → cleansed, structured data in Silver → business-level aggregates analytics-ready in Gold. Usually managed by a central data engineering team; governance happens through layered data-quality improvement. Best for lakehouse environments, analytics, and AI/ML/RAG pipelines.
- **مستودع البيانات (Data Warehouse):** ETL/ELT → منطقة تجهيز (Staging) → المستودع → أسواق البيانات (Data Marts). حوكمة مركزية بفرق BI/المستودع. الأنسب للتقارير ولوحات المعلومات والتحليل التاريخي وذكاء الأعمال.
- **Data warehouse:** ETL/ELT → staging area → warehouse → data marts. Centrally governed by BI/warehouse teams. Best for reporting, dashboards, historical analysis, and business intelligence.
- **شبكة البيانات (Data Mesh):** ملكية لامركزية على مستوى المجالات (Domains)؛ كل فريق ينشر «منتجات بيانات» موثوقة مع عقود بيانات (المخطط، الأمان، مستوى الخدمة SLA) وكتالوجات موحَّدة. الأنسب للمؤسسات الكبيرة التي تحتاج فرقًا مستقلة.
- **Data mesh:** decentralized ownership by domain teams; each publishes trusted data products with data contracts (schema, security, SLA) and unified catalogs. Best for large organizations needing independent team ownership.
- **جدول مقارنة سريع:** الفكرة الجوهرية / تدفق البيانات / مالك البيانات / حالة الاستخدام المثلى / نمط الحوكمة.
- **Quick comparison table:** core idea / data flow / data ownership / best use case / governance style.

---

## V07 — المستودعات والبحيرات ومعمارية Lakehouse (تحديث)
## V07 — Warehouses, Data Lakes & Lakehouse (Update)

- ربط الأنماط الثلاثة (Medallion / المستودع / Data Mesh) بإطار قرار عملي: «متى تختار كل نموذج؟» حسب حجم الفريق وطبيعة الاستخدام.
- Frame the three patterns (Medallion / warehouse / data mesh) as a practical decision guide: "when to choose which" based on team size and use case.
- إدخال مفهومَي **منتج البيانات (Data Product)** و**عقد البيانات (Data Contract)** بوصفهما وحدة التسليم الحديثة في هندسة البيانات.
- Introduce **Data Product** and **Data Contract** as the modern delivery unit in data engineering.
- مثال عملي يربط بالمقرر: مسار Bronze → Silver → Gold ينتهي في فهرس متجهي يغذّي تطبيق RAG.
- A hands-on example tying back to the course: a Bronze → Silver → Gold pipeline ending in a vector index that feeds a RAG application.

---

## V08 — هندسة الخصائص ومخازنها (تحديث طفيف)
## V08 — Feature Engineering & Feature Stores (Minor Update)

- إضافة فقرة تربط مخازن الخصائص باتساق القيم بين بيئة التدريب (Offline) وبيئة الخدمة (Online)، ودورها في خدمة الخصائص لتطبيقات الوكلاء الذكيين (Agentic).
- Add a paragraph connecting feature stores to online/offline consistency and their role in serving features for agentic applications.

---

## V09 — قواعد البيانات المتجهية + إضافة جوهرية: RAG التطبيقي
## V09 — Vector Databases + Major Addition: Applied RAG

**التحديث الجوهري: إضافة مسار RAG كامل من الفهرسة إلى التقييم:**
**The major update: adding a complete RAG pipeline, from indexing to evaluation:**

1. **الفهرسة (Indexing):** استراتيجيات تقسيم النصوص الخمس:
   - **التقسيم ثابت الحجم (Fixed-size):** أبسط الطرق مع تداخل (overlap) بين المقاطع، لكنه غالبًا يقطع الجُمل والأفكار.
   - **Fixed-size chunking:** simplest approach with overlap between chunks, but often breaks sentences and ideas.
   - **التقسيم الدلالي (Semantic):** تجميع المقاطع وفق تشابه الكوساينس بين تمثيلاتها؛ يحافظ على تماسك الفكرة لكنه يعتمد على عتبة حساسة للمستند.
   - **Semantic chunking:** groups segments by embedding cosine similarity; preserves coherent ideas but relies on a document-sensitive threshold.
   - **التقسيم التكراري (Recursive):** فصل حسب الفقرات/الأقسام ثم تقسيم كل ما تجاوز الحد الأقصى للحجم — **الخيار الموصى به افتراضيًا**.
   - **Recursive chunking:** split by paragraphs/sections, then recursively split anything over the size limit — **the recommended default**.
   - **التقسيم بحسب بنية المستند (Document-structure-based):** استخدام العناوين والأقسام؛ يُدمج عادةً مع التقسيم التكراري.
   - **Document-structure-based chunking:** uses headings and sections; typically merged with recursive chunking.
   - **التقسيم بالنموذج اللغوي (LLM-based):** الأدق سياقيًا والأغلى حسابيًا.
   - **LLM-based chunking:** most contextually accurate, most computationally expensive.
   - يُستكمل بـ **نموذج تمثيل متوافق مع المجال (Domain-aligned embedding model)** وفهرس متجهي من نوع **HNSW**.
   - Plus a **domain-aligned embedding model** and an **HNSW** vector index.
2. **الاسترجاع (Retrieval):** بحث هجين (كثيف Dense + متناثر Sparse)، إعادة ترتيب النتائج بنموذج Cross-encoder، وتحويل الاستعلام (Multi-Query).
   **Retrieval:** hybrid search (dense + sparse), cross-encoder reranking, and query transformation (multi-query).
3. **التوليد (Generation):** توجيه النموذج بتوجيهات صارمة تُلزِمه بالنص المسترجع (Grounded Prompting) مع الاستشهاد بالمصادر.
   **Generation:** grounded prompting with strict instructions and source citations.
4. **التقييم (Evaluation):** مثلث تقييم RAG: الوفاء بالمصدر (Faithfulness)، ملاءمة الإجابة (Answer Relevancy)، دقة السياق (Context Precision).
   **Evaluation:** the RAG triad — faithfulness, answer relevancy, context precision.
5. **التحسين (Optimization):** تخزين دلالي مؤقت (Semantic Caching)، توجيه الطلبات بين النماذج (Model Routing)، ومراقبة مستمرة.
   **Optimization:** semantic caching, model routing, and continuous monitoring.

---

## V10 — تصنيف البيانات على نطاق واسع (تحديث بسيط)
## V10 — Labeling at Scale (Minor Update)

- إضافة أساليب توليد التصنيات بمساعدة النماذج اللغوية (LLM-assisted labeling) مع التحقق البشري (human-in-the-loop) قبل قبولها، وبالإحالة إلى أدوات مثل Label Studio وRoboflow وScale AI.
- Add LLM-assisted labeling with human-in-the-loop validation before acceptance, referencing tools like Label Studio, Roboflow, and Scale AI.

---

## V11 — حوكمة البيانات (تحديث معماري)
## V11 — Data Governance (Architectural Update)
**الإضافة: المعمارية المرجعية للذكاء الاصطناعي التوليدي على مستوى المؤسسة (النمط المرجعي لـ McKinsey):**
**Addition: the enterprise GenAI reference architecture (McKinsey pattern):**

- **أ. بوابة منصة GenAI (GenAI Platform Portal):** نافذة موحَّدة تضم كتالوج حلول (Marketplace)، ومحفظة نشطة تتدرج من إثبات المفهوم POC إلى المنتج الأدنى MVP ثم الإنتاج PROD، مع توثيق كامل.
- **A. GenAI platform portal:** a single "pane of glass" with a solution catalog (marketplace), an active portfolio progressing POC → MVP → PROD, and documentation.
- **ب. الأتمتة والامتثال (Automation & Compliance):** خطوط CI/CD مع بوابات تحكم آلية وموافقات مرحلية وفق ممارسات DevSecOps.
- **B. Automation & compliance:** CI/CD pipelines with automated control gates and stage-gate approvals following DevSecOps practices.
- **ج. الخدمات المشتركة (Shared Services):** بوابة AI موحّدة (AI Gateway)، مكتبة موجِّهات (Prompt Library)، خدمة التغذية الراجعة، قاعدة تدقيق لنماذج LLM، وحواجز حماية (Guardrails).
- **C. Shared services:** a unified AI gateway, prompt library, feedback service, an LLM audit database, and guardrails.
- **د. الحوكمة والمراقبة (Governance & Monitoring):** كتالوج الحلول، أمن البيانات وإدارتها، الذكاء الاصطناعي المسؤول (تدقيق التحيّز والهلوسة)، وإدارة التكاليف (FinOps).
- **D. Governance & monitoring:** solution catalog, data security and management, responsible AI (bias and hallucination audits), and FinOps.

---

## V12 — أساسيات MLOps + تمهيد للمختبر (تحديث)
## V12 — MLOps Fundamentals + Lab Introduction (Update)

**الإضافة الأولى: التمييز بين المفاهيم — LLM مقابل الذكاء التوليدي مقابل الوكلاء مقابل الأنظمة الوكيلة:**
**Addition 1: conceptual distinctions — LLM vs Generative AI vs AI Agents vs Agentic AI:**

- **النموذج اللغوي الكبير (LLM):** نموذج يرمّز النص ويفهم السياق ويتنبأ بالرموز التالية (Tokenization → Context → Inference → Prediction).
- **LLM:** a model that tokenizes text, understands context, and predicts the next tokens.
- **الذكاء الاصطناعي التوليدي (Generative AI):** يتعلم الأنماط من البيانات لتوليد محتوى جديد (نص، صورة، صوت).
- **Generative AI:** learns patterns from data to generate new content (text, image, audio).
- **الوكلاء الأذكياء (AI Agents):** يكشفون نية المستخدم ثم ينفّذون قواعد أو نماذج ويستدعون أدوات وواجهات برمجية لإنجاز المهمة.
- **AI Agents:** detect user intent, execute rules/models, and call tools/APIs to complete the task.
- **الأنظمة الوكيلة (Agentic AI):** تخطيط ذاتي وتنفيذ متعدد الخطوات مع مراقبة فورية وتكيّف مع التغيّرات وتقييم للنتائج.
- **Agentic AI:** self-directed planning and multi-step execution with real-time monitoring, adaptation, and outcome evaluation.

**الإضافة الثانية: الذكاء التقليدي مقابل الوكيلي مقابل RAG الوكيلي:**
**Addition 2: Traditional AI vs Agentic AI vs Agentic RAG:**

- **RAG الوكيلي (Agentic RAG):** يجمع البحث المتجهي وجلب البيانات عبر الواجهات البرمجية في عملية متعددة الخطوات، مع ذاكرة تُحدَّث باستمرار وتحقق من النتائج قبل تسليمها.
- **Agentic RAG:** combines vector search and API data fetching in a multi-step process, with continuously refreshed memory and verification of results before delivery.

---

## L03 — المختبر المباشر (جديد): خط مسارات ETL مصغّر ينتهي بنقطة نهاية RAG
## L03 — Live Lab (New): A Mini ETL Pipeline Ending in a RAG Endpoint

**المقترح (دفتر Jupyter أو سكربتات Python):**
**Proposal (Jupyter notebook or Python scripts):**

1. **Bronze:** تحميل مستندات خام (PDF/CSV/Markdown) وتخزينها كما هي دون تعديل.
   **Bronze:** ingest raw documents (PDF/CSV/Markdown) and store them unmodified.
2. **Silver:** تنظيف وتوحيد وإزالة التكرار، ثم تطبيق **التقسيم التكراري (Recursive Chunking)** مع مقارنة سريعة مع التقسيم ثابت الحجم والدلالي.
   **Silver:** clean, normalize, deduplicate, then apply **recursive chunking**, with a quick comparison against fixed-size and semantic chunking.
3. **Gold:** توليد التمثيلات المتجهية (Embeddings) وبناء فهرس متجهي HNSW — باستخدام **ChromaDB** محليًا (الموصى به، تثبيت خفيف عبر pip)، مع FAISS كبديل.
   **Gold:** generate embeddings and build an HNSW vector index — using **ChromaDB** locally (recommended, lightweight pip install), with FAISS as an alternative.
4. **الاسترجاع (Retrieval):** بحث هجين (Dense + BM25) مع إعادة ترتيب Cross-encoder وتحويل الاستعلام (Multi-Query).
   **Retrieval:** hybrid search (dense + BM25) with cross-encoder reranking and multi-query transformation.
5. **التوليد (Generation):** موجِّه مقيَّد بالمصادر المسترجعة مع الاستشهاد بها.
   **Generation:** a prompt grounded strictly in the retrieved sources, with citations.
6. **التقييم (Evaluation):** قياس مثلث RAG (الوفاء، الملاءمة، دقة السياق) باستخدام إطار RAGAS.
   **Evaluation:** measure the RAG triad (faithfulness, answer relevancy, context precision) with RAGAS.
7. **التحسين (اختياري):** تخزين دلالي مؤقت (Semantic Caching) لتقليل التكلفة وزمن الاستجابة.
   **Optimization (optional):** semantic caching to cut cost and latency.

- **نقطة النهاية:** خدمة FastAPI على المسار `/query` تستقبل سؤالاً وتعيد إجابة مع مصادرها.
- **Endpoint:** a FastAPI service exposing `/query` that accepts a question and returns an answer with its sources.

---

## توصيات لتعزيز المسار (✅ منفَّذة بالكامل)
## Track Enhancement Recommendations (✅ fully implemented)

> **القرار النهائي:** اعتُمد **البند 7 فقط (اختبار قصير بعد كل وحدة)**؛ بقية البنود (1–6، 8–9) غير معتمدة حاليًا وتُترك هنا للمرجعية المستقبلية.
> **Final decision:** only **item 7 (short quiz after each module)** is approved; the remaining items (1–6, 8–9) are not approved for now and are kept here for future reference.
>
> **تحديث لاحق:** بقرار جديد اعتُمدت **جميع** التوصيات ونُفِّذت جميعها (انظر قسم «المخرجات المنفَّذة» في نهاية الملف).
> **Later update:** by a new decision, **all** recommendations were approved and **all** have been implemented (see the "Implemented Artifacts" section at the end of this file).

### أولوية عالية / High priority

1. **تمرين مصغّر بعد كل وحدة (Mini-lab لكل عرض):** بدلًا من مختبر واحد في نهاية المسار، تمرين تطبيقي قصير (~15 دقيقة) بعد كل عرض: تنظيف CSV بعد V06، ومقارنة طبقات Bronze/Silver/Gold بعد V07، وبناء فهرس متجهي بعد V09، وهكذا.
   **Mini-lab per module:** instead of a single lab at the end of the track, a short (~15-minute) hands-on exercise after each deck: CSV cleaning after V06, Bronze/Silver/Gold comparison after V07, building a vector index after V09, and so on.
2. **دليل تجهيز البيئة (Environment Setup Guide):** مستند + `requirements.txt` للتثبيت المحلي المباشر بمكوّنات خفيفة (Python في بيئة افتراضية venv، وSQLite المدمجة في بايثون، وChromaDB كفهرس متجهي، ومفاتيح LLM عبر OpenRouter) — دون حاويات Docker — يُسلَّم قبل أسبوع المختبر لتفادي صرف وقت الجلسة في حل مشاكل التثبيت.
   **Environment Setup Guide:** a document + `requirements.txt` for a direct local installation with lightweight components (Python in a virtual environment, built-in SQLite, ChromaDB as the vector index, and LLM keys via OpenRouter) — no Docker — delivered before lab week so session time isn't lost to installation issues.
3. **مجموعة بيانات مرجعية (Golden Dataset) للمختبر:** 10–20 سؤالًا مع إجاباتها ومصادرها الصحيحة؛ يقيس الطلاب نتائج RAGAS الخاصة بهم مقابل معيار موحَّد، فيتحول التقييم من مفهوم نظري إلى ممارسة قابلة للقياس والمقارنة.
   **Golden Dataset for the lab:** 10–20 questions with reference answers and correct sources; students benchmark their RAGAS scores against a shared standard, turning evaluation from a theoretical concept into a measurable, comparable practice.

### أولوية متوسطة / Medium priority

4. **شريحة «الأخطاء الشائعة» في V09 (RAG):** أمثلة واقعية — تقسيم يكسر الجداول، إهمال إعادة الترتيب، غياب تقييم الوفاء — وكيف يظهر أثر كل خطأ في الإجابات؛ فالتعلم من الأخطاء يعلق أكثر من التعلم من النجاح.
   **"Common pitfalls" slide in V09 (RAG):** real examples — chunking that breaks tables, skipping reranking, missing faithfulness evaluation — and how each failure surfaces in the answers; learning from mistakes sticks better than learning from successes.
5. **مقارنة تكلفة/أداء عملية (في V11 أو V12):** أرقام توضيحية لتكلفة التضمين مقابل التوليد وأثر التخزين الدلالي المؤقت (Semantic Caching) في زمن الاستجابة والتكلفة — يربط FinOps النظري بأرقام ملموسة.
   **Practical cost/performance comparison (V11 or V12):** illustrative numbers for embedding vs generation cost and the latency/cost impact of semantic caching — grounding theoretical FinOps in concrete figures.
6. **شريحة «خريطة المسار» في بداية V06:** رسم واحد يوضح رحلة الوحدة: البيانات → التخزين → الخصائص → الفهارس المتجهية → التصنيف → الحوكمة → MLOps → المختبر؛ يمنح المتعلم الصورة الكاملة من اليوم الأول.
   **"Roadmap" slide at the start of V06:** a single diagram showing the module journey: data → storage → features → vector indexes → labeling → governance → MLOps → lab; gives learners the full picture from day one.

### أولوية منخفضة / Low priority (nice to have)

7. **اختبار قصير لكل عرض (Quiz) — ✅ معتمد:** 3–5 أسئلة للتحقق السريع من الفهم بعد كل وحدة (شريحة ختامية أو مستند مصاحب) للعروض V06–V12.
   **Quiz per deck — ✅ approved:** 3–5 quick comprehension-check questions after each module (a closing slide or companion document) for decks V06–V12.
8. **قائمة مصادر للاستزادة لكل وحدة:** روابط التوثيق الرسمي (Feast، MLflow، RAGAS…) للتعمق الذاتي.
   **Further-reading list per module:** official documentation links (Feast, MLflow, RAGAS…) for self-study.
9. **المصطلحات ثنائية اللغة (عربي–إنجليزي):** جميع مصطلحات المسار في جدول مرجعي واحد.
   **Bilingual (Arabic–English) glossary:** all track terminology in a single reference table.

> **توصية التنفيذ:** البدء بالبنود 1–3 لكونها الأعلى قيمة مقابل الجهد؛ تُدرَج البنود 4–6 مع الشرائح المحدَّثة؛ والبنود 7–9 اختيارية حسب الوقت المتاح.
> **Execution recommendation:** start with items 1–3 (highest value for effort); items 4–6 are folded into the updated slides; items 7–9 are optional depending on available time.

> *(هذه التوصية التنفيذية ألغيت بقرار الاعتماد أعلاه — القيد التنفيذي الآن هو البند 7 فقط.)*
> *(This execution note is superseded by the decision above — the only in-scope item now is item 7.)*

---

## ملخص التغييرات لكل ملف
## Change Summary per File

| الملف / File | نوع التغيير / Change | الحجم / Scope |
|---|---|---|
| V06 | إضافة مقارنة Medallion / المستودع / Data Mesh | شريحة إضافية أو إثراء / New slide or enrichment |
| V07 | منتجات البيانات والعقود + متى تختار كل نموذج / Data products & contracts + decision guide | إثراء الشرائح / Slide enrichment |
| V08 | ربط مخازن الخصائص بالتطبيقات الوكيلة / Feature stores for agentic apps | فقرة / Paragraph |
| V09 | **قسم RAG تطبيقي كامل** من التقسيم إلى التقييم / **Full applied RAG section** (chunking → evaluation) | شريحتان إضافتان / Two new slides |
| V10 | تصنيف بمساعدة LLM مع تحقق بشري / LLM-assisted labeling with human validation | فقرة / Paragraph |
| V11 | **المعمارية المرجعية لـ GenAI (أ–د)** / **GenAI reference architecture (A–D)** | شريحة إضافية / One new slide |
| V12 | تمييز LLM/GenAI/Agents/Agentic + Agentic RAG / Concept distinctions + Agentic RAG | شريحة إضافية / One new slide |
| L03 | مختبر عملي جديد كامل / Complete new hands-on lab | جديد / New |

---

## المخرجات المساندة (وفق القرار المعتمد — ✅ منفَّذة جميعها)
## Supporting Deliverables (per the approved decision — ✅ all implemented)

| المخرَج / Deliverable | يخدم / Serves | الحالة / Status |
|---|---|---|
| اختبار قصير لكل عرض (3–5 أسئلة لكل من V06–V12) / Short quiz per deck (3–5 questions for each of V06–V12) | V06–V12 | ✅ منفَّذ / Implemented — شريحة اختبار في كل عرض + `Module02_Quizzes_AR_EN.md` مع الإجابات |
| تمرين مصغّر لكل وحدة / Mini-lab per module | V06–V12 | ✅ منفَّذ / Implemented — `Module02_Mini_Labs_AR_EN.md` |
| دليل تجهيز البيئة (تثبيت محلي: Python venv، SQLite مدمجة، ChromaDB — دون Docker) / Environment Setup Guide (local install: Python venv, built-in SQLite, ChromaDB — no Docker) | L03 | ✅ منفَّذ / Implemented — `L03_Environment_Setup_Guide.md` + `l03_lab/requirements.txt` |
| المجموعة المرجعية الذهبية (10–20 سؤالًا وإجابة) / Golden Dataset (10–20 Q&A) | L03 — تقييم RAGAS / L03 RAGAS evaluation | ✅ منفَّذ / Implemented — `l03_lab/golden_dataset.json` (12 سؤالًا / 12 Q&A) |
| شريحة «الأخطاء الشائعة» / "Common pitfalls" slide | V09 | ✅ منفَّذ / Implemented — شريحة في العرض المحدَّث |
| مقارنة تكلفة/أداء / Cost-performance comparison | V11 أو V12 / V11 or V12 | ✅ منفَّذ / Implemented — شريحة في V12 |
| شريحة «خريطة المسار» / "Roadmap" slide | V06 | ✅ منفَّذ / Implemented — شريحة في V06 |
| قائمة مصادر للاستزادة / Further-reading list | V06–V12 | ✅ منفَّذ / Implemented — شريحة «للاستزادة» في كل عرض |
| المصطلحات ثنائية اللغة / Bilingual glossary | المسار كاملًا / Whole track | ✅ منفَّذ / Implemented — `Glossary_AR_EN.md` |

---

## المخرجات المنفَّذة / Implemented Artifacts

| الملف / File | الوصف / Description |
|---|---|
| `output/Module02_V06_Updated.pptx` … `V12_Updated.pptx` | 7 عروض محدَّثة (خلفية فاتحة، ألوان أساسية فقط، ثنائية اللغة) / 7 updated decks (light theme, basic colors only, bilingual) |
| `Module02_Quizzes_AR_EN.md` | الاختبارات القصيرة لكل الوحدات مع الإجابات / All module quizzes with answers |
| `Module02_Mini_Labs_AR_EN.md` | تمرين مصغّر (~15 دقيقة) بعد كل وحدة / Mini-lab (~15 min) after each module |
| `L03_Environment_Setup_Guide.md` + `l03_lab/requirements.txt` | تثبيت محلي دون Docker / local install, no Docker |
| `l03_lab/etl_pipeline.py` | Bronze → Silver (تقسيم تكراري) → Gold (ChromaDB HNSW) / recursive chunking + local HNSW index |
| `l03_lab/rag_api.py` | FastAPI `/query` (بحث + توليد مقيَّد + تخزين مؤقت) + أمر `evaluate` / retrieval + grounded generation + cache + evaluation |
| `l03_lab/golden_dataset.json` | 12 سؤالًا وإجابة مرجعية مع المصادر المتوقعة / 12 reference Q&A with expected sources |
| `Glossary_AR_EN.md` | المصطلحات ثنائية اللغة / bilingual glossary |
