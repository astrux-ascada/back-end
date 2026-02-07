import pytest
from app.core.email import email_sender

def test_send_email_integration():
    """
    Verifica que el EmailService puede conectar con el servidor SMTP y enviar un correo.
    Requiere que Mailpit (o un servidor SMTP) esté corriendo en el host/puerto configurado.
    """
    to_email = "test@example.com"
    subject = "Test Email from Pytest"
    template_name = "welcome.html"
    context = {
        "user_name": "Test User",
        "login_url": "http://localhost:3000/login",
        "year": 2024
    }
    
    # Datos de tenant simulados para probar la personalización
    tenant_config = {
        "name": "Test Tenant Corp",
        "contact_email": "support@testtenant.com"
    }

    try:
        result = email_sender.send_email(
            to_email=to_email,
            subject=subject,
            template_name=template_name,
            context=context,
            tenant_config=tenant_config
        )
        assert result is True, "El envío de email falló (retornó False)"
    except ConnectionRefusedError:
        pytest.skip("Servidor SMTP no disponible. Saltando test de integración de email.")
    except Exception as e:
        pytest.fail(f"El envío de email lanzó una excepción inesperada: {e}")
