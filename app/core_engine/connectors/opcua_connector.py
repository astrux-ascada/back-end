# /app/core_engine/connectors/opcua_connector.py
"""
Conector específico para el protocolo OPC UA.

Utiliza la librería async-opcua para conectarse a servidores OPC UA, suscribirse
a nodos (tags) y recibir actualizaciones de datos en tiempo real.
"""

import asyncio
import logging
from typing import Callable, Any

from async_opcua import Client, ua

from app.core_engine.models import DataSource

logger = logging.getLogger("app.core_engine.connector.opcua")


class OpcUaConnector:
    """Gestiona una conexión persistente con un servidor OPC UA."""

    def __init__(self, data_source: DataSource, data_callback: Callable):
        """
        Inicializa el conector con la configuración de la fuente de datos y un callback.

        Args:
            data_source: El objeto DataSource con los parámetros de conexión.
            data_callback: Una función a la que se llamará cuando se reciban nuevos datos.
        """
        self.data_source = data_source
        self.data_callback = data_callback
        self.client = Client(url=data_source.connection_params.get("url"))
        self.subscription = None
        self._task = None

    async def start(self):
        """Inicia el ciclo de vida del conector: conectar, suscribir y monitorear."""
        logger.info(f"Iniciando conector OPC UA para: {self.data_source.name}")
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        """Detiene el conector y cierra la conexión de forma segura."""
        logger.info(f"Deteniendo conector OPC UA para: {self.data_source.name}")
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info(f"Conector OPC UA para {self.data_source.name} detenido.")

    async def _run(self):
        """El bucle principal que mantiene la conexión y la suscripción activas."""
        try:
            async with self.client:
                logger.info(f"Conectado a OPC UA server: {self.data_source.name}")
                # Lógica futura: Suscribirse a los tags definidos.
                # self.subscription = await self.client.create_subscription(500, self)
                # nodes_to_subscribe = self.data_source.connection_params.get("nodes", [])
                # for node_id in nodes_to_subscribe:
                #     node = self.client.get_node(node_id)
                #     await self.subscription.subscribe_data_change(node)
                
                while True:
                    await asyncio.sleep(1) # Mantener la conexión viva
        except asyncio.CancelledError:
            logger.info(f"La tarea del conector OPC UA para {self.data_source.name} ha sido cancelada.")
        except Exception as e:
            logger.error(f"Error en el conector OPC UA para {self.data_source.name}: {e}", exc_info=True)
        finally:
            logger.info(f"Cerrando conexión OPC UA para: {self.data_source.name}")

    def datachange_notification(self, node: ua.Node, val: Any, data: ua.DataValue):
        """
        Callback que se ejecuta cuando la librería OPC UA detecta un cambio de valor.
        """
        try:
            logger.debug(f"Dato recibido de {self.data_source.name} - Nodo: {node}, Valor: {val}")
            # Lógica futura: Formatear el dato y llamar al self.data_callback
            # para enviarlo al TelemetryService.
        except Exception as e:
            logger.error(f"Error procesando la notificación de cambio de dato: {e}", exc_info=True)
