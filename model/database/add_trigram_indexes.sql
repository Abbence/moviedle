-- Enable pg_trgm extension for trigram-based text search
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Create GIN indexes with trigram operator classes for fast substring matching
CREATE INDEX IF NOT EXISTS idx_movies_primarytitle_trgm ON movies USING GIN (primarytitle gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_movies_originaltitle_trgm ON movies USING GIN (originaltitle gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_movies_hungariantitle_trgm ON movies USING GIN (hungariantitle gin_trgm_ops);

-- Optional: Create a composite index for sorting by popularity (vote count)
CREATE INDEX IF NOT EXISTS idx_movies_votecount_desc ON movies ("imdbVoteCount" DESC NULLS LAST);
