# /app/payments/gateways/interface.py
"""
Define la interfaz abstracta para todas las pasarelas de pago.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

from app.identity.models import User
from app.identity.models.saas import Plan

class PaymentGatewayInterface(ABC):
    """
    Contrato que todas las pasarelas de pago (Stripe, PayPal, etc.) deben cumplir.
    """

    @abstractmethod
    def create_checkout_session(self, user: User, plan: Plan, success_url: str, cancel_url: str) -> Dict[str, Any]:
        """
        Crea una sesión de pago para una nueva suscripción.
        Debe devolver un diccionario con la información necesaria para redirigir al cliente,
        como una 'checkout_url' o un 'session_id'.
        """
        pass

    @abstractmethod
    def create_portal_session(self, user: User, return_url: str) -> Dict[str, Any]:
        """
        Crea una sesión para que el cliente gestione su suscripción (ej. cambiar de plan,
        actualizar tarjeta).
        Debe devolver un diccionario con una 'portal_url'.
        """
        pass

    @abstractmethod
    def handle_webhook(self, payload: bytes, headers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa un evento de webhook entrante desde la pasarela de pago.
        Debe verificar la firma del webhook y devolver un diccionario con el evento
        parseado y verificado.
        Lanza una excepción si la firma es inválida.
        """
        pass
