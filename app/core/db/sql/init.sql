-- ===================================================================
-- CONFIGURACIÓN INICIAL Y EXTENSIONES
-- ===================================================================
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- ===================================================================
-- CREACIÓN DE ROLES Y SEGURIDAD (¡MEJORA CLAVE!)
-- ===================================================================

-- Se crea un rol específico para la aplicación backend.
-- La contraseña es leída desde las variables de entorno por el entrypoint de Docker.
-- Este usuario NO es superusuario y solo tendrá los permisos que le concedamos.
CREATE ROLE app_user WITH LOGIN PASSWORD '$APP_DB_PASS';

-- Se le da permiso para conectarse a la base de datos principal.
GRANT CONNECT ON DATABASE industrial_orchestrator TO app_user;

-- ===================================================================
-- CREACIÓN DEL ESQUEMA (Tablas, Hypertables, etc.)
-- Todas las tablas son creadas por el usuario 'admin' (superuser)
-- ===================================================================

-- MÓDULO 1: IAM
CREATE TABLE roles (id SERIAL PRIMARY KEY, name VARCHAR(50) UNIQUE NOT NULL, description TEXT);
CREATE TABLE users (id SERIAL PRIMARY KEY, email VARCHAR(255) UNIQUE NOT NULL, password_hash VARCHAR(255) NOT NULL, name VARCHAR(100) NOT NULL, role_id INTEGER REFERENCES roles(id), is_active BOOLEAN DEFAULT TRUE, created_at TIMESTAMPTZ DEFAULT NOW());

-- MÓDULO 2: ACTIVOS Y GEMELO DIGITAL
CREATE TABLE assets (id SERIAL PRIMARY KEY, name VARCHAR(200) NOT NULL, code VARCHAR(50) UNIQUE NOT NULL, type VARCHAR(50) NOT NULL, location TEXT, status VARCHAR(50) DEFAULT 'unknown', health_score FLOAT DEFAULT 100.0, metadata JSONB, created_at TIMESTAMPTZ DEFAULT NOW());
CREATE TABLE asset_hierarchy (parent_asset_id INTEGER NOT NULL REFERENCES assets(id) ON DELETE CASCADE, child_asset_id INTEGER NOT NULL REFERENCES assets(id) ON DELETE CASCADE, PRIMARY KEY (parent_asset_id, child_asset_id));

-- ... (el resto de las tablas se mantienen igual que en la v3) ...
CREATE TABLE sensor_data (time TIMESTAMPTZ NOT NULL, sensor_id INTEGER NOT NULL REFERENCES assets(id), value DOUBLE PRECISION NOT NULL, unit VARCHAR(50), quality VARCHAR(20) DEFAULT 'good');
SELECT create_hypertable('sensor_data', 'time');

-- ===================================================================
-- CONCESIÓN DE PRIVILEGIOS (Principio de Mínimo Privilegio)
-- ===================================================================

-- Se le otorgan permisos de uso sobre el esquema 'public' a la aplicación.
GRANT USAGE ON SCHEMA public TO app_user;

-- Se le otorgan los permisos CRUD básicos sobre TODAS las tablas del esquema.
-- La aplicación podrá leer y escribir datos, pero no alterar la estructura (DROP, ALTER).
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;

-- Se asegura que el rol de la aplicación tenga permisos sobre las secuencias (para los ID autoincrementales).
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- Se aplican estos permisos a futuras tablas que se creen en el esquema.
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO app_user;

-- ================================
-- Mensaje de confirmación
-- ================================

DO $$ BEGIN
    RAISE NOTICE '✅ Base de datos v3.1 (Seguridad Reforzada) inicializada para Orquestador Industrial';
END $$;
