# Referencia de la API de Activos (Assets)

Esta sección documenta los endpoints disponibles para la gestión de activos en el sistema.

---

## Actualizar un Activo

Actualiza los detalles de una instancia de activo existente. Esta operación está restringida a usuarios con rol `Admin` o `Super User`.

- **Método:** `PUT`
- **Ruta:** `/api/v1/assets/{asset_id}`

### Parámetros de Ruta

| Nombre      | Tipo   | Descripción                        |
|-------------|--------|------------------------------------|
| `asset_id`  | `UUID` | El identificador único del activo. |

### Cuerpo de la Petición (`AssetUpdate`)

El cuerpo de la petición debe ser un JSON con los campos que se desean actualizar. Todos los campos son opcionales.

```json
{
  "sector_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "serial_number": "SN-987654321",
  "location": "Planta 2, Línea de Ensamblaje B",
  "status": "maintenance",
  "properties": {
    "voltage": "220V",
    "max_speed": "3000 RPM"
  },
  "last_maintenance_at": "2025-10-11",
  "warranty_expires_at": "2028-10-11"
}
```

### Respuesta Exitosa (Código `200 OK`)

Si la actualización es exitosa, la API devuelve el objeto completo del activo actualizado en formato `AssetReadDTO`.

```json
{
  "uuid": "a4b1c2d3-e4f5-6789-0123-456789abcdef",
  "isActive": false,
  "createdAt": "2025-01-15T10:30:00Z",
  "updatedAt": "2025-10-11T18:00:00Z",
  "name": "Bomba Centrífuga X-100",
  "description": "Bomba para el sistema de refrigeración principal.",
  "type": "PUMP",
  "status": "maintenance",
  "properties": {
    "voltage": "220V",
    "max_speed": "3000 RPM"
  },
  "sector": {
    "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "name": "Sector de Refrigeración"
  },
  "parentId": null
}
```

### Respuestas de Error

- **`403 Forbidden`**: Si el usuario no tiene los permisos de `Admin` o `Super User`.
- **`404 Not Found`**: Si no se encuentra un activo con el `asset_id` proporcionado.
- **`422 Unprocessable Entity`**: Si los datos enviados en el cuerpo de la petición no son válidos (por ejemplo, un tipo de dato incorrecto).
