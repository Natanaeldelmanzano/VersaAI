-- VersaAI Database Initialization Script
-- This script sets up the initial database configuration

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Create custom types
DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('super_admin', 'organization_admin', 'user');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE subscription_plan AS ENUM ('free', 'basic', 'professional', 'enterprise');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE organization_status AS ENUM ('active', 'inactive', 'suspended');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE chatbot_status AS ENUM ('active', 'inactive', 'training');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE chatbot_type AS ENUM ('customer_support', 'sales', 'general', 'custom');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE message_type AS ENUM ('user', 'assistant', 'system');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE message_status AS ENUM ('sent', 'delivered', 'read', 'failed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE conversation_status AS ENUM ('active', 'closed', 'archived');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE document_type AS ENUM ('pdf', 'txt', 'docx', 'md', 'html', 'csv', 'url');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE document_status AS ENUM ('pending', 'processing', 'completed', 'failed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create indexes for better performance
-- These will be created automatically by SQLAlchemy, but we can add custom ones here

-- Full-text search indexes
-- CREATE INDEX IF NOT EXISTS idx_documents_content_fts ON documents USING gin(to_tsvector('english', content));
-- CREATE INDEX IF NOT EXISTS idx_document_chunks_content_fts ON document_chunks USING gin(to_tsvector('english', content));

-- Trigram indexes for fuzzy search
-- CREATE INDEX IF NOT EXISTS idx_organizations_name_trgm ON organizations USING gin(name gin_trgm_ops);
-- CREATE INDEX IF NOT EXISTS idx_chatbots_name_trgm ON chatbots USING gin(name gin_trgm_ops);
-- CREATE INDEX IF NOT EXISTS idx_documents_title_trgm ON documents USING gin(title gin_trgm_ops);

-- Performance indexes
-- CREATE INDEX IF NOT EXISTS idx_messages_conversation_created ON messages(conversation_id, created_at);
-- CREATE INDEX IF NOT EXISTS idx_conversations_chatbot_created ON conversations(chatbot_id, created_at);
-- CREATE INDEX IF NOT EXISTS idx_documents_kb_created ON documents(knowledge_base_id, created_at);

-- Create a function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a function to generate slugs
CREATE OR REPLACE FUNCTION generate_slug(input_text TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN lower(regexp_replace(regexp_replace(trim(input_text), '[^a-zA-Z0-9\s-]', '', 'g'), '\s+', '-', 'g'));
END;
$$ LANGUAGE plpgsql;

-- Create a function for vector similarity search (placeholder)
CREATE OR REPLACE FUNCTION vector_similarity(vector1 FLOAT[], vector2 FLOAT[])
RETURNS FLOAT AS $$
DECLARE
    dot_product FLOAT := 0;
    norm1 FLOAT := 0;
    norm2 FLOAT := 0;
    i INTEGER;
BEGIN
    -- Calculate dot product and norms
    FOR i IN 1..array_length(vector1, 1) LOOP
        dot_product := dot_product + (vector1[i] * vector2[i]);
        norm1 := norm1 + (vector1[i] * vector1[i]);
        norm2 := norm2 + (vector2[i] * vector2[i]);
    END LOOP;
    
    -- Return cosine similarity
    IF norm1 = 0 OR norm2 = 0 THEN
        RETURN 0;
    ELSE
        RETURN dot_product / (sqrt(norm1) * sqrt(norm2));
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE versaai TO versaai_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO versaai_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO versaai_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO versaai_user;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO versaai_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO versaai_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO versaai_user;

-- Insert initial data (will be handled by the application)
-- This is just a placeholder for any initial setup data

COMMIT;