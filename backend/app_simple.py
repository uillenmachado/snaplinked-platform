#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapLinked v3.0 - Aplicação Simplificada
Versão sem middleware complexo para testes e migração
"""

import os
from datetime import datetime, timezone
from functools import wraps
from typing import Dict, Any, Optional

from flask import Flask, request, jsonify, send_from_directory, session, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import config
from models import db, User, AutomationSession, AutomationLog, UserStats


def create_app(config_name: Optional[str] = None) -> Flask:
    """Factory para criar a aplicação Flask simplificada."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(config[config_name])
    
    # Inicializar extensões básicas
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Criar tabelas do banco de dados
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")
    
    return app


# Criar aplicação
app = create_app()


def require_auth(f):
    """Decorator para rotas que requerem autenticação."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token de autenticação necessário'}), 401
        
        token = auth_header.split(' ')[1]
        user = User.verify_auth_token(token)
        if not user:
            return jsonify({'error': 'Token inválido ou expirado'}), 401
        
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function


def get_current_user() -> Optional[User]:
    """Obter usuário atual da sessão ou token JWT."""
    # Tentar obter do token JWT
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        user = User.verify_auth_token(token)
        if user:
            return user
    
    # Tentar obter da sessão
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    
    return None


# ==================== ROTAS PRINCIPAIS ====================

@app.route('/')
def index():
    """Página inicial - Dashboard integrado."""
    return send_from_directory('static', 'index.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard principal."""
    return send_from_directory('static', 'index.html')


# ==================== API DE SAÚDE ====================

@app.route('/api/health')
def health_check():
    """Verificação de saúde da API."""
    return jsonify({
        'status': 'ok',
        'message': 'SnapLinked v3.0 funcionando perfeitamente',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'version': '3.0.0',
        'features': {
            'oauth_linkedin': bool(app.config.get('LINKEDIN_CLIENT_ID')),
            'automation': True,
            'database': True
        }
    })


@app.route('/api/status')
def get_status():
    """Status completo da aplicação."""
    user = get_current_user()
    if not user:
        return jsonify({
            'authenticated': False,
            'version': '3.0.0'
        })
    
    # Obter estatísticas do usuário
    stats = UserStats.query.filter_by(user_id=user.id).first()
    if not stats:
        stats = UserStats(user_id=user.id)
        db.session.add(stats)
        db.session.commit()
    
    return jsonify({
        'authenticated': True,
        'user': user.to_dict(),
        'stats': stats.to_dict(),
        'automation_running': False,
        'version': '3.0.0'
    })


# ==================== AUTENTICAÇÃO ====================

@app.route('/api/auth/manual-login', methods=['POST'])
def manual_login():
    """Iniciar login manual no LinkedIn."""
    try:
        data = request.get_json() or {}
        email = data.get('email')
        name = data.get('name', 'Usuário SnapLinked')
        
        if not email:
            return jsonify({'error': 'Email é obrigatório'}), 400
        
        # Criar ou obter usuário
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, name=name)
            db.session.add(user)
            db.session.commit()
        
        # Criar sessão
        session['user_id'] = user.id
        session.permanent = True
        
        return jsonify({
            'success': True,
            'message': 'Login manual iniciado com sucesso',
            'user': user.to_dict(),
            'auth_token': user.generate_auth_token()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Fazer logout."""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logout realizado com sucesso'
    })


# ==================== AUTOMAÇÃO ====================

@app.route('/api/automation/<action>', methods=['POST'])
@require_auth
def execute_automation(action: str):
    """Executar automação específica."""
    user = request.current_user
    
    try:
        data = request.get_json() or {}
        target_count = data.get('target_count', 1)
        
        # Validar ação
        valid_actions = ['like', 'connect', 'comment']
        if action not in valid_actions:
            return jsonify({
                'success': False,
                'message': f'Ação "{action}" não é válida. Ações disponíveis: {valid_actions}'
            }), 400
        
        # Verificar se há automação em execução
        running_session = AutomationSession.query.filter_by(
            user_id=user.id,
            status='running'
        ).first()
        
        if running_session:
            return jsonify({
                'success': False,
                'message': 'Já existe uma automação em execução'
            }), 409
        
        # Simular execução de automação
        result = {
            'success': True,
            'count': min(target_count, 3),
            'target': target_count,
            'message': f'Automação de {action} executada com sucesso'
        }
        
        # Criar sessão de automação
        session_obj = AutomationSession(
            user_id=user.id,
            action_type=action,
            target_count=target_count,
            actual_count=result['count'],
            status='completed'
        )
        
        db.session.add(session_obj)
        db.session.commit()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro na automação: {str(e)}'
        }), 500


# ==================== TRATAMENTO DE ERROS ====================

@app.errorhandler(404)
def not_found(error):
    """Tratamento de erro 404."""
    return jsonify({'error': 'Endpoint não encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Tratamento de erro 500."""
    db.session.rollback()
    return jsonify({'error': 'Erro interno do servidor'}), 500


# ==================== INICIALIZAÇÃO ====================

if __name__ == '__main__':
    """Executar aplicação em modo de desenvolvimento."""
    print("🚀 Iniciando SnapLinked v3.0 (Versão Simplificada)...")
    
    # Configurações de desenvolvimento
    host = app.config.get('HOST', '127.0.0.1')
    port = app.config.get('PORT', 5001)
    debug = app.config.get('DEBUG', False)
    
    print(f"📊 Dashboard: http://{host}:{port}")
    print(f"🔗 API Health: http://{host}:{port}/api/health")
    print(f"📋 API Status: http://{host}:{port}/api/status")
    print(f"✨ Automação básica ativada!")
    print(f"💾 Persistência de dados ativada!")
    
    app.run(host=host, port=port, debug=debug)
