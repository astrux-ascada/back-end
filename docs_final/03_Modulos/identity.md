# 🔐 Módulo: Identity — Autenticación y Gestión de Acceso

> **Sistema de identidad y acceso con arquitectura Zero Trust, RBAC granular y auditoría, diseñado para proteger la plataforma y garantizar que solo las personas correctas realicen las acciones correctas.**

---

## 🎯 Propósito

El **Módulo de Identidad** es el subsistema central responsable de:

- **Autenticar usuarios** y gestionar sus sesiones de forma segura.
- **Autorizar accesos** mediante un sistema de Roles y Permisos (RBAC).
- **Gestionar la estructura de usuarios** tanto a nivel de Tenant como a nivel de Plataforma.
- **Proteger los endpoints** de la API con dependencias de seguridad.

---

## 🛠️ Arquitectura Técnica

El módulo sigue una arquitectura limpia de 3 capas:

1.  **API Layer (`api_*.py`)**: Define los endpoints, valida los datos de entrada (usando Schemas) y gestiona las respuestas HTTP.
2.  **Service Layer (`*_service.py`)**: Contiene la lógica de negocio pura. Orquesta las operaciones, aplica reglas y llama a los repositorios.
3.  **Repository Layer (`repository.py`)**: Se encarga de la interacción directa con la base de datos a través de los modelos de SQLAlchemy.

---

## 🔑 Gestión de Acceso a Nivel de Tenant

Esta es la funcionalidad estándar que usan los clientes para gestionar sus propios equipos.

- **Alcance:** Un usuario solo puede ver y gestionar a otros usuarios **dentro de su mismo tenant**.
- **Endpoints:**
    - `GET /api/v1/identity/users`: Listar usuarios del tenant.
    - `POST /api/v1/identity/users`: Crear un nuevo usuario en el tenant.
    - `PUT /api/v1/identity/users/{user_id}`: Actualizar un usuario del tenant.
- **Limitaciones:** Esta funcionalidad está sujeta a las limitaciones del plan de suscripción del tenant (ej. número máximo de usuarios).

---

## 👑 Gestión Global de Usuarios (Administradores de Plataforma)

Esta es la funcionalidad avanzada que permite a los administradores de Astruxa gestionar toda la base de usuarios de la plataforma.

- **Alcance:** `GLOBAL_SUPER_ADMIN` y `PLATFORM_ADMIN` pueden ver y gestionar usuarios de **todos los tenants**, o incluso usuarios sin tenant (otros administradores).
- **Endpoints:**
    - **Base URL:** `/api/v1/sys-mgt/identity`

| Método | Endpoint | Descripción | Permiso Requerido |
| :--- | :--- | :--- | :--- |
| `GET` | `/users/all` | Listar **todos** los usuarios de la plataforma. | `user:read_all` |
| `POST` | `/users` | Crear un nuevo usuario en cualquier tenant o sin tenant. | `user:create_any` |
| `PUT` | `/users/{user_id}` | Actualizar cualquier usuario de la plataforma. | `user:update_any` |
| `DELETE` | `/users/{user_id}` | Eliminar (soft delete) cualquier usuario. | `user:delete_any` |

### Lógica de Jerarquía

Para mantener la integridad y seguridad de la plataforma, se aplican las siguientes reglas en la capa de servicio (`AuthService`):

1.  **PLATFORM_ADMIN vs GLOBAL_SUPER_ADMIN:** Un `PLATFORM_ADMIN` **no puede** modificar ni eliminar a un usuario con el rol `GLOBAL_SUPER_ADMIN`. Esto asegura que solo los super administradores puedan gestionar a otros super administradores.
2.  **Prohibido Auto-Modificarse:** Ningún administrador puede usar estos endpoints para modificarse o eliminarse a sí mismo. Esto previene bloqueos accidentales y fuerza el uso de la página de perfil personal para cambios propios.

---

## 🔐 Seguridad y Permisos (RBAC)

El sistema de permisos es el núcleo de la seguridad.

- **Permisos de Tenant:** `user:create`, `user:read`, `user:update`, `user:delete`. Permiten la gestión dentro de un mismo tenant.
- **Permisos de Plataforma:** `user:create_any`, `user:read_all`, `user:update_any`, `user:delete_any`. Otorgan control total y solo deben ser asignados a roles de administración.

El script de inicialización (`scripts/create_superuser.py`) se encarga de crear todos los permisos y asignarlos correctamente a los roles `GLOBAL_SUPER_ADMIN` y `PLATFORM_ADMIN`.
