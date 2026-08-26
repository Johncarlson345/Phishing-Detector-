CREATE TABLE predictions (
    url TEXT PRIMARY KEY,
    prediction TEXT NOT NULL,
    confidence NUMERIC NOT NULL,
    tier TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
 
CREATE INDEX idx_predictions_created_at ON predictions (created_at);