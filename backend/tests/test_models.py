#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapLinked v3.0 - Testes dos Modelos
Testes unitários para os modelos de dados
"""

import unittest
import sys
import os
from datetime import datetime, timezone

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, UserStats, AutomationSession, AutomationLog


class TestModels(unittest.TestCase):
    """Testes para os modelos de dados"""
    
    def setUp(self):
        """Configurar ambiente de teste"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Limpar ambiente de teste"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_creation(self):
        """Testar criação de usuário"""
        user = User(
            email='test@example.com',
            name='Usuário Teste',
            linkedin_id='test123'
        )
        db.session.add(user)
        db.session.commit()
        
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.name, 'Usuário Teste')
        self.assertEqual(user.linkedin_id, 'test123')
        self.assertTrue(user.is_active)
        self.assertIsNotNone(user.created_at)
    
    def test_user_to_dict(self):
        """Testar conversão de usuário para dicionário"""
        user = User(
            email='test@example.com',
            name='Usuário Teste',
            linkedin_id='test123'
        )
        db.session.add(user)
        db.session.commit()
        
        user_dict = user.to_dict()
        
        self.assertIsInstance(user_dict, dict)
        self.assertEqual(user_dict['email'], 'test@example.com')
        self.assertEqual(user_dict['name'], 'Usuário Teste')
        self.assertEqual(user_dict['linkedin_id'], 'test123')
        self.assertTrue(user_dict['is_active'])
    
    def test_user_auth_token(self):
        """Testar geração e verificação de token de autenticação"""
        user = User(
            email='test@example.com',
            name='Usuário Teste'
        )
        db.session.add(user)
        db.session.commit()
        
        # Gerar token
        token = user.generate_auth_token()
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        
        # Verificar token
        verified_user = User.verify_auth_token(token)
        self.assertIsNotNone(verified_user)
        self.assertEqual(verified_user.id, user.id)
    
    def test_user_stats_creation(self):
        """Testar criação de estatísticas de usuário"""
        user = User(email='test@example.com', name='Usuário Teste')
        db.session.add(user)
        db.session.commit()
        
        stats = UserStats(user_id=user.id)
        db.session.add(stats)
        db.session.commit()
        
        self.assertIsNotNone(stats.id)
        self.assertEqual(stats.user_id, user.id)
        self.assertEqual(stats.total_likes, 0)
        self.assertEqual(stats.total_connections, 0)
        self.assertEqual(stats.total_comments, 0)
        self.assertEqual(stats.total_views, 0)
    
    def test_user_stats_update(self):
        """Testar atualização de estatísticas"""
        user = User(email='test@example.com', name='Usuário Teste')
        db.session.add(user)
        db.session.commit()
        
        stats = UserStats(user_id=user.id)
        db.session.add(stats)
        db.session.commit()
        
        # Atualizar estatísticas
        stats.update_stats('like', 5)
        self.assertEqual(stats.total_likes, 5)
        
        stats.update_stats('connect', 3)
        self.assertEqual(stats.total_connections, 3)
        
        stats.update_stats('comment', 2)
        self.assertEqual(stats.total_comments, 2)
        
        self.assertIsNotNone(stats.last_activity)
    
    def test_automation_session_creation(self):
        """Testar criação de sessão de automação"""
        user = User(email='test@example.com', name='Usuário Teste')
        db.session.add(user)
        db.session.commit()
        
        session = AutomationSession(
            user_id=user.id,
            session_type='like',
            target_count=5
        )
        db.session.add(session)
        db.session.commit()
        
        self.assertIsNotNone(session.id)
        self.assertEqual(session.user_id, user.id)
        self.assertEqual(session.session_type, 'like')
        self.assertEqual(session.status, 'pending')
        self.assertEqual(session.target_count, 5)
        self.assertEqual(session.completed_count, 0)
        self.assertEqual(session.error_count, 0)
    
    def test_automation_log_creation(self):
        """Testar criação de log de automação"""
        user = User(email='test@example.com', name='Usuário Teste')
        db.session.add(user)
        db.session.commit()
        
        session = AutomationSession(
            user_id=user.id,
            session_type='like',
            target_count=1
        )
        db.session.add(session)
        db.session.commit()
        
        log = AutomationLog(
            user_id=user.id,
            session_id=session.id,
            action_type='like',
            target_url='https://linkedin.com/feed/update/123',
            target_name='Post de teste',
            status='success',
            message='Teste realizado com sucesso'
        )
        db.session.add(log)
        db.session.commit()
        
        self.assertIsNotNone(log.id)
        self.assertEqual(log.user_id, user.id)
        self.assertEqual(log.session_id, session.id)
        self.assertEqual(log.action_type, 'like')
        self.assertEqual(log.status, 'success')
        self.assertEqual(log.message, 'Teste realizado com sucesso')
    
    def test_user_relationships(self):
        """Testar relacionamentos entre modelos"""
        user = User(email='test@example.com', name='Usuário Teste')
        db.session.add(user)
        db.session.commit()
        
        # Criar estatísticas
        stats = UserStats(user_id=user.id)
        db.session.add(stats)
        
        # Criar sessão
        session = AutomationSession(user_id=user.id, session_type='like')
        db.session.add(session)
        db.session.commit()
        
        # Criar log
        log = AutomationLog(
            user_id=user.id,
            session_id=session.id,
            action_type='like',
            status='success'
        )
        db.session.add(log)
        db.session.commit()
        
        # Testar relacionamentos
        self.assertEqual(user.stats, stats)
        self.assertIn(session, user.automation_sessions)
        self.assertIn(log, user.automation_logs)
        self.assertIn(log, session.logs)


if __name__ == '__main__':
    unittest.main()
