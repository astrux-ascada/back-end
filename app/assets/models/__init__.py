# /app/assets/models/__init__.py
"""
Expone los modelos del módulo de activos y define sus interrelaciones
para evitar dependencias circulares.
"""

from sqlalchemy.orm import relationship

# --- 1. Importar todas las clases de modelo necesarias ---

# Modelos de este módulo
from .asset_type import AssetType
from .asset import Asset
from .asset_hierarchy import AssetHierarchy

# Modelos de otros módulos con los que nos relacionamos
from app.sectors.models.sector import Sector


# --- 2. Definir las relaciones inversas (back-populates) ---
# Ahora que todas las clases están en el mismo ámbito, podemos crear los "puentes".

# Relación Asset <-> Sector
Asset.sector = relationship("Sector", back_populates="assets")
Sector.assets = relationship("Asset", back_populates="sector")
