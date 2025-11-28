-- Script SQL d'exemple pour la couche de persistance
-- À adapter en fonction de votre modèle de données métier.

CREATE TABLE IF NOT EXISTS dim_source (
    id SERIAL PRIMARY KEY,
    source_name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fact_event (
    id BIGSERIAL PRIMARY KEY,
    source_id INT REFERENCES dim_source(id),
    event_time TIMESTAMP,
    -- colonnes métier à adapter :
    metric_1 NUMERIC,
    metric_2 NUMERIC,
    category TEXT,
    raw_reference TEXT, -- identifiant vers le fichier / objet brut
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_fact_event_time ON fact_event(event_time);
CREATE INDEX IF NOT EXISTS idx_fact_event_category ON fact_event(category);
