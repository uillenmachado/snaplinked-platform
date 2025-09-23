#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapLinked v3.0 - Script de Migração de Banco de Dados
Migração segura dos dados existentes para nova estrutura otimizada
"""

import os
import sys
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import structlog

# Configurar logging
logger = structlog.get_logger(__name__)

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from models import db, User, AutomationSession, AutomationLog, UserStats


def backup_database():
    """Criar backup do banco de dados atual"""
    try:
        import shutil
        db_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
        if os.path.exists(db_path):
            backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(db_path, backup_path)
            logger.info(f"Database backup created: {backup_path}")
            return backup_path
        return None
    except Exception as e:
        logger.error(f"Error creating backup: {str(e)}")
        return None


def migrate_user_data():
    """Migrar dados de usuários para nova estrutura"""
    try:
        # Verificar se tabela users existe
        result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'"))
        if not result.fetchone():
            logger.info("Users table does not exist, skipping migration")
            return True
        
        # Adicionar novas colunas se não existirem
        new_columns = [
            ('is_premium', 'BOOLEAN DEFAULT FALSE'),
            ('last_login_at', 'DATETIME'),
            ('login_count', 'INTEGER DEFAULT 0'),
            ('automation_enabled', 'BOOLEAN DEFAULT TRUE'),
            ('daily_limit_likes', 'INTEGER DEFAULT 50'),
            ('daily_limit_connections', 'INTEGER DEFAULT 20'),
            ('daily_limit_comments', 'INTEGER DEFAULT 10')
        ]
        
        for column_name, column_def in new_columns:
            try:
                db.session.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {column_def}"))
                logger.info(f"Added column {column_name} to users table")
            except Exception:
                # Coluna já existe
                pass
        
        db.session.commit()
        logger.info("User data migration completed")
        return True
        
    except Exception as e:
        logger.error(f"Error migrating user data: {str(e)}")
        db.session.rollback()
        return False


def migrate_session_data():
    """Migrar dados de sessões para nova estrutura"""
    try:
        # Verificar se tabela automation_sessions existe
        result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='automation_sessions'"))
        if not result.fetchone():
            logger.info("Automation sessions table does not exist, skipping migration")
            return True
        
        # Adicionar novas colunas se não existirem
        new_columns = [
            ('session_metadata', 'JSON'),
            ('started_at', 'DATETIME'),
            ('completed_at', 'DATETIME')
        ]
        
        for column_name, column_def in new_columns:
            try:
                db.session.execute(text(f"ALTER TABLE automation_sessions ADD COLUMN {column_name} {column_def}"))
                logger.info(f"Added column {column_name} to automation_sessions table")
            except Exception:
                # Coluna já existe
                pass
        
        db.session.commit()
        logger.info("Session data migration completed")
        return True
        
    except Exception as e:
        logger.error(f"Error migrating session data: {str(e)}")
        db.session.rollback()
        return False


def migrate_log_data():
    """Migrar dados de logs para nova estrutura"""
    try:
        # Verificar se tabela automation_logs existe
        result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='automation_logs'"))
        if not result.fetchone():
            logger.info("Automation logs table does not exist, skipping migration")
            return True
        
        # Adicionar novas colunas se não existirem
        new_columns = [
            ('execution_time_ms', 'INTEGER'),
            ('target_element', 'VARCHAR(50)')
        ]
        
        for column_name, column_def in new_columns:
            try:
                db.session.execute(text(f"ALTER TABLE automation_logs ADD COLUMN {column_name} {column_def}"))
                logger.info(f"Added column {column_name} to automation_logs table")
            except Exception:
                # Coluna já existe
                pass
        
        db.session.commit()
        logger.info("Log data migration completed")
        return True
        
    except Exception as e:
        logger.error(f"Error migrating log data: {str(e)}")
        db.session.rollback()
        return False


def create_user_stats():
    """Criar estatísticas para usuários existentes"""
    try:
        users = User.query.all()
        
        for user in users:
            if not user.user_stats:
                # Calcular estatísticas baseadas em dados existentes
                sessions = AutomationSession.query.filter_by(user_id=user.id).all()
                
                total_likes = sum(s.actual_count for s in sessions if s.action_type == 'like')
                total_connections = sum(s.actual_count for s in sessions if s.action_type == 'connect')
                total_comments = sum(s.actual_count for s in sessions if s.action_type == 'comment')
                
                successful_sessions = len([s for s in sessions if s.status == 'completed'])
                failed_sessions = len([s for s in sessions if s.status == 'failed'])
                
                stats = UserStats(
                    user_id=user.id,
                    total_likes=total_likes,
                    total_connections=total_connections,
                    total_comments=total_comments,
                    total_sessions=len(sessions),
                    successful_sessions=successful_sessions,
                    failed_sessions=failed_sessions
                )
                
                db.session.add(stats)
                logger.info(f"Created stats for user {user.id}")
        
        db.session.commit()
        logger.info("User stats creation completed")
        return True
        
    except Exception as e:
        logger.error(f"Error creating user stats: {str(e)}")
        db.session.rollback()
        return False


def create_indexes():
    """Criar índices para melhor performance"""
    try:
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_user_email_active ON users(email, is_active)",
            "CREATE INDEX IF NOT EXISTS idx_user_linkedin_id ON users(linkedin_id)",
            "CREATE INDEX IF NOT EXISTS idx_user_created_at ON users(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_session_user_status ON automation_sessions(user_id, status)",
            "CREATE INDEX IF NOT EXISTS idx_session_action_type ON automation_sessions(action_type)",
            "CREATE INDEX IF NOT EXISTS idx_session_created_at ON automation_sessions(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_log_session_id ON automation_logs(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_log_user_action ON automation_logs(user_id, action)",
            "CREATE INDEX IF NOT EXISTS idx_log_created_at ON automation_logs(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_stats_user_id ON user_stats(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_stats_updated_at ON user_stats(updated_at)"
        ]
        
        for index_sql in indexes:
            try:
                db.session.execute(text(index_sql))
                logger.info(f"Created index: {index_sql.split('ON')[1].split('(')[0].strip()}")
            except Exception as e:
                logger.warning(f"Index creation failed (may already exist): {str(e)}")
        
        db.session.commit()
        logger.info("Index creation completed")
        return True
        
    except Exception as e:
        logger.error(f"Error creating indexes: {str(e)}")
        db.session.rollback()
        return False


def verify_migration():
    """Verificar se migração foi bem-sucedida"""
    try:
        # Verificar se todas as tabelas existem
        tables = ['users', 'automation_sessions', 'automation_logs', 'user_stats']
        
        for table in tables:
            result = db.session.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"))
            if not result.fetchone():
                logger.error(f"Table {table} does not exist after migration")
                return False
        
        # Verificar se dados básicos existem
        user_count = User.query.count()
        session_count = AutomationSession.query.count()
        
        logger.info(f"Migration verification: {user_count} users, {session_count} sessions")
        return True
        
    except Exception as e:
        logger.error(f"Error verifying migration: {str(e)}")
        return False


def main():
    """Executar migração completa"""
    print("🔄 Iniciando migração do banco de dados SnapLinked v3.0...")
    
    try:
        # Importar app para configurar contexto
        from app import app
        
        with app.app_context():
            # 1. Criar backup
            print("📦 Criando backup do banco de dados...")
            backup_path = backup_database()
            if backup_path:
                print(f"✅ Backup criado: {backup_path}")
            
            # 2. Criar todas as tabelas
            print("🏗️ Criando estrutura de tabelas...")
            db.create_all()
            print("✅ Estrutura de tabelas criada")
            
            # 3. Migrar dados existentes
            print("📊 Migrando dados de usuários...")
            if migrate_user_data():
                print("✅ Dados de usuários migrados")
            else:
                print("❌ Erro na migração de usuários")
                return False
            
            print("🔄 Migrando dados de sessões...")
            if migrate_session_data():
                print("✅ Dados de sessões migrados")
            else:
                print("❌ Erro na migração de sessões")
                return False
            
            print("📝 Migrando dados de logs...")
            if migrate_log_data():
                print("✅ Dados de logs migrados")
            else:
                print("❌ Erro na migração de logs")
                return False
            
            # 4. Criar estatísticas
            print("📈 Criando estatísticas de usuários...")
            if create_user_stats():
                print("✅ Estatísticas criadas")
            else:
                print("❌ Erro na criação de estatísticas")
                return False
            
            # 5. Criar índices
            print("🔍 Criando índices de performance...")
            if create_indexes():
                print("✅ Índices criados")
            else:
                print("❌ Erro na criação de índices")
                return False
            
            # 6. Verificar migração
            print("🔍 Verificando migração...")
            if verify_migration():
                print("✅ Migração verificada com sucesso")
            else:
                print("❌ Erro na verificação da migração")
                return False
            
            print("\n🎉 Migração concluída com sucesso!")
            print("💾 Banco de dados otimizado e pronto para uso")
            return True
            
    except Exception as e:
        logger.error(f"Error in migration: {str(e)}")
        print(f"❌ Erro na migração: {str(e)}")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
