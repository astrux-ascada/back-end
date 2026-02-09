# Módulo de Integración de Videovigilancia (El "Ojo Digital")

## 1. Visión General

Este documento describe la arquitectura para integrar un sistema de videovigilancia inteligente en Astruxa. El objetivo es transformar las cámaras IP de simples dispositivos de visualización en **sensores activos** que forman parte del sistema de control y diagnóstico de la planta.

El sistema, apodado el "Ojo Digital", permitirá:

-   **Visualización en Tiempo Real:** Supervisar zonas críticas o de difícil acceso desde un dashboard centralizado.
-   **Grabación por Evento:** Grabar clips de vídeo automáticamente en respuesta a eventos del sistema (alertas de sensores, creación de órdenes de trabajo, etc.), optimizando el almacenamiento y facilitando el análisis de causa raíz.
-   **Análisis con IA (Futuro):** Utilizar modelos de Computer Vision para detectar anomalías visuales (fugas, humo, intrusiones) y generar alertas o acciones proactivas.

---

## 2. Arquitectura Propuesta

La implementación se integrará de forma nativa en nuestra arquitectura modular existente.

### 2.1. Módulo `@/assets`

Las cámaras se tratarán como un tipo más de activo dentro del sistema.

-   **`AssetType`**: Se creará un nuevo tipo de activo con la categoría `CAMERA`.
    -   **Ejemplo:** `name: "Cámara IP Axis P1375"`, `category: "CAMERA"`.
-   **`Asset`**: Cada cámara física instalada en la planta será una instancia de `Asset`.
    -   **Ejemplo:** `serial_number: "AX-P1375-001"`, `sector: "Línea de Estampado 1"`.
    -   El campo `properties` del activo almacenará la información de conexión, como la URL del stream RTSP.

### 2.2. Módulo `@/core_engine`

El motor de comunicación se encargará de conectarse a los streams de vídeo.

-   **`DataSource`**: Se creará una `DataSource` por cada cámara, con el protocolo `RTSP`.
-   **`RtspConnector`**: Se desarrollará un nuevo conector, similar al `OpcUaConnector`, que utilizará librerías como OpenCV o GStreamer para conectarse al stream RTSP de la cámara.
    -   Este conector no leerá "tags", sino que proporcionará acceso a los fotogramas de vídeo.

### 2.3. Nuevo Módulo `@/video`

Se creará un nuevo módulo de dominio para gestionar la lógica específica de vídeo.

-   **Modelos:**
    -   `VideoClip`: Un modelo para registrar los clips de vídeo grabados. Campos: `asset_id` (la cámara que grabó), `start_time`, `end_time`, `triggering_event` (ej. "WorkOrder-123"), `storage_path` (dónde se guarda el archivo .mp4).
-   **`VideoService`**: Contendrá la lógica de negocio:
    -   `start_recording(asset_id, duration)`: Inicia una grabación.
    -   `get_clip(clip_id)`: Devuelve la información de un clip.
    -   `get_clips_for_work_order(work_order_id)`: Encuentra todos los clips asociados a una orden de trabajo.
-   **API:** Expondrá endpoints para que el frontend pueda listar y reproducir los clips grabados.

---

## 3. Flujo de Trabajo: Grabación por Evento

Este es un ejemplo de cómo funcionaría el sistema de forma proactiva:

1.  **Evento:** Un sensor de vibración en la `Prensa-L1` supera un umbral crítico.
2.  **Alerta:** El `TelemetryService` o un futuro `AlarmsService` genera un evento de "Alerta de Alta Vibración".
3.  **Acción:** El `AstruxaLogHandler` (nuestro "oyente") o un futuro sistema de reglas de negocio intercepta este evento.
4.  **Llamada al Servicio:** El manejador del evento llama a `maintenance_service.create_work_order(...)` para crear una orden de trabajo correctiva.
5.  **Grabación de Vídeo:** Inmediatamente después, llama a `video_service.start_recording(camera_id, duration=60)`, donde `camera_id` es el ID de la cámara que está apuntando a la `Prensa-L1`.
6.  **Registro:** El `VideoService` se conecta al stream a través del `RtspConnector`, graba un clip de 60 segundos, lo guarda en el almacenamiento y crea un nuevo registro `VideoClip` en la base de datos, asociándolo a la nueva orden de trabajo.

## 4. Roadmap a Futuro: Análisis con IA

Una vez que el sistema de grabación esté funcionando, el siguiente paso será el análisis en tiempo real.

-   El `RtspConnector` podría enviar fotogramas (ej. 1 por segundo) a un servicio de inferencia de IA.
-   Este servicio ejecutaría modelos de Computer Vision (ej. YOLOv8) para detectar objetos, humo, fugas, etc.
-   Si se detecta una anomalía, el servicio de IA podría generar un evento que, a su vez, dispare una alerta o una orden de trabajo, cerrando el ciclo de la supervisión autónoma.
