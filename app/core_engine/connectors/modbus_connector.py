# /app/core_engine/connectors/modbus_connector.py
"""
Conector específico para el protocolo Modbus TCP.

Implementa un bucle de sondeo (polling) para leer registros de dispositivos
Modbus a intervalos regulares.
"""

import asyncio
import logging
from typing import Callable, List, Dict, Any
from datetime import datetime, timezone

from pymodbus.client import ModbusTcpClient

from app.core_engine.models import DataSource
from app.telemetry.schemas import SensorReadingCreate

logger = logging.getLogger("app.core_engine.connector.modbus")


class ModbusConnector:
    """Gestiona un ciclo de sondeo para un dispositivo Modbus TCP."""

    def __init__(self, data_source: DataSource, data_callback: Callable[[List[SensorReadingCreate]], None]):
        self.data_source = data_source
        self.data_callback = data_callback
        self.params = data_source.connection_params
        self.client = ModbusTcpClient(self.params.get("host"), port=self.params.get("port", 502))
        self._task = None

    async def start(self):
        logger.info(f"Iniciando conector Modbus para: {self.data_source.name}")
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        logger.info(f"Deteniendo conector Modbus para: {self.data_source.name}")
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info(f"Conector Modbus para {self.data_source.name} detenido.")

    def _read_registers(self, registers: List[Dict[str, Any]]) -> List[SensorReadingCreate]:
        """Función síncrona que se ejecuta en un hilo separado para leer los registros."""
        readings = []
        try:
            self.client.connect()
            for reg_config in registers:
                address = reg_config["address"]
                count = reg_config.get("count", 1)
                # Usamos código de función 3 para leer registros "holding"
                result = self.client.read_holding_registers(address, count, slave=self.params.get("slave_id", 1))
                
                if not result.isError():
                    value = result.registers[0] # Asumimos que leemos un solo registro por ahora
                    reading = SensorReadingCreate(
                        asset_id=reg_config["asset_id"],
                        timestamp=datetime.now(timezone.utc),
                        metric_name=reg_config["metric_name"],
                        value=float(value)
                    )
                    readings.append(reading)
                else:
                    logger.warning(f"Error leyendo registro Modbus en la dirección {address} para {self.data_source.name}")
            return readings
        finally:
            self.client.close()

    async def _run(self):
        """El bucle principal que sondea los registros Modbus a intervalos."""
        polling_interval = self.params.get("polling_interval_seconds", 5)
        registers_to_read = self.params.get("registers", [])

        if not registers_to_read:
            logger.warning(f"No hay registros configurados para sondear en {self.data_source.name}. El conector no hará nada.")
            return

        while True:
            try:
                # Ejecutar la lectura síncrona en un hilo separado para no bloquear el bucle de eventos
                readings = await asyncio.to_thread(self._read_registers, registers_to_read)
                
                if readings:
                    logger.debug(f"{len(readings)} lecturas recibidas de {self.data_source.name}")
                    self.data_callback(readings)
                
                await asyncio.sleep(polling_interval)
            except asyncio.CancelledError:
                logger.info(f"La tarea del conector Modbus para {self.data_source.name} ha sido cancelada.")
                break
            except Exception as e:
                logger.error(f"Error en el conector Modbus para {self.data_source.name}: {e}", exc_info=True)
                await asyncio.sleep(polling_interval * 2) # Esperar más tiempo si hay un error
