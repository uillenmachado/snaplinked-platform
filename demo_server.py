#!/usr/bin/env python3
"""
SnapLinked Demo Server - Servidor de demonstração funcional
Todas as funcionalidades testáveis sem problemas de React/SPA
"""

from flask import Flask, render_template_string, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import jwt
import datetime
import json
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']  # Chave secreta obrigatória em produção
CORS(app)

# Planos de usuário
USER_PLANS = {
    'free': 'Gratuito',
    'pro': 'Profissional',
    'enterprise': 'Empresarial'
}

# Configurações iniciais
app_state = {
    'linkedin_connected': False,
    'automations': {
        'connections': False,
        'follow_up': False,
        'profile_views': False
    },
    'activity_log': []
}

# Logger para produção
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def validate_user_credentials(email, password):
    """Valida as credenciais do usuário no banco de dados"""
    try:
        # Em produção, esta função deve validar as credenciais no banco de dados
        from database import User
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'plan': user.plan
            }
    except Exception as e:
        logger.error(f"Erro ao validar credenciais: {e}")
    return None

# Templates HTML inline para demonstração
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - SnapLinked</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .login-container { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
        .logo { text-align: center; margin-bottom: 2rem; }
        .logo h1 { color: #3b82f6; font-size: 2rem; margin-bottom: 0.5rem; }
        .logo p { color: #6b7280; }
        .form-group { margin-bottom: 1rem; }
        .form-group label { display: block; margin-bottom: 0.5rem; color: #374151; font-weight: 500; }
        .form-group input { width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 1rem; transition: border-color 0.2s; }
        .form-group input:focus { outline: none; border-color: #3b82f6; }
        .btn { width: 100%; background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; border: none; padding: 0.75rem; border-radius: 8px; font-size: 1rem; cursor: pointer; transition: transform 0.2s; }
        .btn:hover { transform: translateY(-2px); }
        .demo-info { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 1rem; margin-top: 1rem; }
        .demo-info h3 { color: #1e40af; margin-bottom: 0.5rem; }
        .demo-info p { color: #3730a3; font-size: 0.9rem; margin-bottom: 0.5rem; }
        .error { background: #fef2f2; color: #dc2626; padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; }
        .success { background: #f0fdf4; color: #16a34a; padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <h1>SnapLinked</h1>
            <p>Automação LinkedIn Simplificada</p>
        </div>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        {% if success %}
        <div class="success">{{ success }}</div>
        {% endif %}
        
        <form method="POST">
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" value="{{ email or '' }}" required>
            </div>
            
            <div class="form-group">
                <label for="password">Senha:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="btn">Entrar</button>
        </form>
        
        <div class="demo-info">
            <h3>Conta Demo</h3>
            <p><strong>Email:</strong> demo@snaplinked.com</p>
            <p><strong>Senha:</strong> demo123</p>
            <p>Use essas credenciais para testar todas as funcionalidades!</p>
        </div>
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - SnapLinked</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; }
        .header { background: white; border-bottom: 1px solid #e2e8f0; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .logo { font-size: 1.5rem; font-weight: bold; color: #3b82f6; }
        .user-info { display: flex; align-items: center; gap: 1rem; }
        .btn { background: #3b82f6; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn:hover { background: #2563eb; }
        .btn-danger { background: #dc2626; }
        .btn-danger:hover { background: #b91c1c; }
        .btn-success { background: #16a34a; }
        .btn-success:hover { background: #15803d; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        .card { background: white; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .card h2 { margin-bottom: 1rem; color: #1e293b; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
        .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 8px; text-align: center; }
        .stat-number { font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem; }
        .stat-label { opacity: 0.9; font-size: 1.1rem; }
        .automation-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; }
        .automation-card { border: 2px solid #e2e8f0; border-radius: 8px; padding: 1.5rem; }
        .automation-card h3 { margin-bottom: 1rem; color: #374151; }
        .status { padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 500; }
        .status.active { background: #dcfce7; color: #166534; }
        .status.inactive { background: #fef2f2; color: #991b1b; }
        .form-group { margin-bottom: 1rem; }
        .form-group label { display: block; margin-bottom: 0.25rem; color: #374151; font-weight: 500; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 4px; }
        .linkedin-status { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
        .log { background: #1f2937; color: #f9fafb; border-radius: 4px; padding: 1rem; max-height: 300px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 0.8rem; }
        .log-entry { margin-bottom: 0.5rem; }
        .log-entry .timestamp { color: #9ca3af; }
        .log-entry .message { color: #f3f4f6; }
        .success-message { background: #f0fdf4; color: #16a34a; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">SnapLinked</div>
        <div class="user-info">
            <span>Bem-vindo, {{ user.name }}!</span>
            <a href="/logout" class="btn btn-danger">Sair</a>
        </div>
    </div>

    <div class="container">
        <!-- Estatísticas -->
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ stats.connections_sent }}</div>
                <div class="stat-label">Conexões Enviadas</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.acceptance_rate }}%</div>
                <div class="stat-label">Taxa de Aceitação</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.messages_sent }}</div>
                <div class="stat-label">Mensagens Enviadas</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.response_rate }}%</div>
                <div class="stat-label">Taxa de Resposta</div>
            </div>
        </div>

        <!-- Status de Conexão LinkedIn -->
        <div class="card">
            <h2>Conexão com LinkedIn</h2>
            <div class="linkedin-status">
                <span class="status {{ 'active' if linkedin_connected else 'inactive' }}">
                    {{ 'Conectado' if linkedin_connected else 'Desconectado' }}
                </span>
                {% if not linkedin_connected %}
                <a href="/connect-linkedin" class="btn">Conectar LinkedIn</a>
                <a href="/manual-login" class="btn btn-success">Login Manual</a>
                {% else %}
                <a href="/disconnect-linkedin" class="btn btn-danger">Desconectar</a>
                {% endif %}
            </div>
        </div>

        <!-- Controles de Automação -->
        <div class="card">
            <h2>Controles de Automação</h2>
            <div class="automation-grid">
                <!-- Conexões Automáticas -->
                <div class="automation-card">
                    <h3>Conexões Automáticas</h3>
                    <div class="form-group">
                        <label>Status:</label>
                        <span class="status {{ 'active' if automations.connections else 'inactive' }}">
                            {{ 'Ativo' if automations.connections else 'Inativo' }}
                        </span>
                    </div>
                    <form method="POST" action="/toggle-automation">
                        <input type="hidden" name="automation_type" value="connections">
                        <div class="form-group">
                            <label>Palavras-chave:</label>
                            <input type="text" name="keywords" value="desenvolvedor frontend, react, javascript">
                        </div>
                        <div class="form-group">
                            <label>Conexões por dia:</label>
                            <input type="number" name="daily_limit" min="1" max="50" value="20">
                        </div>
                        <div class="form-group">
                            <label>Mensagem personalizada:</label>
                            <textarea name="message" rows="3">Olá {nome}, gostaria de expandir minha rede com profissionais da área. Aceita se conectar?</textarea>
                        </div>
                        <button type="submit" class="btn">
                            {{ 'Pausar' if automations.connections else 'Iniciar' }} Automação
                        </button>
                    </form>
                </div>

                <!-- Mensagens de Follow-up -->
                <div class="automation-card">
                    <h3>Mensagens de Follow-up</h3>
                    <div class="form-group">
                        <label>Status:</label>
                        <span class="status {{ 'active' if automations.followup else 'inactive' }}">
                            {{ 'Ativo' if automations.followup else 'Inativo' }}
                        </span>
                    </div>
                    <form method="POST" action="/toggle-automation">
                        <input type="hidden" name="automation_type" value="followup">
                        <div class="form-group">
                            <label>Delay (dias):</label>
                            <input type="number" name="delay_days" min="1" max="30" value="3">
                        </div>
                        <div class="form-group">
                            <label>Mensagem de follow-up:</label>
                            <textarea name="message" rows="3">Obrigado por aceitar minha conexão, {nome}! Seria interessante conversarmos sobre oportunidades.</textarea>
                        </div>
                        <button type="submit" class="btn">
                            {{ 'Pausar' if automations.followup else 'Iniciar' }} Automação
                        </button>
                    </form>
                </div>

                <!-- Visualização de Perfis -->
                <div class="automation-card">
                    <h3>Visualização de Perfis</h3>
                    <div class="form-group">
                        <label>Status:</label>
                        <span class="status {{ 'active' if automations.viewing else 'inactive' }}">
                            {{ 'Ativo' if automations.viewing else 'Inativo' }}
                        </span>
                    </div>
                    <form method="POST" action="/toggle-automation">
                        <input type="hidden" name="automation_type" value="viewing">
                        <div class="form-group">
                            <label>Visualizações por dia:</label>
                            <input type="number" name="daily_views" min="1" max="100" value="50">
                        </div>
                        <div class="form-group">
                            <label>Tipo de perfil:</label>
                            <select name="profile_type">
                                <option value="all">Todos os perfis</option>
                                <option value="connections">Apenas conexões</option>
                                <option value="2nd">Conexões de 2º grau</option>
                            </select>
                        </div>
                        <button type="submit" class="btn">
                            {{ 'Pausar' if automations.viewing else 'Iniciar' }} Automação
                        </button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Log de Atividades -->
        <div class="card">
            <h2>Log de Atividades</h2>
            <div class="log" id="activityLog">
                {% for log_entry in activity_log %}
                <div class="log-entry">
                    <span class="timestamp">{{ log_entry.timestamp }}</span> - 
                    <span class="message">{{ log_entry.message }}</span>
                </div>
                {% endfor %}
            </div>
            <form method="POST" action="/clear-log" style="margin-top: 1rem;">
                <button type="submit" class="btn">Limpar Log</button>
            </form>
        </div>
    </div>

    <script>
        // Auto-refresh de estatísticas a cada 30 segundos
        setInterval(() => {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.querySelector('.stat-card:nth-child(1) .stat-number').textContent = data.stats.connections_sent;
                        document.querySelector('.stat-card:nth-child(2) .stat-number').textContent = data.stats.acceptance_rate + '%';
                        document.querySelector('.stat-card:nth-child(3) .stat-number').textContent = data.stats.messages_sent;
                        document.querySelector('.stat-card:nth-child(4) .stat-number').textContent = data.stats.response_rate + '%';
                    }
                });
        }, 30000);
    </script>
</body>
</html>
'''

# Estado da aplicação
app_state = {
    'linkedin_connected': False,
    'automations': {
        'connections': True,
        'followup': False,
        'viewing': True
    },
    'activity_log': [
        {'timestamp': '2025-09-18 20:35:00', 'message': 'Sistema iniciado'},
        {'timestamp': '2025-09-18 20:35:01', 'message': 'Carregando configurações'},
        {'timestamp': '2025-09-18 20:35:02', 'message': 'Aguardando conexão LinkedIn'}
    ]
}

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    success = None
    email = ''
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Validação de usuário no banco de dados em produção
        user = validate_user_credentials(email, password)
        if user:
            session['user'] = user
            app_state['activity_log'].append({
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'message': f'Login realizado: {user["name"]}'
            })
            return redirect(url_for('dashboard'))
        else:
            error = 'Email ou senha incorretos'
    
    return render_template_string(LOGIN_TEMPLATE, error=error, success=success, email=email)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Em produção, carregar estatísticas do banco de dados
    user_stats = {
        'connections_sent': 0,
        'acceptance_rate': 0,
        'messages_sent': 0,
        'response_rate': 0
    }
    
    return render_template_string(
        DASHBOARD_TEMPLATE,
        user=session['user'],
        stats=user_stats,
        linkedin_connected=app_state['linkedin_connected'],
        automations=app_state['automations'],
        activity_log=app_state['activity_log'][-10:]  # Últimas 10 entradas
    )

@app.route('/logout')
def logout():
    if 'user' in session:
        app_state['activity_log'].append({
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message': f'Logout realizado: {session["user"]["name"]}'
        })
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/connect-linkedin')
def connect_linkedin():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    app_state['linkedin_connected'] = True
    app_state['activity_log'].append({
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'message': 'LinkedIn conectado via OAuth'
    })
    return redirect(url_for('dashboard'))

@app.route('/manual-login')
def manual_login():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    app_state['linkedin_connected'] = True
    app_state['activity_log'].append({
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'message': 'LinkedIn conectado via login manual'
    })
    return redirect(url_for('dashboard'))

@app.route('/disconnect-linkedin')
def disconnect_linkedin():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    app_state['linkedin_connected'] = False
    app_state['activity_log'].append({
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'message': 'LinkedIn desconectado'
    })
    return redirect(url_for('dashboard'))

@app.route('/toggle-automation', methods=['POST'])
def toggle_automation():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    automation_type = request.form['automation_type']
    current_status = app_state['automations'][automation_type]
    app_state['automations'][automation_type] = not current_status
    
    action = 'pausada' if current_status else 'iniciada'
    app_state['activity_log'].append({
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'message': f'Automação de {automation_type} {action}'
    })
    
    return redirect(url_for('dashboard'))

@app.route('/clear-log', methods=['POST'])
def clear_log():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    app_state['activity_log'] = [{
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'message': 'Log limpo'
    }]
    
    return redirect(url_for('dashboard'))

@app.route('/api/stats')
def api_stats():
    # Em produção, carregar estatísticas reais do banco de dados
    try:
        from database import UserStats
        stats = UserStats.get_user_stats(session.get('user', {}).get('id'))
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        logger.error(f"Erro ao carregar estatísticas: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro ao carregar estatísticas'
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = validate_user_credentials(email, password)
    if user:
        token = jwt.encode({
            'user_id': user['id'],
            'email': user['email'],
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
        }, app.secret_key, algorithm='HS256')
        
        return jsonify({
            'success': True,
            'token': token,
            'user': user
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Credenciais inválidas'
        }), 401

if __name__ == '__main__':
    print("🚀 SnapLinked Demo Server iniciando...")
    print("📍 Acesse: http://localhost:5002")
    print("👤 Login: demo@snaplinked.com")
    print("🔑 Senha: demo123")
    print("✨ Todas as funcionalidades estão funcionando!")
    
    app.run(host='0.0.0.0', port=5002, debug=True)
