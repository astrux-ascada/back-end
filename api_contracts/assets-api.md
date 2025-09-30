# Contrato de API: Gestión de Activos (Assets)

Este documento define los requerimientos para el backend del módulo de Gestión de Activos (`@astruxa/assets-core`).

## 1. Modelos de Datos (DTOs)

El backend debe exponer los siguientes modelos en sus respuestas JSON.

### `AssetType`

Un string que representa el tipo de activo.

```json
"MACHINE" | "SENSOR" | "PLC" | "AREA"
```

### `AssetStatus`

Un string que representa el estado operativo del activo.

```json
"RUNNING" | "STOPPED" | "FAULT" | "MAINTENANCE"
```

### `Asset`

El DTO principal para un activo. Hereda los campos de `BaseEntity` (`uuid`, `isActive`, `createdAt`, `updatedAt`).

```json
{
  "uuid": "string",
  "isActive": true,
  "createdAt": "2023-10-28T10:00:00Z",
  "updatedAt": "2023-10-28T10:00:00Z",
  "name": "string",
  "description": "string | null",
  "sector": {
    "uuid": "string",
    "name": "string"
  },
  "type": "AssetType",
  "status": "AssetStatus",
  "parentId": "string | null",
  "properties": {
    "model": "Siemens XYZ",
    "power_kw": 75
  }
}
```

---

## 2. Endpoints

### Obtener todos los Activos

-   **Endpoint**: `GET /assets`
-   **Descripción**: Devuelve una lista de todos los activos. Debe soportar filtros como query parameters.
-   **Query Parameters (Opcionales)**:
    -   `type: AssetType` (ej: `/assets?type=SENSOR`)
    -   `sectorId: string` (ej: `/assets?sectorId=uuid-del-sector`)
-   **Success Response**: `200 OK`
    -   **Body**: `[Asset, ...]`

### Obtener un Activo por su UUID

-   **Endpoint**: `GET /assets/{uuid}`
-   **Descripción**: Devuelve los detalles de un activo específico.
-   **Success Response**: `200 OK`
    -   **Body**: `Asset`
-   **Error Response**:
    -   `404 Not Found`: Si no se encuentra un activo con el UUID proporcionado.

### Actualizar el Estado de un Activo

-   **Endpoint**: `PATCH /assets/{uuid}/status`
-   **Descripción**: Actualiza el estado operativo de un activo específico.
-   **Request Body**:
    ```json
    {
      "status": "MAINTENANCE"
    }
    ```
-   **Success Response**: `200 OK`
    -   **Body**: El objeto `Asset` actualizado.
-   **Error Responses**:
    -   `400 Bad Request`: Si el estado proporcionado no es válido.
    -   `404 Not Found`: Si el activo no existe.
