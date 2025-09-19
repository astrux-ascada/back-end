# Proyecto Astruxa (Back-End)

Este es el repositorio del back-end para el proyecto Astruxa, un sistema de orquestación industrial.

## Requisitos Previos

- Python 3.12 o superior
- pip para la gestión de paquetes
- Git para el control de versiones

## Instalación

1.  **Clona el repositorio:**
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd back-end
    ```

2.  **Crea y activa un entorno virtual:**
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```sh
    pip install -r requirements.txt
    ```

## Comandos de la Base de Datos (Alembic)

La gestión de la base de datos se realiza con Alembic. Antes de ejecutar estos comandos, asegúrate de que las variables de entorno para la conexión a la base de datos están configuradas o de que los valores por defecto en `alembic/env.py` son correctos.

**Crear una nueva migración (autogenerada):**
*Alembic comparará los modelos de SQLAlchemy con el estado actual de la base de datos y generará un script de migración.*
```sh
alembic revision --autogenerate -m "un_mensaje_descriptivo_sin_acentos"
```

**Aplicar la última migración a la base de datos:**
*Esto ejecuta el último script de migración para actualizar el esquema de la base de datos.*
```sh
alembic upgrade head
```

**Revertir la última migración:**
*Esto deshará los cambios de la última migración aplicada.*
```sh
alembic downgrade -1
```

**Ver la revisión actual de la base de datos:**
*Muestra el ID de la última migración aplicada a la base de datos.*
```sh
alembic current
```

## Ejecutar la Aplicación

Para ejecutar el servidor de desarrollo localmente:
```sh
uvicorn app.main:app --reload
```
