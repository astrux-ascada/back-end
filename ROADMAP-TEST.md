# Guía de Pruebas y Verificación de Astruxa

Este documento proporciona una serie de "smoke tests" para verificar que las funcionalidades clave del backend de Astruxa se comportan como se espera.

**Prerrequisito:** Antes de ejecutar estas pruebas, asegúrate de haber seguido el `Development & Testing Workflow` del archivo `README.md` para tener la aplicación y los simuladores corriendo.

---

## Prueba 1: Flujo de Datos de Extremo a Extremo (API de Dashboard)

**Objetivo:** Confirmar que los datos de telemetría se pueden consultar de forma agregada a través de la API.

**Pasos:**
1.  **Autentícate:** Abre la [documentación de la API](http://localhost:8071/api/v1/docs), usa `POST /auth/login` con `admin@astruxa.com` y autoriza las peticiones con el token recibido.
2.  **Obtén un `asset_id`:** Usa `GET /assets` para encontrar y copiar el `uuid` del activo "Prensa Hidráulica Schuler 500T".
3.  **Consulta la Telemetría:** Usa `GET /telemetry/readings/{asset_id}`, pega el `uuid` y establece `metric_name` a `temperature_celsius`.

**Resultado Esperado:** Una respuesta `200 OK` con una lista de datos de temperatura agregados por minuto.

---

## Prueba 2: Sistema de Autodiagnóstico (Creación Automática de OT)

**Objetivo:** Confirmar que la aplicación crea una orden de trabajo cuando un dispositivo falla.

**Pasos:**
1.  **Observa el Flujo Normal:** Con todo corriendo, mira los logs de `backend_api` (`docker-compose logs -f backend_api`) y confirma que llegan datos.
2.  **Simula un Fallo:** Detén el `plc_simulator.py` con `Ctrl + C`.
3.  **Observa la Reacción:** En los logs del backend, verás errores de `Connection refused`, seguidos de un mensaje `INFO` que dice: `Orden de trabajo correctiva creada automáticamente...`.
4.  **Verifica la OT:** Usa la API (`GET /maintenance/work-orders`) para confirmar que se ha creado una nueva orden de trabajo con el resumen "Fallo de conexión detectado...".

---

## Prueba 3: Sistema de Alertas Proactivo

**Objetivo:** Confirmar que el sistema dispara una alarma cuando se cumple una regla definida por el usuario.

**Pasos:**
1.  **Crea una Regla de Alerta:** Usa `POST /alarming/rules` con el `uuid` de la prensa y el siguiente cuerpo:
    ```json
    {
      "assetId": "<el-uuid-de-la-prensa>",
      "metricName": "temperature_celsius",
      "condition": ">",
      "threshold": 28,
      "severity": "CRITICAL"
    }
    ```
2.  **Observa la Reacción:** El PLC simulado genera una temperatura que varía. Espera a que supere los 28 grados. En los logs del backend, busca un `WARNING` que diga: `¡ALERTA! Regla ... disparada ...`.
3.  **Verifica la Alarma:** Usa `GET /alarming/alarms` para confirmar que se ha creado una nueva alarma en estado `ACTIVE`.

---

## Prueba 4: Flujo de Configuración y Uso de 2FA

**Objetivo:** Confirmar que un usuario puede configurar y utilizar el 2FA para autorizar una acción.

**Pasos:**
1.  **Prerrequisitos:** Asegúrate de estar autenticado como `admin@astruxa.com` en la documentación de la API.

2.  **Iniciar Configuración de 2FA:**
    -   Busca y ejecuta el endpoint `POST /auth/tfa/setup`.
    -   En la respuesta, copia el valor de `otpauth_url`.

3.  **Escanear el Código QR:**
    -   Pega la `otpauth_url` en un generador de códigos QR online (ej: `www.the-qrcode-generator.com`).
    -   Escanea el código QR generado con tu aplicación de autenticación (Google Authenticator, Authy, etc.). Verás una nueva cuenta para `admin@astruxa.com`.

4.  **Habilitar 2FA:**
    -   Busca el endpoint `POST /auth/tfa/enable`.
    -   Introduce el código de 6 dígitos que muestra tu app en el cuerpo de la petición:
        ```json
        {
          "token": "123456"
        }
        ```
    -   Ejecuta. Deberías recibir una respuesta `204 No Content`, indicando que el 2FA se ha activado correctamente.

5.  **Verificar un Token:**
    -   Espera a que tu app genere un nuevo código.
    -   Busca y ejecuta el endpoint `POST /auth/verify-token` con el nuevo código.

**Resultado Esperado:**

-   Debes recibir una respuesta `200 OK` con el cuerpo `{"verified": true}`, confirmando que el sistema puede validar los tokens correctamente.
