import asyncio
import json
from typing import Dict, Optional
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)

class ProgressManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.progress_data: Dict[str, Dict] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Conectar un cliente WebSocket"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"📡 Cliente conectado: {session_id}")
    
    def disconnect(self, session_id: str):
        """Desconectar un cliente"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in self.progress_data:
            del self.progress_data[session_id]
        logger.info(f"📡 Cliente desconectado: {session_id}")
    
    async def send_progress(self, session_id: str, percentage: int, message: str, status: str = "processing"):
        """Enviar progreso a un cliente específico"""
        if session_id not in self.active_connections:
            return
        
        progress_info = {
            "type": "progress",
            "percentage": percentage,
            "message": message,
            "status": status,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Guardar progreso
        self.progress_data[session_id] = progress_info
        
        try:
            websocket = self.active_connections[session_id]
            await websocket.send_text(json.dumps(progress_info))
            logger.debug(f"📤 Progreso enviado a {session_id}: {percentage}% - {message}")
        except Exception as e:
            logger.error(f"❌ Error enviando progreso a {session_id}: {e}")
            self.disconnect(session_id)
    
    async def send_completion(self, session_id: str, success: bool, data: Optional[dict] = None, error: Optional[str] = None):
        """Enviar notificación de finalización"""
        if session_id not in self.active_connections:
            return
        
        completion_info = {
            "type": "completion",
            "success": success,
            "data": data,
            "error": error,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        try:
            websocket = self.active_connections[session_id]
            await websocket.send_text(json.dumps(completion_info))
            logger.info(f"🏁 Finalización enviada a {session_id}: {'✅' if success else '❌'}")
        except Exception as e:
            logger.error(f"❌ Error enviando finalización a {session_id}: {e}")
        finally:
            # Desconectar después de completar
            self.disconnect(session_id)

# Instancia global
progress_manager = ProgressManager()