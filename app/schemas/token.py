# Esquemas Pydantic para la autenticación y tokens JWT
import uuid
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: Optional[uuid.UUID] = None
