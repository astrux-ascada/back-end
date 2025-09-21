from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IExternalMedicalService(ABC):
    """
    Contrato (Interfaz) para cualquier servicio de consulta médica externa.

    Define los métodos que todas las implementaciones de servicios externos
    (ICD-11, SNOMED, etc.) deben tener.
    """

    @abstractmethod
    async def search(self, term: str, lang: str = "en") -> List[Dict[str, Any]]:
        """
        Busca un término en la API externa y devuelve una lista de resultados estandarizados.
        """
        pass