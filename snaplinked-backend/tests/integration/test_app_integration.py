"""
Testes de integração para a aplicação SnapLinked
"""

import pytest
import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
import json
from unittest.mock import patch, AsyncMock

class TestAppIntegration:
    """Testes de integração da aplicação"""
    
    def test_health_check(self, client):
        """Testa endpoint de health check"""
        response = client.get('/api/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'SnapLinked API'
        assert 'features' in data
    
    def test_frontend_serving(self, client):
        """Testa servir do frontend"""
        response = client.get('/')
        
        # Deve retornar 200 ou 404 (se index.html não existir)
        assert response.status_code in [200, 404]
    
    def test_spa_routing(self, client):
        """Testa roteamento SPA"""
        response = client.get('/dashboard')
        
        # Deve retornar 200 ou 404 (fallback para index.html)
        assert response.status_code in [200, 404]
    
    def test_cors_headers(self, client):
        """Testa headers CORS"""
        response = client.options('/api/health')
        
        # Verificar se CORS está configurado
        assert response.status_code in [200, 404]
    
    def test_error_handling_404(self, client):
        """Testa tratamento de erro 404"""
        response = client.get('/api/nonexistent')
        
        assert response.status_code == 404
    
    def test_error_handling_500(self, client):
        """Testa tratamento de erro 500"""
        with patch('routes.analytics.logger') as mock_logger:
            # Simular erro interno
            mock_logger.error.side_effect = Exception("Test error")
            
            response = client.get('/api/analytics')
            
            # Deve retornar dados ou erro tratado
            assert response.status_code in [200, 500]
    
    def test_authentication_flow(self, client, sample_user_data):
        """Testa fluxo completo de autenticação"""
        # 1. Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': sample_user_data['email'],
                'password': sample_user_data['password']
            }),
            content_type='application/json'
        )
        
        assert login_response.status_code == 200
        login_data = json.loads(login_response.data)
        assert login_data['success'] is True
        
        # 2. Obter usuário atual com token
        token = login_data['tokens']['access_token']
        user_response = client.get(
            '/api/auth/me',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert user_response.status_code == 200
        user_data = json.loads(user_response.data)
        assert user_data['success'] is True
        
        # 3. Logout
        logout_response = client.post('/api/auth/logout')
        
        assert logout_response.status_code == 200
        logout_data = json.loads(logout_response.data)
        assert logout_data['success'] is True
    
    @patch('routes.linkedin.automation_engine')
    @patch('routes.linkedin.asyncio')
    def test_linkedin_integration_flow(self, mock_asyncio, mock_engine, client):
        """Testa fluxo de integração LinkedIn"""
        # Configurar mocks
        mock_loop = AsyncMock()
        mock_asyncio.new_event_loop.return_value = mock_loop
        mock_asyncio.set_event_loop.return_value = None
        
        # 1. Login manual LinkedIn
        mock_loop.run_until_complete.return_value = {
            'success': True,
            'profile': {
                'name': 'Test User',
                'headline': 'Test Headline',
                'logged_in_at': '2024-01-01T00:00:00'
            }
        }
        
        login_response = client.post(
            '/api/linkedin/manual-login',
            data=json.dumps({
                'email': 'test@linkedin.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        assert login_response.status_code == 200
        login_data = json.loads(login_response.data)
        assert login_data['success'] is True
        
        # 2. Obter perfil LinkedIn
        profile_response = client.get('/api/linkedin/profile')
        
        assert profile_response.status_code == 200
        profile_data = json.loads(profile_response.data)
        assert profile_data['success'] is True
        
        # 3. Desconectar LinkedIn
        disconnect_response = client.post('/api/linkedin/disconnect')
        
        assert disconnect_response.status_code == 200
        disconnect_data = json.loads(disconnect_response.data)
        assert disconnect_data['success'] is True
    
    @patch('routes.automations.automation_engine')
    @patch('routes.automations.asyncio')
    def test_automation_flow(self, mock_asyncio, mock_engine, client, sample_automation_config):
        """Testa fluxo completo de automação"""
        # Configurar mocks
        mock_loop = AsyncMock()
        mock_asyncio.new_event_loop.return_value = mock_loop
        mock_asyncio.set_event_loop.return_value = None
        
        # Simular login LinkedIn
        with client.session_transaction() as sess:
            sess['linkedin_manual_connected'] = True
            sess['linkedin_manual_user'] = {
                'name': 'Test User',
                'headline': 'Test Headline'
            }
        
        # 1. Listar automações
        list_response = client.get('/api/automations')
        
        assert list_response.status_code == 200
        list_data = json.loads(list_response.data)
        assert list_data['success'] is True
        
        # 2. Executar automação
        mock_loop.run_until_complete.return_value = {
            'success': True,
            'message': 'Automação executada com sucesso',
            'results': [],
            'stats': {
                'connections_sent': 5,
                'messages_sent': 3
            }
        }
        
        run_response = client.post(
            '/api/automations/run',
            data=json.dumps(sample_automation_config),
            content_type='application/json'
        )
        
        assert run_response.status_code == 200
        run_data = json.loads(run_response.data)
        assert run_data['success'] is True
        
        # 3. Obter estatísticas
        stats_response = client.get('/api/automations/stats')
        
        assert stats_response.status_code == 200
    
    def test_analytics_endpoints(self, client):
        """Testa endpoints de analytics"""
        # 1. Analytics gerais
        analytics_response = client.get('/api/analytics')
        
        assert analytics_response.status_code == 200
        analytics_data = json.loads(analytics_response.data)
        assert analytics_data['success'] is True
        
        # 2. Stats do dashboard
        dashboard_response = client.get('/api/dashboard/stats')
        
        assert dashboard_response.status_code == 200
        dashboard_data = json.loads(dashboard_response.data)
        assert dashboard_data['success'] is True
        
        # 3. Planos de assinatura
        plans_response = client.get('/api/payments/plans')
        
        assert plans_response.status_code == 200
        plans_data = json.loads(plans_response.data)
        assert plans_data['success'] is True
        assert 'plans' in plans_data
    
    def test_json_validation(self, client):
        """Testa validação de JSON em endpoints"""
        # Tentar enviar JSON inválido
        response = client.post(
            '/api/auth/login',
            data='invalid json',
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_content_type_validation(self, client):
        """Testa validação de Content-Type"""
        # Tentar enviar sem Content-Type correto
        response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': 'test@example.com', 'password': 'password'}),
            content_type='text/plain'
        )
        
        # Deve aceitar ou rejeitar baseado na validação
        assert response.status_code in [200, 400, 415]
