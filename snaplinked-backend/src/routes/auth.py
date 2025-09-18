"""
Rotas de autenticação da aplicação SnapLinked
"""

from flask import Blueprint, request, jsonify, session, redirect
from datetime import datetime
import logging
import requests
import urllib.parse
import base64
import hashlib
import time

from ..config.settings import Config

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint de login demo"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email e senha são obrigatórios'
            }), 400
        
        # Validação demo - aceita qualquer credencial válida
        if email and password:
            return jsonify({
                'success': True,
                'message': 'Login realizado com sucesso',
                'user': {
                    'id': 1,
                    'email': email,
                    'first_name': 'Demo',
                    'last_name': 'User',
                    'company': 'SnapLinked',
                    'subscription_plan': 'premium'
                },
                'tokens': {
                    'access_token': 'demo_token_snaplinked_2024',
                    'refresh_token': 'demo_refresh_snaplinked_2024'
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Credenciais inválidas'
            }), 401
            
    except Exception as e:
        logger.error(f"Erro no login: {e}")
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint de registro demo"""
    try:
        data = request.get_json()
        
        # Validação básica
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Campo {field} é obrigatório'
                }), 400
        
        # Registro demo
        return jsonify({
            'success': True,
            'message': 'Registro realizado com sucesso',
            'user': {
                'id': 2,
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'company': data.get('company', ''),
                'subscription_plan': 'free'
            },
            'tokens': {
                'access_token': 'demo_token_snaplinked_2024',
                'refresh_token': 'demo_refresh_snaplinked_2024'
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Erro no registro: {e}")
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Endpoint de logout"""
    try:
        # Limpar sessão
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Logout realizado com sucesso'
        }), 200
        
    except Exception as e:
        logger.error(f"Erro no logout: {e}")
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Obtém dados do usuário atual"""
    try:
        # Verificar token (demo)
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'message': 'Token de acesso necessário'
            }), 401
        
        return jsonify({
            'success': True,
            'user': {
                'id': 1,
                'email': 'demo@snaplinked.com',
                'first_name': 'Demo',
                'last_name': 'User',
                'company': 'SnapLinked',
                'subscription_plan': 'premium'
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter usuário: {e}")
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500

@auth_bp.route('/linkedin/connect', methods=['GET'])
def initiate_linkedin_auth():
    """Inicia autenticação OAuth 2.0 com LinkedIn"""
    try:
        if not Config.LINKEDIN_CLIENT_ID or not Config.LINKEDIN_CLIENT_SECRET:
            return jsonify({
                'success': False,
                'error': 'Credenciais LinkedIn não configuradas'
            }), 500
        
        # Generate state for CSRF protection
        state = base64.urlsafe_b64encode(
            hashlib.sha256(str(time.time()).encode()).digest()
        ).decode()[:32]
        
        session['linkedin_oauth_state'] = state
        session['user_id'] = 1
        
        # LinkedIn OAuth parameters
        scopes = ['openid', 'profile', 'email']
        
        params = {
            'response_type': 'code',
            'client_id': Config.LINKEDIN_CLIENT_ID,
            'redirect_uri': Config.LINKEDIN_REDIRECT_URI,
            'state': state,
            'scope': ' '.join(scopes)
        }
        
        auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urllib.parse.urlencode(params)}"
        
        logger.info("Iniciando autenticação LinkedIn OAuth")
        
        return jsonify({
            'success': True,
            'auth_url': auth_url,
            'state': state,
            'message': 'Redirecionando para LinkedIn...'
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar autenticação: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@auth_bp.route('/linkedin/callback', methods=['GET'])
def linkedin_callback():
    """Callback OAuth 2.0 do LinkedIn"""
    try:
        authorization_code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if error:
            logger.error(f"Erro na autorização: {error}")
            return redirect(f"{Config.CORS_ORIGINS[0]}/linkedin-accounts?error={error}")
        
        if not authorization_code:
            return redirect(f"{Config.CORS_ORIGINS[0]}/linkedin-accounts?error=no_code")
        
        # Verificar state
        session_state = session.get('linkedin_oauth_state')
        if not session_state or session_state != state:
            return redirect(f"{Config.CORS_ORIGINS[0]}/linkedin-accounts?error=invalid_state")
        
        # Trocar código por token
        token_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': Config.LINKEDIN_REDIRECT_URI,
            'client_id': Config.LINKEDIN_CLIENT_ID,
            'client_secret': Config.LINKEDIN_CLIENT_SECRET
        }
        
        token_response = requests.post(
            'https://www.linkedin.com/oauth/v2/accessToken',
            data=token_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if token_response.status_code != 200:
            logger.error(f"Erro ao obter token: {token_response.text}")
            return redirect(f"{Config.CORS_ORIGINS[0]}/linkedin-accounts?error=token_error")
        
        token_info = token_response.json()
        access_token = token_info.get('access_token')
        
        # Buscar informações básicas do usuário
        profile_headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Buscar perfil básico
        profile_response = requests.get(
            'https://api.linkedin.com/v2/people/~',
            headers=profile_headers
        )
        
        user_info = {}
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            user_info = {
                'id': profile_data.get('id'),
                'firstName': profile_data.get('localizedFirstName', ''),
                'lastName': profile_data.get('localizedLastName', ''),
            }
            
            # Buscar email
            email_response = requests.get(
                'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))',
                headers=profile_headers
            )
            
            if email_response.status_code == 200:
                email_data = email_response.json()
                elements = email_data.get('elements', [])
                if elements:
                    user_info['email'] = elements[0].get('handle~', {}).get('emailAddress')
        
        # Salvar na sessão
        session['linkedin_oauth_connected'] = True
        session['linkedin_oauth_user'] = user_info
        session['linkedin_oauth_token'] = access_token
        session.pop('linkedin_oauth_state', None)
        
        logger.info(f"LinkedIn OAuth conectado: {user_info.get('firstName', '')} {user_info.get('lastName', '')}")
        
        return redirect(f"{Config.CORS_ORIGINS[0]}/linkedin-accounts?success=oauth_connected")
        
    except Exception as e:
        logger.error(f"Erro no callback: {e}")
        return redirect(f"{Config.CORS_ORIGINS[0]}/linkedin-accounts?error=callback_error")
