-- ===================================================================
-- CONFIGURACIÓN INICIAL Y EXTENSIONES
-- ===================================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- ===================================================================
-- CREACIÓN DE ROLES Y SEGURIDAD
-- ===================================================================
CREATE ROLE app_user WITH LOGIN PASSWORD '$APP_DB_PASS';
GRANT CONNECT ON DATABASE industrial_orchestrator TO app_user;

-- ===================================================================
-- CREACIÓN DEL ESQUEMA (Tablas, Hypertables, etc.)
-- ===================================================================

-- MÓDULO: PLANT STRUCTURE & HIERARCHY
CREATE TABLE sections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

-- MÓDULO: IAM (Identity and Access Management)
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role_id UUID REFERENCES roles(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE user_sections (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    section_id UUID NOT NULL REFERENCES sections(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, section_id)
);

-- MÓDULO: ASSETS & DIGITAL TWIN
CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,
    location TEXT,
    status VARCHAR(50) DEFAULT 'unknown',
    health_score FLOAT DEFAULT 100.0,
    asset_metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    section_id UUID NOT NULL REFERENCES sections(id)
);

CREATE TABLE asset_hierarchy (
    parent_asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    child_asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    PRIMARY KEY (parent_asset_id, child_asset_id)
);

CREATE TABLE sensor_data (
    time TIMESTAMPTZ NOT NULL,
    sensor_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE, -- Assuming sensors are a type of asset
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(50),
    quality VARCHAR(20) DEFAULT 'good'
);
SELECT create_hypertable('sensor_data', 'time');

-- MÓDULO: MAINTENANCE & OPERATIONS
CREATE TABLE maintenance_orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(50) NOT NULL DEFAULT 'medium',
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    due_date TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    asset_id UUID NOT NULL REFERENCES assets(id),
    assigned_to_id UUID REFERENCES users(id),
    checklist JSONB,
    evidence JSONB
);

CREATE TABLE spare_parts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(100),
    location TEXT,
    stock_level INTEGER NOT NULL DEFAULT 0,
    min_level INTEGER NOT NULL DEFAULT 5,
    avg_monthly_usage INTEGER DEFAULT 0,
    last_used TIMESTAMPTZ
);

-- ===================================================================
-- CONCESIÓN DE PRIVILEGIOS (Principio de Mínimo Privilegio)
-- ===================================================================
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;

-- Se aplican estos permisos a futuras tablas que se creen en el esquema.
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;

-- ================================
-- Mensaje de confirmación
-- ================================
DO $$ BEGIN
    RAISE NOTICE '✅ Base de datos v4.0 (UUIDs & SQL-First) inicializada para Orquestador Industrial';
END $$;
