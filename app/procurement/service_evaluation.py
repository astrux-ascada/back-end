# /app/procurement/service_evaluation.py
"""
Servicio para el Motor de Evaluación de Cotizaciones y el ciclo de vida de las PO.
"""
import uuid
from typing import List
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

# Corregir la importación de modelos
from app.procurement.models.purchase_order import RequestForQuotation, Quote, PurchaseOrder, POStatus
from app.procurement.models.provider import Provider
from app.procurement import schemas_procurement as schemas
from app.procurement.repository import ProcurementRepository
from app.core.exceptions import NotFoundException, ConflictException

class EvaluationService:
    def __init__(self, db: Session):
        self.db = db
        self.procurement_repo = ProcurementRepository(db)

    def evaluate_rfq(self, rfq_id: uuid.UUID, tenant_id: uuid.UUID) -> schemas.RFQEvaluationReport:
        """
        Evalúa todas las cotizaciones para una RFQ y genera un reporte con una recomendación.
        """
        rfq = self.db.query(RequestForQuotation).options(
            joinedload(RequestForQuotation.quotes).joinedload(Quote.provider)
        ).filter(
            RequestForQuotation.id == rfq_id,
            RequestForQuotation.tenant_id == tenant_id
        ).first()

        if not rfq:
            raise NotFoundException("RFQ no encontrada.")

        if not rfq.quotes:
            raise NotFoundException("No se han recibido cotizaciones para esta RFQ.")

        evaluated_quotes: List[schemas.QuoteEvaluation] = []
        
        min_price = min(quote.total_price for quote in rfq.quotes)

        for quote in rfq.quotes:
            price_score = (min_price / quote.total_price) * 100
            performance_score = quote.provider.performance_score or 70
            delivery_score = 100 - (quote.delivery_days * 5) if quote.delivery_days else 70
            final_score = (price_score * 0.4) + (performance_score * 0.5) + (delivery_score * 0.1)

            justification = f"Puntuación final: {final_score:.1f}. "
            if final_score > 85:
                justification += "Opción muy recomendada por su excelente balance entre precio y fiabilidad."
            elif final_score > 70:
                justification += "Opción sólida con un buen balance general."
            else:
                justification += "Opción económica pero con riesgos de desempeño o entrega."

            evaluated_quotes.append(schemas.QuoteEvaluation(
                **quote.__dict__,
                provider_performance=performance_score,
                score=final_score,
                justification=justification
            ))

        evaluated_quotes.sort(key=lambda q: q.score, reverse=True)
        recommended_id = evaluated_quotes[0].id if evaluated_quotes else None

        return schemas.RFQEvaluationReport(
            rfq=rfq,
            quotes=evaluated_quotes,
            recommended_quote_id=recommended_id
        )

    def receive_purchase_order(self, po_id: uuid.UUID, receive_in: schemas.POReceive, tenant_id: uuid.UUID) -> PurchaseOrder:
        """
        Registra la recepción de una orden de compra y evalúa al proveedor.
        """
        po = self.db.query(PurchaseOrder).options(
            joinedload(PurchaseOrder.quote).joinedload(Quote.provider)
        ).filter(
            PurchaseOrder.id == po_id,
            PurchaseOrder.tenant_id == tenant_id
        ).first()

        if not po:
            raise NotFoundException("Orden de Compra no encontrada.")
        
        if po.status != POStatus.ISSUED:
            raise ConflictException(f"Solo se pueden recibir órdenes de compra en estado 'ISSUED'. Estado actual: {po.status.value}")

        # 1. Actualizar la PO
        po.status = POStatus.COMPLETED
        po.completed_at = datetime.utcnow()
        po.provider_rating = receive_in.provider_rating
        po.provider_feedback = receive_in.provider_feedback
        
        # 2. Actualizar el desempeño del proveedor (promedio móvil simple)
        provider = po.quote.provider
        current_score = provider.performance_score or 70
        new_rating_normalized = receive_in.provider_rating * 20
        
        provider.performance_score = (current_score * 0.8) + (new_rating_normalized * 0.2)

        self.db.add(po)
        self.db.add(provider)
        self.db.commit()
        self.db.refresh(po)
        
        return po
