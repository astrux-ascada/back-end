# /app/reporting/service.py
"""
Servicio de Reporting para exponer información de estado y KPIs.
"""
from uuid import UUID
from app.core_engine.state_detector import StateDetector
from app.reporting.schemas import MachineStateDTO


class ReportingService:
    """
    Provee acceso a los datos de estado y reportes.
    """

    def __init__(self, state_detector: StateDetector):
        self.state_detector = state_detector

    def get_machine_state(self, asset_id: UUID) -> MachineStateDTO:
        """Obtiene el estado actual de una máquina desde el detector de estado."""
        current_state = self.state_detector.get_current_state(asset_id)
        return MachineStateDTO(asset_id=asset_id, state=current_state)
