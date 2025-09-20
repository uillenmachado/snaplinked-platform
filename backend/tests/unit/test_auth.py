"""
Testes unitários para autenticação
"""
import pytest
import jwt
from datetime import datetime, timedelta
from src.main import app
from src.config.security import SecurityConfig

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_success(client):
    """Teste de login com sucesso usando credenciais demo"""
    response = client.post('/api/auth/login', json={
        'email': 'demo@snaplinked.com',
        'password': 'demo123'
    })
    assert response.status_code == 200
    assert response.json['success'] is True
    assert 'token' in response.json
    assert 'user' in response.json

def test_login_invalid_credentials(client):
    """Teste de login com credenciais inválidas"""
    response = client.post('/api/auth/login', json={
        'email': 'wrong@email.com',
        'password': 'wrongpass'
    })
    assert response.status_code == 401
    assert response.json['success'] is False

def test_token_generation():
    """Teste de geração de token JWT"""
    user_id = 1
    email = 'test@example.com'
    token = jwt.encode(
        {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        SecurityConfig.JWT_SECRET_KEY,
        algorithm='HS256'
    )
    assert token is not None
    decoded = jwt.decode(token, SecurityConfig.JWT_SECRET_KEY, algorithms=['HS256'])
    assert decoded['user_id'] == user_id
    assert decoded['email'] == email