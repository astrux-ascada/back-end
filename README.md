# EmergQR - Backend

Este proyecto es el Backend principal construido con **FastAPI** para la aplicación móvil **EmergQR
**.

## Descripción

El Backend de EmergQR está diseñado para ser el punto central de lógica de negocio, gestión de datos
y autenticación. Proporciona una API RESTful segura y eficiente para que la aplicación móvil pueda
operar.

## Características

- Autenticación de usuarios con JWT.
- Gestión de perfil de cliente completo (datos personales, dirección, datos de emergencia).
- Gestión de contactos de emergencia.
- **Gestión de perfil médico:**
    - Alergias
    - Enfermedades crónicas
    - Historial de eventos médicos (cirugías, estudios, etc.)
    - Recordatorios de medicación
- **Perfil Público de Emergencia:** Generación de un perfil público (JSON y vista HTML) accesible a
  través de un código QR.
- **Almacenamiento de Archivos:** Subida y servicio de archivos estáticos para avatares de perfil.
- **Procesamiento DICOM:** Endpoint para la extracción de metadatos de archivos DICOM.
- **Seguridad:**
    - Rate Limiting para proteger endpoints sensibles contra ataques de fuerza bruta.
    - Middleware de CORS configurado para permitir la comunicación con el frontend.
    - Manejo de errores y excepciones personalizadas para respuestas de API consistentes.
- **Base de Datos:**
    - Integración con PostgreSQL a través de SQLAlchemy 2.0 (ORM asíncrono).
- Uso de Alembic para migraciones de base de datos.
- **Entorno de Desarrollo:**
    - Soporte completo para Docker y Docker Compose para un entorno aislado y reproducible.
    - Siembra de datos (seeding) para poblar la base de datos con datos de prueba realistas.
- **Documentación:** API documentada automáticamente con Swagger UI y ReDoc.
- Soporte para pruebas unitarias y de integración.
- Configuración de variables de entorno para facilitar el despliegue en diferentes entornos.
- Integración con un sistema de logging para registrar eventos importantes y errores.

## Requisitos

- Python 3.12+
- PostgreSQL 16+
- Docker y Docker Compose (altamente recomendado)

Las dependencias principales de Python se gestionan a través de `requirements.txt`:

- `fastapi`
- `uvicorn[standard]`
- `sqlalchemy`
- `psycopg[binary]`
- `alembic`
- `pydantic`
- `passlib[bcrypt]`
- `python-jose[cryptography]`
- `python-dotenv`
- `slowapi`

## Instalación

Para instalar y ejecutar el proyecto, sigue estos pasos:

1. Clona el repositorio:

```sh
git clone https://github.com/emergqr/back-end.git
cd back-end
```

## Estructura del Proyecto

```

    bff_mobil/
    ├── app/
    │ ├── api/
    │ │ └── endpoints/
    │ │ └── files.py
    │ ├── core/
    │ │ ├── config.py
    │ │ └── tasks.py
    │ ├── dependencies/
    │ │ └── auth.py
    │ ├── middlewares/
    │ │ └── file_validation.py
    │ ├── models/
    │ │ ├── schemas.py
    │ │ ├── client.py
    │ │ ├── contact.py
    │ │ └── client_contact.py
    │ ├── routers/
    │ │ └── auth.py
    │ └── main.py
    ├── requirements.txt
    ├── Dockerfile
    ├── .dockerignore
    └── docker-compose.yml

```

## Configuración

### 1. Dependencias

El archivo `requirements.txt` contiene todas las dependencias de Python. Para instalarlas, ejecuta:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 2. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con la siguiente estructura:

```env
# Base de Datos (para desarrollo local, Docker lo sobreescribe)
POSTGREs_HOST=localhost
POSTGREs_PORT=5432
POSTGREs_ CLIENT=your_client
POSTGREs_PASSWORD=your_password
POSTGREs_NAME=your_database

# JWT
JWT_SECRET=tu-clave-secreta-muy-segura
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440 # 24 horas

# Entorno
ENV=development # development | testing | production
```

Para trabajar ya en docekr directamente con el contenedor, puedes crear un archivo `.env` en la raíz
del proyecto con la siguiente estructura:
destruye el contenedor y crea uno nuevo con los cambios.

```bash
docker-compose down -v
```

create a new container with the changes.

```bash
docker-compose up -d --build
```

### 3. Base de Datos

Para inicializar la base de datos, asegúrate de que el contenedor de PostgreSQL esté corriendo.
Luego, ejecuta las migraciones:

```bash     
docker-compose exec bff_mobil alembic upgrade head
```

### 4. Comandos Útiles

#### Crear una nueva migración

Después de modificar un modelo de SQLAlchemy, crea una nueva migración:

```bash
docker-compose exec bff_mobil alembic revision --autogenerate -m "Descripción de la migración"
```

#### Aplicar las migraciones

Aplica las migraciones pendientes a la base de datos:

```bash
docker-compose exec bff_mobil alembic upgrade head
```

#### Revertir la última migración

Si necesitas deshacer la última migración, usa:

```bash
docker-compose exec bff_mobil alembic downgrade -1
``` 

¡Listo! Tu backend está ahora corriendo y completamente funcional.

## Documentación de la API

Con la aplicación corriendo, puedes acceder a la documentación interactiva de la API, donde podrás
ver todos los endpoints y probarlos directamente desde el navegador.

- **Swagger UI**: http://localhost:8051/api/v1/docs
- **ReDoc**: http://localhost:8051/api/v1/redoc

## Comandos Útiles de Desarrollo

Todos los comandos se ejecutan desde la raíz del proyecto.

#### Ver Logs en Tiempo Real

Para ver los logs de la aplicación y depurar problemas:

### 🐳 Comandos útiles de Docker Compose

Esta aplicación utiliza Docker Compose para gestionar los servicios. A continuación se listan los
comandos más comunes que puedes usar durante el desarrollo.

#### 🔧 Comandos básicos

| Comando                     | Descripción                                                                                                   |
|-----------------------------|---------------------------------------------------------------------------------------------------------------|
| `docker compose up`         | Crea y arranca todos los contenedores. Usa `-d` para ejecutar en segundo plano.                               |
| `docker compose down`       | Detiene y elimina contenedores, redes e imágenes creadas por `up`.                                            |
| `docker compose up --build` | Reconstruye las imágenes antes de iniciar los contenedores. Útil tras cambios en el código o en `Dockerfile`. |

#### 🛠️ Gestión de servicios

| Comando                                    | Descripción                                                                                        |
|--------------------------------------------|----------------------------------------------------------------------------------------------------|
| `docker compose ps`                        | Muestra el estado de los contenedores en ejecución.                                                |
| `docker compose logs`                      | Muestra los logs de todos los servicios. Usa `logs -f <servicio>` para seguir logs en tiempo real. |
| `docker compose exec <servicio> <comando>` | Ejecuta un comando dentro de un contenedor en ejecución. Ej: `docker compose exec app bash`        |
| `docker compose restart <servicio>`        | Reinicia un servicio específico.                                                                   |
| `docker compose stop`                      | Detiene los contenedores sin eliminarlos.                                                          |
| `docker compose start`                     | Inicia contenedores previamente detenidos.                                                         |

#### 📦 Construcción e imágenes

| Comando                | Descripción                                                         |
|------------------------|---------------------------------------------------------------------|
| `docker compose build` | Construye o reconstruye las imágenes definidas en el `compose.yml`. |
| `docker compose pull`  | Descarga las imágenes especificadas en el archivo compose.          |
| `docker compose push`  | Sube las imágenes de los servicios a un registry.                   |

#### 🧪 Mantenimiento

| Comando                     | Descripción                                                                   |
|-----------------------------|-------------------------------------------------------------------------------|
| `docker compose config`     | Valida y muestra la configuración final del archivo `compose.yml` (resuelto). |
| `docker compose rm`         | Elimina contenedores detenidos.                                               |
| `docker compose images`     | Lista las imágenes usadas por los servicios.                                  |
| `docker compose volumes ls` | Muestra los volúmenes asociados al proyecto.                                  |

#### 🚀 Desarrollo (opcional)

| Comando                                   | Descripción                                                                                      |
|-------------------------------------------|--------------------------------------------------------------------------------------------------|
| `docker compose watch`                    | Monitorea cambios en el código y reinicia contenedores automáticamente (requiere configuración). |
| `docker compose run <servicio> <comando>` | Ejecuta un comando ad-hoc en un nuevo contenedor del servicio. Ideal para migraciones o pruebas. |

> 💡 **Consejo**: Si usas múltiples archivos de compose (ej: `docker-compose.yml`,
`docker-compose.prod.yml`), puedes especificarlos con `-f`:
> ```bash
> docker compose -f docker-compose.yml -f docker-compose.prod.yml up
> ```

> 📁 **Proyecto**: Puedes cambiar el nombre del proyecto con `-p`:
> ```bash
> docker compose -p mi-app-proyecto up
> ```

