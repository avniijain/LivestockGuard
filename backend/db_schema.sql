-- LivestockGuard relational schema (PostgreSQL compatible)

CREATE TABLE IF NOT EXISTS diseases (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL UNIQUE,
  type VARCHAR(20) NOT NULL,
  zoonotic BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS symptoms (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS disease_symptoms (
  disease_id INTEGER NOT NULL REFERENCES diseases(id) ON DELETE CASCADE,
  symptom_id INTEGER NOT NULL REFERENCES symptoms(id) ON DELETE CASCADE,
  probability DOUBLE PRECISION NOT NULL,
  PRIMARY KEY (disease_id, symptom_id)
);

CREATE TABLE IF NOT EXISTS transmission_routes (
  id SERIAL PRIMARY KEY,
  disease_id INTEGER NOT NULL REFERENCES diseases(id) ON DELETE CASCADE,
  route VARCHAR(60) NOT NULL,
  base_probability DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(120) NOT NULL DEFAULT '',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reports (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  disease_predicted VARCHAR(120) NOT NULL,
  confidence DOUBLE PRECISION NOT NULL,
  latitude DOUBLE PRECISION NOT NULL,
  longitude DOUBLE PRECISION NOT NULL,
  risk_score INTEGER,
  risk_tier VARCHAR(20),
  source VARCHAR(30) NOT NULL DEFAULT 'image',
  exposure_summary JSONB,
  symptoms_reported JSONB,
  pdf_reference VARCHAR(40),
  pdf_url VARCHAR(255),
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cluster_alerts (
  id SERIAL PRIMARY KEY,
  disease VARCHAR(120) NOT NULL,
  severity VARCHAR(20) NOT NULL,
  centroid_lat DOUBLE PRECISION NOT NULL,
  centroid_lng DOUBLE PRECISION NOT NULL,
  case_count INTEGER NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS device_tokens (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  token VARCHAR(512) NOT NULL UNIQUE,
  last_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS user_locations (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  device_token VARCHAR(512) NOT NULL UNIQUE,
  latitude DOUBLE PRECISION NOT NULL,
  longitude DOUBLE PRECISION NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cluster_alert_notifications (
  id SERIAL PRIMARY KEY,
  alert_id INTEGER NOT NULL REFERENCES cluster_alerts(id) ON DELETE CASCADE,
  device_token_id INTEGER NOT NULL REFERENCES device_tokens(id) ON DELETE CASCADE,
  sent_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (alert_id, device_token_id)
);

