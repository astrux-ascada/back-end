# Esquemas Pydantic para el modelo Role
import uuid
from typing import Optional

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
