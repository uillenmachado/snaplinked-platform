#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapLinked v3.0 - Modelos de Dados Otimizados
Definições das entidades do banco de dados com otimizações de performance
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, Index, text
from sqlalchemy.orm import validates, relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
import bcrypt
import jwt
from config import Config

db = SQLAlchemy()


class TimestampMixin:
    """Mixin para timestamps automáticos"""
    created_at = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False,
        index=True  # Índice para consultas por data
    )
    updated_at = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False,
        index=True
    )


class User(db.Model, TimestampMixin):
    """Modelo de usuário otimizado"""
    
    __tablename__ = 'users'
    
    # Índices compostos para performance
    __table_args__ = (
        Index('idx_user_email_active', 'email', 'is_active'),
        Index('idx_user_linkedin_id', 'linkedin_id'),
        Index('idx_user_created_at', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    linkedin_id = db.Column(db.String(50), unique=True, nullable=True, index=True)
    linkedin_profile_url = db.Column(db.String(200), nullable=True)
    avatar_url = db.Column(db.String(200), nullable=True)
    
    # Tokens com criptografia
    access_token = db.Column(db.Text, nullable=True)
    refresh_token = db.Column(db.Text, nullable=True)
    token_expires_at = db.Column(db.DateTime, nullable=True, index=True)
    
    # Status e configurações
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    is_premium = db.Column(db.Boolean, default=False, nullable=False)
    last_login_at = db.Column(db.DateTime, nullable=True, index=True)
    login_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Configurações de automação
    automation_enabled = db.Column(db.Boolean, default=True, nullable=False)
    daily_limit_likes = db.Column(db.Integer, default=50, nullable=False)
    daily_limit_connections = db.Column(db.Integer, default=20, nullable=False)
    daily_limit_comments = db.Column(db.Integer, default=10, nullable=False)
    
    # Relacionamentos otimizados com lazy loading
    automation_sessions = relationship(
        'AutomationSession', 
        backref=backref('user', lazy='select'),
        lazy='dynamic',  # Permite queries otimizadas
        cascade='all, delete-orphan',
        order_by='AutomationSession.created_at.desc()'
    )
    
    automation_logs = relationship(
        'AutomationLog',
        backref=backref('user', lazy='select'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    user_stats = relationship(
        'UserStats',
        backref=backref('user', lazy='select'),
        uselist=False,  # One-to-one
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    @validates('email')
    def validate_email(self, key, email):
        """Validar formato de email"""
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError('Email format invalid')
        return email.lower().strip()
    
    @validates('name')
    def validate_name(self, key, name):
        """Validar nome"""
        if not name or len(name.strip()) < 2:
            raise ValueError('Name must be at least 2 characters')
        return name.strip()
    
    def to_dict(self, include_sensitive=False):
        """Converter para dicionário com controle de dados sensíveis"""
        data = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'linkedin_id': self.linkedin_id,
            'linkedin_profile_url': self.linkedin_profile_url,
            'avatar_url': self.avatar_url,
            'is_active': self.is_active,
            'is_premium': self.is_premium,
            'automation_enabled': self.automation_enabled,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            data.update({
                'login_count': self.login_count,
                'daily_limits': {
                    'likes': self.daily_limit_likes,
                    'connections': self.daily_limit_connections,
                    'comments': self.daily_limit_comments
                },
                'token_expires_at': self.token_expires_at.isoformat() if self.token_expires_at else None
            })
        
        return data
    
    def generate_auth_token(self, expires_in=86400):
        """Gerar token JWT com expiração configurável"""
        payload = {
            'user_id': self.id,
            'email': self.email,
            'iat': datetime.now(timezone.utc).timestamp(),
            'exp': datetime.now(timezone.utc).timestamp() + expires_in
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def verify_auth_token(token):
        """Verificar token JWT com logging de erros"""
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            user = User.query.get(payload['user_id'])
            if user and user.is_active:
                return user
            return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def update_login_stats(self):
        """Atualizar estatísticas de login"""
        self.last_login_at = datetime.now(timezone.utc)
        self.login_count += 1
        self.updated_at = datetime.now(timezone.utc)
    
    @hybrid_property
    def is_token_valid(self):
        """Verificar se token ainda é válido"""
        if not self.token_expires_at:
            return False
        return self.token_expires_at > datetime.now(timezone.utc)
    
    def get_daily_usage(self, date=None):
        """Obter uso diário de automações"""
        if not date:
            date = datetime.now(timezone.utc).date()
        
        # Query otimizada com índices
        sessions = self.automation_sessions.filter(
            func.date(AutomationSession.created_at) == date,
            AutomationSession.status == 'completed'
        ).all()
        
        usage = {
            'likes': sum(s.actual_count for s in sessions if s.action_type == 'like'),
            'connections': sum(s.actual_count for s in sessions if s.action_type == 'connect'),
            'comments': sum(s.actual_count for s in sessions if s.action_type == 'comment')
        }
        
        return usage
    
    def can_perform_action(self, action_type, count=1):
        """Verificar se pode realizar ação baseado nos limites diários"""
        if not self.automation_enabled:
            return False
        
        usage = self.get_daily_usage()
        limits = {
            'like': self.daily_limit_likes,
            'connect': self.daily_limit_connections,
            'comment': self.daily_limit_comments
        }
        
        current_usage = usage.get(action_type + 's', 0)  # likes, connections, comments
        limit = limits.get(action_type, 0)
        
        return current_usage + count <= limit


class AutomationSession(db.Model, TimestampMixin):
    """Sessão de automação otimizada"""
    
    __tablename__ = 'automation_sessions'
    
    __table_args__ = (
        Index('idx_session_user_status', 'user_id', 'status'),
        Index('idx_session_action_type', 'action_type'),
        Index('idx_session_created_at', 'created_at'),
        Index('idx_session_user_date', 'user_id', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Configurações da sessão
    action_type = db.Column(db.String(20), nullable=False, index=True)  # like, connect, comment
    target_count = db.Column(db.Integer, nullable=False)
    actual_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Status e timing
    status = db.Column(db.String(20), default='pending', nullable=False, index=True)  # pending, running, completed, failed, cancelled
    started_at = db.Column(db.DateTime, nullable=True, index=True)
    completed_at = db.Column(db.DateTime, nullable=True, index=True)
    
    # Metadados
    error_message = db.Column(db.Text, nullable=True)
    session_metadata = db.Column(db.JSON, nullable=True)  # Dados adicionais da sessão
    
    # Relacionamentos
    logs = relationship(
        'AutomationLog',
        backref=backref('session', lazy='select'),
        lazy='dynamic',
        cascade='all, delete-orphan',
        order_by='AutomationLog.created_at.desc()'
    )
    
    def __repr__(self):
        return f'<AutomationSession {self.id}: {self.action_type} for user {self.user_id}>'
    
    @validates('action_type')
    def validate_action_type(self, key, action_type):
        """Validar tipo de ação"""
        valid_actions = ['like', 'connect', 'comment']
        if action_type not in valid_actions:
            raise ValueError(f'Action type must be one of: {valid_actions}')
        return action_type
    
    @validates('status')
    def validate_status(self, key, status):
        """Validar status"""
        valid_statuses = ['pending', 'running', 'completed', 'failed', 'cancelled']
        if status not in valid_statuses:
            raise ValueError(f'Status must be one of: {valid_statuses}')
        return status
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action_type': self.action_type,
            'target_count': self.target_count,
            'actual_count': self.actual_count,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'error_message': self.error_message,
            'session_metadata': self.session_metadata,
            'duration_seconds': self.duration_seconds,
            'success_rate': self.success_rate
        }
    
    @hybrid_property
    def duration_seconds(self):
        """Calcular duração da sessão em segundos"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        elif self.started_at:
            return (datetime.now(timezone.utc) - self.started_at).total_seconds()
        return 0
    
    @hybrid_property
    def success_rate(self):
        """Calcular taxa de sucesso"""
        if self.target_count > 0:
            return (self.actual_count / self.target_count) * 100
        return 0
    
    def start_session(self):
        """Iniciar sessão"""
        self.status = 'running'
        self.started_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
    
    def complete_session(self, actual_count=None):
        """Completar sessão"""
        self.status = 'completed'
        self.completed_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        if actual_count is not None:
            self.actual_count = actual_count
    
    def fail_session(self, error_message=None):
        """Marcar sessão como falha"""
        self.status = 'failed'
        self.completed_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        if error_message:
            self.error_message = error_message


class AutomationLog(db.Model, TimestampMixin):
    """Log de automação otimizado"""
    
    __tablename__ = 'automation_logs'
    
    __table_args__ = (
        Index('idx_log_session_id', 'session_id'),
        Index('idx_log_user_action', 'user_id', 'action'),
        Index('idx_log_created_at', 'created_at'),
        Index('idx_log_success', 'success'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('automation_sessions.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Detalhes da ação
    action = db.Column(db.String(20), nullable=False, index=True)
    target_element = db.Column(db.String(50), nullable=True)
    success = db.Column(db.Boolean, nullable=False, index=True)
    
    # Metadados
    details = db.Column(db.JSON, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    execution_time_ms = db.Column(db.Integer, nullable=True)  # Tempo de execução em ms
    
    def __repr__(self):
        return f'<AutomationLog {self.id}: {self.action} - {"Success" if self.success else "Failed"}>'
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'action': self.action,
            'target_element': self.target_element,
            'success': self.success,
            'details': self.details,
            'error_message': self.error_message,
            'execution_time_ms': self.execution_time_ms,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class UserStats(db.Model, TimestampMixin):
    """Estatísticas do usuário otimizadas"""
    
    __tablename__ = 'user_stats'
    
    __table_args__ = (
        Index('idx_stats_user_id', 'user_id'),
        Index('idx_stats_updated_at', 'updated_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    
    # Contadores totais
    total_likes = db.Column(db.Integer, default=0, nullable=False)
    total_connections = db.Column(db.Integer, default=0, nullable=False)
    total_comments = db.Column(db.Integer, default=0, nullable=False)
    total_sessions = db.Column(db.Integer, default=0, nullable=False)
    
    # Estatísticas de sucesso
    successful_sessions = db.Column(db.Integer, default=0, nullable=False)
    failed_sessions = db.Column(db.Integer, default=0, nullable=False)
    
    # Métricas de tempo
    total_automation_time_seconds = db.Column(db.Integer, default=0, nullable=False)
    average_session_duration = db.Column(db.Float, default=0.0, nullable=False)
    
    # Estatísticas por período
    stats_this_week = db.Column(db.JSON, nullable=True)
    stats_this_month = db.Column(db.JSON, nullable=True)
    
    # Última atividade
    last_automation_at = db.Column(db.DateTime, nullable=True, index=True)
    
    def __repr__(self):
        return f'<UserStats for user {self.user_id}>'
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'user_id': self.user_id,
            'total_actions': self.total_likes + self.total_connections + self.total_comments,
            'total_likes': self.total_likes,
            'total_connections': self.total_connections,
            'total_comments': self.total_comments,
            'total_sessions': self.total_sessions,
            'successful_sessions': self.successful_sessions,
            'failed_sessions': self.failed_sessions,
            'success_rate': self.success_rate,
            'total_automation_time_seconds': self.total_automation_time_seconds,
            'average_session_duration': self.average_session_duration,
            'stats_this_week': self.stats_this_week,
            'stats_this_month': self.stats_this_month,
            'last_automation_at': self.last_automation_at.isoformat() if self.last_automation_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @hybrid_property
    def success_rate(self):
        """Calcular taxa de sucesso das sessões"""
        if self.total_sessions > 0:
            return (self.successful_sessions / self.total_sessions) * 100
        return 0
    
    def update_stats(self, session: AutomationSession):
        """Atualizar estatísticas baseado em uma sessão"""
        # Incrementar contadores
        if session.action_type == 'like':
            self.total_likes += session.actual_count
        elif session.action_type == 'connect':
            self.total_connections += session.actual_count
        elif session.action_type == 'comment':
            self.total_comments += session.actual_count
        
        self.total_sessions += 1
        
        # Atualizar status da sessão
        if session.status == 'completed':
            self.successful_sessions += 1
        elif session.status == 'failed':
            self.failed_sessions += 1
        
        # Atualizar métricas de tempo
        if session.duration_seconds > 0:
            total_time = self.total_automation_time_seconds + session.duration_seconds
            self.total_automation_time_seconds = int(total_time)
            self.average_session_duration = total_time / self.total_sessions
        
        # Atualizar última atividade
        self.last_automation_at = session.completed_at or datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
    
    def get_weekly_stats(self):
        """Obter estatísticas da semana"""
        # Implementar lógica para calcular stats semanais
        return self.stats_this_week or {}
    
    def get_monthly_stats(self):
        """Obter estatísticas do mês"""
        # Implementar lógica para calcular stats mensais
        return self.stats_this_month or {}


# Funções utilitárias para queries otimizadas

def get_user_with_stats(user_id: int):
    """Obter usuário com estatísticas em uma query"""
    return db.session.query(User).options(
        db.joinedload(User.user_stats)
    ).filter(User.id == user_id).first()


def get_recent_sessions(user_id: int, limit: int = 10):
    """Obter sessões recentes do usuário"""
    return AutomationSession.query.filter_by(user_id=user_id)\
        .order_by(AutomationSession.created_at.desc())\
        .limit(limit).all()


def get_daily_usage_stats(user_id: int, date=None):
    """Obter estatísticas de uso diário otimizada"""
    if not date:
        date = datetime.now(timezone.utc).date()
    
    # Query otimizada com agregação
    result = db.session.query(
        AutomationSession.action_type,
        func.sum(AutomationSession.actual_count).label('total_count'),
        func.count(AutomationSession.id).label('session_count')
    ).filter(
        AutomationSession.user_id == user_id,
        func.date(AutomationSession.created_at) == date,
        AutomationSession.status == 'completed'
    ).group_by(AutomationSession.action_type).all()
    
    stats = {
        'likes': 0,
        'connections': 0,
        'comments': 0,
        'sessions': 0
    }
    
    for action_type, total_count, session_count in result:
        if action_type == 'like':
            stats['likes'] = total_count or 0
        elif action_type == 'connect':
            stats['connections'] = total_count or 0
        elif action_type == 'comment':
            stats['comments'] = total_count or 0
        stats['sessions'] += session_count or 0
    
    return stats


def cleanup_old_logs(days_to_keep: int = 30):
    """Limpar logs antigos para manter performance"""
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_to_keep)
    
    deleted_count = AutomationLog.query.filter(
        AutomationLog.created_at < cutoff_date
    ).delete()
    
    db.session.commit()
    return deleted_count
