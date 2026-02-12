
import redis
from app.core.config import settings

def unlock_user(email: str):
    """
    Elimina la clave de bloqueo de un usuario en Redis.
    """
    try:
        # Configura la conexión a Redis usando la configuración del proyecto
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )

        lockout_key = f"lockout:{email}"
        login_attempts_key = f"login_attempts:{email}"

        # Verificar si la clave de bloqueo existe
        if redis_client.exists(lockout_key):
            redis_client.delete(lockout_key)
            print(f"✅ Clave de bloqueo '{lockout_key}' eliminada para el usuario '{email}'.")
        else:
            print(f"ℹ️ No se encontró ninguna clave de bloqueo para el usuario '{email}'.")

        # Opcional: Resetear también el contador de intentos fallidos
        if redis_client.exists(login_attempts_key):
            redis_client.delete(login_attempts_key)
            print(f"✅ Contador de intentos de login reseteado para '{email}'.")

    except redis.exceptions.ConnectionError as e:
        print(f"❌ Error de conexión a Redis: {e}")
        print("Asegúrate de que Redis esté corriendo y accesible en la configuración (.env).")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    # --- Cambia este email por el del usuario que quieres desbloquear ---
    user_to_unlock = "admin@astruxa.com"
    
    print(f"Intentando desbloquear al usuario: {user_to_unlock}...")
    unlock_user(user_to_unlock)
