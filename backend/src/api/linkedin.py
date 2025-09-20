"""
Rotas relacionadas ao LinkedIn da aplicação SnapLinked
"""

from flask import Blueprint, request, jsonify, session, redirect, url_for
from datetime import datetime
import logging
import asyncio
import requests
import os
from urllib.parse import urlencode

# Import correto do engine de automação
from linkedin_automation_engine import automation_engine

logger = logging.getLogger(__name__)

linkedin_bp = Blueprint('linkedin', __name__, url_prefix='/api/linkedin')

# Configurações OAuth LinkedIn
LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID', '77jmwin70p0gge')
LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET', 'ZGeGVXoeopPADn4v')
LINKEDIN_REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:3000/auth/linkedin/callback')

@linkedin_bp.route('/oauth/url', methods=['GET'])
def get_oauth_url():
    """Gera URL de autorização OAuth do LinkedIn"""
    try:
        params = {
            'response_type': 'code',
            'client_id': LINKEDIN_CLIENT_ID,
            'redirect_uri': LINKEDIN_REDIRECT_URI,
            'scope': 'openid profile email',
            'state': 'random_state_string'  # Em produção, usar estado aleatório seguro
        }
        
        auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"
        
        return jsonify({
            'success': True,
            'auth_url': auth_url
        })
        
    except Exception as e:
        logger.error(f"Erro ao gerar URL OAuth: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@linkedin_bp.route('/oauth/callback', methods=['POST'])
def oauth_callback():
    """Processa callback OAuth do LinkedIn"""
    try:
        data = request.get_json()
        code = data.get('code')
        state = data.get('state')
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'Código de autorização não recebido'
            }), 400
        
        # Trocar código por token de acesso
        token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': LINKEDIN_REDIRECT_URI,
            'client_id': LINKEDIN_CLIENT_ID,
            'client_secret': LINKEDIN_CLIENT_SECRET
        }
        
        token_response = requests.post(token_url, data=token_data)
        
        if token_response.status_code != 200:
            logger.error(f"Erro ao obter token: {token_response.text}")
            return jsonify({
                'success': False,
                'error': 'Erro ao obter token de acesso'
            }), 400
        
        token_info = token_response.json()
        access_token = token_info.get('access_token')
        
        # Obter dados do perfil
        profile_url = 'https://api.linkedin.com/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        
        profile_response = requests.get(profile_url, headers=headers)
        
        if profile_response.status_code != 200:
            logger.error(f"Erro ao obter perfil: {profile_response.text}")
            return jsonify({
                'success': False,
                'error': 'Erro ao obter dados do perfil'
            }), 400
        
        profile_data = profile_response.json()
        
        # Salvar dados na sessão
        session['linkedin_oauth_connected'] = True
        session['linkedin_oauth_user'] = {
            'name': profile_data.get('name', ''),
            'email': profile_data.get('email', ''),
            'picture': profile_data.get('picture', ''),
            'connectionType': 'oauth',
            'automationEnabled': False,
            'lastSync': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'success': True,
            'message': 'Conexão OAuth realizada com sucesso',
            'profile': session['linkedin_oauth_user']
        })
        
    except Exception as e:
        logger.error(f"Erro no callback OAuth: {e}")
        return jsonify({
            'success': False,
            'error': f'Erro no callback OAuth: {str(e)}'
        }), 500

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
        
        logger.info(f"Tentando login manual para: {email}")
        
        # Executar login assíncrono de forma mais robusta
        try:
            # Verificar se já existe um loop rodando
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Se já há um loop rodando, criar uma nova thread
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, automation_engine.login_with_credentials(email, password))
                        result = future.result(timeout=60)  # 60 segundos timeout
                else:
                    result = loop.run_until_complete(automation_engine.login_with_credentials(email, password))
            except RuntimeError:
                # Não há loop, criar um novo
                result = asyncio.run(automation_engine.login_with_credentials(email, password))
            
            logger.info(f"Resultado do login: {result}")
            
            if result.get('success'):
                # Salvar na sessão
                session['linkedin_manual_connected'] = True
                session['linkedin_manual_user'] = result.get('profile', {})
                session['linkedin_credentials'] = {'email': email}  # Não salvar senha
                
                return jsonify({
                    'success': True,
                    'message': 'Login manual realizado com sucesso',
                    'profile': result.get('profile', {}),
                    'connection_type': 'manual'
                })
            else:
                error_msg = result.get('message', 'Erro desconhecido no login')
                logger.error(f"Login falhou: {error_msg}")
                return jsonify({
                    'success': False,
                    'error': error_msg
                }), 400
                
        except Exception as login_error:
            logger.error(f"Erro específico no login: {login_error}")
            return jsonify({
                'success': False,
                'error': f'Erro no processo de login: {str(login_error)}'
            }), 500
            
    except Exception as e:
        logger.error(f"Erro geral no login manual: {e}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
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
