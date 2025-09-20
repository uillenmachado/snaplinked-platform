"""
Testes de integração com LinkedIn
"""
import pytest
from src.main import app
from src.config.security import SecurityConfig

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_linkedin_health_check(client):
    """Teste de verificação de saúde da integração LinkedIn"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['features']['linkedin_integration'] is True

def test_linkedin_automation_toggle(client):
    """Teste de toggle da automação LinkedIn"""
    # Primeiro login para obter token
    login_response = client.post('/api/auth/login', json={
        'email': 'demo@snaplinked.com',
        'password': 'demo123'
    })
    token = login_response.json['token']
    
    # Teste com token válido
    response = client.post('/api/linkedin/toggle', 
        headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'success' in response.json
    assert 'connected' in response.json

def test_linkedin_automation_unauthorized(client):
    """Teste de acesso não autorizado à automação LinkedIn"""
    response = client.post('/api/linkedin/toggle')
    assert response.status_code == 401