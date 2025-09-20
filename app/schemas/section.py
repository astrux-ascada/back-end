# Esquemas Pydantic para el modelo Section
import uuid
from pydantic import BaseModel
from typing import Optional


# --- Esquema Base ---
# Contiene los campos comunes que se comparten entre la creación y la lectura.
class SectionBase(BaseModel):
    name: str
    description: Optional[str] = None


# --- Esquema para la Creación ---
# Se utiliza para validar los datos de entrada al crear una nueva sección.
# En este caso, no tiene campos adicionales al base, pero se crea por consistencia.
class SectionCreate(SectionBase):
    pass


# --- Esquema para la Lectura ---
# Se utiliza para formatear los datos de salida al devolver una sección desde la API.
class Section(SectionBase):
    id: uuid.UUID

    class Config:
        # Esta configuración permite que el esquema Pydantic se cree a partir
        # de un objeto de modelo de SQLAlchemy (modo ORM).
        orm_mode = True
