"""
WebSocket consumers for real-time updates.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)


class DashboardConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for dashboard real-time updates.
    Broadcasts monitoring data and alerts to connected clients.
    """
    
    async def connect(self):
        """
        Handle WebSocket connection.
        """
        self.room_name = 'dashboard'
        self.room_group_name = f'dashboard_{self.room_name}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f'WebSocket connected: {self.channel_name}')
        
        # Send welcome message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to Quantum real-time dashboard'
        }))
    
    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.
        """
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f'WebSocket disconnected: {self.channel_name}')
    
    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        """
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': data.get('timestamp')
                }))
            else:
                logger.warning(f'Unknown message type: {message_type}')
        
        except json.JSONDecodeError:
            logger.error('Invalid JSON received')
    
    async def monitoring_update(self, event):
        """
        Send monitoring data update to WebSocket.
        Called when a message is sent to the room group.
        """
        await self.send(text_data=json.dumps({
            'type': 'monitoring_update',
            'data': event['data']
        }))
    
    async def anomaly_alert(self, event):
        """
        Send anomaly alert to WebSocket.
        """
        await self.send(text_data=json.dumps({
            'type': 'anomaly_alert',
            'data': event['data']
        }))
