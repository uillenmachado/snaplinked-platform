"""
Rotas relacionadas ao LinkedIn da aplicação SnapLinked
"""

from flask import Blueprint, request, jsonify, session
from datetime import datetime
import logging
import asyncio

from ..services.linkedin_automation import automation_engine

logger = logging.getLogger(__name__)

linkedin_bp = Blueprint('linkedin', __name__, url_prefix='/api/linkedin')

@linkedin_bp.route('/manual-login', methods=['POST'])
def manual_linkedin_login():
    """Login manual no LinkedIn para automações"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email e senha são obrigatórios'
            }), 400
        
        # Executar login assíncrono
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(automation_engine.login_with_credentials(email, password))
            
            if result['success']:
                # Salvar na sessão
                session['linkedin_manual_connected'] = True
                session['linkedin_manual_user'] = result['profile']
                session['linkedin_credentials'] = {'email': email}  # Não salvar senha
                
                return jsonify({
                    'success': True,
                    'message': 'Login manual realizado com sucesso',
                    'profile': result['profile'],
                    'connection_type': 'manual'
                })
            else:
                return jsonify(result), 400
                
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Erro no login manual: {e}")
        return jsonify({
            'success': False,
            'error': f'Erro no login: {str(e)}'
        }), 500

@linkedin_bp.route('/profile', methods=['GET'])
def get_linkedin_profile():
    """Obtém perfil LinkedIn conectado (OAuth ou Manual)"""
    try:
        # Verificar conexão OAuth
        if session.get('linkedin_oauth_connected'):
            user_info = session.get('linkedin_oauth_user', {})
            return jsonify({
                'success': True,
                'profile': {
                    'id': user_info.get('id'),
                    'firstName': user_info.get('firstName'),
                    'lastName': user_info.get('lastName'),
                    'email': user_info.get('email'),
                    'connectionStatus': 'oauth_connected',
                    'connectionType': 'oauth',
                    'lastSync': datetime.utcnow().isoformat(),
                    'automationEnabled': False
                }
            })
        
        # Verificar conexão manual
        elif session.get('linkedin_manual_connected'):
            user_info = session.get('linkedin_manual_user', {})
            return jsonify({
                'success': True,
                'profile': {
                    'name': user_info.get('name', 'Usuário LinkedIn'),
                    'headline': user_info.get('headline', ''),
                    'connectionStatus': 'manual_connected',
                    'connectionType': 'manual',
                    'lastSync': user_info.get('logged_in_at'),
                    'automationEnabled': True
                }
            })
        
        else:
            return jsonify({
                'success': False,
                'error': 'Nenhuma conta LinkedIn conectada'
            }), 400
            
    except Exception as e:
        logger.error(f"Erro ao buscar perfil: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@linkedin_bp.route('/disconnect', methods=['POST'])
def disconnect_linkedin():
    """Desconecta conta LinkedIn"""
    try:
        # Limpar sessões OAuth
        session.pop('linkedin_oauth_connected', None)
        session.pop('linkedin_oauth_user', None)
        session.pop('linkedin_oauth_token', None)
        
        # Limpar sessões manuais
        session.pop('linkedin_manual_connected', None)
        session.pop('linkedin_manual_user', None)
        session.pop('linkedin_credentials', None)
        
        # Fechar navegador se estiver aberto
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(automation_engine.close())
        finally:
            loop.close()
        
        return jsonify({
            'success': True,
            'message': 'Conta LinkedIn desconectada'
        })
        
    except Exception as e:
        logger.error(f"Erro ao desconectar: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno'
        }), 500

@linkedin_bp.route('/stats', methods=['GET'])
def get_linkedin_stats():
    """Obtém estatísticas do LinkedIn"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(automation_engine.get_stats())
            return jsonify(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Erro ao buscar stats: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno'
        }), 500
