# Contrato de API: Sistema de Alertas

Este documento define los requerimientos para el backend del módulo de Alertas (`@astruxa/alarming-core`).

## 1. Visión General

Este módulo proporciona el "cerebro" reactivo del sistema. Permite a los usuarios definir reglas sobre los datos de telemetría y genera alertas accionables cuando esas reglas se cumplen. Las alertas pueden ser visualizadas, reconocidas por los operarios y, en el futuro, pueden disparar acciones automáticas.

---

## 2. Modelos de Datos (DTOs)

### `AlarmSeverity`

Un string que representa la criticidad de una alerta.

```json
"INFO" | "WARNING" | "CRITICAL"
```

### `AlarmStatus`

Un string que representa el estado de una alerta activa.

```json
"ACTIVE" | "ACKNOWLEDGED" | "CLEARED"
```

### `AlarmRule`

El DTO para definir una regla de alerta.

```json
{
  "uuid": "string",
  "assetId": "string",
  "metricName": "string",      // ej: "temperature_celsius"
  "condition": "string",       // ej: ">", "<", "=="
  "threshold": "number",
  "severity": "AlarmSeverity",
  "isEnabled": "boolean"
}
```

### `Alarm`

El DTO que representa una alerta que se ha disparado.

```json
{
  "uuid": "string",
  "triggeredAt": "string",     // (ISO 8601 Date)
  "acknowledgedAt": "string | null",
  "clearedAt": "string | null",
  "status": "AlarmStatus",
  "rule": "AlarmRule",         // La regla que disparó la alerta
  "triggeringValue": "number"  // El valor que causó la alerta
}
```

---

## 3. Endpoints

### Crear una Regla de Alerta

-   **Endpoint**: `POST /alarming/rules`
-   **Descripción**: Crea una nueva regla de alerta para un activo y una métrica.
-   **Permisos**: `Supervisor` o superior.
-   **Request Body**: Un objeto para crear la `AlarmRule` (sin el `uuid`).
-   **Success Response**: `201 Created`
    -   **Body**: La `AlarmRule` recién creada.

### Obtener todas las Alertas Activas

-   **Endpoint**: `GET /alarming/alarms`
-   **Descripción**: Devuelve una lista de todas las alertas que están actualmente en estado `ACTIVE` o `ACKNOWLEDGED`.
-   **Success Response**: `200 OK`
    -   **Body**: `[Alarm, ...]`

### Acusar Recibo de una Alerta

-   **Endpoint**: `POST /alarming/alarms/{uuid}/acknowledge`
-   **Descripción**: Permite a un usuario marcar una alerta como "vista" o "reconocida".
-   **Permisos**: `Operator` o superior.
-   **Success Response**: `200 OK`
    -   **Body**: El objeto `Alarm` actualizado.
