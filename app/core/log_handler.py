# /app/core/log_handler.py
"""
Handler de logging personalizado para la lógica de negocio de Astruxa.

Este handler intercepta los logs, los parsea y puede disparar acciones
(como crear órdenes de trabajo) basadas en su contenido.
"""

import logging
import json
from typing import Callable, Optional


class AstruxaLogHandler(logging.Handler):
    """Un handler de logging que puede reaccionar a eventos específicos."""

    def __init__(self):
        super().__init__()
        # Estos "manejadores de eventos" se inyectarán después de la inicialización
        # para evitar importaciones circulares.
        self.event_handlers: dict[str, Callable] = {}

    def emit(self, record: logging.LogRecord):
        """
        Procesa un registro de log. Si el log es relevante, dispara un evento.
        """
        try:
            log_data = json.loads(self.format(record))
            
            # --- Lógica de Despacho de Eventos ---
            # Ejemplo: Reaccionar a un error de conexión en el core_engine
            if (
                log_data.get("level") == "ERROR" and
                log_data.get("source", {}).get("logger_name") == "app.core_engine.connector.opcua" and
                "Connection refused" in log_data.get("message", "")
            ):
                if "handle_connection_error" in self.event_handlers:
                    # Extraer detalles relevantes para el manejador del evento
                    details = log_data.get("details", {})
                    self.event_handlers["handle_connection_error"](details)

            # Se podrían añadir más condiciones para otros eventos aquí...

        except (json.JSONDecodeError, AttributeError):
            # Si el log no es un JSON o no tiene el formato esperado, lo ignoramos.
            pass
        except Exception as e:
            # Evitar que el handler de logs cause un crash en la aplicación
            logging.critical(f"Error crítico en AstruxaLogHandler: {e}", exc_info=True)


# --- Instancia Singleton del Handler ---
# La aplicación usará una única instancia de este handler.
astruxa_log_handler = AstruxaLogHandler()
