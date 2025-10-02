# Guía de Pruebas y Verificación de Astruxa

Este documento proporciona una serie de "smoke tests" para verificar que las funcionalidades clave del backend de Astruxa se comportan como se espera después de una instalación o un cambio importante.

**Prerrequisito:** Antes de ejecutar estas pruebas, asegúrate de haber seguido el `Development & Testing Workflow` del archivo `README.md` para tener la aplicación y el PLC simulado corriendo.

---

## Prueba 1: Verificar el Flujo de Datos de Extremo a Extremo (API de Dashboard)

**Objetivo:** Confirmar que los datos de telemetría generados por el PLC simulado se pueden consultar de forma agregada a través de la API.

**Pasos:**

1.  **Abre la Documentación de la API:**
    -   Navega a [http://localhost:8071/api/v1/docs](http://localhost:8071/api/v1/docs) en tu navegador.

2.  **Obtén un Token de Autenticación:**
    -   Busca el endpoint `POST /auth/login`.
    -   Haz clic en "Try it out" e introduce las credenciales del usuario administrador:
        ```json
        {
          "email": "admin@astruxa.com",
          "password": "admin_password"
        }
        ```
    -   Ejecuta y copia el `access_token` de la respuesta.

3.  **Autoriza tus Peticiones:**
    -   En la parte superior derecha, haz clic en el botón "Authorize".
    -   Pega el `access_token` en el campo "Value" y autoriza.

4.  **Obtén el `uuid` de un Activo:**
    -   Busca el endpoint `GET /assets`.
    -   Ejecútalo. En la respuesta, busca el activo cuyo `name` es "Prensa Hidráulica Schuler 500T".
    -   Copia el valor de su `uuid`.

5.  **Consulta la Telemetría del Activo:**
    -   Busca el endpoint `GET /telemetry/readings/{asset_id}`.
    -   Pega el `uuid` del activo en el campo `asset_id`.
    -   En el campo `metric_name`, escribe `temperature_celsius`.
    -   Ejecuta la petición.

**Resultado Esperado:**

-   Debes recibir una respuesta `200 OK` con un cuerpo JSON que es una lista de objetos. Cada objeto representará un minuto de datos de temperatura agregados, con los campos `bucket`, `avg_value`, `min_value` y `max_value`.

---

## Prueba 2: Verificar el Sistema de Autodiagnóstico

**Objetivo:** Confirmar que la aplicación detecta un fallo de conexión con un PLC y crea automáticamente una orden de trabajo correctiva.

**Pasos:**

1.  **Asegúrate de que el Sistema Esté Estable:**
    -   Con el PLC simulado y la aplicación corriendo, observa los logs de `backend_api` con `docker-compose logs -f backend_api`.
    -   Deberías ver los logs de `DEBUG` indicando que se están recibiendo datos del PLC.

2.  **Simula un Fallo Crítico:**
    -   Ve a la terminal donde está corriendo el `plc_simulator.py`.
    -   **Detén el simulador** presionando `Ctrl + C`.

3.  **Observa la Reacción del Sistema:**
    -   Vuelve a la terminal de los logs de `backend_api`.
    -   Verás que los logs de `DEBUG` se detienen.
    -   Después de unos segundos, empezarás a ver logs de `ERROR` con el mensaje `Connection refused`.
    -   **Espera un momento.** Inmediatamente después de los errores, nuestro `AstruxaLogHandler` debería activarse. Busca un log con el siguiente mensaje:
        ```
        INFO:app.core_engine.actions:Orden de trabajo correctiva creada automáticamente para el activo [UUID del activo].
        ```

4.  **Verifica la Creación de la Orden de Trabajo:**
    -   Vuelve a la documentación de la API en tu navegador (asegúrate de seguir autenticado).
    -   Busca el endpoint `GET /maintenance/work-orders/{work_order_id}`. Para encontrar el ID de la nueva orden, primero puedes listar todas con `GET /maintenance/work-orders`.
    -   Al consultar la nueva orden, deberías ver en el `summary` el texto: `Fallo de conexión detectado en la fuente de datos: PLC Simulator`.

---

## Prueba 3: Verificar el Sistema de Alertas Proactivo

**Objetivo:** Confirmar que el sistema evalúa los datos de telemetría entrantes y dispara una alarma cuando se cumple una regla definida por el usuario.

**Pasos:**

1.  **Prerrequisitos:**
    -   Asegúrate de que el sistema completo esté corriendo (PLC simulado y Docker).
    -   Asegúrate de estar autenticado como `admin@astruxa.com` en la documentación de la API (ver Prueba 1, pasos 2 y 3).
    -   Obtén el `uuid` del activo "Prensa Hidráulica Schuler 500T" (ver Prueba 1, paso 4).

2.  **Crea una Regla de Alerta:**
    -   Busca el endpoint `POST /alarming/rules`.
    -   Haz clic en "Try it out" e introduce el siguiente cuerpo de petición, **reemplazando `"string"` con el `uuid` real del activo** que copiaste:
        ```json
        {
          "assetId": "string",
          "metricName": "temperature_celsius",
          "condition": ">",
          "threshold": 28,
          "severity": "CRITICAL",
          "isEnabled": true
        }
        ```
    -   Ejecuta la petición. Deberías recibir una respuesta `201 Created`.

3.  **Observa la Reacción del Sistema:**
    -   El PLC simulado genera una temperatura que sigue una onda sinusoidal entre 10 y 30 grados. Tarde o temprano, superará los 28 grados.
    -   Observa los logs de `backend_api` con `docker-compose logs -f backend_api`.
    -   Espera a ver un log de `WARNING` con un mensaje similar a:
        ```
        WARNING:app.alarming.service:¡ALERTA! Regla [UUID de la regla] disparada para el activo [UUID del activo] con valor 28.19
        ```

4.  **Verifica la Alarma Activa:**
    -   En la documentación de la API, busca y ejecuta el endpoint `GET /alarming/alarms`.
    -   En la respuesta, deberías ver un nuevo objeto de alarma en estado `ACTIVE`, correspondiente a la regla que creaste.

5.  **Acusa Recibo de la Alarma (Opcional):**
    -   Copia el `uuid` de la alarma que acabas de ver.
    -   Busca el endpoint `POST /alarming/alarms/{alarm_id}/acknowledge`.
    -   Pega el `uuid` de la alarma en el campo `alarm_id` y ejecuta.
    -   La respuesta debería mostrar la misma alarma, pero ahora con el `status`: `ACKNOWLEDGED`.
