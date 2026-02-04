from pydantic import BaseModel
from datetime import datetime

class TelemetryPayload(BaseModel):
    """
    Define la estructura de datos que se espera recibir desde los sensores/gateways.
    Pydantic se encargará de la validación automática.
    """
    machine_id: str
    sensor_id: str
    timestamp: datetime
    value: float
    unit: str
    type: str
