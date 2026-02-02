# Contrato de API: Autenticación y Autorización

Este documento define los requerimientos para el backend del módulo de autenticación y autorización (`@astruxa/auth-core`).

---

## 1. Roles & Permissions

El sistema se basa en un modelo de Control de Acceso Basado en Roles (RBAC) con los siguientes perfiles jerárquicos:

-   **`SuperUser`**: El "Dueño de la Plataforma". Rol técnico para la configuración del sistema.
-   **`Administrator`**: El "Jefe de Planta". Gestiona usuarios, roles operativos y catálogos.
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

(Los modelos `User`, `Role`, `Sector` se mantienen como están definidos anteriormente)

---

## 3. Endpoints de Autenticación Principal

### Iniciar Sesión

-   **Endpoint**: `POST /auth/login`
-   **Body**: `{ "email": "...", "password": "..." }`
-   **Response**: `{ "access_token": "...", "user": { ... } }`

### Obtener Usuario Actual

-   **Endpoint**: `GET /auth/me`
-   **Response**: El objeto `User` completo.

### Cerrar Sesión

-   **Endpoint**: `POST /auth/logout`
-   **Response**: `204 No Content`

---

## 4. Gestión de 2FA (Two-Factor Authentication)

### Iniciar Configuración de 2FA

-   **Endpoint**: `POST /auth/tfa/setup`
-   **Descripción**: Genera un nuevo secreto de 2FA para el usuario actual y devuelve la información necesaria para que el usuario lo escanee en su app de autenticación (Google Authenticator, Authy, etc.).
-   **Success Response**: `200 OK`
    -   **Body**:
        ```json
        {
          "setup_key": "string", // El secreto en formato base32
          "otpauth_url": "string" // La URL que se convierte en el código QR
        }
        ```

### Habilitar 2FA

-   **Endpoint**: `POST /auth/tfa/enable`
-   **Descripción**: Verifica el token proporcionado por el usuario y, si es correcto, activa permanentemente el 2FA para su cuenta.
-   **Request Body**:
    ```json
    {
      "token": "123456" // El código de 6 dígitos de la app de autenticación
    }
    ```
-   **Success Response**: `204 No Content`

### Verificar Token para Operación Crítica

-   **Endpoint**: `POST /auth/verify-token`
-   **Descripción**: Verifica un token de 2FA para autorizar una operación crítica.
-   **Request Body**:
    ```json
    {
      "token": "123456"
    }
    ```
-   **Success Response**: `200 OK`
    -   **Body**: `{ "verified": true }`
