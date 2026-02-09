Excelente! Vamos con el **módulo más crítico de todo el sistema** — el corazón que late 24/7 en tu fábrica:

---

## 📄 `03-modulos/core-engine.md` — LISTO PARA COPIAR Y PEGAR

```markdown
# ⚙️ Módulo: Core Engine — El Corazón del Sistema

> **Motor de tiempo real que conecta, controla y sincroniza toda la planta: PLCs, sensores, actuadores, HMIs y comandos — con latencia milisegundos, tolerancia a fallos y seguridad industrial embebida.**

---

## 🎯 Propósito

El **Core Engine** es el **subsistema responsable de:**

- Conectar y mantener comunicación **estable y segura** con dispositivos industriales (PLCs, RTUs, sensores, actuadores).
- Procesar y almacenar **datos de telemetría en tiempo real** (cada 10ms - 1s).
- Ejecutar **comandos de control** (encender, parar, ajustar) con confirmación de seguridad.
- Sincronizar estado de planta con **interfaces de usuario (web, móvil, tablet)**.
- Gestionar **reconexiones automáticas, buffers locales y modos degradados**.
- Exponer APIs estandarizadas para que otros módulos (IA, mantenimiento, reporting) consuman datos.

> Sin este módulo, el sistema es un dashboard muerto. Con él, es un cerebro vivo.

---

## 🧩 Componentes Internos

```
[ PLCs / Sensores ] ←→ [ Protocol Adapters ] ←→ [ Data Ingestion Engine ]
                             ↓                           ↓
                      [ Command Router ] ←→ [ State Synchronizer ]
                             ↓                           ↓
                      [ Redis (Pub/Sub) ] ←→ [ PostgreSQL + TimescaleDB ]
                             ↓
                  [ WebSocket Gateway ] → [ HMIs Web / Móvil ]
```

---

## 🔌 Protocol Adapters (Conectores Industriales)

Cada protocolo tiene su propio adaptador (plugin-based):

| Protocolo   | Librería Python          | Función                                     | Estado Inicial |
|-------------|--------------------------|---------------------------------------------|----------------|
| OPC UA      | `opcua-asyncio`          | Conexión segura con PLCs modernos (Siemens, Beckhoff) | ✅ Activo      |
| Modbus TCP  | `pymodbus`               | Comunicación con PLCs legacy (Schneider, Allen-Bradley) | ✅ Activo      |
| MQTT        | `paho-mqtt`              | Sensores IoT, dispositivos de bajo consumo  | ⚙️ En desarrollo |
| Profinet    | Pasarela OPC UA ↔ Profinet | Integración con redes Profinet (requiere HW) | 🚧 Futuro      |

> ✅ **Cada adaptador se ejecuta como un microservicio independiente** → si uno falla, no cae todo el sistema.

---

## 📥 Data Ingestion Engine (Motor de Ingesta)

- **Función**: Recibe datos de los adaptadores → valida → normaliza → almacena → notifica.
- **Formato estandarizado interno**:
  ```json
  {
    "timestamp": "2025-04-05T14:23:45.123Z",
    "source_id": "plc_003",
    "machine_id": 7,
    "tag": "TEMP_MOTOR",
    "value": 87.4,
    "unit": "°C",
    "quality": "good" // o "bad", "uncertain"
  }
  ```
- **Almacenamiento**: Inserta en `sensor_data` (TimescaleDB) → optimizado para millones de registros/segundo.
- **Notificación**: Publica en Redis (canal `sensor_updates`) → para que WebSocket y módulos de IA escuchen.

---

## 🎛️ Command Router (Enrutador de Comandos)

- **Función**: Recibe comandos de usuarios (vía API/WebSocket) → valida permisos → ejecuta en PLC → confirma.
- **Ejemplo de comando**:
  ```json
  {
    "command_id": "cmd_20250405_001",
    "target": "plc_003",
    "action": "SET_SPEED",
    "value": 1200,
    "unit": "rpm",
    "user_id": 45,
    "auth_token": "jwt...",
    "confirmation_code": "7XK9" // MFA temporal
  }
  ```
- **Flujo de seguridad**:
  1. Valida JWT + rol del usuario.
  2. Verifica que el usuario tenga permiso sobre esa máquina.
  3. Genera código MFA temporal (enviado por app móvil o email).
  4. Espera confirmación (máx. 30 segundos).
  5. Ejecuta comando en PLC vía adaptador.
  6. Registra en tabla `command_audit` (quién, cuándo, qué, resultado).

---

## 🔄 State Synchronizer (Sincronizador de Estado)

- **Función**: Mantiene un “estado en vivo” de toda la planta en Redis (clave-valor).
- **Ejemplo**:
  ```bash
  # Redis
  SET machine:7:status "RUNNING"
  SET machine:7:speed "1200"
  SET machine:7:last_update "2025-04-05T14:23:45Z"
  ```
- **Beneficios**:
  - Las interfaces (web/móvil) leen de Redis → respuesta en <10ms.
  - Si PostgreSQL está ocupado, el sistema sigue respondiendo.
  - En caso de fallo, se reconstruye desde la última lectura en TimescaleDB.

---

## 📡 WebSocket Gateway (Puente en Tiempo Real)

- **Función**: Conecta las HMIs (web, móvil, tablet) con el motor en tiempo real.
- **Tecnología**: FastAPI + WebSockets (con `websockets` o `socket.io`).
- **Canales suscribibles**:
  - `machine_updates/{machine_id}`
  - `sensor_updates/{sensor_id}`
  - `alerts`
  - `command_confirmations/{user_id}`

> ✅ Soporta reconexión automática y re-suscripción → ideal para redes inestables en planta.

---

## 🛡️ Seguridad Embebida

- **Autenticación de comandos**: JWT + MFA temporal (código de 4 dígitos).
- **Autorización por máquina**: Tabla `user_machine_permissions` en PostgreSQL.
- **Encriptación en tránsito**: TLS 1.3 entre adaptadores y core.
- **Rate limiting**: Máx. 5 comandos por minuto por usuario (evita errores humanos).
- **Modo “Solo Lectura”**: Si el sistema detecta ataque, bloquea todos los comandos.

---

## 🧪 Modos de Operación

| Modo               | Comportamiento                                  | Caso de Uso                     |
|--------------------|-------------------------------------------------|----------------------------------|
| **Normal**         | Todo activo, latencia <100ms                   | Operación diaria                 |
| **Degradado**      | Sin conexión a PLC → usa último valor conocido  | Fallo de red temporal            |
| **Solo Lectura**   | No se permiten comandos                        | Ataque detectado / modo pánico   |
| **Simulación**     | Usa datos de archivo, no de PLC real           | Entrenamiento / pruebas          |
| **Offline (Móvil)**| App móvil guarda comandos localmente → sincroniza luego | Zonas sin señal Wi-Fi       |

---

## 📈 Métricas Clave (Monitoreadas por Prometheus)

- `core_engine_commands_per_second`
- `core_engine_latency_ms` (promedio de procesamiento)
- `core_engine_plc_connections_active`
- `core_engine_dropped_commands` (por errores o timeouts)
- `core_engine_reconnects_total`

---

## 🚨 Manejo de Errores y Tolerancia a Fallos

- **Reconexión automática**: Si un PLC se desconecta, el adaptador reintenta cada 5s.
- **Buffer local**: Si PostgreSQL no responde, guarda en Redis y reintentar en 10s.
- **Dead Letter Queue**: Comandos fallidos se guardan en `failed_commands` para análisis.
- **Heartbeat**: Cada PLC envía “latido” cada 10s → si no llega, alerta de desconexión.

---

## 🧪 Ejemplo de Flujo: Operario Ajusta Velocidad de Máquina

1. Operario en app móvil → toca “Ajustar velocidad” → ingresa 1500 rpm.
2. App envía comando vía WebSocket → Core Engine.
3. Core valida JWT → verifica permiso → genera MFA → envía push al móvil.
4. Operario confirma con código 7XK9.
5. Core envía comando SET_SPEED=1500 al adaptador Modbus.
6. Adaptador escribe en registro del PLC → recibe ACK.
7. Core guarda en `command_audit` → publica en Redis → WebSocket notifica a todas las HMIs.
8. Dashboard web actualiza velocidad en tiempo real.

⏱️ **Tiempo total: < 800ms.**

---

## 📁 Estructura de Código Recomendada (Backend)

```
backend/
├── core_engine/
│   ├── __init__.py
│   ├── protocol_adapters/
│   │   ├── opcua_adapter.py
│   │   ├── modbus_adapter.py
│   │   └── mqtt_adapter.py
│   ├── data_ingestion.py
│   ├── command_router.py
│   ├── state_synchronizer.py
│   ├── websocket_gateway.py
│   └── security.py
├── models/
│   └── core_models.py  # Pydantic models
├── database/
│   └── db_core.py      # Acceso a TimescaleDB + Redis
└── main.py             # FastAPI app + rutas
```

---

## 🧭 ¿Cómo empezar a desarrollar?

```bash
# 1. Entra a la carpeta backend
cd backend

# 2. Instala dependencias
pip install fastapi uvicorn opcua-asyncio pymodbus redis pydantic

# 3. Levanta el core engine
uvicorn core_engine.main:app --reload

# 4. Prueba conexión con PLC simulado (ver /simulators/plc_simulator.py)
python simulators/plc_simulator.py --protocol modbus --port 5020

# 5. Abre http://localhost:8000/docs → prueba endpoint /core/health
```

---

## 📌 Decisiones Clave

- **Redis como estado en vivo**: Para baja latencia en HMIs.
- **Comandos con MFA temporal**: Seguridad sin sacrificar usabilidad.
- **Adaptadores como plugins**: Fácil añadir nuevos protocolos sin tocar el core.
- **Formato estandarizado interno**: Desacopla protocolos de lógica de negocio.

---

> “El Core Engine no es el módulo más brillante. Es el más confiable.  
> Debe funcionar aunque la red tiemble, el PLC se reinicie, o el operario pulse el botón equivocado.”

➡️ **Siguiente paso recomendado: definir el módulo de IA (`ai-orchestrator.md`)**
```

---

