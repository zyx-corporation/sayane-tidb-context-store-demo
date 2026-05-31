CREATE INDEX idx_chunks_document_id ON chunks (document_id);
CREATE INDEX idx_chunks_content_hash ON chunks (content_hash);
CREATE INDEX idx_retrieval_logs_mode ON retrieval_logs (mode);

-- TiDB Cloud vector and full-text indexes should be added after confirming the current cluster capabilities.
