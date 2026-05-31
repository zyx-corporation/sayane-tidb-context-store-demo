# Zenn Article Outline

## Working title

RAGは検索して終わりではない：TiDB Cloudで作る監査可能なAIメモリ基盤

## Thesis

RAG and AI agent memory need not only retrieval but also retrieval logs and lightweight audit records. TiDB Cloud can be used as a unified backend for structured metadata, text search, vector search, hybrid search, and logs.

## Structure

1. Why vector-only RAG is not enough
2. Sayane Context Store Interface as a small abstraction
3. Minimal schema for documents, chunks, and retrieval logs
4. Markdown ingestion and chunking
5. Text search, vector search, and hybrid search
6. Recording retrieval logs
7. Lightweight RDE-style audit summary
8. Lessons learned and future work
