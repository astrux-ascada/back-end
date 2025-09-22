#!/bin/bash

# Detiene la ejecución del script si un comando falla.
set -e

# El primer argumento pasado al script (ej: "uvicorn", "pytest", "env")
first_arg="$1"

# --- Lógica Inteligente ---
# Solo ejecuta las migraciones si el comando es para iniciar el servidor web.
# Esto evita que las migraciones se ejecuten durante tests, linters o depuración.
if [ "$first_arg" = "uvicorn" ]; then
    echo "Esperando a que la base de datos esté lista..."
    # Aunque docker-compose tiene un healthcheck, una pequeña espera puede
    # prevenir condiciones de carrera en el primer inicio.
    sleep 2

    echo "Ejecutando migraciones de la base de datos con Alembic..."
    alembic upgrade head
    echo "Migraciones completadas."
fi

# Finalmente, ejecuta el comando que se le pasó originalmente al contenedor.
# Esto podría ser `uvicorn app.main:app...` o `env` o `pytest`.
echo "Iniciando el comando principal: $@"
exec "$@"
