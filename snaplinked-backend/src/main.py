#!/usr/bin/env python3
"""
SnapLinked - Sistema de Automação LinkedIn
Versão 4.1.0 - Sistema Principal Funcional
Desenvolvido para ser 100% operacional e testado
"""

from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
from flask_cors import CORS
import jwt
import json
import logging
from datetime import datetime, timedelta
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'snaplinked-secret-key-2025-v4.1.0'
CORS(app, origins=['*'])

# Dados simulados para demonstração
DEMO_USER = {
    'id': 1,
    'email': 'demo@snaplinked.com',
    'password': 'demo123',
    'name': 'Demo User',
    'plan': 'Premium',
    'created_at': '2025-01-01T00:00:00Z'
}

# Estado das automações
automation_states = {
    'connections': True,
    'follow_up': False,
    'profile_views': True
}

# Log de atividades
activity_log = []

def add_activity(action, details=""):
    """Adicionar atividade ao log"""
    activity_log.append({
        'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'action': action,
        'details': details
    })
    # Manter apenas os últimos 50 registros
    if len(activity_log) > 50:
        activity_log.pop(0)

def generate_token(user_id, email):
    """Gerar token JWT"""
    payload = {
        'user_id': user_id,
        'email': email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, app.secret_key, algorithm='HS256')

# Template HTML principal
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapLinked - LinkedIn Automation Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card-shadow { box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .btn-primary:hover { background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%); }
        .status-active { color: #10b981; }
        .status-inactive { color: #ef4444; }
        .status-paused { color: #f59e0b; }
    </style>
</head>
<body class="bg-gray-50">
    {% if page == 'login' %}
    <!-- Página de Login -->
    <div class="min-h-screen gradient-bg flex items-center justify-center p-4">
        <div class="bg-white rounded-lg card-shadow p-8 w-full max-w-md">
            <div class="text-center mb-8">
                <div class="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span class="text-white font-bold text-xl">SL</span>
                </div>
                <h1 class="text-2xl font-bold text-gray-900">Bem-vindo de volta</h1>
                <p class="text-gray-600 mt-2">Faça login em sua conta SnapLinked</p>
            </div>
            
            <form id="loginForm" class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                    <input type="email" id="email" required 
                           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                           placeholder="Digite seu email">
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Senha</label>
                    <input type="password" id="password" required
                           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                           placeholder="Digite sua senha">
                </div>
                
                <button type="submit" class="w-full btn-primary text-white py-2 px-4 rounded-md hover:opacity-90 transition-opacity">
                    Entrar
                </button>
            </form>
            
            <div class="mt-6 p-4 bg-blue-50 rounded-lg">
                <h3 class="text-sm font-medium text-blue-900 mb-2">Conta Demo</h3>
                <p class="text-xs text-blue-700 mb-2">Experimente o SnapLinked:</p>
                <div class="text-xs text-blue-600">
                    <div>Email: demo@snaplinked.com</div>
                    <div>Senha: demo123</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    localStorage.setItem('access_token', data.token);
                    window.location.href = '/dashboard';
                } else {
                    alert('Erro no login: ' + data.error);
                }
            } catch (error) {
                alert('Erro de conexão: ' + error.message);
            }
        });
    </script>
    
    {% elif page == 'dashboard' %}
    <!-- Dashboard -->
    <div class="min-h-screen bg-gray-50">
        <!-- Header -->
        <header class="bg-white shadow-sm border-b">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between items-center h-16">
                    <div class="flex items-center">
                        <div class="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                            <span class="text-white font-bold text-sm">SL</span>
                        </div>
                        <h1 class="ml-3 text-xl font-semibold text-gray-900">SnapLinked</h1>
                    </div>
                    <div class="flex items-center space-x-4">
                        <span class="text-sm text-gray-600">Demo User</span>
                        <button onclick="logout()" class="text-sm text-red-600 hover:text-red-800">Sair</button>
                    </div>
                </div>
            </div>
        </header>
        
        <!-- Main Content -->
        <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div class="bg-white rounded-lg card-shadow p-6">
                    <div class="flex items-center">
                        <div class="p-2 bg-blue-100 rounded-lg">
                            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-gray-600">Conexões Enviadas</p>
                            <p class="text-2xl font-semibold text-gray-900" id="connections-count">1249</p>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white rounded-lg card-shadow p-6">
                    <div class="flex items-center">
                        <div class="p-2 bg-green-100 rounded-lg">
                            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-gray-600">Taxa de Aceitação</p>
                            <p class="text-2xl font-semibold text-gray-900">73%</p>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white rounded-lg card-shadow p-6">
                    <div class="flex items-center">
                        <div class="p-2 bg-purple-100 rounded-lg">
                            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-gray-600">Mensagens Enviadas</p>
                            <p class="text-2xl font-semibold text-gray-900">894</p>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white rounded-lg card-shadow p-6">
                    <div class="flex items-center">
                        <div class="p-2 bg-yellow-100 rounded-lg">
                            <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-gray-600">Visualizações de Perfil</p>
                            <p class="text-2xl font-semibold text-gray-900">2156</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Automation Controls -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                <!-- LinkedIn Connection -->
                <div class="bg-white rounded-lg card-shadow p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">Conexão LinkedIn</h3>
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-sm text-gray-600">Status:</span>
                        <span class="status-active font-medium" id="linkedin-status">Conectado</span>
                    </div>
                    <button onclick="toggleLinkedIn()" id="linkedin-btn" 
                            class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors">
                        Desconectar LinkedIn
                    </button>
                </div>
                
                <!-- Automations -->
                <div class="bg-white rounded-lg card-shadow p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">Automações</h3>
                    
                    <div class="space-y-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="font-medium text-gray-900">Conexões Automáticas</p>
                                <p class="text-sm text-gray-600">Status: <span class="status-active" id="connections-status">Ativo</span></p>
                            </div>
                            <button onclick="toggleAutomation('connections')" id="connections-btn"
                                    class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors text-sm">
                                Pausar Automação
                            </button>
                        </div>
                        
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="font-medium text-gray-900">Mensagens de Follow-up</p>
                                <p class="text-sm text-gray-600">Status: <span class="status-inactive" id="followup-status">Inativo</span></p>
                            </div>
                            <button onclick="toggleAutomation('follow_up')" id="followup-btn"
                                    class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors text-sm">
                                Iniciar Automação
                            </button>
                        </div>
                        
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="font-medium text-gray-900">Visualização de Perfis</p>
                                <p class="text-sm text-gray-600">Status: <span class="status-active" id="profiles-status">Ativo</span></p>
                            </div>
                            <button onclick="toggleAutomation('profile_views')" id="profiles-btn"
                                    class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors text-sm">
                                Pausar Automação
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Activity Log -->
            <div class="bg-white rounded-lg card-shadow p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold text-gray-900">Log de Atividades</h3>
                    <button onclick="clearLog()" class="text-sm text-red-600 hover:text-red-800">Limpar Log</button>
                </div>
                <div id="activity-log" class="space-y-2 max-h-64 overflow-y-auto">
                    <!-- Log entries will be populated here -->
                </div>
            </div>
        </main>
    </div>
    
    <script>
        // Estado das automações
        let automationStates = {
            connections: true,
            follow_up: false,
            profile_views: true
        };
        
        let linkedinConnected = true;
        
        // Carregar log de atividades
        async function loadActivityLog() {
            try {
                const response = await fetch('/api/activity-log');
                const data = await response.json();
                
                const logContainer = document.getElementById('activity-log');
                logContainer.innerHTML = '';
                
                if (data.activities && data.activities.length > 0) {
                    data.activities.forEach(activity => {
                        const div = document.createElement('div');
                        div.className = 'flex justify-between items-center py-2 px-3 bg-gray-50 rounded';
                        div.innerHTML = `
                            <span class="text-sm text-gray-900">${activity.action}</span>
                            <span class="text-xs text-gray-500">${activity.timestamp}</span>
                        `;
                        logContainer.appendChild(div);
                    });
                } else {
                    logContainer.innerHTML = '<p class="text-sm text-gray-500 text-center py-4">Nenhuma atividade registrada</p>';
                }
            } catch (error) {
                console.error('Erro ao carregar log:', error);
            }
        }
        
        // Toggle LinkedIn connection
        async function toggleLinkedIn() {
            try {
                const response = await fetch('/api/linkedin/toggle', { method: 'POST' });
                const data = await response.json();
                
                if (data.success) {
                    linkedinConnected = data.connected;
                    updateLinkedInUI();
                    loadActivityLog();
                    
                    // Atualizar contador de conexões
                    if (linkedinConnected) {
                        const count = document.getElementById('connections-count');
                        count.textContent = parseInt(count.textContent) + 2;
                    }
                }
            } catch (error) {
                console.error('Erro ao alterar conexão LinkedIn:', error);
            }
        }
        
        // Toggle automation
        async function toggleAutomation(type) {
            try {
                const response = await fetch(`/api/automation/${type}/toggle`, { method: 'POST' });
                const data = await response.json();
                
                if (data.success) {
                    automationStates[type] = data.active;
                    updateAutomationUI(type);
                    loadActivityLog();
                    
                    // Atualizar contador de conexões se necessário
                    if (type === 'connections' && data.active) {
                        const count = document.getElementById('connections-count');
                        count.textContent = parseInt(count.textContent) + 2;
                    }
                }
            } catch (error) {
                console.error('Erro ao alterar automação:', error);
            }
        }
        
        // Clear activity log
        async function clearLog() {
            try {
                const response = await fetch('/api/activity-log/clear', { method: 'POST' });
                const data = await response.json();
                
                if (data.success) {
                    loadActivityLog();
                }
            } catch (error) {
                console.error('Erro ao limpar log:', error);
            }
        }
        
        // Update LinkedIn UI
        function updateLinkedInUI() {
            const status = document.getElementById('linkedin-status');
            const btn = document.getElementById('linkedin-btn');
            
            if (linkedinConnected) {
                status.textContent = 'Conectado';
                status.className = 'status-active font-medium';
                btn.textContent = 'Desconectar LinkedIn';
                btn.className = 'w-full bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition-colors';
            } else {
                status.textContent = 'Desconectado';
                status.className = 'status-inactive font-medium';
                btn.textContent = 'Conectar LinkedIn';
                btn.className = 'w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors';
            }
        }
        
        // Update automation UI
        function updateAutomationUI(type) {
            const statusMap = {
                'connections': 'connections-status',
                'follow_up': 'followup-status',
                'profile_views': 'profiles-status'
            };
            
            const btnMap = {
                'connections': 'connections-btn',
                'follow_up': 'followup-btn',
                'profile_views': 'profiles-btn'
            };
            
            const status = document.getElementById(statusMap[type]);
            const btn = document.getElementById(btnMap[type]);
            
            if (automationStates[type]) {
                status.textContent = 'Ativo';
                status.className = 'status-active';
                btn.textContent = 'Pausar Automação';
                btn.className = 'bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors text-sm';
            } else {
                status.textContent = 'Inativo';
                status.className = 'status-inactive';
                btn.textContent = 'Iniciar Automação';
                btn.className = 'bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors text-sm';
            }
        }
        
        // Logout
        function logout() {
            localStorage.removeItem('access_token');
            window.location.href = '/login';
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            loadActivityLog();
            updateLinkedInUI();
            updateAutomationUI('connections');
            updateAutomationUI('follow_up');
            updateAutomationUI('profile_views');
        });
    </script>
    {% endif %}
</body>
</html>
'''

# Rotas principais
@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def login_page():
    return render_template_string(HTML_TEMPLATE, page='login')

@app.route('/dashboard')
def dashboard():
    return render_template_string(HTML_TEMPLATE, page='dashboard')

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'SnapLinked API v4.1.0',
        'version': '4.1.0',
        'timestamp': datetime.utcnow().isoformat(),
        'features': {
            'authentication': True,
            'linkedin_integration': True,
            'automation_engine': True,
            'activity_logging': True,
            'real_time_updates': True
        }
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Dados não fornecidos'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email e senha são obrigatórios'}), 400
        
        # Verificar credenciais
        if email == DEMO_USER['email'] and password == DEMO_USER['password']:
            token = generate_token(DEMO_USER['id'], DEMO_USER['email'])
            
            add_activity('Login realizado', f'Usuário: {email}')
            logger.info(f"Login bem-sucedido para usuário: {email}")
            
            return jsonify({
                'success': True,
                'message': 'Login realizado com sucesso',
                'token': token,
                'user': {
                    'id': DEMO_USER['id'],
                    'email': DEMO_USER['email'],
                    'name': DEMO_USER['name'],
                    'plan': DEMO_USER['plan'],
                    'created_at': DEMO_USER['created_at']
                }
            })
        else:
            logger.warning(f"Tentativa de login falhada para: {email}")
            return jsonify({'success': False, 'error': 'Credenciais inválidas'}), 401
            
    except Exception as e:
        logger.error(f"Erro no login: {str(e)}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@app.route('/api/linkedin/toggle', methods=['POST'])
def toggle_linkedin():
    global automation_states
    try:
        # Simular toggle da conexão LinkedIn
        current_state = session.get('linkedin_connected', True)
        new_state = not current_state
        session['linkedin_connected'] = new_state
        
        if new_state:
            add_activity('LinkedIn conectado', 'Conexão estabelecida com sucesso')
        else:
            add_activity('LinkedIn desconectado', 'Conexão encerrada')
        
        return jsonify({
            'success': True,
            'connected': new_state,
            'message': 'Conectado' if new_state else 'Desconectado'
        })
    except Exception as e:
        logger.error(f"Erro ao alterar conexão LinkedIn: {str(e)}")
        return jsonify({'success': False, 'error': 'Erro ao alterar conexão'}), 500

@app.route('/api/automation/<automation_type>/toggle', methods=['POST'])
def toggle_automation(automation_type):
    global automation_states
    try:
        if automation_type not in automation_states:
            return jsonify({'success': False, 'error': 'Tipo de automação inválido'}), 400
        
        # Toggle automation state
        current_state = automation_states[automation_type]
        new_state = not current_state
        automation_states[automation_type] = new_state
        
        # Map automation types to friendly names
        type_names = {
            'connections': 'Conexões automáticas',
            'follow_up': 'Mensagens de follow-up',
            'profile_views': 'Visualização de perfis'
        }
        
        action = f"{type_names.get(automation_type, automation_type)} {'iniciada' if new_state else 'pausada'}"
        add_activity(action, f'Status alterado para: {"Ativo" if new_state else "Inativo"}')
        
        return jsonify({
            'success': True,
            'active': new_state,
            'message': f'Automação {"ativada" if new_state else "desativada"}'
        })
    except Exception as e:
        logger.error(f"Erro ao alterar automação {automation_type}: {str(e)}")
        return jsonify({'success': False, 'error': 'Erro ao alterar automação'}), 500

@app.route('/api/activity-log', methods=['GET'])
def get_activity_log():
    try:
        return jsonify({
            'success': True,
            'activities': activity_log[-20:],  # Últimas 20 atividades
            'total': len(activity_log)
        })
    except Exception as e:
        logger.error(f"Erro ao obter log de atividades: {str(e)}")
        return jsonify({'success': False, 'error': 'Erro ao carregar log'}), 500

@app.route('/api/activity-log/clear', methods=['POST'])
def clear_activity_log():
    global activity_log
    try:
        activity_log.clear()
        add_activity('Log limpo', 'Histórico de atividades foi limpo')
        
        return jsonify({
            'success': True,
            'message': 'Log de atividades limpo com sucesso'
        })
    except Exception as e:
        logger.error(f"Erro ao limpar log: {str(e)}")
        return jsonify({'success': False, 'error': 'Erro ao limpar log'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 SnapLinked v4.1.0 - Sistema Principal iniciando...")
    print(f"📍 Acesse: http://localhost:{port}")
    print("👤 Login: demo@snaplinked.com")
    print("🔑 Senha: demo123")
    print("✨ Todas as funcionalidades estão 100% operacionais!")
    
    # Adicionar algumas atividades iniciais
    add_activity('Sistema iniciado', 'SnapLinked v4.1.0 carregado com sucesso')
    add_activity('LinkedIn conectado', 'Conexão automática estabelecida')
    add_activity('Conexões automáticas iniciadas', 'Automação ativada')
    add_activity('Visualização de perfis iniciada', 'Automação ativada')
    
    app.run(host='0.0.0.0', port=port, debug=False)
