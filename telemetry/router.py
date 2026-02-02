from fastapi import APIRouter, HTTPException
from .schemas import TelemetryPayload

# Creamos un router específico para telemetría
router = APIRouter(
    prefix="/api/v1/telemetry",
    tags=["telemetry"]
)

@router.post("/ingest")
async def ingest_telemetry(payload: TelemetryPayload):
    """
    Recibe datos de telemetría de sensores o gateways.
    
    Por ahora, solo imprime los datos en la consola para verificar la conexión.
    En el futuro, esto guardará los datos en TimescaleDB y notificará a Redis.
    """
    try:
        # Aquí iría la lógica de negocio:
        # 1. Guardar en DB
        # 2. Analizar si es una parada (Core Engine)
        # 3. Notificar si es necesario
        
        print(f"📥 [BACKEND] Dato recibido: {payload.machine_id} -> {payload.value} {payload.unit}")
        
        return {"status": "received", "timestamp": payload.timestamp}
    
    except Exception as e:
        print(f"❌ Error procesando telemetría: {e}")
        raise HTTPException(status_code=500, detail="Error interno procesando datos")
