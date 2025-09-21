#!/bin/bash

# Detiene la ejecución del script si un comando falla
# El comando "$@" al final ejecutará lo que se pase como CMD en el Dockerfile
# o como 'command' en docker-compose.
set -e

echo "Esperando a que la base de datos esté lista..."
# El healthcheck en docker-compose ya se encarga de la disponibilidad,
# pero una pequeña espera adicional puede prevenir race conditions al iniciar.
sleep 2

echo "Ejecutando migraciones de la base de datos con Alembic..."
alembic upgrade head

echo "Migraciones completadas. Iniciando el comando principal de la aplicación..."
exec "$@"