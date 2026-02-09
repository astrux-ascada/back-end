# Módulo de Alertas

## 1. Visión General

El módulo de Alertas es el "cerebro" reactivo de Astruxa. Su función es evaluar continuamente el flujo de datos de telemetría contra un conjunto de reglas predefinidas por el usuario. Cuando una regla se cumple (ej: una temperatura supera un umbral), el módulo genera una "Alarma" accionable.

Este sistema permite una supervisión proactiva de la planta, notificando a los operarios sobre condiciones anómalas en el momento en que ocurren.

---

## 2. Arquitectura y Componentes

-   **Modelo `AlarmRule`**: Define las condiciones para disparar una alarma. Contiene el `asset_id` y `metric_name` a monitorear, la `condition` (>, <, ==), el `threshold` (umbral) y la `severity` (criticidad).

-   **Modelo `Alarm`**: Representa una instancia de una alerta que se ha disparado. Registra qué regla la causó, el valor que la disparó y su ciclo de vida (`ACTIVE`, `ACKNOWLEDGED`, `CLEARED`).

-   **`AlarmingService`**: El corazón del módulo. Mantiene una copia de las reglas activas en memoria para una evaluación de alto rendimiento. Su método `evaluate_reading` es llamado por el `TelemetryService` por cada nuevo dato de sensor, permitiendo una reacción en tiempo real.

-   **API (`/alarming`)**: Expone endpoints para que los usuarios gestionen el sistema:
    -   `POST /rules`: Permite a los supervisores crear nuevas reglas de alerta.
    -   `GET /alarms`: Permite a los operarios ver las alarmas activas.
    -   `POST /alarms/{id}/acknowledge`: Permite a un operario "acusar recibo" de una alarma, indicando que está siendo atendida.
