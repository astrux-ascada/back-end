# /simulators/modbus_simulator.py
"""
Un simulador de dispositivos Modbus TCP.

Expone un servidor Modbus con varios registros que simulan el estado
de equipos industriales, como el nivel de un tanque y el estado de una válvula.
"""

import asyncio
import logging
import random

from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# Configuración del Logger
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("modbus_simulator")

async def run_server():
    """Configura y corre el servidor Modbus y el bucle de actualización de datos."""
    # Inicializa el almacén de datos del servidor
    # Usaremos registros "holding" (código de función 3)
    # Dirección 0: Nivel del Tanque (0-1000)
    # Dirección 1: Estado de la Válvula (0=OFF, 1=ON)
    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [0] * 100),
    )
    context = ModbusServerContext(slaves=store, single=True)

    # Inicia el servidor en el puerto 5020
    server_task = StartAsyncTcpServer(context, address=("", 5020))

    _logger.info("Servidor Modbus TCP Simulador iniciado en el puerto 5020.")
    _logger.info("Registros disponibles:")
    _logger.info("  - Dirección 0: Nivel del Tanque (Holding Register)")
    _logger.info("  - Dirección 1: Estado de la Válvula (Holding Register)")

    # Bucle para actualizar los valores de los registros
    while True:
        try:
            current_level = store.getValues(3, 0, 1)[0]
            
            # Simular fluctuación del nivel del tanque
            new_level = current_level + random.randint(-50, 50)
            if new_level < 0: new_level = 0
            if new_level > 1000: new_level = 1000

            # Simular cambio de estado de la válvula
            valve_status = 1 if new_level > 800 else (0 if new_level < 200 else store.getValues(3, 1, 1)[0])

            store.setValues(3, 0, [new_level])
            store.setValues(3, 1, [valve_status])

            _logger.info(f"Actualizando registros -> Nivel Tanque: {new_level}, Estado Válvula: {'ON' if valve_status == 1 else 'OFF'}")
            
            await asyncio.sleep(3) # Actualizar cada 3 segundos
        except Exception as e:
            _logger.error(f"Error en el bucle de actualización: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        _logger.info("Simulador Modbus detenido por el usuario.")
