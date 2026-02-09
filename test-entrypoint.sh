#!/bin/bash
set -e

# Variables de la base de datos de prueba
DB_HOST="$POSTGRES_HOST"
DB_PORT="$POSTGRES_PORT"
DB_USER="$POSTGRES_USER"
DB_PASS="$POSTGRES_PASSWORD"

# Esperar a que la base de datos esté lista
echo "Test Runner: Esperando a que la base de datos de prueba ($DB_HOST:$DB_PORT) esté lista..."
until PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -c '\q'; do
  >&2 echo "Test Runner: La base de datos no está lista - esperando..."
  sleep 1
done
echo "Test Runner: La base de datos de prueba está lista."

# Ejecutar el comando pasado al contenedor (ej: "alembic upgrade head && pytest")
echo "Test Runner: Iniciando el comando principal: $@"
exec "$@"
