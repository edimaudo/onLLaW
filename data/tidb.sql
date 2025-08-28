CREATE TABLE IF NOT EXISTS test.esa_chunks (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    section VARCHAR(255),
    chunk TEXT,
    embedding JSON,  -- store Gemini embedding as JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);