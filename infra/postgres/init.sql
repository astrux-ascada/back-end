-- Habilitar TimescaleDB
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- ================================
-- Tablas Principales (MVP Fase 1)
-- ================================

-- Usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255), -- Columna para la contraseña hasheada
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Activos (máquinas, sensores, etc.)
CREATE TABLE assets (
    id UUID PRIMARY KEY,
    asset_type_id UUID NOT NULL,
    sector_id UUID,
    serial_number VARCHAR(100) UNIQUE,
    location VARCHAR(150),
    status VARCHAR(50) NOT NULL DEFAULT 'operational',
    properties JSONB,
    installed_at DATE,
    last_maintenance_at DATE,
    warranty_expires_at DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ¡NUEVA TABLA! Fuentes de Datos (PLCs, Gateways)
CREATE TABLE data_sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    protocol VARCHAR(50) NOT NULL, -- 'modbus_tcp', 'opc_ua', 'http'
    connection_params JSONB NOT NULL, -- { "host": "192.168.1.10", "port": 502 }
    is_active BOOLEAN DEFAULT TRUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Datos de sensores (¡HYPERTABLE!)
CREATE TABLE sensor_readings (
    "timestamp" TIMESTAMPTZ NOT NULL,
    asset_id UUID NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    PRIMARY KEY ("timestamp", asset_id, metric_name)
);

SELECT create_hypertable('sensor_readings', 'timestamp');

-- Reglas de Alarma
CREATE TABLE alarm_rules (
    id UUID PRIMARY KEY,
    asset_id UUID NOT NULL REFERENCES assets(id),
    metric_name VARCHAR NOT NULL,
    condition VARCHAR NOT NULL,
    threshold FLOAT NOT NULL,
    severity VARCHAR NOT NULL,
    is_enabled BOOLEAN DEFAULT TRUE
);

-- Alarmas
CREATE TABLE alarms (
    id UUID PRIMARY KEY,
    alarm_rule_id UUID NOT NULL REFERENCES alarm_rules(id),
    asset_id UUID NOT NULL REFERENCES assets(id),
    triggered_at TIMESTAMPTZ DEFAULT NOW(),
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMPTZ,
    severity VARCHAR,
    triggered_value FLOAT
);


-- Órdenes de trabajo (mantenimiento)
CREATE TABLE maintenance_orders (
    id SERIAL PRIMARY KEY,
    machine_id UUID REFERENCES assets(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(10) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    order_type VARCHAR(20) NOT NULL DEFAULT 'routine',
    maintenance_type VARCHAR(20) NOT NULL DEFAULT 'corrective',
    assigned_to INTEGER REFERENCES users(id),
    due_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- Historial de Órdenes de Trabajo
CREATE TABLE work_order_history (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES maintenance_orders(id),
    from_status VARCHAR(20),
    to_status VARCHAR(20) NOT NULL,
    changed_by INTEGER NOT NULL REFERENCES users(id),
    changed_at TIMESTAMPTZ DEFAULT NOW(),
    notes TEXT
);

-- Auditoría de accesos (seguridad)
CREATE TABLE access_audit_log (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource VARCHAR(200),
    ip_address VARCHAR(45),
    success BOOLEAN NOT NULL,
    mfa_used BOOLEAN DEFAULT FALSE
);

-- ================================
-- Índices Clave
-- ================================
CREATE INDEX idx_sensor_readings_time ON sensor_readings ("timestamp" DESC);
CREATE INDEX idx_sensor_readings_asset_time ON sensor_readings (asset_id, "timestamp" DESC);
CREATE INDEX idx_maintenance_orders_status ON maintenance_orders (status);
CREATE INDEX idx_access_audit_log_user ON access_audit_log (user_id);

-- ================================
-- Datos de Ejemplo (Semilla)
-- ================================
INSERT INTO users (email, name, role) VALUES
    ('operario@planta.com', 'Juan Pérez', 'operator'),
    ('tecnico@planta.com', 'Carlos Gómez', 'technician'),
    ('supervisor@planta.com', 'Ana López', 'supervisor');

-- ¡DATO SEMILLA PARA DATA_SOURCES!
INSERT INTO data_sources (name, protocol, connection_params, is_active, description) VALUES
    ('PLC_Corrugadora', 'modbus_tcp', '{ "host": "192.168.1.10", "port": 502, "slave_id": 1 }', true, 'PLC principal de la máquina corrugadora.');

-- ================================
-- Mensaje de confirmación
-- ================================
DO $$ BEGIN
    RAISE NOTICE '✅ Base de datos v2 inicializada para Astruxa';
END $$;
