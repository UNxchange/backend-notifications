# app/core/email.py
import smtplib
from email.message import EmailMessage
from app.core.config import settings

def enviar_email(destinatario: str, asunto: str, cuerpo: str):
    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = settings.EMAIL_ADDRESS
    msg["To"] = destinatario
    msg.set_content(cuerpo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        smtp.send_message(msg)
