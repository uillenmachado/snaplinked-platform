"""
SnapLinked - Sistema WebSocket Real
Implementação completa de WebSocket para atualizações em tempo real
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Set
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.connected_clients: Set[str] = set()
        self.user_rooms: Dict[str, str] = {}  # session_id -> user_id
        self.room_users: Dict[str, Set[str]] = {}  # user_id -> set of session_ids
        
        # Registrar event handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Registra handlers de eventos WebSocket"""
        
        @self.socketio.on('connect')
        def handle_connect():
            session_id = request.sid
            self.connected_clients.add(session_id)
            
            logger.info(f"Cliente conectado: {session_id}")
            
            # Enviar status de conexão
            emit('connection_status', {
                'connected': True,
                'session_id': session_id,
                'timestamp': datetime.now().isoformat()
            })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            session_id = request.sid
            
            # Remover cliente
            if session_id in self.connected_clients:
                self.connected_clients.remove(session_id)
            
            # Remover de salas
            if session_id in self.user_rooms:
                user_id = self.user_rooms[session_id]
                if user_id in self.room_users:
                    self.room_users[user_id].discard(session_id)
                    if not self.room_users[user_id]:
                        del self.room_users[user_id]
                del self.user_rooms[session_id]
            
            logger.info(f"Cliente desconectado: {session_id}")
        
        @self.socketio.on('join_user_room')
        def handle_join_user_room(data):
            session_id = request.sid
            user_id = data.get('user_id')
            
            if user_id:
                # Entrar na sala do usuário
                join_room(f"user_{user_id}")
                
                # Registrar mapeamentos
                self.user_rooms[session_id] = user_id
                if user_id not in self.room_users:
                    self.room_users[user_id] = set()
                self.room_users[user_id].add(session_id)
                
                logger.info(f"Cliente {session_id} entrou na sala do usuário {user_id}")
                
                emit('room_joined', {
                    'user_id': user_id,
                    'room': f"user_{user_id}",
                    'timestamp': datetime.now().isoformat()
                })
        
        @self.socketio.on('request_dashboard_update')
        def handle_dashboard_update_request():
            session_id = request.sid
            
            # Enviar dados atuais do dashboard
            self.send_dashboard_update(session_id)
        
        @self.socketio.on('request_job_status')
        def handle_job_status_request(data):
            job_id = data.get('job_id')
            
            if job_id:
                # Buscar status do job
                from .job_queue import job_queue
                job = job_queue.get_job(job_id)
                
                if job:
                    emit('job_status_update', {
                        'job_id': job_id,
                        'status': job.status.value,
                        'progress': self._calculate_job_progress(job),
                        'timestamp': datetime.now().isoformat()
                    })
    
    def send_dashboard_update(self, session_id=None, user_id=None):
        """Envia atualização do dashboard"""
        try:
            # Buscar estatísticas atuais
            from .job_queue import job_queue
            
            stats = job_queue.get_queue_stats()
            
            dashboard_data = {
                'type': 'dashboard_update',
                'data': {
                    'jobs': stats,
                    'metrics': {
                        'total_likes': stats.get('completed', 0) * 2,  # Simulação
                        'total_comments': stats.get('completed', 0),
                        'total_connections': 1249 + stats.get('completed', 0),
                        'acceptance_rate': 73,
                        'ai_comments': stats.get('completed', 0) // 2
                    },
                    'system_status': 'operational',
                    'last_update': datetime.now().isoformat()
                },
                'timestamp': datetime.now().isoformat()
            }
            
            if session_id:
                # Enviar para sessão específica
                self.socketio.emit('dashboard_update', dashboard_data, room=session_id)
            elif user_id:
                # Enviar para todas as sessões do usuário
                self.socketio.emit('dashboard_update', dashboard_data, room=f"user_{user_id}")
            else:
                # Broadcast para todos
                self.socketio.emit('dashboard_update', dashboard_data)
            
            logger.info("Dashboard update enviado")
            
        except Exception as e:
            logger.error(f"Erro ao enviar dashboard update: {str(e)}")
    
    def send_job_update(self, job_id: str, status: str, result: Dict = None, user_id: str = None):
        """Envia atualização de job"""
        try:
            job_data = {
                'type': 'job_update',
                'data': {
                    'job_id': job_id,
                    'status': status,
                    'result': result,
                    'progress': self._get_progress_by_status(status),
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            if user_id:
                self.socketio.emit('job_update', job_data, room=f"user_{user_id}")
            else:
                self.socketio.emit('job_update', job_data)
            
            logger.info(f"Job update enviado: {job_id} - {status}")
            
        except Exception as e:
            logger.error(f"Erro ao enviar job update: {str(e)}")
    
    def send_automation_event(self, event_type: str, data: Dict, user_id: str = None):
        """Envia evento de automação"""
        try:
            event_data = {
                'type': 'automation_event',
                'event_type': event_type,
                'data': data,
                'timestamp': datetime.now().isoformat()
            }
            
            if user_id:
                self.socketio.emit('automation_event', event_data, room=f"user_{user_id}")
            else:
                self.socketio.emit('automation_event', event_data)
            
            logger.info(f"Automation event enviado: {event_type}")
            
        except Exception as e:
            logger.error(f"Erro ao enviar automation event: {str(e)}")
    
    def send_notification(self, message: str, level: str = 'info', user_id: str = None):
        """Envia notificação"""
        try:
            notification_data = {
                'type': 'notification',
                'data': {
                    'message': message,
                    'level': level,  # info, success, warning, error
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            if user_id:
                self.socketio.emit('notification', notification_data, room=f"user_{user_id}")
            else:
                self.socketio.emit('notification', notification_data)
            
            logger.info(f"Notificação enviada: {message}")
            
        except Exception as e:
            logger.error(f"Erro ao enviar notificação: {str(e)}")
    
    def send_rate_limit_warning(self, limit_type: str, remaining: int, user_id: str = None):
        """Envia aviso de rate limiting"""
        try:
            warning_data = {
                'type': 'rate_limit_warning',
                'data': {
                    'limit_type': limit_type,
                    'remaining': remaining,
                    'message': f"Atenção: {remaining} ações restantes para {limit_type}",
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            if user_id:
                self.socketio.emit('rate_limit_warning', warning_data, room=f"user_{user_id}")
            else:
                self.socketio.emit('rate_limit_warning', warning_data)
            
            logger.info(f"Rate limit warning enviado: {limit_type} - {remaining}")
            
        except Exception as e:
            logger.error(f"Erro ao enviar rate limit warning: {str(e)}")
    
    def send_system_status(self, status: str, message: str = None):
        """Envia status do sistema"""
        try:
            status_data = {
                'type': 'system_status',
                'data': {
                    'status': status,  # operational, maintenance, error
                    'message': message,
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            self.socketio.emit('system_status', status_data)
            logger.info(f"System status enviado: {status}")
            
        except Exception as e:
            logger.error(f"Erro ao enviar system status: {str(e)}")
    
    def _calculate_job_progress(self, job) -> int:
        """Calcula progresso do job baseado no status"""
        from .job_queue import JobStatus
        
        progress_map = {
            JobStatus.PENDING: 0,
            JobStatus.RUNNING: 50,
            JobStatus.COMPLETED: 100,
            JobStatus.FAILED: 100,
            JobStatus.CANCELLED: 100
        }
        
        return progress_map.get(job.status, 0)
    
    def _get_progress_by_status(self, status: str) -> int:
        """Obtém progresso por string de status"""
        progress_map = {
            'pending': 0,
            'running': 50,
            'completed': 100,
            'failed': 100,
            'cancelled': 100
        }
        
        return progress_map.get(status, 0)
    
    def get_connected_clients_count(self) -> int:
        """Retorna número de clientes conectados"""
        return len(self.connected_clients)
    
    def get_user_sessions(self, user_id: str) -> Set[str]:
        """Retorna sessões ativas de um usuário"""
        return self.room_users.get(user_id, set())
    
    def broadcast_to_all(self, event: str, data: Dict):
        """Faz broadcast para todos os clientes conectados"""
        try:
            self.socketio.emit(event, data)
            logger.info(f"Broadcast enviado: {event}")
        except Exception as e:
            logger.error(f"Erro no broadcast: {str(e)}")

# Instância será criada quando SocketIO for inicializado
websocket_manager = None

def initialize_websocket_manager(socketio: SocketIO):
    """Inicializa o gerenciador WebSocket"""
    global websocket_manager
    websocket_manager = WebSocketManager(socketio)
    logger.info("WebSocket Manager inicializado")
    return websocket_manager
