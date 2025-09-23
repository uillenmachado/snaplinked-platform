#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapLinked v3.0 - Modelos de Dados
Definições das entidades do banco de dados
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import bcrypt
import jwt
from config import Config

db = SQLAlchemy()


class User(db.Model):
    """Modelo de usuário"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    linkedin_id = db.Column(db.String(50), unique=True, nullable=True, index=True)
    linkedin_profile_url = db.Column(db.String(200), nullable=True)
    avatar_url = db.Column(db.String(200), nullable=True)
    access_token = db.Column(db.Text, nullable=True)  # Token OAuth LinkedIn
    refresh_token = db.Column(db.Text, nullable=True)
    token_expires_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), 
                          onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relacionamentos
    automation_sessions = db.relationship('AutomationSession', backref='user', lazy=True, cascade='all, delete-orphan')
    automation_logs = db.relationship('AutomationLog', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'linkedin_id': self.linkedin_id,
            'linkedin_profile_url': self.linkedin_profile_url,
            'avatar_url': self.avatar_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def generate_auth_token(self):
        """Gerar token JWT para autenticação"""
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': datetime.now(timezone.utc).timestamp() + 86400  # 24 horas
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def verify_auth_token(token):
        """Verificar token JWT"""
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            return User.query.get(payload['user_id'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


class AutomationSession(db.Model):
    """Sessão de automação"""
    
    __tablename__ = 'automation_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_type = db.Column(db.String(50), nullable=False)  # 'like', 'connect', 'comment'
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, running, completed, failed
    target_count = db.Column(db.Integer, default=0, nullable=False)
    completed_count = db.Column(db.Integer, default=0, nullable=False)
    error_count = db.Column(db.Integer, default=0, nullable=False)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relacionamentos
    logs = db.relationship('AutomationLog', backref='session', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<AutomationSession {self.id} - {self.session_type}>'
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_type': self.session_type,
            'status': self.status,
            'target_count': self.target_count,
            'completed_count': self.completed_count,
            'error_count': self.error_count,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AutomationLog(db.Model):
    """Log de ações de automação"""
    
    __tablename__ = 'automation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('automation_sessions.id'), nullable=True)
    action_type = db.Column(db.String(50), nullable=False)  # 'like', 'connect', 'comment', 'view'
    target_url = db.Column(db.String(500), nullable=True)  # URL do post/perfil
    target_name = db.Column(db.String(200), nullable=True)  # Nome da pessoa/empresa
    status = db.Column(db.String(20), nullable=False)  # 'success', 'failed', 'skipped'
    message = db.Column(db.Text, nullable=True)  # Mensagem de erro ou sucesso
    metadata = db.Column(db.JSON, nullable=True)  # Dados adicionais em JSON
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    def __repr__(self):
        return f'<AutomationLog {self.id} - {self.action_type}>'
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'action_type': self.action_type,
            'target_url': self.target_url,
            'target_name': self.target_name,
            'status': self.status,
            'message': self.message,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class UserStats(db.Model):
    """Estatísticas do usuário"""
    
    __tablename__ = 'user_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    total_likes = db.Column(db.Integer, default=0, nullable=False)
    total_connections = db.Column(db.Integer, default=0, nullable=False)
    total_comments = db.Column(db.Integer, default=0, nullable=False)
    total_views = db.Column(db.Integer, default=0, nullable=False)
    last_activity = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), 
                          onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relacionamento
    user = db.relationship('User', backref=db.backref('stats', uselist=False))
    
    def __repr__(self):
        return f'<UserStats user_id={self.user_id}>'
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'user_id': self.user_id,
            'total_likes': self.total_likes,
            'total_connections': self.total_connections,
            'total_comments': self.total_comments,
            'total_views': self.total_views,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_stats(self, action_type, count=1):
        """Atualizar estatísticas"""
        if action_type == 'like':
            self.total_likes += count
        elif action_type == 'connect':
            self.total_connections += count
        elif action_type == 'comment':
            self.total_comments += count
        elif action_type == 'view':
            self.total_views += count
        
        self.last_activity = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
