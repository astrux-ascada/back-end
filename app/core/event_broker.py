# /app/core/event_broker.py
"""
Módulo para la gestión de eventos y comunicación entre servicios (EDA).
Utiliza Redis Pub/Sub como message broker.
"""
import redis
import json
import logging
from typing import Callable, Dict, Any

logger = logging.getLogger("app.event_broker")

class EventBroker:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.pubsub = self.redis_client.pubsub()
        self.subscriptions: Dict[str, Callable] = {}

    def publish(self, channel: str, data: Dict[str, Any]):
        """
        Publica un mensaje (evento) en un canal de Redis.
        """
        message = json.dumps(data)
        self.redis_client.publish(channel, message)
        logger.debug(f"Evento publicado en el canal '{channel}': {message}")

    def subscribe(self, channel: str, handler: Callable):
        """
        Se suscribe a un canal y asigna un manejador para los mensajes.
        """
        self.pubsub.subscribe(channel)
        self.subscriptions[channel] = handler
        logger.info(f"Suscrito al canal '{channel}' con el manejador '{handler.__name__}'")

    def _listen_in_thread(self):
        """
        (Método privado) Escucha continuamente los mensajes en un hilo separado.
        """
        for message in self.pubsub.listen():
            if message["type"] == "message":
                channel = message["channel"].decode("utf-8")
                handler = self.subscriptions.get(channel)
                if handler:
                    try:
                        data = json.loads(message["data"])
                        handler(data) # Llama al manejador con los datos del evento
                    except Exception as e:
                        logger.error(f"Error al procesar evento del canal '{channel}': {e}")

    def start_listening(self):
        """
        Inicia el proceso de escucha en un hilo de background para no bloquear
        la aplicación principal.
        """
        import threading
        thread = threading.Thread(target=self._listen_in_thread, daemon=True)
        thread.start()
        logger.info("El Event Broker ha iniciado la escucha de eventos en background.")
