# Contrato de API: Autenticación y Autorización

Este documento define los requerimientos para el backend del módulo de autenticación y autorización (`@astruxa/auth-core`).

---

## 1. Roles & Permissions

El sistema se basa en un modelo de Control de Acceso Basado en Roles (RBAC) con los siguientes perfiles jerárquicos:

-   **`SuperUser`**: El "Dueño de la Plataforma". Rol técnico para la configuración del sistema. No participa en las operaciones diarias.
-   **`Administrator`**: El "Jefe de Planta". Gestiona usuarios, roles operativos y catálogos (ej. `AssetTypes`).
-   **`Supervisor`**: El "Jefe de Turno". Gestiona y asigna órdenes de trabajo.
-   **`Technician`**: El "Técnico de Mantenimiento". Ejecuta órdenes de trabajo asignadas.
-   **`Operator`**: El "Operario de Máquina". Solo puede visualizar el estado de los activos.

### `Permission`

Un string que representa un permiso atómico en formato `entidad:accion`.

**Ejemplos:**
- `asset:read`, `asset:create`
- `workorder:read`, `workorder:create`, `workorder:assign`
- `user:create`, `user:read`
- `configuration:read`, `configuration:update`
- `auditing:read`
- `admin:full-access` (un permiso especial para el `SuperUser`)

---

## 2. Modelos de Datos (DTOs)

### `Role`

```json
{
  "uuid": "string",
  "name": "string", // ej: "SuperUser"
  "permissions": ["Permission", ...]
}
```

### `Sector`

```json
{
  "uuid": "string",
  "name": "string",
  "description": "string | null"
}
```

### `User`

```json
{
  "uuid": "string",
  "isActive": true,
  "createdAt": "2023-10-27T10:00:00Z",
  "updatedAt": "2023-10-27T10:00:00Z",
  "name": "string",
  "email": "string",
  "avatarUrl": "string | null",
  "roles": ["Role", ...],
  "assignedSectors": ["Sector", ...]
}
```

---

## 3. Endpoints

### Iniciar Sesión

-   **Endpoint**: `POST /auth/login`
-   **Descripción**: Autentica a un usuario con email y contraseña.
-   **Request Body**:
    ```json
    {
      "email": "user@example.com",
      "password": "string"
    }
    ```
-   **Success Response**: `200 OK`
    -   **Body**: Un objeto que contiene el `access_token` (JWT) y el objeto `User` completo.

### Obtener Usuario Actual

-   **Endpoint**: `GET /auth/me`
-   **Descripción**: Devuelve el usuario autenticado basado en el token JWT actual.
-   **Success Response**: `200 OK`
    -   **Body**: El objeto `User` completo.

### Cerrar Sesión

-   **Endpoint**: `POST /auth/logout`
-   **Descripción**: Invalida el token JWT actual del usuario, eliminando la sesión del backend (Redis).
-   **Success Response**: `204 No Content`

### Limpiar Todas las Sesiones (SuperUser)

-   **Endpoint**: `POST /auth/sessions/clear-all`
-   **Descripción**: Invalida **todas** las sesiones de usuario activas. Acción crítica para cambios de turno.
-   **Permisos**: `admin:full-access`
-   **Success Response**: `200 OK`
