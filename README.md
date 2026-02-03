# Astruxa - Industrial Orchestrator 5.0 (SaaS Backend)

Este proyecto es el backend principal para **Astruxa**, una plataforma de orquestación industrial Multi-Tenant (SaaS) construida con **FastAPI**, diseñada para la Industria 5.0.

## 🚀 Descripción

Astruxa permite a múltiples organizaciones industriales gestionar sus activos, mantenimiento y operaciones de forma segura y aislada en una única plataforma.

### Características Clave
- **Arquitectura Multi-Tenant Híbrida:** Aislamiento lógico de datos por `tenant_id`.
- **Modelo de Negocio SaaS:** Gestión de Partners, Planes y Suscripciones.
- **Seguridad Enterprise:** Login con "Gatekeeper" (validación de suscripción), protección contra fuerza bruta y control de sesiones.
- **Media Manager:** Sistema seguro de subida de archivos (Local/S3).
- **Módulo de Aprobaciones:** Flujo "Maker-Checker" para acciones críticas.

---

## 🏗️ Arquitectura y Roles

El sistema se divide en tres niveles de gestión:

### 1. Nivel Plataforma (`/sys-mgt`)
Gestionado por los dueños del SaaS y Partners Regionales.
- **`GLOBAL_SUPER_ADMIN`**: Acceso total. Gestiona Partners y Planes.
- **`PARTNER_ADMIN`**: Gestiona sus propios Tenants (Clientes).

### 2. Nivel Organización (`/back-office`)
Gestionado por el cliente final.
- **`TENANT_ADMIN`**: El "Gerente de Planta". Gestiona usuarios, roles y facturación de su organización.

### 3. Nivel Operativo (`/ops`)
El día a día en la planta.
- **`MAINTENANCE_MANAGER`**: Planifica paradas y mantenimientos.
- **`SUPERVISOR`**: Aprueba solicitudes y asigna tareas.
- **`TECHNICIAN`**: Ejecuta órdenes de trabajo.

---

## 🛠️ Stack Tecnológico

- **Backend:** FastAPI (Python 3.12)
- **Base de Datos:** PostgreSQL 16 + TimescaleDB (Series de Tiempo)
- **ORM:** SQLAlchemy 2.0
- **Cache & Sesiones:** Redis
- **Migraciones:** Alembic
- **Infraestructura:** Docker Compose

---

## ⚡ Guía de Inicio Rápido (Desarrollo)

Sigue estos pasos para levantar el entorno completo desde cero.

### Prerrequisitos
- Docker y Docker Compose instalados.
- Python 3.12+ (opcional, para herramientas locales).

### 1. Configuración de Entorno
Copia el archivo de ejemplo y ajústalo si es necesario (por defecto funciona para local).
```sh
cp .env.example .env
```

### 2. Levantar Servicios
```sh
docker-compose up --build -d
```

### 3. Inicializar Base de Datos (Migraciones)
Aplica el esquema más reciente.
```sh
docker-compose exec backend_api alembic upgrade head
```

### 4. Poblar Datos Maestros (Seeding SaaS)
Este script crea el Partner Global, los Planes y un Tenant de Demostración.
```sh
docker-compose exec backend_api python scripts/seed_saas.py
```
*Credenciales generadas:*
- **Super Admin:** `admin@astruxa.com` / `AstruxaAdmin2024!`

---

## 🧪 Testing y Verificación

### Acceso a la API
- **Swagger UI:** [http://localhost:8071/api/v1/docs](http://localhost:8071/api/v1/docs)
- **ReDoc:** [http://localhost:8071/api/v1/redoc](http://localhost:8071/api/v1/redoc)

### Generar Archivos de Traducción (I18N)
Si añades nuevos mensajes de error en el backend, actualiza el JSON para el frontend:
```sh
docker-compose exec backend_api python scripts/generate_i18n.py
```

---

## 📦 Estructura del Proyecto

```
/app
  /api          # Routers (v1/ops, v1/sys-mgt, etc.)
  /core         # Configuración, seguridad, middlewares
  /identity     # Usuarios, Auth, Modelos SaaS (Tenant, Plan)
  /assets       # Gestión de Activos
  /maintenance  # Órdenes de Trabajo
  /procurement  # Compras y Almacén
  /media        # Media Manager (Archivos)
  /auditing     # Logs y Aprobaciones
/alembic        # Migraciones de BD
/scripts        # Scripts de utilidad (seeding, i18n)
```
