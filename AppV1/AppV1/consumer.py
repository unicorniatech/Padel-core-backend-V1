import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)  # Configuración para logging

class MyConsumer(AsyncWebsocketConsumer):
    """
    Este Consumer maneja conexiones WebSocket y mensajes enviados por el cliente.
    """

    async def connect(self):
        """
        Método llamado cuando un cliente intenta conectarse al WebSocket.
        """
        await self.accept()
        logger.info("Cliente conectado al WebSocket")

    async def disconnect(self, close_code):
        """
        Método llamado cuando un cliente se desconecta del WebSocket.

        Args:
        - close_code: Código de cierre enviado por el cliente o el servidor.
        """
        logger.info(f"Cliente desconectado del WebSocket con código {close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        """
        Método llamado cuando el cliente envía un mensaje al WebSocket.

        Args:
        - text_data: Datos enviados por el cliente en formato de texto (JSON).
        - bytes_data: Datos binarios enviados por el cliente (si los hay).
        """
        if text_data:
            # Convertir el mensaje JSON en un diccionario
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '')

            # Registrar el mensaje recibido
            logger.info(f"Mensaje recibido: {message}")

            # Responder al cliente
            await self.send(text_data=json.dumps({
                'message': f'Recibido: {message}'
            }))

        if bytes_data:
            # Manejo opcional para datos binarios
            logger.warning("Datos binarios recibidos, pero no se procesarán.")

 