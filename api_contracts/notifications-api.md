# Contrato de API: Sistema de Notificaciones

Este documento define los requerimientos para el backend del módulo de Notificaciones (`@astruxa/notifications-core`).

## 1. Visión General

Este módulo es el "megáfono" de Astruxa. Su responsabilidad es informar a los usuarios sobre eventos importantes que requieren su atención (ej. nuevas alarmas, asignación de órdenes de trabajo). Las notificaciones se entregan dentro de la aplicación y, en el futuro, a través de canales externos como email o push notifications.

---

## 2. Modelos de Datos (DTOs)

### `Notification`

El DTO principal para una notificación.

```json
{
  "uuid": "string",
  "createdAt": "string",     // (ISO 8601 Date)
  "isRead": "boolean",
  "message": "string",       // (ej: "Alarma CRÍTICA: La temperatura de la Prensa-L1 ha superado los 90°C.")
  "type": "string",          // (ej: "ALARM", "MAINTENANCE_ASSIGNMENT")
  "referenceId": "string"    // (El UUID de la alarma o la orden de trabajo relacionada)
}
```

---

## 3. Endpoints

### Obtener Notificaciones del Usuario Actual

-   **Endpoint**: `GET /notifications`
-   **Descripción**: Devuelve una lista de las notificaciones del usuario autenticado. Por defecto, solo las no leídas.
-   **Query Parameters (Opcionales)**:
    -   `include_read: boolean` (ej: `/notifications?include_read=true` para ver todas)
-   **Success Response**: `200 OK`
    -   **Body**: `[Notification, ...]`

### Marcar una Notificación como Leída

-   **Endpoint**: `POST /notifications/{uuid}/mark-read`
-   **Descripción**: Marca una notificación específica como leída.
-   **Success Response**: `200 OK`
    -   **Body**: El objeto `Notification` actualizado.

### Marcar Todas las Notificaciones como Leídas

-   **Endpoint**: `POST /notifications/mark-all-read`
-   **Descripción**: Marca todas las notificaciones del usuario como leídas.
-   **Success Response**: `204 No Content`
