# Proyecto Astruxa (Back-End)

Este es el repositorio del back-end para el proyecto Astruxa, un sistema de orquestación industrial que utiliza FastAPI, PostgreSQL y TimescaleDB, todo gestionado a través de Docker.

## Requisitos Previos

- **Docker** y **Docker Compose**: El entorno de desarrollo está completamente contenedorizado.
- **Git** para el control de versiones.

## Puesta en Marcha (Primer Uso)

1.  **Clona el repositorio:**
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd back_end_astruxa
    ```

2.  **Crea el archivo de entorno:**
    Crea un archivo llamado `.env` en la raíz del proyecto y copia el siguiente contenido. Este archivo alimenta las credenciales a los contenedores de forma segura.
    ```env
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=IndustrialSecreto2025!
    POSTGRES_DB=industrial_orchestrator
    APP_DB_PASS=tu_contraseña_para_app_user # Define una contraseña para el usuario de la aplicación
    ```

3.  **Construye y levanta los contenedores:**
    Este comando construirá las imágenes de la base de datos y del backend, y los iniciará en segundo plano.
    ```sh
    docker-compose up --build -d
    ```

4.  **Inicializa la base de datos con Alembic:**
    La primera vez, necesitas "sellar" la base de datos para que Alembic sepa que el esquema ya ha sido creado por el script `init.sql`.
    ```sh
    docker-compose run --rm backend python -m alembic stamp head
    ```

¡Y eso es todo! Tu entorno está listo.

## Flujo de Trabajo Diario

- **Iniciar el entorno:** `docker-compose up -d`
- **Detener el entorno:** `docker-compose down`
- **Ver logs del backend:** `docker-compose logs -f backend`

## Comandos de la Base de Datos (Alembic)

**Importante:** Todos los comandos de Alembic deben ejecutarse a través de `docker-compose` para asegurar que se ejecutan en el entorno correcto.

**Crear una nueva migración (autogenerada):**
*Después de hacer cambios en los modelos de SQLAlchemy, ejecuta este comando para generar el script de migración.*
```sh
docker-compose run --rm backend python -m alembic revision --autogenerate -m "un_mensaje_descriptivo"
```

**Aplicar la última migración a la base de datos:**
```sh
docker-compose run --rm backend python -m alembic upgrade head
```

**Revertir la última migración:**
```sh
docker-compose run --rm backend python -m alembic downgrade -1
```

**Ver la revisión actual de la base de datos:**
```sh
docker-compose run --rm backend python -m alembic current
```

## Acceso a los Servicios

- **API Backend**: La API estará disponible en `http://localhost:8090`
- **Documentación Interactiva (Swagger UI)**: `http://localhost:8090/docs`
- **Base de Datos (PostgreSQL)**: Puedes conectarte desde una herramienta externa (DBeaver, pgAdmin) usando el puerto `5433` en `localhost`.
