import asyncio
import sys
import os
import sys

# Agregar el directorio padre al path para poder importar 'core' y 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from sqlalchemy import text

async def create_superuser():
    print("🔐 Creando Super Usuario Administrador...")
    
    # --- CONFIGURACIÓN DEL ADMIN ---
    email = "admin@astruxa.com"
    password = "admin123"  # ¡Cámbiala en producción!
    name = "Administrador del Sistema"
    role = "admin"
    # -------------------------------

    hashed_password = get_password_hash(password)

    async with AsyncSessionLocal() as session:
        try:
            # 1. Verificar si ya existe
            result = await session.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {"email": email}
            )
            user = result.scalar()

            if user:
                print(f"⚠️ El usuario {email} ya existe. Actualizando contraseña...")
                await session.execute(
                    text("UPDATE users SET password_hash = :pwd, role = :role WHERE email = :email"),
                    {"pwd": hashed_password, "role": role, "email": email}
                )
            else:
                print(f"✨ Creando nuevo usuario {email}...")
                # Nota: Asegúrate de que tu tabla 'users' tenga la columna 'password_hash'
                # Si usaste el init.sql original, es posible que falte esa columna.
                # Este script asume que la tabla está lista para auth.
                await session.execute(
                    text("""
                        INSERT INTO users (email, name, role, password_hash) 
                        VALUES (:email, :name, :role, :pwd)
                    """),
                    {"email": email, "name": name, "role": role, "pwd": hashed_password}
                )
            
            await session.commit()
            print(f"✅ ¡Éxito! Usuario: {email} / Password: {password}")
            print("🚀 Ahora puedes loguearte en el frontend.")

        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Pista: ¿Ya ejecutaste la migración para agregar 'password_hash' a la tabla users?")

if __name__ == "__main__":
    asyncio.run(create_superuser())
