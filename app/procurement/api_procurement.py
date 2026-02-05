# /app/procurement/api_procurement.py
"""
API Router para el flujo de Cotizaciones y Órdenes de Compra.
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, status

from app.procurement import schemas_procurement as schemas
from app.procurement.service_evaluation import EvaluationService
from app.dependencies.services import get_evaluation_service
from app.dependencies.tenant import get_tenant_id
from app.dependencies.permissions import require_permission

router = APIRouter(
    prefix="/procurement-flow", 
    tags=["Procurement Flow (RFQ, Quotes, PO)"]
)

@router.get("/rfq/{rfq_id}/evaluate", response_model=schemas.RFQEvaluationReport, dependencies=[Depends(require_permission("quote:evaluate"))])
def evaluate_rfq_quotes(
    rfq_id: uuid.UUID,
    evaluation_service: EvaluationService = Depends(get_evaluation_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """
    Ejecuta el motor de evaluación para una RFQ y devuelve un reporte
    con la recomendación de la mejor cotización.
    """
    return evaluation_service.evaluate_rfq(rfq_id, tenant_id)

@router.post("/po/{po_id}/receive", response_model=schemas.PORead, dependencies=[Depends(require_permission("po:receive"))])
def receive_purchase_order(
    po_id: uuid.UUID,
    receive_in: schemas.POReceive,
    evaluation_service: EvaluationService = Depends(get_evaluation_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """
    Registra la recepción de una Orden de Compra, actualiza el desempeño del proveedor
    y (en el futuro) el stock de repuestos.
    """
    return evaluation_service.receive_purchase_order(po_id, receive_in, tenant_id)

# Aquí se añadirían los endpoints para crear RFQs, enviar Quotes, y crear POs.
