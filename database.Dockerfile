# Dockerfile para la base de datos del Orquestador Industrial v3

# === Imagen Base ===
# Se fija una versión específica de TimescaleDB con PostgreSQL 15 para garantizar la reproducibilidad.
# Esto evita que futuras actualizaciones de la imagen rompan el sistema.
FROM timescale/timescaledb:2.10.1-pg15

# === Metadatos de la Imagen ===
LABEL maintainer="equipo.arquitectura@industrial.com"
LABEL description="PostgreSQL 15 + TimescaleDB 2.10.1 para Orquestador Industrial 5.0"

# === Script de Inicializacion ===
# Copia el script SQL que creará el esquema, roles y permisos.
COPY init.sql /docker-entrypoint-initdb.d/

# === Exposicion de Puertos ===
# Expone el puerto 5432. El mapeo real se controla en docker-compose.yml.
EXPOSE 5432

# === Chequeo de Salud ===
# El healthcheck se define en docker-compose.yml, que tiene acceso a las variables de entorno.

# === Entrypoint y Usuario ===
# No se define un ENTRYPOINT, CMD o USER aquí. La imagen base ya se encarga de:
# 1. Iniciar PostgreSQL de forma segura.
# 2. Ejecutarse como el usuario no-root 'postgres'.
# 3. Ejecutar los scripts del directorio /docker-entrypoint-initdb.d/.
