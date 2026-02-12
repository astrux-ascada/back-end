import os
import sys
import logging
from dotenv import load_dotenv
from sqlalchemy import text

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Entorno y Configuración ---
load_dotenv(os.path.join(os.getcwd(), ".env"))

# Ajuste para ejecución local fuera de Docker
if os.environ.get("POSTGRES_HOST") == "backend_db" or not os.environ.get("POSTGRES_HOST"):
    os.environ["POSTGRES_HOST"] = "localhost"
    os.environ["POSTGRES_PORT"] = "5433"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.identity.models import User, Role, Permission

def check_user_permissions(email: str):
    db = SessionLocal()
    try:
        logger.info(f"🔍 Verificando permisos para: {email}")
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            logger.error(f"❌ Usuario no encontrado: {email}")
            return

        logger.info(f"✅ Usuario encontrado: {user.name} (ID: {user.id})")
        logger.info(f"   Activo: {user.is_active}")
        
        if not user.roles:
            logger.warning("⚠️ El usuario no tiene roles asignados.")
        
        for role in user.roles:
            logger.info(f"   🎭 Rol: {role.name}")
            permissions = [p.name for p in role.permissions]
            if "user:read_all" in permissions:
                logger.info(f"      ✅ Tiene permiso 'user:read_all'")
            else:
                logger.error(f"      ❌ NO tiene permiso 'user:read_all'")
            
            logger.info(f"      Total permisos: {len(permissions)}")
            # logger.info(f"      Permisos: {permissions}") # Descomentar para ver todos

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_user_permissions("admin@astruxa.com")
