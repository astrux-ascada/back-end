# Módulo de Auditoría

## 1. Visión General

El módulo de Auditoría proporciona un historial inmutable de las operaciones críticas que ocurren en el sistema. Su propósito es responder a la pregunta "¿Quién hizo qué, sobre qué y cuándo?". Esto es fundamental para la trazabilidad, el cumplimiento de normativas y el análisis forense de incidentes.

---

## 2. Arquitectura y Componentes

-   **Modelo `AuditLog`**: Es el corazón del módulo. Cada registro en esta tabla representa una única acción de negocio. Sus campos clave son:
    -   `timestamp`: Cuándo ocurrió el evento.
    -   `user_id`: Quién realizó la acción. Es `null` si la acción fue iniciada por el sistema (ej: una orden de trabajo automática).
    -   `entity_type` y `entity_id`: Qué entidad fue afectada (ej: "WorkOrder", "Asset").
    -   `action`: Qué se hizo (ej: "UPDATE_STATUS", "CREATE_ASSET").
    -   `details`: Un campo JSON que almacena el contexto del cambio (ej: `{"from": "OPEN", "to": "IN_PROGRESS"}`).

-   **`AuditService`**: Un servicio centralizado y desacoplado. Otros servicios de negocio (como `AssetService` o `MaintenanceService`) lo utilizan para registrar sus operaciones. No contiene lógica de negocio propia, su única responsabilidad es escribir en el log.

-   **API (`/auditing`)**: Expone un único endpoint principal:
    -   `GET /logs`: Un endpoint protegido para `Administrator` o `SuperUser` que permite consultar y filtrar el historial de auditoría, proporcionando una visión completa de la actividad en la planta.
