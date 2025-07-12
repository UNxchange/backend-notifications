# app/core/email.py
import smtplib
import logging
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def enviar_email(destinatario: str, asunto: str, cuerpo: str, html_content: str | None = None):
    """
    Envía un email simple con soporte para HTML
    """
    try:
        logger.info(f"Enviando email a {destinatario} con asunto: {asunto}")
        
        if html_content:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = asunto
            msg["From"] = settings.EMAIL_ADDRESS
            msg["To"] = destinatario
            
            # Crear partes del mensaje
            text_part = MIMEText(cuerpo, "plain")
            html_part = MIMEText(html_content, "html")
            
            msg.attach(text_part)
            msg.attach(html_part)
        else:
            msg = EmailMessage()
            msg["Subject"] = asunto
            msg["From"] = settings.EMAIL_ADDRESS
            msg["To"] = destinatario
            msg.set_content(cuerpo)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
            smtp.send_message(msg)
            
        logger.info(f"Email enviado exitosamente a {destinatario}")
        
    except Exception as e:
        logger.error(f"Error al enviar email a {destinatario}: {str(e)}")
        raise

def enviar_correo_confirmacion(destinatario: str, nombre_usuario: str):
    """
    Envía un correo de confirmación a un usuario recién creado
    """
    asunto = "¡Bienvenido a UnxChange!"
    
    # Contenido en texto plano
    cuerpo_texto = f"""
    Hola {nombre_usuario},

    ¡Bienvenido a UnxChange!

    Tu cuenta ha sido creada exitosamente. Ya puedes acceder a la plataforma y explorar las convocatorias de movilidad académica disponibles.

    Si no creaste esta cuenta, por favor ignora este mensaje.

    Saludos,
    El equipo de UnxChange
    """
    
    # Contenido en HTML
    cuerpo_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Bienvenido a UnxChange</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ background-color: #f8f9fa; padding: 20px; border-radius: 0 0 5px 5px; }}
            .welcome {{ color: #007bff; font-size: 24px; margin-bottom: 20px; }}
            .footer {{ margin-top: 20px; font-size: 12px; color: #666; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>¡Bienvenido a UnxChange!</h1>
            </div>
            <div class="content">
                <p class="welcome">Hola {nombre_usuario},</p>
                <p>Tu cuenta ha sido creada exitosamente en UnxChange, la plataforma de movilidad académica.</p>
                <p>Ya puedes acceder a la plataforma y explorar las convocatorias disponibles.</p>
                <p>Si no creaste esta cuenta, por favor ignora este mensaje.</p>
                <p>Saludos,<br>El equipo de UnxChange</p>
            </div>
            <div class="footer">
                <p>Este es un mensaje automático, por favor no responder.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    enviar_email(destinatario, asunto, cuerpo_texto, cuerpo_html)

def enviar_correo_convocatoria_elegida(
    destinatario: str, 
    nombre_usuario: str, 
    titulo_convocatoria: str,
    descripcion_convocatoria: str,
    universidad_destino: str,
    fecha_inicio: str,
    fecha_fin: str
):
    """
    Envía un correo de confirmación cuando un usuario elige una convocatoria
    """
    asunto = f"Confirmación de Postulación - {titulo_convocatoria}"
    
    # Contenido en texto plano
    cuerpo_texto = f"""
    Hola {nombre_usuario},

    ¡Confirmamos que te has postulado exitosamente a la convocatoria!

    DETALLES DE LA CONVOCATORIA:
    Título: {titulo_convocatoria}
    Descripción: {descripcion_convocatoria}
    Universidad de Destino: {universidad_destino}
    Período: {fecha_inicio} - {fecha_fin}

    Tu postulación ha sido registrada y será evaluada por nuestro equipo académico. 
    Te notificaremos sobre el estado de tu postulación a través de este correo.

    Mientras tanto, puedes seguir explorando otras convocatorias disponibles en la plataforma.

    ¡Mucha suerte en tu proceso de movilidad académica!

    Saludos,
    El equipo de UnxChange
    """
    
    # Contenido en HTML
    cuerpo_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Confirmación de Postulación - UnxChange</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #28a745; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ background-color: #f8f9fa; padding: 20px; border-radius: 0 0 5px 5px; }}
            .success {{ color: #28a745; font-size: 24px; margin-bottom: 20px; }}
            .convocatoria-details {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .detail-item {{ margin-bottom: 10px; }}
            .detail-label {{ font-weight: bold; color: #495057; }}
            .footer {{ margin-top: 20px; font-size: 12px; color: #666; text-align: center; }}
            .highlight {{ background-color: #fff3cd; padding: 10px; border-radius: 3px; border-left: 4px solid #ffc107; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 ¡Postulación Confirmada!</h1>
            </div>
            <div class="content">
                <p class="success">Hola {nombre_usuario},</p>
                <p>¡Excelente noticia! Tu postulación ha sido registrada exitosamente.</p>
                
                <div class="convocatoria-details">
                    <h3 style="color: #28a745; margin-top: 0;">📚 Detalles de la Convocatoria</h3>
                    <div class="detail-item">
                        <span class="detail-label">Título:</span> {titulo_convocatoria}
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Descripción:</span> {descripcion_convocatoria}
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Universidad de Destino:</span> {universidad_destino}
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Período:</span> {fecha_inicio} - {fecha_fin}
                    </div>
                </div>
                
                <div class="highlight">
                    <strong>📋 Próximos Pasos:</strong>
                    <ul>
                        <li>Tu postulación será evaluada por nuestro equipo académico</li>
                        <li>Recibirás notificaciones sobre el estado de tu postulación</li>
                        <li>Puedes seguir explorando otras convocatorias disponibles</li>
                    </ul>
                </div>
                
                <p>¡Mucha suerte en tu proceso de movilidad académica!</p>
                <p>Saludos,<br>El equipo de UnxChange</p>
            </div>
            <div class="footer">
                <p>Este es un mensaje automático, por favor no responder.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    enviar_email(destinatario, asunto, cuerpo_texto, cuerpo_html)
