# /app/contracts/IGoogleTranslateService.py (NUEVO ARCHIVO)

from abc import ABC, abstractmethod
from typing import List


class IGoogleTranslateService(ABC):
    """Define el contrato para cualquier servicio de traducción."""

    @abstractmethod
    async def translate(self, text: str, target_language: str,
                        source_language: str | None = None) -> str:
        ...

    @abstractmethod
    async def translate_batch(self, texts: List[str], target_language: str,
                              source_language: str | None = None) -> List[str]:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...
