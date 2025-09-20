from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    name: str
    role: str

class AssetBase(BaseModel):
    name: str
    code: str
    type: str
    location: Optional[str] = None
    status: Optional[str] = "operativo"
