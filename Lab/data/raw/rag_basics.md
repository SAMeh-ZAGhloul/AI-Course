# RAG Basics

Retrieval-Augmented Generation (RAG) combines a retrieval step with a generative LLM.
Instead of relying only on what the model memorized during training, RAG fetches relevant
documents from a vector index and injects them into the prompt.

## Chunking

Recursive chunking is the recommended default: split by paragraphs first, then split any
oversized chunk by sentences. Aim for 300-800 characters with 10-20% overlap.

## Evaluation

The RAG triad measures faithfulness, answer relevancy, and context precision.
The RAGAS framework implements these metrics.
