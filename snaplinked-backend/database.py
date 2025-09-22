"""
Sistema de persistência de dados para SnapLinked
Usando SQLite para armazenar dados de automação e estatísticas
"""

import sqlite3
import json
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

class SnapLinkedDatabase:
    def __init__(self, db_path='snaplinked.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializar banco de dados e criar tabelas"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Tabela de usuários
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        name TEXT,
                        linkedin_profile TEXT,
                        connection_type TEXT DEFAULT 'oauth',
                        is_active BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabela de automações
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS automations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        name TEXT NOT NULL,
                        automation_type TEXT NOT NULL,
                        config TEXT,
                        is_active BOOLEAN DEFAULT 1,
                        total_executed INTEGER DEFAULT 0,
                        success_count INTEGER DEFAULT 0,
                        last_executed TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                # Tabela de execuções de automação
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS automation_executions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        automation_id INTEGER,
                        execution_type TEXT NOT NULL,
                        target_data TEXT,
                        result TEXT,
                        success BOOLEAN,
                        error_message TEXT,
                        executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (automation_id) REFERENCES automations (id)
                    )
                ''')
                
                # Tabela de estatísticas diárias
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS daily_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        date DATE NOT NULL,
                        connections_sent INTEGER DEFAULT 0,
                        messages_sent INTEGER DEFAULT 0,
                        profiles_viewed INTEGER DEFAULT 0,
                        likes_given INTEGER DEFAULT 0,
                        comments_posted INTEGER DEFAULT 0,
                        success_rate REAL DEFAULT 0.0,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        UNIQUE(user_id, date)
                    )
                ''')
                
                # Tabela de logs de atividade
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS activity_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        action_type TEXT NOT NULL,
                        description TEXT,
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                conn.commit()
                logger.info("Banco de dados inicializado com sucesso")
                
        except Exception as e:
            logger.error(f"Erro ao inicializar banco de dados: {e}")
            raise
    
    def create_user(self, email, name=None, linkedin_profile=None, connection_type='oauth'):
        """Criar novo usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO users (email, name, linkedin_profile, connection_type)
                    VALUES (?, ?, ?, ?)
                ''', (email, name, json.dumps(linkedin_profile) if linkedin_profile else None, connection_type))
                
                user_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"Usuário criado/atualizado: {email}")
                return user_id
                
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Obter usuário por email"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        'id': row[0],
                        'email': row[1],
                        'name': row[2],
                        'linkedin_profile': json.loads(row[3]) if row[3] else None,
                        'connection_type': row[4],
                        'is_active': bool(row[5]),
                        'created_at': row[6],
                        'updated_at': row[7]
                    }
                return None
                
        except Exception as e:
            logger.error(f"Erro ao obter usuário: {e}")
            return None
    
    def create_automation(self, user_id, name, automation_type, config=None):
        """Criar nova automação"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO automations (user_id, name, automation_type, config)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, name, automation_type, json.dumps(config) if config else None))
                
                automation_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"Automação criada: {name} para usuário {user_id}")
                return automation_id
                
        except Exception as e:
            logger.error(f"Erro ao criar automação: {e}")
            return None
    
    def log_automation_execution(self, automation_id, execution_type, target_data=None, result=None, success=True, error_message=None):
        """Registrar execução de automação"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Inserir log de execução
                cursor.execute('''
                    INSERT INTO automation_executions 
                    (automation_id, execution_type, target_data, result, success, error_message)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    automation_id, 
                    execution_type, 
                    json.dumps(target_data) if target_data else None,
                    json.dumps(result) if result else None,
                    success,
                    error_message
                ))
                
                # Atualizar contadores da automação
                cursor.execute('''
                    UPDATE automations 
                    SET total_executed = total_executed + 1,
                        success_count = success_count + ?,
                        last_executed = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (1 if success else 0, automation_id))
                
                conn.commit()
                logger.info(f"Execução registrada para automação {automation_id}")
                
        except Exception as e:
            logger.error(f"Erro ao registrar execução: {e}")
    
    def update_daily_stats(self, user_id, stats_data):
        """Atualizar estatísticas diárias"""
        try:
            today = datetime.now().date()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Inserir ou atualizar estatísticas do dia
                cursor.execute('''
                    INSERT OR REPLACE INTO daily_stats 
                    (user_id, date, connections_sent, messages_sent, profiles_viewed, 
                     likes_given, comments_posted, success_rate)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    today,
                    stats_data.get('connections_sent', 0),
                    stats_data.get('messages_sent', 0),
                    stats_data.get('profiles_viewed', 0),
                    stats_data.get('likes_given', 0),
                    stats_data.get('comments_posted', 0),
                    stats_data.get('success_rate', 0.0)
                ))
                
                conn.commit()
                logger.info(f"Estatísticas diárias atualizadas para usuário {user_id}")
                
        except Exception as e:
            logger.error(f"Erro ao atualizar estatísticas: {e}")
    
    def get_user_stats(self, user_id, days=30):
        """Obter estatísticas do usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Estatísticas totais
                cursor.execute('''
                    SELECT 
                        SUM(connections_sent) as total_connections,
                        SUM(messages_sent) as total_messages,
                        SUM(profiles_viewed) as total_profiles,
                        SUM(likes_given) as total_likes,
                        SUM(comments_posted) as total_comments,
                        AVG(success_rate) as avg_success_rate
                    FROM daily_stats 
                    WHERE user_id = ? AND date >= date('now', '-{} days')
                '''.format(days), (user_id,))
                
                stats_row = cursor.fetchone()
                
                # Estatísticas de hoje
                cursor.execute('''
                    SELECT connections_sent, messages_sent, profiles_viewed, 
                           likes_given, comments_posted, success_rate
                    FROM daily_stats 
                    WHERE user_id = ? AND date = date('now')
                ''', (user_id,))
                
                today_row = cursor.fetchone()
                
                return {
                    'total': {
                        'connections_sent': stats_row[0] or 0,
                        'messages_sent': stats_row[1] or 0,
                        'profiles_viewed': stats_row[2] or 0,
                        'likes_given': stats_row[3] or 0,
                        'comments_posted': stats_row[4] or 0,
                        'success_rate': round(stats_row[5] or 0, 1)
                    },
                    'today': {
                        'connections_sent': today_row[0] if today_row else 0,
                        'messages_sent': today_row[1] if today_row else 0,
                        'profiles_viewed': today_row[2] if today_row else 0,
                        'likes_given': today_row[3] if today_row else 0,
                        'comments_posted': today_row[4] if today_row else 0,
                        'success_rate': round(today_row[5] if today_row else 0, 1)
                    }
                }
                
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return None
    
    def log_activity(self, user_id, action_type, description, metadata=None):
        """Registrar atividade do usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO activity_logs (user_id, action_type, description, metadata)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, action_type, description, json.dumps(metadata) if metadata else None))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Erro ao registrar atividade: {e}")
    
    def get_recent_activity(self, user_id, limit=10):
        """Obter atividades recentes do usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT action_type, description, metadata, created_at
                    FROM activity_logs 
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (user_id, limit))
                
                rows = cursor.fetchall()
                
                return [{
                    'action_type': row[0],
                    'description': row[1],
                    'metadata': json.loads(row[2]) if row[2] else None,
                    'created_at': row[3]
                } for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao obter atividades: {e}")
            return []
    
    def get_automations(self, user_id):
        """Obter automações do usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name, automation_type, config, is_active, 
                           total_executed, success_count, last_executed, created_at
                    FROM automations 
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                ''', (user_id,))
                
                rows = cursor.fetchall()
                
                return [{
                    'id': row[0],
                    'name': row[1],
                    'automation_type': row[2],
                    'config': json.loads(row[3]) if row[3] else None,
                    'is_active': bool(row[4]),
                    'total_executed': row[5],
                    'success_count': row[6],
                    'success_rate': round((row[6] / row[5] * 100) if row[5] > 0 else 0, 1),
                    'last_executed': row[7],
                    'created_at': row[8]
                } for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao obter automações: {e}")
            return []

# Instância global do banco de dados
db = SnapLinkedDatabase()
