# Módulo de Telemetría

## 1. Visión General

El módulo de Telemetría es el sistema receptor de datos de series temporales de la aplicación. Su principal responsabilidad es la ingesta, almacenamiento y consulta eficiente de grandes volúmenes de lecturas de sensores provenientes de los activos de la planta.

---

## 2. Arquitectura y Componentes

-   **Modelo `SensorReading`**: Es el modelo principal, optimizado para TimescaleDB. Se almacena en una **hypertable** particionada por tiempo, lo que permite inserciones y consultas de rangos de tiempo extremadamente rápidas.

-   **`TelemetryRepository`**: Encapsula la lógica de acceso a datos. Está diseñado para:
    -   **Ingesta Masiva (`create_bulk_readings`)**: Inserta lotes de lecturas en una sola transacción para un rendimiento máximo.
    -   **Consultas Agregadas (`get_aggregated_readings_for_asset`)**: Utiliza la función `time_bucket()` de TimescaleDB para agregar datos sobre la marcha (promedio, mínimo, máximo) en intervalos de tiempo definidos, ideal para alimentar dashboards sin sobrecargar la base de datos.

-   **`TelemetryService`**: Orquesta la lógica de negocio. Actualmente, su función más importante es la **integración con el módulo de Alertas**. Después de cada ingesta de datos, pasa las nuevas lecturas al `AlarmingService` para su evaluación en tiempo real.

-   **API (`/telemetry`)**: Expone dos endpoints principales:
    -   `POST /readings`: Un endpoint de alto rendimiento para la ingesta masiva de datos.
    -   `GET /readings/{asset_id}`: Un endpoint potente y auditable para que los clientes (como dashboards) consulten datos agregados de series temporales.
