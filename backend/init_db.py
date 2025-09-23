#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapLinked v3.0 - Inicialização do Banco de Dados
Script para criar e configurar o banco de dados
"""

import os
import sys
from datetime import datetime, timezone

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, UserStats, AutomationSession, AutomationLog


def init_database():
    """Inicializar banco de dados"""
    print("🗄️ Inicializando banco de dados SnapLinked v3.0...")
    
    app = create_app()
    
    with app.app_context():
        # Criar todas as tabelas
        print("📋 Criando tabelas...")
        db.create_all()
        
        # Verificar se já existem dados
        user_count = User.query.count()
        print(f"👥 Usuários existentes: {user_count}")
        
        if user_count == 0:
            print("🆕 Criando dados de exemplo...")
            create_sample_data()
        
        print("✅ Banco de dados inicializado com sucesso!")
        print(f"📊 Localização: {app.config['SQLALCHEMY_DATABASE_URI']}")


def create_sample_data():
    """Criar dados de exemplo para demonstração"""
    try:
        # Usuário de exemplo
        sample_user = User(
            email='demo@snaplinked.com',
            name='Usuário Demo',
            linkedin_id='demo_user_123',
            linkedin_profile_url='https://linkedin.com/in/demo',
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        
        db.session.add(sample_user)
        db.session.flush()  # Para obter o ID
        
        # Estatísticas iniciais
        sample_stats = UserStats(
            user_id=sample_user.id,
            total_likes=15,
            total_connections=8,
            total_comments=3,
            total_views=45,
            last_activity=datetime.now(timezone.utc)
        )
        
        db.session.add(sample_stats)
        
        # Sessão de automação de exemplo
        sample_session = AutomationSession(
            user_id=sample_user.id,
            session_type='like',
            status='completed',
            target_count=5,
            completed_count=5,
            error_count=0,
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc)
        )
        
        db.session.add(sample_session)
        db.session.flush()
        
        # Logs de exemplo
        sample_logs = [
            AutomationLog(
                user_id=sample_user.id,
                session_id=sample_session.id,
                action_type='like',
                target_url='https://linkedin.com/feed/update/123',
                target_name='Post sobre tecnologia',
                status='success',
                message='Post curtido com sucesso',
                metadata={'post_type': 'article', 'author': 'Tech Expert'}
            ),
            AutomationLog(
                user_id=sample_user.id,
                session_id=sample_session.id,
                action_type='like',
                target_url='https://linkedin.com/feed/update/456',
                target_name='Post sobre carreira',
                status='success',
                message='Post curtido com sucesso',
                metadata={'post_type': 'text', 'author': 'Career Coach'}
            )
        ]
        
        for log in sample_logs:
            db.session.add(log)
        
        db.session.commit()
        print("✅ Dados de exemplo criados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados de exemplo: {str(e)}")
        db.session.rollback()


def reset_database():
    """Resetar banco de dados (CUIDADO: apaga todos os dados)"""
    print("⚠️ ATENÇÃO: Esta operação irá apagar todos os dados!")
    confirm = input("Digite 'CONFIRMAR' para continuar: ")
    
    if confirm != 'CONFIRMAR':
        print("❌ Operação cancelada.")
        return
    
    app = create_app()
    
    with app.app_context():
        print("🗑️ Removendo todas as tabelas...")
        db.drop_all()
        
        print("📋 Recriando tabelas...")
        db.create_all()
        
        print("🆕 Criando dados de exemplo...")
        create_sample_data()
        
        print("✅ Banco de dados resetado com sucesso!")


def show_stats():
    """Mostrar estatísticas do banco de dados"""
    app = create_app()
    
    with app.app_context():
        print("📊 Estatísticas do Banco de Dados:")
        print("-" * 40)
        
        user_count = User.query.count()
        session_count = AutomationSession.query.count()
        log_count = AutomationLog.query.count()
        
        print(f"👥 Usuários: {user_count}")
        print(f"🤖 Sessões de Automação: {session_count}")
        print(f"📝 Logs de Automação: {log_count}")
        
        if user_count > 0:
            print("\n👤 Usuários:")
            users = User.query.all()
            for user in users:
                stats = UserStats.query.filter_by(user_id=user.id).first()
                print(f"  - {user.name} ({user.email})")
                if stats:
                    print(f"    👍 {stats.total_likes} curtidas, 🤝 {stats.total_connections} conexões, 💬 {stats.total_comments} comentários")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Gerenciar banco de dados SnapLinked')
    parser.add_argument('action', choices=['init', 'reset', 'stats'], 
                       help='Ação a ser executada')
    
    args = parser.parse_args()
    
    if args.action == 'init':
        init_database()
    elif args.action == 'reset':
        reset_database()
    elif args.action == 'stats':
        show_stats()
