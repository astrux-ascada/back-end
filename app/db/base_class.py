# /app/db/base_class.py (NUEVO ARCHIVO)

# /app/db/base_class.py (VERSIÓN CORREGIDA Y RECOMENDADA)

"""
Este módulo define la Base declarativa para todos los modelos de SQLAlchemy.
Todos los modelos de la aplicación deben heredar de esta Base para ser
registrados correctamente en los metadatos de SQLAlchemy.
"""
from sqlalchemy.orm import declarative_base

# Esta es la única instancia de Base que debe existir en todo el proyecto.
# Es un objeto, no una clase.
Base = declarative_base()