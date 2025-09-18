"""
SnapLinked Backend - Aplicação Principal Refatorada
Sistema modular de automação LinkedIn com arquitetura limpa
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import logging
from datetime import datetime

from config import config
from routes import auth_bp, linkedin_bp, automations_bp, analytics_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__, static_folder='static', static_url_path='')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'snaplinked-secret-key-2024')
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Enable CORS
CORS(app, origins=['*'])

# LinkedIn OAuth Configuration
LINKEDIN_CLIENT_ID = "77jmwin70p0gqe"
LINKEDIN_CLIENT_SECRET = "ZGeGVXoeopPADn4v"
LINKEDIN_REDIRECT_URI = "https://3dhkilc8y185.manus.space/api/auth/linkedin/callback"

# Serve static files (frontend)
@app.route('/')
def serve_frontend():
    """Serve the React frontend"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serve static files or fallback to index.html for SPA routing"""
    try:
        return send_from_directory(app.static_folder, path)
    except:
        return send_from_directory(app.static_folder, 'index.html')

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SnapLinked API',
        'version': '4.0.0',
        'features': {
            'linkedin_oauth': True,
            'automation_engine': True,
            'manual_login': True,
            'real_automation': True
        },
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Demo login endpoint"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
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

# LinkedIn OAuth 2.0 Routes
@app.route('/api/auth/linkedin/connect', methods=['GET'])
def initiate_linkedin_auth():
    """Inicia autenticação OAuth 2.0 com LinkedIn"""
    try:
        import urllib.parse
        import base64
        import hashlib
        import time
        
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
            'client_id': LINKEDIN_CLIENT_ID,
            'redirect_uri': LINKEDIN_REDIRECT_URI,
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

@app.route('/api/auth/linkedin/callback', methods=['GET'])
def linkedin_callback():
    """Callback OAuth 2.0 do LinkedIn"""
    try:
        authorization_code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if error:
            logger.error(f"Erro na autorização: {error}")
            return redirect(f"https://3dhkilc8y185.manus.space/linkedin-accounts?error={error}")
        
        if not authorization_code:
            return redirect("https://3dhkilc8y185.manus.space/linkedin-accounts?error=no_code")
        
        # Verificar state
        session_state = session.get('linkedin_oauth_state')
        if not session_state or session_state != state:
            return redirect("https://3dhkilc8y185.manus.space/linkedin-accounts?error=invalid_state")
        
        # Trocar código por token
        token_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': LINKEDIN_REDIRECT_URI,
            'client_id': LINKEDIN_CLIENT_ID,
            'client_secret': LINKEDIN_CLIENT_SECRET
        }
        
        token_response = requests.post(
            'https://www.linkedin.com/oauth/v2/accessToken',
            data=token_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if token_response.status_code != 200:
            logger.error(f"Erro ao obter token: {token_response.text}")
            return redirect("https://3dhkilc8y185.manus.space/linkedin-accounts?error=token_error")
        
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
        
        return redirect("https://3dhkilc8y185.manus.space/linkedin-accounts?success=oauth_connected")
        
    except Exception as e:
        logger.error(f"Erro no callback: {e}")
        return redirect("https://3dhkilc8y185.manus.space/linkedin-accounts?error=callback_error")

# LinkedIn Manual Login Routes
@app.route('/api/linkedin/manual-login', methods=['POST'])
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

@app.route('/api/linkedin/profile', methods=['GET'])
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

@app.route('/api/linkedin/disconnect', methods=['POST'])
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

# Automation Routes
@app.route('/api/automations/run', methods=['POST'])
def run_automation():
    """Executa automação LinkedIn"""
    try:
        if not session.get('linkedin_manual_connected'):
            return jsonify({
                'success': False,
                'error': 'Login manual necessário para automações'
            }), 400
        
        data = request.get_json()
        automation_config = {
            'type': data.get('type', 'connection_requests'),
            'keywords': data.get('keywords', ''),
            'max_actions': data.get('max_actions', 25),
            'message': data.get('message', '')
        }
        
        # Executar automação
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(automation_engine.run_automation(automation_config))
            return jsonify(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Erro na automação: {e}")
        return jsonify({
            'success': False,
            'error': f'Erro na automação: {str(e)}'
        }), 500

@app.route('/api/automations/stats', methods=['GET'])
def get_automation_stats():
    """Obtém estatísticas de automação"""
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

# API endpoints para dados simulados (frontend)
@app.route('/api/automations', methods=['GET'])
def get_automations():
    """Automações configuradas"""
    return jsonify({
        'success': True,
        'automations': [
            {
                'id': 1,
                'name': 'Conexões Tech',
                'type': 'connection_requests',
                'status': 'active',
                'keywords': 'desenvolvedor, programador, tech',
                'daily_limit': 50,
                'used_today': 23,
                'success_rate': 78.5,
                'automation_type': 'real_browser',
                'created_at': '2024-01-15',
                'last_run': '2024-01-20 15:30'
            },
            {
                'id': 2,
                'name': 'Mensagens Follow-up',
                'type': 'messages',
                'status': 'paused',
                'keywords': 'CEO, founder, startup',
                'daily_limit': 25,
                'used_today': 0,
                'success_rate': 82.1,
                'automation_type': 'real_browser',
                'created_at': '2024-01-10',
                'last_run': '2024-01-19 14:20'
            }
        ]
    })

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Analytics de automações"""
    return jsonify({
        'success': True,
        'analytics': {
            'connections_sent': 156,
            'connections_accepted': 122,
            'messages_sent': 89,
            'messages_replied': 37,
            'profile_views': 342,
            'success_rate': 78.5,
            'automation_method': 'Real Browser Automation',
            'daily_stats': [
                {'date': '2024-01-15', 'connections': 12, 'messages': 8},
                {'date': '2024-01-16', 'connections': 15, 'messages': 10},
                {'date': '2024-01-17', 'connections': 18, 'messages': 12},
                {'date': '2024-01-18', 'connections': 14, 'messages': 9},
                {'date': '2024-01-19', 'connections': 16, 'messages': 11},
                {'date': '2024-01-20', 'connections': 13, 'messages': 7}
            ]
        }
    })

@app.route('/api/payments/plans', methods=['GET'])
def get_payment_plans():
    """Planos de assinatura"""
    plans = [
        {
            'id': 'starter',
            'name': 'Starter',
            'price': 29,
            'currency': 'BRL',
            'interval': 'month',
            'features': [
                'Automação real integrada',
                '100 conexões/dia',
                '50 mensagens/dia',
                'Suporte por email'
            ]
        },
        {
            'id': 'professional',
            'name': 'Professional',
            'price': 79,
            'currency': 'BRL',
            'interval': 'month',
            'features': [
                'Automação avançada',
                '300 conexões/dia',
                '150 mensagens/dia',
                'Múltiplas contas LinkedIn',
                'Suporte prioritário'
            ],
            'popular': True
        },
        {
            'id': 'enterprise',
            'name': 'Enterprise',
            'price': 199,
            'currency': 'BRL',
            'interval': 'month',
            'features': [
                'Automação ilimitada',
                '1000 conexões/dia',
                '500 mensagens/dia',
                'API personalizada',
                'Suporte dedicado',
                'Treinamento personalizado'
            ]
        }
    ]
    
    return jsonify({
        'success': True,
        'plans': plans
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 by serving frontend"""
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'message': 'Erro interno do servidor'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
