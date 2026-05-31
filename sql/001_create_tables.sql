CREATE TABLE IF NOT EXISTS documents (
  id VARCHAR(64) PRIMARY KEY,
  title TEXT NOT NULL,
  source_path TEXT,
  source_type VARCHAR(32) NOT NULL DEFAULT 'markdown',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chunks (
  id VARCHAR(64) PRIMARY KEY,
  document_id VARCHAR(64) NOT NULL,
  chunk_index INT NOT NULL,
  content TEXT NOT NULL,
  content_hash VARCHAR(128) NOT NULL,
  embedding JSON,
  metadata JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS retrieval_logs (
  id VARCHAR(64) PRIMARY KEY,
  query TEXT NOT NULL,
  mode VARCHAR(32) NOT NULL,
  retrieved_chunk_ids JSON,
  scores JSON,
  selected_chunk_ids JSON,
  audit_summary JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
