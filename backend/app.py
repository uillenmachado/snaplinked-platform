#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapLinked v3.0 - Aplicação Principal
Plataforma completa de automação LinkedIn com funcionalidades reais
"""

import asyncio
import os
import secrets
from datetime import datetime, timezone
from functools import wraps
from urllib.parse import parse_qs, urlparse

from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import config
from models import db, User, AutomationSession, AutomationLog, UserStats
from services.linkedin_service import oauth_service, automation_service


def create_app(config_name=None):
    """Factory para criar a aplicação Flask"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Criar tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app


# Criar aplicação
app = create_app()


def require_auth(f):
    """Decorator para rotas que requerem autenticação"""
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


def get_current_user():
    """Obter usuário atual da sessão ou token"""
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
    """Página inicial - Dashboard integrado"""
    return send_from_directory('static', 'index.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard principal"""
    return send_from_directory('static', 'index.html')


# ==================== API DE SAÚDE ====================

@app.route('/api/health')
def health_check():
    """Verificação de saúde da API"""
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
    """Status completo da aplicação"""
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
        'automation_running': False,  # TODO: implementar verificação de automação ativa
        'version': '3.0.0'
    })


# ==================== AUTENTICAÇÃO LINKEDIN ====================

@app.route('/api/auth/linkedin')
def linkedin_auth():
    """Iniciar autenticação OAuth do LinkedIn"""
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    auth_url = oauth_service.get_authorization_url(state)
    return jsonify({
        'auth_url': auth_url,
        'state': state
    })


@app.route('/auth/linkedin/callback')
def linkedin_callback():
    """Callback OAuth do LinkedIn"""
    try:
        # Verificar state para prevenir CSRF
        state = request.args.get('state')
        if state != session.get('oauth_state'):
            return jsonify({'error': 'Estado OAuth inválido'}), 400
        
        # Obter código de autorização
        code = request.args.get('code')
        if not code:
            error = request.args.get('error')
            return jsonify({'error': f'Erro OAuth: {error}'}), 400
        
        # Trocar código por token
        token_data = oauth_service.exchange_code_for_token(code)
        if not token_data:
            return jsonify({'error': 'Erro ao obter token de acesso'}), 400
        
        # Obter perfil do usuário
        profile_data = oauth_service.get_user_profile(token_data['access_token'])
        if not profile_data:
            return jsonify({'error': 'Erro ao obter perfil do usuário'}), 400
        
        # Criar ou atualizar usuário
        user = User.query.filter_by(linkedin_id=profile_data['id']).first()
        if not user:
            user = User.query.filter_by(email=profile_data['email']).first()
        
        if not user:
            user = User(
                email=profile_data['email'],
                name=f"{profile_data['first_name']} {profile_data['last_name']}",
                linkedin_id=profile_data['id']
            )
            db.session.add(user)
        else:
            user.name = f"{profile_data['first_name']} {profile_data['last_name']}"
            user.linkedin_id = profile_data['id']
        
        # Atualizar dados OAuth
        user.access_token = token_data['access_token']
        user.avatar_url = profile_data.get('profile_picture')
        user.updated_at = datetime.now(timezone.utc)
        
        db.session.commit()
        
        # Criar sessão
        session['user_id'] = user.id
        session.permanent = True
        
        # Redirecionar para dashboard com sucesso
        return redirect(f'/dashboard?auth=success&user={user.name}')
        
    except Exception as e:
        app.logger.error(f"Erro no callback OAuth: {str(e)}")
        return redirect('/dashboard?auth=error')


@app.route('/api/auth/manual-login', methods=['POST'])
def manual_login():
    """Iniciar login manual no LinkedIn"""
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
        
        # Iniciar navegador para login manual
        success = await automation_service.login_manual(user.id)
        if not success:
            return jsonify({
                'success': False,
                'message': 'Erro ao iniciar login manual'
            }), 500
        
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
        app.logger.error(f"Erro no login manual: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Fazer logout"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logout realizado com sucesso'
    })


# ==================== AUTOMAÇÃO ====================

@app.route('/api/automation/<action>', methods=['POST'])
@require_auth
def execute_automation(action):
    """Executar automação específica"""
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
                'message': 'Já existe uma automação em execução. Aguarde a conclusão.'
            }), 400
        
        # Executar automação baseada no tipo
        if action == 'like':
            result = await automation_service.like_posts(user.id, target_count or 3)
        elif action == 'connect':
            result = await automation_service.send_connection_requests(user.id, target_count or 2)
        elif action == 'comment':
            result = await automation_service.comment_on_posts(user.id, target_count or 1)
        
        # Obter estatísticas atualizadas
        stats = UserStats.query.filter_by(user_id=user.id).first()
        
        return jsonify({
            'success': result['success'],
            'message': f'Automação de {action} concluída',
            'details': {
                'completed_count': result['completed_count'],
                'error_count': result['error_count'],
                'errors': result['errors'][:5]  # Limitar erros retornados
            },
            'stats': stats.to_dict() if stats else None
        })
        
    except Exception as e:
        app.logger.error(f"Erro na automação {action}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Erro interno na automação: {str(e)}'
        }), 500


@app.route('/api/automation/sessions')
@require_auth
def get_automation_sessions():
    """Obter histórico de sessões de automação"""
    user = request.current_user
    
    sessions = AutomationSession.query.filter_by(user_id=user.id)\
        .order_by(AutomationSession.created_at.desc())\
        .limit(50).all()
    
    return jsonify({
        'sessions': [session.to_dict() for session in sessions]
    })


@app.route('/api/automation/logs')
@require_auth
def get_automation_logs():
    """Obter logs de automação"""
    user = request.current_user
    session_id = request.args.get('session_id', type=int)
    
    query = AutomationLog.query.filter_by(user_id=user.id)
    if session_id:
        query = query.filter_by(session_id=session_id)
    
    logs = query.order_by(AutomationLog.created_at.desc()).limit(100).all()
    
    return jsonify({
        'logs': [log.to_dict() for log in logs]
    })


# ==================== ESTATÍSTICAS ====================

@app.route('/api/stats/reset', methods=['POST'])
@require_auth
def reset_stats():
    """Resetar estatísticas do usuário"""
    user = request.current_user
    
    stats = UserStats.query.filter_by(user_id=user.id).first()
    if stats:
        stats.total_likes = 0
        stats.total_connections = 0
        stats.total_comments = 0
        stats.total_views = 0
        stats.updated_at = datetime.now(timezone.utc)
        db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Estatísticas resetadas com sucesso',
        'stats': stats.to_dict() if stats else None
    })


# ==================== ARQUIVOS ESTÁTICOS ====================

@app.route('/<path:filename>')
def serve_static(filename):
    """Servir arquivos estáticos"""
    return send_from_directory('static', filename)


# ==================== TRATAMENTO DE ERROS ====================

@app.errorhandler(404)
def not_found(error):
    """Página não encontrada"""
    return jsonify({
        'error': 'Endpoint não encontrado',
        'message': 'Verifique a URL e tente novamente'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Erro interno do servidor"""
    db.session.rollback()
    return jsonify({
        'error': 'Erro interno do servidor',
        'message': 'Tente novamente em alguns instantes'
    }), 500


@app.errorhandler(403)
def forbidden(error):
    """Acesso negado"""
    return jsonify({
        'error': 'Acesso negado',
        'message': 'Você não tem permissão para acessar este recurso'
    }), 403


# ==================== EXECUÇÃO ====================

if __name__ == '__main__':
    print("🚀 Iniciando SnapLinked v3.0...")
    print(f"📊 Dashboard: http://{app.config['HOST']}:{app.config['PORT']}")
    print(f"🔗 API Health: http://{app.config['HOST']}:{app.config['PORT']}/api/health")
    print(f"📋 API Status: http://{app.config['HOST']}:{app.config['PORT']}/api/status")
    print("✨ Automação real LinkedIn ativada!")
    print("🔐 OAuth LinkedIn configurado!")
    print("💾 Persistência de dados ativada!")
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG'],
        threaded=True
    )
