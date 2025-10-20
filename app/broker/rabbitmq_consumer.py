# app/broker/rabbitmq_consumer.py
"""
Consumidor RabbitMQ para procesar mensajes de la cola de notificaciones
Consumer de eventos del servicio de notificaciones
"""

import json
import logging
import threading
from typing import Optional
import pika
from pika.exceptions import AMQPConnectionError
import os
import time

# Importar funciones de notificación
from app.core.email import send_email
from app.db.session import SessionLocal
from app.db.model import User as NotificationUser
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class MessageConsumer:
    """
    Consumidor de mensajes de RabbitMQ para procesar notificaciones
    """
    
    def __init__(self, rabbitmq_url: str = None):
        """
        Inicializa el consumidor de RabbitMQ
        
        Args:
            rabbitmq_url: URL de conexión a RabbitMQ
        """
        self.rabbitmq_url = rabbitmq_url or os.getenv(
            "RABBITMQ_URL", 
            "amqp://unxchange_user:unxchange_password@localhost:5672/"
        )
        self.connection = None
        self.channel = None
        self.exchange_name = "unxchange_events"
        self.queue_name = "notifications_queue"
        self._should_stop = False
    
    def _connect(self):
        """Establece conexión con RabbitMQ con reintentos"""
        max_retries = 5
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                parameters = pika.URLParameters(self.rabbitmq_url)
                parameters.heartbeat = 600
                parameters.blocked_connection_timeout = 300
                
                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
                
                # Declarar exchange
                self.channel.exchange_declare(
                    exchange=self.exchange_name,
                    exchange_type='topic',
                    durable=True
                )
                
                # Declarar cola
                self.channel.queue_declare(
                    queue=self.queue_name,
                    durable=True,
                    arguments={'x-message-ttl': 86400000}
                )
                
                # Bind de la cola al exchange
                self.channel.queue_bind(
                    exchange=self.exchange_name,
                    queue=self.queue_name,
                    routing_key='user.#'
                )
                
                # Configurar QoS para procesar un mensaje a la vez
                self.channel.basic_qos(prefetch_count=1)
                
                logger.info(f"✅ Consumidor conectado a RabbitMQ: {self.rabbitmq_url}")
                return True
                
            except AMQPConnectionError as e:
                logger.error(f"❌ Intento {attempt + 1}/{max_retries} - Error conectando a RabbitMQ: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    logger.error("❌ No se pudo conectar a RabbitMQ después de varios intentos")
                    return False
    
    def _process_user_created(self, message: dict, db: Session):
        """
        Procesa un evento de usuario creado
        
        Args:
            message: Mensaje recibido del broker
            db: Sesión de base de datos
        """
        try:
            user_id = message.get("user_id")
            user_name = message.get("user_name")
            user_email = message.get("user_email")
            user_role = message.get("user_role", "ESTUDIANTE")
            
            logger.info(f"📧 Procesando notificación para nuevo usuario ID {user_id}: {user_email}")
            
            # Crear usuario en la base de datos de notificaciones
            existing_user = db.query(NotificationUser).filter(
                NotificationUser.id == user_id
            ).first()
            
            if not existing_user:
                new_notification_user = NotificationUser(
                    id=user_id,
                    name=user_name,
                    email=user_email,
                    role=user_role
                )
                db.add(new_notification_user)
                db.commit()
                logger.info(f"✅ Usuario {user_id} registrado en base de datos de notificaciones")
            else:
                logger.info(f"ℹ️ Usuario {user_id} ya existe en base de datos de notificaciones")
            
            # Enviar correo de bienvenida
            subject = "¡Bienvenido a UnxChange!"
            body = f"""
            <html>
            <body>
                <h2>¡Hola {user_name}!</h2>
                <p>Bienvenido a <strong>UnxChange</strong>, la plataforma de intercambio académico de la Universidad Nacional de Colombia.</p>
                <p>Tu cuenta ha sido creada exitosamente con el rol: <strong>{user_role}</strong></p>
                <p>Ahora puedes acceder a la plataforma y explorar las oportunidades de intercambio disponibles.</p>
                <br>
                <p>Saludos,<br>El equipo de UnxChange</p>
            </body>
            </html>
            """
            
            success = send_email(
                to_email=user_email,
                subject=subject,
                body=body
            )
            
            if success:
                logger.info(f"✅ Correo de bienvenida enviado a {user_email}")
            else:
                logger.error(f"❌ No se pudo enviar correo de bienvenida a {user_email}")
                
        except Exception as e:
            logger.error(f"❌ Error procesando usuario creado: {e}")
            raise
    
    def _process_message(self, ch, method, properties, body):
        """
        Callback para procesar mensajes recibidos
        
        Args:
            ch: Canal de RabbitMQ
            method: Método de entrega
            properties: Propiedades del mensaje
            body: Cuerpo del mensaje
        """
        db = SessionLocal()
        
        try:
            # Decodificar mensaje
            message = json.loads(body.decode('utf-8'))
            event_type = message.get("event_type")
            
            logger.info(f"📬 Mensaje recibido: {event_type}")
            
            # Procesar según el tipo de evento
            if event_type == "user_created":
                self._process_user_created(message, db)
            elif event_type == "user_updated":
                logger.info(f"ℹ️ Evento de actualización de usuario: {message}")
                # Implementar lógica de actualización si es necesario
            else:
                logger.warning(f"⚠️ Tipo de evento desconocido: {event_type}")
            
            # Confirmar procesamiento del mensaje
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"✅ Mensaje procesado y confirmado")
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error decodificando mensaje JSON: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.error(f"❌ Error procesando mensaje: {e}")
            # Reenviar a la cola para reintentar
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        finally:
            db.close()
    
    def start_consuming(self):
        """
        Inicia el consumo de mensajes de la cola
        """
        if not self._connect():
            logger.error("❌ No se pudo iniciar el consumidor")
            return
        
        try:
            logger.info(f"🚀 Consumidor iniciado. Esperando mensajes en '{self.queue_name}'...")
            
            self.channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=self._process_message,
                auto_ack=False
            )
            
            self.channel.start_consuming()
            
        except KeyboardInterrupt:
            logger.info("⏹️ Consumidor detenido por usuario")
            self.stop()
        except Exception as e:
            logger.error(f"❌ Error en el consumidor: {e}")
            self.stop()
    
    def stop(self):
        """Detiene el consumidor y cierra las conexiones"""
        try:
            self._should_stop = True
            if self.channel and not self.channel.is_closed:
                self.channel.stop_consuming()
                self.channel.close()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            logger.info("✅ Consumidor detenido correctamente")
        except Exception as e:
            logger.error(f"Error deteniendo consumidor: {e}")


# Instancia global del consumidor
_consumer: Optional[MessageConsumer] = None
_consumer_thread: Optional[threading.Thread] = None


def start_consumer():
    """
    Inicia el consumidor en un hilo separado
    """
    global _consumer, _consumer_thread
    
    if _consumer_thread is None or not _consumer_thread.is_alive():
        _consumer = MessageConsumer()
        _consumer_thread = threading.Thread(
            target=_consumer.start_consuming,
            daemon=True,
            name="RabbitMQConsumer"
        )
        _consumer_thread.start()
        logger.info("🚀 Hilo del consumidor iniciado")
    else:
        logger.warning("⚠️ El consumidor ya está ejecutándose")


def stop_consumer():
    """
    Detiene el consumidor
    """
    global _consumer
    if _consumer:
        _consumer.stop()
