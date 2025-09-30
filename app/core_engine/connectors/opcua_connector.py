# /app/core_engine/connectors/opcua_connector.py
"""
Conector específico para el protocolo OPC UA.

Utiliza la librería asyncua para conectarse a servidores OPC UA, suscribirse
a nodos (tags) y recibir actualizaciones de datos en tiempo real.
"""

import asyncio
import logging
from typing import Callable, Any, List, Dict
from datetime import datetime, timezone

from asyncua import Client, Node, ua

from app.core_engine.models import DataSource
from app.telemetry.schemas import SensorReadingCreate

logger = logging.getLogger("app.core_engine.connector.opcua")


class OpcUaDataChangeHandler:
    """Clase para manejar los callbacks de cambio de datos de la suscripción OPC UA."""
    def __init__(self, connector: 'OpcUaConnector'):
        self.connector = connector


    def datachange_notification(self, node: Node, val: Any, data: ua.DataValue):
        """Callback que se ejecuta cuando la librería OPC UA detecta un cambio de valor."""

        self.connector.process_data_change(node, val, data)


class OpcUaConnector:
    """Gestiona una conexión persistente con un servidor OPC UA."""

    def __init__(self, data_source: DataSource, data_callback: Callable[[List[SensorReadingCreate]], None]):
        self.data_source = data_source
        self.data_callback = data_callback
        self.client = Client(url=self.data_source.connection_params.get("url"))
        self.subscription = None
        self._task = None
        self._node_map: Dict[str, Dict[str, Any]] = {}

    async def start(self):
        logger.info(f"Iniciando conector OPC UA para: {self.data_source.name}")
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        logger.info(f"Deteniendo conector OPC UA para: {self.data_source.name}")
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info(f"Conector OPC UA para {self.data_source.name} detenido.")

    async def _run(self):
        handler = OpcUaDataChangeHandler(self)
        try:
            async with self.client:
                logger.info(f"Conectado a OPC UA server: {self.data_source.name}")
                self.subscription = await self.client.create_subscription(500, handler)
                
                nodes_to_subscribe = self.data_source.connection_params.get("nodes", [])
                node_objects = []
                for node_config in nodes_to_subscribe:
                    node = self.client.get_node(node_config["node_id"])
                    node_objects.append(node)
                    self._node_map[node.nodeid.to_string()] = node_config

                if node_objects:
                    await self.subscription.subscribe_data_change(node_objects)
                    logger.info(f"Suscrito a {len(node_objects)} nodos para {self.data_source.name}.")
                
                while True:
                    await asyncio.sleep(3600)

        except asyncio.CancelledError:
            logger.info(f"La tarea del conector OPC UA para {self.data_source.name} ha sido cancelada.")
        except Exception as e:
            logger.error(f"Error en el conector OPC UA para {self.data_source.name}: {e}", exc_info=True)
        finally:
            logger.info(f"Cerrando conexión OPC UA para: {self.data_source.name}")


    # --- CORRECCIÓN: La pista de tipo correcta es solo 'Node' ---

    def process_data_change(self, node: Node, val: Any, data: ua.DataValue):
        try:
            node_id_str = node.nodeid.to_string()
            node_config = self._node_map.get(node_id_str)

            if not node_config:
                logger.warning(f"Dato recibido de un nodo no mapeado: {node_id_str}")
                return

            logger.debug(f"Dato recibido de {self.data_source.name} - Nodo: {node_id_str}, Valor: {val}")

            reading = SensorReadingCreate(
                asset_id=node_config["asset_id"],
                timestamp=data.SourceTimestamp or datetime.now(timezone.utc),
                metric_name=node_config["metric_name"],
                value=float(val)
            )

            self.data_callback([reading])

        except Exception as e:
            logger.error(f"Error procesando la notificación de cambio de dato: {e}", exc_info=True)
