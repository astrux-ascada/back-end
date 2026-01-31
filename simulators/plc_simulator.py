import time
import random
import requests
import json
import uuid
from datetime import datetime, timezone # Importar timezone

# Configuración
API_URL = "http://localhost:8071/api/v1/telemetry/readings"  
MACHINE_ID = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11" 

# Parámetros de simulación
NORMAL_OPERATION_MIN = 40
NORMAL_OPERATION_MAX = 90
STOP_VALUE = 0

def generate_value(current_state):
    """Genera un valor realista basado en el estado actual."""
    if current_state == "RUNNING":
        return random.uniform(NORMAL_OPERATION_MIN, NORMAL_OPERATION_MAX)
    else:
        return random.uniform(0, 5)

def main():
    print(f"🚀 Iniciando simulador de PLC para {MACHINE_ID}...")
    
    state = "RUNNING"
    state_duration = 0
    max_state_duration = 60
    
    while True:
        state_duration += 1
        if state_duration > max_state_duration:
            if random.random() > 0.7:
                state = "STOPPED" if state == "RUNNING" else "RUNNING"
                print(f"⚠️ CAMBIO DE ESTADO: La máquina ahora está {state}")
                state_duration = 0
                max_state_duration = random.randint(20, 100)

        value = generate_value(state)
        
        # --- CORRECCIÓN: Usar datetime.now(timezone.utc) ---
        reading = {
            "asset_id": MACHINE_ID,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metric_name": "process_speed",
            "value": round(value, 2)
        }
        
        payload = {
            "readings": [reading]
        }

        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 202:
                print(f"📡 Enviado: {value:.2f} ({state}) - Status: {response.status_code}")
            else:
                print(f"⚠️ Error del servidor: {response.status_code} - {response.text}")
            
        except Exception as e:
            print(f"❌ Error de conexión (¿Backend apagado?): {e}")

        time.sleep(1)

if __name__ == "__main__":
    main()
