# PoC: Integración Real con Siemens LOGO! 8 (Corrugadora de Cartón)

Este documento describe paso a paso cómo conectar un PLC físico **Siemens LOGO! 8** a la plataforma **Astruxa** para monitorear una línea de producción de cartón corrugado en tiempo real.

---

## 1. Arquitectura de la Solución

El objetivo es leer variables críticas del proceso (temperatura, velocidad, metros producidos) desde el PLC y enviarlas a la nube (Astruxa) para su análisis.

```mermaid
graph LR
    A[PLC Siemens LOGO! 8] -- Modbus TCP (Puerto 502) --> B[Edge Gateway (Python Script)]
    B -- HTTPS (REST API) --> C[Astruxa Backend]
    C --> D[Base de Datos TimescaleDB]
```

### Variables del Proceso (Data Points)
Vamos a monitorear las siguientes variables simuladas en el PLC:

| Variable | Dirección LOGO! (VM) | Tipo Modbus | Unidad | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| **Estado Máquina** | V0.0 | Coil (Bool) | On/Off | 1=Corriendo, 0=Parada |
| **Velocidad Línea** | VW0 | Holding Register (Int) | m/min | Velocidad de los rodillos |
| **Temp. Rodillo A** | VW2 | Holding Register (Int) | °C | Temperatura de pre-calentamiento |
| **Temp. Rodillo B** | VW4 | Holding Register (Int) | °C | Temperatura de corrugado |
| **Metros Totales** | VD6 | Holding Register (DWord) | m | Contador acumulado de producción |

---

## 2. Configuración del PLC (LOGO! Soft Comfort)

Para que el LOGO! 8 actúe como Servidor Modbus TCP, sigue estos pasos en el software **LOGO! Soft Comfort**:

1.  **Configuración de Red:**
    *   Ve a `Herramientas` -> `Selección de dispositivo`.
    *   Configura la IP del LOGO! (ej. `192.168.1.10`) y la Máscara de Subred (`255.255.255.0`).
    *   Asegúrate de que tu PC esté en el mismo rango de red.

2.  **Habilitar Modbus TCP:**
    *   En la configuración del dispositivo, ve a `Configuración Ethernet` -> `Modbus`.
    *   Activa la casilla **"Permitir acceso vía Modbus"**.
    *   Puerto: **502** (por defecto).

3.  **Programa de Simulación (Lógica FBD/Ladder):**
    *   Crea un programa sencillo para simular datos cambiantes:
        *   **Generador de Pulsos Asíncrono:** Para simular el "latido" de la máquina.
        *   **Contador Adelante/Atrás:** Conectado al generador de pulsos para simular los "Metros Totales". Asigna su salida a la memoria `VD6`.
        *   **Entrada Analógica (o Potenciómetro Virtual):** Si tienes un módulo de expansión AM2, úsalo. Si no, usa un bloque "Amplificador Analógico" y asígnale un valor fijo o variable para simular la `Temperatura` en `VW2`.
        *   **Marcas (Flags):** Usa la marca `M1` para el estado de marcha/paro y mapéala a `V0.0`.

4.  **Mapeo de Variables (VM Mapping):**
    *   Ve a `Herramientas` -> `Mapeado de variables VM`.
    *   Asegúrate de que las direcciones de memoria (VW0, VW2, etc.) coincidan con las que leeremos vía Modbus.

5.  **Cargar Programa:**
    *   Sube el programa al PLC (`Ctrl+D`) y ponlo en modo **RUN**.

---

## 3. Configuración en Astruxa (Backend)

Ahora preparamos la plataforma para recibir los datos. Usa Postman o Swagger (`/docs`) para ejecutar estas llamadas.

### Paso 3.1: Login
Obtén tu token de acceso.
*   **POST** `/api/v1/auth/login`
*   **User:** `admin@demo.com` (o tu usuario admin)

### Paso 3.2: Crear Tipo de Activo
Definimos qué es una "Corrugadora".
*   **POST** `/api/v1/ops/assets/types`
*   **Body:**
    ```json
    {
      "name": "Corrugadora Industrial",
      "description": "Máquina para la fabricación de cartón corrugado.",
      "category": "MACHINE"
    }
    ```
*   *Nota el `id` retornado (ej. `uuid-type-1`).*

### Paso 3.3: Crear el Activo (La Máquina Real)
*   **POST** `/api/v1/ops/assets/`
*   **Body:**
    ```json
    {
      "name": "Corrugadora Línea 1",
      "asset_type_id": "uuid-type-1",
      "serial_number": "SIEMENS-LOGO-001",
      "location": "Nave Principal"
    }
    ```
*   *Nota el `id` retornado (ej. `uuid-asset-1`). Este será el `ASSET_ID` en el script.*

---

## 4. El "Edge Connector" (Script Python)

Este script actuará como puente. Correrá en tu PC (o en una Raspberry Pi conectada al PLC).

### Requisitos
Instala las librerías necesarias:
```bash
pip install pymodbus requests schedule
```

### Código del Conector (`edge_connector.py`)

Crea un archivo llamado `edge_connector.py` con el siguiente contenido:

```python
import time
import json
import requests
import schedule
from pymodbus.client import ModbusTcpClient
from datetime import datetime

# --- CONFIGURACIÓN ---
PLC_IP = "192.168.1.10"  # IP de tu LOGO!
PLC_PORT = 502

API_URL = "http://localhost:8000/api/v1/ops/telemetry/readings"
API_TOKEN = "TU_TOKEN_BEARER_AQUI"  # Pega el token obtenido en el Paso 3.1
ASSET_ID = "TU_UUID_DEL_ACTIVO_AQUI" # Pega el ID del activo creado en el Paso 3.3

# --- CONEXIÓN MODBUS ---
client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

def read_plc_data():
    """Lee los registros del PLC y retorna un diccionario con los valores."""
    try:
        if not client.connect():
            print("❌ Error: No se pudo conectar al PLC")
            return None

        # Leer Holding Registers (VW0, VW2, VW4) - 3 registros desde la dirección 0
        # Nota: En Modbus, las direcciones a veces tienen un offset de -1 o 40001.
        # Para LOGO!, VW0 suele ser la dirección 0.
        rr = client.read_holding_registers(0, 6, slave=1) 
        
        if rr.isError():
            print("❌ Error leyendo registros Modbus")
            return None

        # Decodificar datos (Ejemplo simplificado)
        velocidad = rr.registers[0]      # VW0
        temp_rodillo_a = rr.registers[1] # VW2
        temp_rodillo_b = rr.registers[2] # VW4
        
        # Leer Coils (Estado Máquina)
        rc = client.read_coils(0, 1, slave=1)
        estado_maquina = 1 if rc.bits[0] else 0

        return {
            "speed_m_min": velocidad,
            "temp_roller_a_c": temp_rodillo_a,
            "temp_roller_b_c": temp_rodillo_b,
            "machine_status": estado_maquina
        }

    except Exception as e:
        print(f"❌ Excepción: {e}")
        return None
    finally:
        client.close()

def send_telemetry():
    """Orquesta la lectura y el envío a la API."""
    data = read_plc_data()
    if not data:
        return

    # Preparar payload para Astruxa
    payload = {
        "readings": []
    }
    
    timestamp = datetime.utcnow().isoformat() + "Z"

    for metric, value in data.items():
        payload["readings"].append({
            "asset_id": ASSET_ID,
            "timestamp": timestamp,
            "metric_name": metric,
            "value": float(value)
        })

    # Enviar a la API
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        if response.status_code == 202:
            print(f"✅ [{datetime.now()}] Datos enviados: {data}")
        else:
            print(f"⚠️ Error API ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión API: {e}")

# --- BUCLE PRINCIPAL ---
print("🚀 Iniciando Edge Connector para Corrugadora...")
# Ejecutar cada 5 segundos
schedule.every(5).seconds.do(send_telemetry)

while True:
    schedule.run_pending()
    time.sleep(1)
```

---

## 5. Ejecución y Verificación

1.  **Asegura la conectividad:** Haz `ping 192.168.1.10` desde tu terminal para confirmar que ves al PLC.
2.  **Ejecuta el script:**
    ```bash
    python edge_connector.py
    ```
3.  **Verifica en Astruxa:**
    *   Usa el endpoint `GET /api/v1/ops/telemetry/readings/{asset_id}?metric_name=temp_roller_a_c` para ver cómo se acumulan los datos históricos.
    *   Si configuras una **Regla de Alarma** (ej. `temp_roller_a_c > 100`), verás cómo se dispara una alerta en el sistema cuando subas la temperatura simulada en el PLC.

---

## 6. Siguientes Pasos (Mejoras)

*   **Dockerizar el Script:** Convertir `edge_connector.py` en un contenedor Docker para desplegarlo fácilmente en cualquier gateway industrial.
*   **Escritura (Control):** Implementar la escritura inversa (API -> PLC) para, por ejemplo, detener la máquina remotamente si hay una emergencia (escribiendo en el Coil de Parada).
