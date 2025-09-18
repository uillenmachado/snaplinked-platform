"""
Configuração de testes para o SnapLinked Backend
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Importar módulos do projeto
import main
from services.linkedin_automation import LinkedInAutomationEngine

@pytest.fixture
def app():
    """Fixture da aplicação Flask para testes"""
    app = main.create_app('testing')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app

@pytest.fixture
def client(app):
    """Fixture do cliente de teste Flask"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Fixture do runner CLI"""
    return app.test_cli_runner()

@pytest.fixture
def mock_automation_engine():
    """Mock do engine de automação"""
    engine = Mock(spec=LinkedInAutomationEngine)
    
    # Configurar métodos assíncronos
    engine.login_with_credentials = AsyncMock(return_value={
        'success': True,
        'profile': {
            'name': 'Test User',
            'headline': 'Test Headline',
            'logged_in_at': '2024-01-01T00:00:00'
        }
    })
    
    engine.run_automation = AsyncMock(return_value={
        'success': True,
        'message': 'Automação executada com sucesso',
        'results': [],
        'stats': {
            'connections_sent': 5,
            'messages_sent': 3,
            'profiles_viewed': 10,
            'errors': 0
        }
    })
    
    engine.get_stats = AsyncMock(return_value={
        'success': True,
        'stats': {
            'connections_sent': 10,
            'messages_sent': 5,
            'profiles_viewed': 20,
            'errors': 0,
            'is_logged_in': True,
            'profile': {
                'name': 'Test User',
                'headline': 'Test Headline'
            }
        }
    })
    
    engine.close = AsyncMock()
    
    return engine

@pytest.fixture
def auth_headers():
    """Headers de autenticação para testes"""
    return {
        'Authorization': 'Bearer test_token',
        'Content-Type': 'application/json'
    }

@pytest.fixture
def sample_user_data():
    """Dados de usuário para testes"""
    return {
        'email': 'test@example.com',
        'password': 'TestPassword123',
        'first_name': 'Test',
        'last_name': 'User',
        'company': 'Test Company'
    }

@pytest.fixture
def sample_automation_config():
    """Configuração de automação para testes"""
    return {
        'type': 'connection_requests',
        'keywords': 'desenvolvedor python',
        'max_actions': 10,
        'message': 'Olá! Gostaria de conectar.'
    }

@pytest.fixture
def mock_session():
    """Mock de sessão Flask"""
    return {
        'linkedin_manual_connected': True,
        'linkedin_manual_user': {
            'name': 'Test User',
            'headline': 'Test Headline',
            'logged_in_at': '2024-01-01T00:00:00'
        }
    }

# Configuração para testes assíncronos
@pytest.fixture(scope="session")
def event_loop():
    """Cria um loop de eventos para testes assíncronos"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
