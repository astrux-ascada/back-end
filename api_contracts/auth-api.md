# Contrato de API: Autenticación y Autorización

Este documento define los requerimientos para el backend del módulo de autenticación y autorización (`@astruxa/auth-core`).

## 1. Modelos de Datos (DTOs - Data Transfer Objects)

El backend debe exponer los siguientes modelos en sus respuestas JSON.

### `BaseEntity`

Todo modelo principal debe incluir estos campos.

```json
{
  "uuid": "string",         // (UUID v4)
  "isActive": "boolean",
  "createdAt": "string",    // (ISO 8601 Date)
  "updatedAt": "string"     // (ISO 8601 Date)
}
```

### `Permission`

Un string que representa un permiso atómico.

```json
"entidad:accion" // ej: "alarm:acknowledge"
```

### `Role`

```json
{
  "uuid": "string",
  "name": "string",
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

## 2. Endpoints

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
    -   **Body**: El objeto `User` completo.
    -   **Nota**: El backend debe gestionar la sesión (ej: mediante una cookie `httpOnly` segura).
-   **Error Responses**:
    -   `401 Unauthorized`: Credenciales incorrectas.
    -   `403 Forbidden`: Usuario inactivo (`isActive: false`).

### Verificar Token 2FA

-   **Endpoint**: `POST /auth/verify-token`
-   **Descripción**: Verifica un token de 2FA después del login.
-   **Request Body**:
    ```json
    {
      "token": "123456"
    }
    ```
-   **Success Response**: `200 OK`
    -   **Body**: El objeto `User` completo.
-   **Error Response**:
    -   `401 Unauthorized`: Token inválido o expirado.

### Obtener Usuario Actual

-   **Endpoint**: `GET /auth/me`
-   **Descripción**: Devuelve el usuario autenticado basado en la sesión actual (cookie).
-   **Success Response**: `200 OK`
    -   **Body**: El objeto `User` completo.
-   **Error Response**:
    -   `401 Unauthorized`: No hay una sesión válida.

### Cerrar Sesión

-   **Endpoint**: `POST /auth/logout`
-   **Descripción**: Invalida la sesión actual del usuario.
-   **Success Response**: `204 No Content`
-   **Error Response**:
    -   `401 Unauthorized`: No hay una sesión que cerrar.
