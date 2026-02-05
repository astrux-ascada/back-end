# /app/payments/gateways/paypal.py
"""
Implementación de la pasarela de pago de PayPal.
"""
import httpx
from typing import Dict, Any

from app.core.config import settings
from app.payments.gateways.interface import PaymentGatewayInterface
from app.identity.models import User
from app.identity.models.saas import Plan

class PayPalGateway(PaymentGatewayInterface):
    """
    Implementa la lógica para interactuar con la API de PayPal.
    """
    def __init__(self):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.base_url = settings.PAYPAL_API_BASE_URL

    async def _get_access_token(self) -> str:
        """Obtiene un token de acceso OAuth2 de PayPal."""
        auth = (self.client_id, self.client_secret)
        data = {"grant_type": "client_credentials"}
        headers = {"Accept": "application/json", "Accept-Language": "en_US"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/v1/oauth2/token", auth=auth, data=data, headers=headers)
            response.raise_for_status()
            return response.json()["access_token"]

    async def create_checkout_session(self, user: User, plan: Plan, success_url: str, cancel_url: str) -> Dict[str, Any]:
        """
        Crea una orden de pago en PayPal y devuelve la URL de aprobación.
        """
        access_token = await self._get_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        
        # Usamos el precio mensual como ejemplo. En una implementación real, esto sería más complejo.
        order_payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": plan.currency,
                    "value": str(plan.price_monthly)
                },
                "description": f"Suscripción al plan {plan.name} en {settings.PROJECT_NAME}"
            }],
            "application_context": {
                "return_url": success_url,
                "cancel_url": cancel_url,
                "brand_name": settings.PROJECT_NAME,
                "user_action": "PAY_NOW"
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/v2/checkout/orders", headers=headers, json=order_payload)
            response.raise_for_status()
            order_data = response.json()
            
            # Encontrar el link de aprobación para redirigir al usuario
            approval_link = next((link for link in order_data['links'] if link['rel'] == 'approve'), None)
            
            if not approval_link:
                raise Exception("No se pudo encontrar la URL de aprobación de PayPal.")

            return {
                "checkout_url": approval_link['href'],
                "order_id": order_data['id']
            }

    def create_portal_session(self, user: User, return_url: str) -> Dict[str, Any]:
        # La gestión de suscripciones de PayPal (portal de cliente) es más compleja
        # y requiere la creación de Productos y Planes en la API de PayPal.
        # Por ahora, devolvemos una URL de placeholder.
        return {"portal_url": "https://www.paypal.com/myaccount/autopay/"}

    def handle_webhook(self, payload: bytes, headers: Dict[str, Any]) -> Dict[str, Any]:
        # La verificación de webhooks de PayPal requiere una llamada a la API.
        # Esto es un placeholder. En producción, se debe implementar la verificación.
        # https://developer.paypal.com/docs/api/webhooks/v1/#webhooks_verify-signature
        import json
        return json.loads(payload)
