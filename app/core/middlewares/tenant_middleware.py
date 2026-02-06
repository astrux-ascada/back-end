# /app/core/middlewares/tenant_middleware.py
"""
Middleware de FastAPI para identificar y establecer el contexto del Tenant en cada petición.
"""
import uuid
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.context import tenant_id_context, user_id_context
from app.identity.models.user import User

# Define paths that do not require tenant identification
# These paths will bypass the tenant identification logic in the middleware.
EXCLUDED_PATHS = [
    "/api/v1/auth/login",
    # "/api/v1/auth/register", # Descomentar si tienes un endpoint de registro público
    "/api/v1/openapi.json", # Documentación OpenAPI
    "/api/v1/docs",         # Swagger UI
    "/api/v1/redoc",        # ReDoc
    # Añade aquí cualquier otra ruta que deba ser accesible sin un tenant_id pre-establecido
]

class TenantMiddleware(BaseHTTPMiddleware):
    """
    Este middleware se encarga de identificar el tenant del usuario autenticado
    y de inyectarlo en el contexto de la petición (`ContextVar`).
    """
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        Procesa la petición para extraer el tenant_id.
        """
        # Si la ruta actual está en la lista de excluidos, simplemente pasa la petición.
        if request.url.path in EXCLUDED_PATHS:
            response = await call_next(request)
            return response

        user_id_str = request.scope.get("user", {}).get("id")

        if user_id_str:
            try:
                user_id = uuid.UUID(user_id_str)
                user_id_context.set(user_id)

                db: Session = SessionLocal()
                try:
                    user_tenant = db.query(User.tenant_id).filter(User.id == user_id).first()
                    if user_tenant and user_tenant.tenant_id:
                        tenant_id_context.set(user_tenant.tenant_id)
                finally:
                    db.close()

            except (ValueError, TypeError):
                pass

        # Si user_id_str no está presente (ej. petición no autenticada a una ruta no excluida),
        # o si no se pudo determinar el tenant, el tenant_id_context no se establecerá.
        # Cualquier dependencia que requiera el tenant_id y no lo encuentre, lanzará una excepción.
        response = await call_next(request)
        return response
