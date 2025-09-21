# /app/core/logging_config.py

"""
Módulo para la configuración centralizada del sistema de logging,
optimizado para FastAPI y Uvicorn.

Combina lo mejor de ambos mundos:
- Integración nativa con Uvicorn para evitar logs duplicados.
- Formato con colores en consola para un desarrollo más amigable.
- Handler de archivo rotativo para un logging robusto en producción.
- Logger nombrado ("app") para un control granular sobre el código de la aplicación.
"""

# --- MEJORA: Unimos tu idea del handler de archivo con la integración de Uvicorn ---
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        # Formato para la consola, usa el de Uvicorn para mantener los colores
        "console_formatter": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s [%(name)s] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True,
        },
        # Formato detallado para el archivo de logs
        "file_formatter": {
            "format": "%(asctime)s - %(levelname)s - %(name)s:%(funcName)s:%(lineno)d - %(message)s"
        },
    },
    "handlers": {
        # Handler para la consola que usa el formato de Uvicorn
        "console": {
            "formatter": "console_formatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        # Handler para el archivo, con rotación
        "file": {
            "formatter": "file_formatter",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",  # Se puede sobreescribir desde la configuración principal
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "loggers": {
        # Logger principal de nuestra aplicación
        "app": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        # Loggers de Uvicorn, los forzamos a usar nuestros handlers
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

# Para usarlo, simplemente importa este diccionario y aplícalo con logging.config.dictConfig(LOGGING_CONFIG)
# en tu archivo de configuración principal o en main.py.