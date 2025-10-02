# Astruxa - Industrial Orchestrator 5.0 (Backend)

Este proyecto es el backend principal para **Astruxa**, un sistema de control, monitoreo y automatización industrial de última generación, construido con **FastAPI**.

## Descripción

Astruxa es el cerebro digital de una planta industrial. Su propósito es unificar sistemas dispares (SCADA, MES, ERP), predecir fallos mediante IA y automatizar operaciones. Este backend proporciona una API modular, segura y de alto rendimiento para gestionar todos los aspectos de la planta.

## Arquitectura y Principios

- **Arquitectura Limpia y Modular:** La lógica está organizada por dominios de negocio (`identity`, `assets`, `maintenance`, etc.).
- **Principios SOLID:** Cada componente tiene una única responsabilidad, promoviendo un código mantenible y escalable.
- **Seguridad Zero Trust:** Ningún componente confía en otro por defecto. Se aplica autenticación y autorización en cada capa.
- **Enfoque Industrial e IoT:** Diseñado para ser robusto, operar on-premise y comunicarse con hardware industrial.

---

## Roles & Permissions Architecture

El sistema utiliza un modelo de Control de Acceso Basado en Roles (RBAC) con una clara separación de responsabilidades:

-   **`SuperUser`**: El "Dueño de la Plataforma". Rol técnico para la configuración del sistema (parámetros, enums dinámicos). No participa en las operaciones diarias.
-   **`Administrator`**: El "Jefe de Planta". Gestiona usuarios, roles operativos y catálogos (ej. `AssetTypes`).
-   **`Supervisor`**: El "Jefe de Turno". Gestiona y asigna órdenes de trabajo.
-   **`Technician`**: El "Técnico de Mantenimiento". Ejecuta las órdenes de trabajo que se le asignan.
-   **`Operator`**: El "Operario de Máquina". Solo puede visualizar el estado de los activos.

Cada rol está compuesto por un conjunto de permisos atómicos (ej. `asset:read`, `workorder:create`) que definen qué acciones puede realizar.

---

## Stack Tecnológico

- **Backend:** FastAPI
- **Base de Datos:** PostgreSQL + TimescaleDB
- **ORM:** SQLAlchemy 2.0
- **Migraciones:** Alembic
- **Contenedores:** Docker y Docker Compose
- **Protocolos Industriales:** OPC UA

---

## Development & Testing Workflow

Esta sección describe la secuencia exacta de comandos para levantar el entorno de desarrollo completo.

**Necesitarás dos terminales abiertas en la raíz del proyecto.**

### Terminal 1: Docker (La Aplicación Principal)

1.  **Limpieza Total (Opcional, pero recomendado para cambios estructurales):**
    ```sh
    docker-compose down -v
    ```
2.  **Construir y Levantar los Contenedores:**
    ```sh
    docker-compose up --build -d
    ```
3.  **Poblar la Base de Datos (Seeding):**
    ```sh
    docker-compose run --rm runner python -m app.db.seeding.seed_all
    ```
4.  **Monitorear los Logs:**
    ```sh
    docker-compose logs -f backend_api
    ```

### Terminal 2: Local (El PLC Simulador)

1.  **Activar el Entorno Virtual:**
    ```sh
    source .venv/bin/activate
    ```
2.  **Instalar las Dependencias:**
    ```sh
    pip install -r requirements-dev.txt
    ```
3.  **Iniciar el Simulador:**
    ```sh
    python simulators/plc_simulator.py
    ```

---

## Documentación de la API

Con la aplicación corriendo, puedes acceder a la documentación interactiva en:

- **Swagger UI**: [http://localhost:8071/api/v1/docs](http://localhost:8071/api/v1/docs)
- **ReDoc**: [http://localhost:8071/api/v1/redoc](http://localhost:8071/api/v1/redoc)
