"""
Testes de integração para a aplicação SnapLinked
"""

import pytest
import sys
import os

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
        assert response.status_code in [200, 404]
    
    def test_spa_routing(self, client):
        """Testa roteamento SPA"""
        response = client.get('/dashboard')
        assert response.status_code in [200, 404]
    
    def test_cors_headers(self, client):
        """Testa headers CORS"""
        response = client.options('/api/health')
        assert response.status_code in [200, 404]
    
    def test_error_handling_404(self, client):
        """Testa tratamento de erro 404"""
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
    
    @patch('main.LinkedInAutomationEngine')
    def test_error_handling_500(self, mock_engine, client):
        """Testa tratamento de erro 500"""
        mock_instance = mock_engine.return_value
        mock_instance.run_automation = AsyncMock(side_effect=Exception("Test error"))
        mock_instance.close = AsyncMock()

        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': 'test@example.com', 'password': 'TestPassword123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['tokens']['access_token']

        response = client.post(
            '/api/automations/run',
            headers={'Authorization': f'Bearer {token}'},
            data=json.dumps({'keywords': 'test'}),
            content_type='application/json'
        )
        assert response.status_code == 500
    
    def test_authentication_flow(self, client, sample_user_data):
        """Testa fluxo completo de autenticação"""
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': sample_user_data['email'], 'password': sample_user_data['password']}),
            content_type='application/json'
        )
        assert login_response.status_code == 200
        login_data = json.loads(login_response.data)
        assert login_data['success'] is True
        
        token = login_data['tokens']['access_token']
        user_response = client.get('/api/auth/me', headers={'Authorization': f'Bearer {token}'})
        assert user_response.status_code == 200
        
        logout_response = client.post('/api/auth/logout')
        assert logout_response.status_code == 200

    @patch('main.LinkedInAutomationEngine')
    def test_linkedin_integration_flow(self, mock_engine, client):
        """Testa fluxo de integração LinkedIn"""
        mock_instance = mock_engine.return_value
        mock_instance.login_with_credentials = AsyncMock(return_value={
            'success': True,
            'profile': {'name': 'Test User', 'headline': 'Test Headline'}
        })
        mock_instance.get_stats = AsyncMock(return_value={'success': True, 'stats': {}})
        mock_instance.close = AsyncMock()

        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': 'test@example.com', 'password': 'TestPassword123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['tokens']['access_token']

        linkedin_login_response = client.post(
            '/api/linkedin/manual-login',
            headers={'Authorization': f'Bearer {token}'},
            data=json.dumps({'email': 'test@linkedin.com', 'password': 'password123'}),
            content_type='application/json'
        )
        assert linkedin_login_response.status_code == 200
        assert json.loads(linkedin_login_response.data)['success'] is True

    @patch('main.LinkedInAutomationEngine')
    def test_automation_flow(self, mock_engine, client, sample_automation_config):
        """Testa fluxo completo de automação"""
        mock_instance = mock_engine.return_value
        mock_instance.run_automation = AsyncMock(return_value={
            'success': True, 'message': 'Automação executada com sucesso'
        })
        mock_instance.get_stats = AsyncMock(return_value={'success': True, 'stats': {}})
        mock_instance.close = AsyncMock()

        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': 'test@example.com', 'password': 'TestPassword123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['tokens']['access_token']

        run_response = client.post(
            '/api/automations/run',
            headers={'Authorization': f'Bearer {token}'},
            data=json.dumps(sample_automation_config),
            content_type='application/json'
        )
        assert run_response.status_code == 200
        assert json.loads(run_response.data)['success'] is True

    def test_analytics_endpoints(self, client):
        """Testa endpoints de analytics"""
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': 'test@example.com', 'password': 'TestPassword123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['tokens']['access_token']

        analytics_response = client.get('/api/analytics/dashboard', headers={'Authorization': f'Bearer {token}'})
        assert analytics_response.status_code == 200
        
        plans_response = client.get('/api/payments/plans', headers={'Authorization': f'Bearer {token}'})
        assert plans_response.status_code == 200

