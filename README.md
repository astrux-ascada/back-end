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

(Se asume que se usan dos terminales en la raíz del proyecto).

### Terminal 1: Docker (Aplicación Principal)

1.  **Limpieza Total (Opcional, pero recomendado):**
    ```sh
    docker-compose down -v
    ```
2.  **Construir y Levantar:**
    ```sh
    docker-compose up --build -d
    ```
3.  **Poblar la Base de Datos:**
    ```sh
    docker-compose run --rm runner python -m app.db.seeding.seed_all
    ```

### Terminal 2: Local (PLC Simulador)

1.  **Activar Entorno Virtual y Dependencias:**
    ```sh
    source .venv/bin/activate
    pip install -r requirements-dev.txt
    ```
2.  **Iniciar el Simulador:**
    ```sh
    python simulators/plc_simulator.py
    ```

---

## Smoke Test: Verifying the End-to-End Data Flow

Después de seguir el workflow anterior, la aplicación estará corriendo y recibiendo datos. Esta guía te ayudará a verificar que puedes consultar esos datos a través de la API.

1.  **Abre la Documentación de la API:**
    -   Navega a [http://localhost:8071/api/v1/docs](http://localhost:8071/api/v1/docs) en tu navegador.

2.  **Obtén un Token de Autenticación:**
    -   Busca el endpoint `POST /auth/login`.
    -   Haz clic en "Try it out" e introduce las credenciales del usuario administrador:
        ```json
        {
          "email": "admin@astruxa.com",
          "password": "admin_password"
        }
        ```
    -   Ejecuta y copia el `access_token` de la respuesta.

3.  **Autoriza tus Peticiones:**
    -   En la parte superior derecha, haz clic en el botón "Authorize".
    -   Pega el `access_token` en el campo "Value" y autoriza.

4.  **Obtén un `asset_id`:**
    -   Busca el endpoint `GET /assets`.
    -   Ejecútalo. En la respuesta, busca el activo con el `serial_number`: "SCH-L1-001".
    -   Copia el valor de su `uuid`.

5.  **Prueba la API del Dashboard:**
    -   Busca el endpoint `GET /telemetry/readings/{asset_id}`.
    -   Pega el `uuid` del activo en el campo `asset_id`.
    -   En el campo `metric_name`, escribe `temperature_celsius`.
    -   Ejecuta la petición.

6.  **Verifica la Respuesta:**
    -   Deberías recibir una respuesta `200 OK` con un cuerpo JSON que es una lista de objetos, cada uno representando un punto de datos agregado por minuto. ¡Felicidades, el flujo de datos de extremo a extremo está funcionando!

---

## Documentación de la API

Con la aplicación corriendo, puedes acceder a la documentación interactiva en:

- **Swagger UI**: [http://localhost:8071/api/v1/docs](http://localhost:8071/api/v1/docs)
- **ReDoc**: [http://localhost:8071/api/v1/redoc](http://localhost:8071/api/v1/redoc)
