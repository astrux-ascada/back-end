# /app/identity/api_partner.py
"""
API Router para el Portal de Partners.
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException

from app.dependencies.permissions import require_permission
from app.dependencies.services import get_partner_service
from app.identity.service_partner import PartnerService
from app.identity.schemas_saas import PartnerTenantRead
from app.dependencies.auth import get_current_active_user
from app.identity.models import User

router = APIRouter(
    prefix="/partners", 
    tags=["Partner Portal"]
)

@router.get("/my-tenants", response_model=List[PartnerTenantRead])
def list_my_tenants(
    partner_service: PartnerService = Depends(get_partner_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista los tenants gestionados por el partner autenticado.
    """
    # TODO: Implementar la lógica para obtener el partner_id del usuario actual.
    # Por ahora, esto requeriría que el modelo User tenga una relación con Partner.
    # Como workaround para el MVP, si el usuario es Super Admin, podría ver todos,
    # o podríamos pasar el partner_id como parámetro si el usuario tiene permisos de admin.
    
    # Para este ejemplo, asumimos que hay una forma de obtener el ID.
    # Si no, devolvemos una lista vacía o un error 501 (Not Implemented) hasta que se actualice el modelo User.
    
    # partner_id = current_user.partner_id 
    # return partner_service.list_tenants_by_partner(partner_id)
    
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="La vinculación Usuario-Partner aún no está implementada en el modelo.")
