# /app/payments/gateways/configurable.py
"""
Implementación de una pasarela de pago genérica/configurable.
"""
from typing import Dict, Any

from app.payments.gateways.interface import PaymentGatewayInterface
from app.identity.models import User
from app.identity.models.saas import Plan

class ConfigurableGateway(PaymentGatewayInterface):
    """
    Pasarela genérica que puede ser configurada para diferentes métodos de pago
    que no tienen una API directa (ej: transferencia bancaria genérica).
    """
    def __init__(self, config: Dict[str, Any]):
        self.name = config.get("name", "Generic Gateway")
        self.instructions = config.get("instructions", "Please follow the payment instructions provided.")

    async def create_checkout_session(self, user: User, plan: Plan, success_url: str, cancel_url: str) -> Dict[str, Any]:
        """
        Para una pasarela configurable, no hay una sesión de checkout automática.
        En su lugar, devolvemos las instrucciones para el usuario.
        """
        return {
            "gateway_name": self.name,
            "instructions": self.instructions,
            "next_step": "Awaiting manual payment confirmation."
        }

    def create_portal_session(self, user: User, return_url: str) -> Dict[str, Any]:
        return {"portal_url": return_url} # Devuelve al usuario a la app

    def handle_webhook(self, payload: bytes, headers: Dict[str, Any]) -> Dict[str, Any]:
        # No hay webhooks para este tipo de pasarela.
        return {}
