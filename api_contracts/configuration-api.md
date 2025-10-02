# Contrato de API: Configuración del Sistema

Este documento define los requerimientos para el backend del módulo de Configuración (`@astruxa/configuration-core`).

## 1. Visión General

Este módulo permite a un `SuperUser` ajustar el comportamiento de la aplicación sin necesidad de modificar el código. Gestiona parámetros clave-valor y "enums" dinámicos.

---

## 2. Modelos de Datos (DTOs)

### `ConfigurationParameter`

```json
{
  "key": "string",         // (ej: "maintenance.preventive.default_days_interval")
  "value": "string",       // (El valor se interpreta en el backend)
  "description": "string",
  "isEditable": "boolean"  // (Indica si el frontend debe permitir su edición)
}
```

### `EnumType`

```json
{
  "name": "string",        // (ej: "WorkOrderStatus")
  "description": "string",
  "values": ["EnumValue", ...]
}
```

### `EnumValue`

```json
{
  "value": "string",       // (ej: "IN_PROGRESS")
  "label": "string",       // (ej: "En Progreso")
  "color": "string | null" // (ej: "#3b82f6")
}
```

---

## 3. Endpoints

Todos los endpoints en este módulo requieren permisos de `SuperUser`.

### Obtener todos los Parámetros de Configuración

-   **Endpoint**: `GET /configuration/parameters`
-   **Descripción**: Devuelve una lista de todos los parámetros de configuración del sistema.
-   **Success Response**: `200 OK`
    -   **Body**: `[ConfigurationParameter, ...]`

### Actualizar un Parámetro de Configuración

-   **Endpoint**: `PATCH /configuration/parameters/{key}`
-   **Descripción**: Actualiza el valor de un parámetro de configuración específico.
-   **Request Body**:
    ```json
    {
      "value": "120" // Nuevo valor como string
    }
    ```
-   **Success Response**: `200 OK`
    -   **Body**: El objeto `ConfigurationParameter` actualizado.

### Obtener todos los Enums Dinámicos

-   **Endpoint**: `GET /configuration/enums`
-   **Descripción**: Devuelve una lista de todos los tipos de enums gestionables.
-   **Success Response**: `200 OK`
    -   **Body**: `[EnumType, ...]`

### Añadir un Valor a un Enum

-   **Endpoint**: `POST /configuration/enums/{enumName}/values`
-   **Descripción**: Añade un nuevo valor a un enum existente (ej: un nuevo estado para las órdenes de trabajo).
-   **Request Body**: `EnumValue`
-   **Success Response**: `201 Created`
    -   **Body**: El objeto `EnumType` actualizado.
