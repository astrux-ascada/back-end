# /simulators/plc_simulator.py
"""
Un simulador de PLC simple que actúa como un servidor OPC UA.

Expone un conjunto de variables (nodos) que cambian de valor con el tiempo,
permitiendo probar la funcionalidad del CoreEngine y los conectores sin hardware real.
"""

import asyncio
import logging
import math
import random

from asyncua import Server

# Configuración del Logger
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("plc_simulator")

async def main():
    # --- Configuración del Servidor OPC UA ---
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/astruxa/simulator/")
    server.set_server_name("Astruxa PLC Simulator")

    # --- Creación del Espacio de Nombres y Objetos ---
    uri = "http://astruxa.com/simulator"
    idx = await server.register_namespace(uri)
    objects = await server.get_objects_node().add_object(idx, "PLC_1")

    # --- Definición de Variables (Nodos/Tags) ---
    temp_node = await objects.add_variable(idx, "Temperature", 0.0)
    pressure_node = await objects.add_variable(idx, "Pressure", 0.0)
    await temp_node.set_writable()
    await pressure_node.set_writable()

    _logger.info("Servidor OPC UA Simulador iniciado en opc.tcp://localhost:4840/astruxa/simulator/")
    _logger.info(f"Nodo de Temperatura: {temp_node}")
    _logger.info(f"Nodo de Presión: {pressure_node}")

    # --- Bucle Principal de Simulación ---
    async with server:
        _logger.info("Iniciando simulación de cambio de datos...")
        i = 0
        while True:
            # Simular una onda sinusoidal para la temperatura
            temperature = 20 + 10 * math.sin(math.radians(i))
            # Simular un valor aleatorio para la presión
            pressure = 1000 + random.uniform(-20, 20)
            
            _logger.info(f"Actualizando valores -> Temperatura: {temperature:.2f}, Presión: {pressure:.2f}")
            await temp_node.write_value(temperature)
            await pressure_node.write_value(pressure)
            
            await asyncio.sleep(2)
            i = (i + 5) % 360

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        _logger.info("Simulador detenido por el usuario.")
