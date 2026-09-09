# Module 02 — الاختبارات القصيرة مع الإجابات / Short Quizzes with Answers

## V06 — أساسيات البيانات / Data Fundamentals

**س1:** ما الفرق الجوهري بين ETL وELT؟
**Q1:** What is the key difference between ETL and ELT?
- ✅ **الإجابة:** ETL يحوّل قبل التحميل؛ ELT يحمّل أولاً ثم يحوّل داخل المنصة الهدف.
- ✅ **Answer:** ETL transforms before loading; ELT loads first and transforms inside the target platform.

**س2:** أين تُستخدم طبقة Gold في المعمارية المتدرِّجة؟
**Q2:** Where is the Gold layer used in the Medallion architecture?
- ✅ **الإجابة:** تجميعات على مستوى الأعمال جاهزة للتحليل.
- ✅ **Answer:** Business-level aggregates that are analytics-ready.

**س3:** أي نمط يناسب مؤسسة كبيرة بفرق مستقلة وملكية لامركزية؟
**Q3:** Which pattern suits a large organization with independent, decentralized teams?
- ✅ **الإجابة:** شبكة البيانات Data Mesh.
- ✅ **Answer:** Data mesh.

**س4:** ما التنسيق الأنسب للتحليلات عالية الأداء ولماذا؟
**Q4:** Which format suits high-performance analytics and why?
- ✅ **الإجابة:** Parquet — تنسيق عمودي يقلل الحجم ويسرّع القراءة.
- ✅ **Answer:** Parquet — columnar, smaller and faster for analytical reads.

## V07 — المستودعات والبحيرات ومعمارية Lakehouse / Warehouses, Data Lakes & Lakehouse

**س1:** ما معنى «مخطط عند القراءة»؟
**Q1:** What does 'schema-on-read' mean?
- ✅ **الإجابة:** لا يُفرض المخطط عند الكتابة بل عند القراءة — سمة البحيرات.
- ✅ **Answer:** Schema is enforced at read time, not write time — a lake trait.

**س2:** ما مكونات عقد البيانات الثلاثة؟
**Q2:** What are the three components of a data contract?
- ✅ **الإجابة:** المخطط، الأمان، مستوى الخدمة SLA.
- ✅ **Answer:** Schema, security, and SLA.

**س3:** ماذا يضيف Lakehouse عن البحيرة المجردة؟
**Q3:** What does a lakehouse add over a raw lake?
- ✅ **الإجابة:** معاملات ACID وأداء SQL وحوكمة.
- ✅ **Answer:** ACID transactions, SQL performance, and governance.

## V08 — هندسة الخصائص ومخازنها / Feature Engineering & Feature Stores

**س1:** ما المشكلة التي يحلها مخزن الخصائص؟
**Q1:** What problem does a feature store solve?
- ✅ **الإجابة:** انحراف الميزات بين التدريب والخدمة وتكرار العمل.
- ✅ **Answer:** Feature skew between training/serving and duplicated work.

**س2:** فرّق بين المخزن Offline وOnline.
**Q2:** Differentiate offline vs online stores.
- ✅ **الإجابة:** Offline للتدريب التاريخي؛ Online لخدمة فورية منخفضة الكمون.
- ✅ **Answer:** Offline for historical training; online for low-latency serving.

**س3:** اذكر أداتين لمخازن الخصائص.
**Q3:** Name two feature-store tools.
- ✅ **الإجابة:** Feast وHopsworks (أو Tecton).
- ✅ **Answer:** Feast and Hopsworks (or Tecton).

## V09 — قواعد البيانات المتجهية + RAG التطبيقي / Vector Databases + Applied RAG

**س1:** ما استراتيجية التقسيم الموصى بها افتراضيًا؟
**Q1:** Which chunking strategy is the recommended default?
- ✅ **الإجابة:** التقسيم التكراري Recursive Chunking.
- ✅ **Answer:** Recursive chunking.

**س2:** لماذا نجمع البحث الكثيف مع BM25؟
**Q2:** Why combine dense search with BM25?
- ✅ **الإجابة:** الكثيف يفهم المعنى وBM25 يطابق الكلمات النادرة حرفيًا.
- ✅ **Answer:** Dense captures meaning; BM25 matches rare exact keywords.

**س3:** ما مكونات مثلث تقييم RAG الثلاثة؟
**Q3:** Name the three parts of the RAG evaluation triad.
- ✅ **الإجابة:** الوفاء، ملاءمة الإجابة، دقة السياق.
- ✅ **Answer:** Faithfulness, answer relevancy, context precision.

**س4:** ما وظيفة إعادة الترتيب Cross-encoder؟
**Q4:** What does cross-encoder reranking do?
- ✅ **الإجابة:** يعيد ترتيب المرشحين بنموذج أدق لرفع ملاءمة النتائج.
- ✅ **Answer:** Re-scores candidates with a more accurate model.

**س5:** كيف يقلل التخزين الدلالي المؤقت التكلفة؟
**Q5:** How does semantic caching cut cost?
- ✅ **الإجابة:** يعيد استخدام إجابات الأسئلة المشابهة بدل استدعاء النموذج كل مرة.
- ✅ **Answer:** Reuses answers for similar questions.

## V10 — تصنيف البيانات على نطاق واسع / Labeling at Scale

**س1:** لماذا لا نعتمد تصنيفات LLM مباشرة دون مراجعة؟
**Q1:** Why not accept LLM labels directly without review?
- ✅ **الإجابة:** لأن النموذج قد يخطئ أو يتحيز — التحقق البشري يضمن الجودة.
- ✅ **Answer:** The model can err or be biased — human validation guarantees quality.

**س2:** أي أداة تناسب مشاريع الرؤية الحاسوبية؟
**Q2:** Which tool fits computer-vision projects?
- ✅ **الإجابة:** Roboflow.
- ✅ **Answer:** Roboflow.

## V11 — حوكمة البيانات وسلسلة العهدة والفهرسة / Data Governance, Lineage & Cataloging

**س1:** ما وظيفة بوابة AI الموحدة (AI Gateway)؟
**Q1:** What does a unified AI gateway do?
- ✅ **الإجابة:** نقطة دخول موحدة تفرض المصادقة والحدود والتسجيل على كل الاستدعاءات.
- ✅ **Answer:** A single entry point enforcing auth, limits, and logging for all calls.

**س2:** لماذا نحتاج قاعدة تدقيق لنماذج LLM؟
**Q2:** Why keep an LLM audit database?
- ✅ **الإجابة:** لتتبع الموجِّهات والإجابات والامتثال والتحقيق في الحوادث.
- ✅ **Answer:** To trace prompts/answers for compliance and investigation.

**س3:** ما دور CI/CD في حوكمة GenAI؟
**Q3:** What is CI/CD's role in GenAI governance?
- ✅ **الإجابة:** بوابات تحكم وموافقات مرحلية آلية قبل الإنتاج.
- ✅ **Answer:** Automated control gates and approvals before production.

## V12 — أساسيات MLOps + تمهيد للمختبر / MLOps Fundamentals + Lab Prelude

**س1:** فرّق بين AI Agent وAgentic AI.
**Q1:** Differentiate an AI agent from agentic AI.
- ✅ **الإجابة:** الوكيل يستجيب ويستدعي أدوات؛ الوكيلي يخطط ذاتيًا وينفذ خطوات متعددة ويتكيف.
- ✅ **Answer:** An agent responds and calls tools; agentic AI self-plans multi-step execution.

**س2:** ما أرخص: تضمين أم توليد؟
**Q2:** Which is cheaper: embedding or generation?
- ✅ **الإجابة:** التضمين — أقل بتكلفة مرتبة كاملة.
- ✅ **Answer:** Embedding — roughly an order of magnitude cheaper.

**س3:** ما أدوات تتبع التجارب وإصدارات البيانات؟
**Q3:** Which tools track experiments and version data?
- ✅ **الإجابة:** MLflow للتتبع وDVC لإصدارات البيانات.
- ✅ **Answer:** MLflow for tracking, DVC for data versioning.
