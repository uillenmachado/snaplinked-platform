"""
Testes unitários para rotas de autenticação
"""

import pytest
import json
from unittest.mock import patch, Mock

class TestAuthRoutes:
    """Testes para as rotas de autenticação"""
    
    def test_login_success(self, client, sample_user_data):
        """Testa login bem-sucedido"""
        response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': sample_user_data['email'],
                'password': sample_user_data['password']
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'user' in data
        assert 'tokens' in data
        assert data['user']['email'] == sample_user_data['email']
    
    def test_login_missing_credentials(self, client):
        """Testa login com credenciais ausentes"""
        response = client.post(
            '/api/auth/login',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Email e senha são obrigatórios' in data['message']
    
    def test_login_invalid_json(self, client):
        """Testa login com JSON inválido"""
        response = client.post(
            '/api/auth/login',
            data='invalid json',
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_register_success(self, client, sample_user_data):
        """Testa registro bem-sucedido"""
        response = client.post(
            '/api/auth/register',
            data=json.dumps(sample_user_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'user' in data
        assert 'tokens' in data
        assert data['user']['email'] == sample_user_data['email']
    
    def test_register_missing_fields(self, client):
        """Testa registro com campos ausentes"""
        response = client.post(
            '/api/auth/register',
            data=json.dumps({
                'email': 'test@example.com'
                # Campos obrigatórios ausentes
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'obrigatório' in data['message']
    
    def test_logout_success(self, client):
        """Testa logout bem-sucedido"""
        response = client.post('/api/auth/logout')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'Logout realizado com sucesso' in data['message']
    
    def test_get_current_user_with_token(self, client, auth_headers):
        """Testa obtenção do usuário atual com token"""
        response = client.get(
            '/api/auth/me',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'user' in data
    
    def test_get_current_user_without_token(self, client):
        """Testa obtenção do usuário atual sem token"""
        response = client.get('/api/auth/me')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Token de acesso necessário' in data['message']
    
    @patch('routes.auth.Config')
    def test_linkedin_connect_missing_credentials(self, mock_config, client):
        """Testa conexão LinkedIn sem credenciais configuradas"""
        mock_config.LINKEDIN_CLIENT_ID = None
        mock_config.LINKEDIN_CLIENT_SECRET = None
        
        response = client.get('/api/auth/linkedin/connect')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Credenciais LinkedIn não configuradas' in data['error']
    
    @patch('routes.auth.Config')
    def test_linkedin_connect_success(self, mock_config, client):
        """Testa início da conexão LinkedIn com sucesso"""
        mock_config.LINKEDIN_CLIENT_ID = 'test_client_id'
        mock_config.LINKEDIN_CLIENT_SECRET = 'test_client_secret'
        mock_config.LINKEDIN_REDIRECT_URI = 'http://localhost:5000/callback'
        
        response = client.get('/api/auth/linkedin/connect')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'auth_url' in data
        assert 'state' in data
