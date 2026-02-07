# /app/core/email.py
"""
Módulo central para el envío de correos electrónicos (SMTP).
Soporta personalización por tenant y plantillas HTML (Jinja2).
"""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict, Any
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.config import settings

logger = logging.getLogger("app.core.email")

# Configuración de Jinja2 para plantillas de email
TEMPLATE_DIR = Path(__file__).parent.parent / "templates" / "email"
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_tls = settings.SMTP_TLS
        self.default_from_email = settings.EMAILS_FROM_EMAIL
        self.default_from_name = settings.EMAILS_FROM_NAME

    def _get_smtp_connection(self):
        """Crea y devuelve una conexión SMTP segura."""
        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            if self.smtp_tls:
                server.starttls()
            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
            return server
        except Exception as e:
            logger.error(f"Error conectando al servidor SMTP: {e}")
            raise

    def send_email(
        self,
        to_email: str,
        subject: str,
        template_name: str,
        context: Dict[str, Any],
        tenant_config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Envía un correo electrónico renderizado desde una plantilla.
        
        Args:
            to_email: Destinatario.
            subject: Asunto del correo.
            template_name: Nombre del archivo de plantilla (ej: 'welcome.html').
            context: Datos para renderizar la plantilla.
            tenant_config: Configuración del tenant para personalizar el remitente.
        """
        try:
            # 1. Determinar el remitente (Personalización por Tenant)
            from_email = self.default_from_email
            from_name = self.default_from_name
            
            if tenant_config:
                # Si el tenant tiene configuración de email personalizada, usarla
                # Nota: Esto asume que el servidor SMTP permite enviar como cualquier usuario (común en Mailpit/SendGrid verificado)
                if tenant_config.get("contact_email"):
                    from_email = tenant_config["contact_email"]
                if tenant_config.get("name"):
                    from_name = tenant_config["name"]

            # 2. Renderizar la plantilla
            template = jinja_env.get_template(template_name)
            # Inyectar datos del tenant en el contexto para el logo y colores
            if tenant_config:
                context["tenant"] = tenant_config
            
            html_content = template.render(**context)

            # 3. Construir el mensaje
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{from_name} <{from_email}>"
            msg["To"] = to_email

            # Versión texto plano (opcional, por ahora solo HTML)
            # part1 = MIMEText(text_content, "plain")
            part2 = MIMEText(html_content, "html")
            msg.attach(part2)

            # 4. Enviar
            with self._get_smtp_connection() as server:
                server.sendmail(from_email, to_email, msg.as_string())
            
            logger.info(f"Email enviado a {to_email} | Asunto: {subject}")
            return True

        except Exception as e:
            logger.error(f"Fallo al enviar email a {to_email}: {e}", exc_info=True)
            return False

# Instancia global
email_sender = EmailService()
