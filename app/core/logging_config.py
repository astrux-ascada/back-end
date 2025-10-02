# /app/core/logging_config.py
"""
Módulo para la configuración centralizada del sistema de logging.

Implementa un formato JSON estructurado para los archivos de log, facilitando
la ingesta y el análisis por parte de sistemas de monitoreo y auditoría.
"""

import json
import logging
from datetime import datetime

# --- MEJORA: Formateador JSON Personalizado ---
class JsonFormatter(logging.Formatter):
    """Formateador de logs que produce JSON estructurado."""
    def format(self, record: logging.LogRecord) -> str:
        log_object = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "source": {
                "logger_name": record.name,
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            },
        }
        # Añadir datos extra si existen
        if hasattr(record, "details"):
            log_object["details"] = record.details

        return json.dumps(log_object)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console_formatter": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s [%(name)s] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True,
        },
        # --- MEJORA: Nuevo formateador JSON ---
        "json_formatter": {
            "()": JsonFormatter,
        },
    },
    "handlers": {
        "console": {
            "formatter": "console_formatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "file": {
            # --- MEJORA: El handler de archivo ahora usa el formateador JSON ---
            "formatter": "json_formatter",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.error": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
    },
}
