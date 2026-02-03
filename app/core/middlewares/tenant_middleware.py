# /app/core/middlewares/tenant_middleware.py
"""
Middleware de FastAPI para identificar y establecer el contexto del Tenant en cada petición.
"""
import uuid
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseFunction
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.context import tenant_id_context, user_id_context
from app.identity.models.user import User

class TenantMiddleware(BaseHTTPMiddleware):
    """
    Este middleware se encarga de identificar el tenant del usuario autenticado
    y de inyectarlo en el contexto de la petición (`ContextVar`).

    Se ejecuta en cada petición después del middleware de autenticación.
    """
    async def dispatch(
        self, request: Request, call_next: RequestResponseFunction
    ) -> Response:
        """
        Procesa la petición para extraer el tenant_id.

        1. Obtiene el `user_id` del `scope` de la petición (inyectado por el middleware de autenticación).
        2. Si existe, abre una sesión de base de datos para buscar el `tenant_id` asociado a ese usuario.
        3. Establece el `tenant_id` y el `user_id` en sus respectivas `ContextVar`.
        4. Continúa con el flujo de la petición.

        Nota: Esta implementación realiza una consulta a la BD en cada petición.
        Para optimizar, se podría incluir el `tenant_id` en el payload del token JWT.
        """
        # Obtener el user_id del scope de la petición
        user_id_str = request.scope.get("user", {}).get("id")

        if user_id_str:
            try:
                user_id = uuid.UUID(user_id_str)
                user_id_context.set(user_id)

                # Abrir una sesión de BD para obtener el tenant_id
                db: Session = SessionLocal()
                try:
                    # Optimización: solo consultar la columna tenant_id
                    user_tenant = db.query(User.tenant_id).filter(User.id == user_id).first()
                    if user_tenant and user_tenant.tenant_id:
                        tenant_id_context.set(user_tenant.tenant_id)
                finally:
                    db.close()

            except (ValueError, TypeError):
                # El user_id en el token no es un UUID válido, ignorar.
                pass

        # Continuar con la petición
        response = await call_next(request)
        return response
