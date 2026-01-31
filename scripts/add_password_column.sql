-- Script para agregar la columna de contraseña si no existe
ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);
