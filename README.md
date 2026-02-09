# Astruxa - El Sistema Operativo Industrial (Industrial OS)

> **Visión:** Astruxa no es solo un software de mantenimiento; es la infraestructura digital que orquesta la operación de la fábrica moderna, desde la gestión de activos hasta la inteligencia predictiva.

Este repositorio contiene el **Backend Core** de la plataforma, construido con una arquitectura robusta, escalable y segura para soportar operaciones de misión crítica en entornos industriales.

---

## 📚 Documentación Oficial

Para entender en profundidad cómo interactuar con la plataforma, consulta nuestros manuales:

*   📖 **[Manual de Uso de la API y Arquitectura](./MANUAL_DE_USO_API.md)**: Guía completa de endpoints, roles, modelo SaaS y visión del frontend.
*   🗺️ **[Roadmap Estratégico](./ROADMAP.md)**: Hacia dónde vamos (Mantenimiento Predictivo, Gemelo Digital).

---

## 🚀 Arquitectura y Capacidades

Astruxa está diseñada bajo una arquitectura **Multi-Tenant Híbrida** que garantiza el aislamiento de datos y la escalabilidad.

### 1. Núcleo SaaS (Software as a Service)
*   **Gestión de Inquilinos (Tenants):** Aislamiento lógico total de datos por organización.
*   **Planes y Suscripciones:** Control granular de límites (cuotas) y características (feature flags) según el plan contratado.
*   **Onboarding Automatizado:** Flujo de registro público y provisión instantánea de entornos.

### 2. Módulos Operativos (The "OS" Kernel)
*   **Activos (Assets):** Registro jerárquico y trazabilidad completa del ciclo de vida de la maquinaria.
*   **Mantenimiento (Maintenance):** Gestión de Órdenes de Trabajo (OTs) con flujos de aprobación y ejecución móvil.
*   **Compras (Procurement):** Gestión integrada de proveedores y repuestos críticos.
*   **Telemetría e IoT:** Ingesta masiva de datos de sensores para monitoreo en tiempo real.
*   **Alarmas Inteligentes:** Motor de reglas para detección temprana de anomalías.

### 3. Seguridad y Control (Enterprise Grade)
*   **RBAC Granular:** Sistema de roles y permisos dinámicos (`GLOBAL_SUPER_ADMIN`, `PLATFORM_ADMIN`, `TENANT_ADMIN`, `OPERATOR`).
*   **Auditoría Completa:** Registro inmutable de todas las acciones críticas ("Quién hizo qué y cuándo").
*   **Aprobaciones (Maker-Checker):** Flujos de doble validación para acciones sensibles (ej. borrado de activos).

---

## 🛠️ Stack Tecnológico

Construido sobre hombros de gigantes para garantizar rendimiento y mantenibilidad a largo plazo:

- **Backend Framework:** FastAPI (Python 3.12) - Alto rendimiento y tipado estático.
- **Base de Datos:** PostgreSQL 16 + TimescaleDB (Optimizado para series de tiempo IoT).
- **ORM:** SQLAlchemy 2.0 (Moderno, asíncrono).
- **Cache & Sesiones:** Redis.
- **Infraestructura:** Docker & Docker Compose.

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

### 4. Poblar Datos Maestros (Seeding)
Este script crea la estructura base: Roles, Permisos, Planes y un Tenant de Demostración.
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
