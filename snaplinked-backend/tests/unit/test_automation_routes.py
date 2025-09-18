"""
Testes unitários para rotas de automação
"""

import pytest
import json
from unittest.mock import patch, AsyncMock

class TestAutomationRoutes:
    """Testes para as rotas de automação"""
    
    def test_get_automations_success(self, client):
        """Testa listagem de automações"""
        response = client.get('/api/automations')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'automations' in data
        assert isinstance(data['automations'], list)
    
    def test_create_automation_success(self, client, sample_automation_config):
        """Testa criação de automação"""
        automation_data = {
            'name': 'Test Automation',
            'type': 'connection_requests',
            'keywords': 'desenvolvedor python',
            'daily_limit': 50
        }
        
        response = client.post(
            '/api/automations',
            data=json.dumps(automation_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'automation' in data
        assert data['automation']['name'] == automation_data['name']
    
    def test_create_automation_missing_fields(self, client):
        """Testa criação de automação com campos ausentes"""
        response = client.post(
            '/api/automations',
            data=json.dumps({
                'name': 'Test Automation'
                # Campos obrigatórios ausentes
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'obrigatório' in data['error']
    
    def test_update_automation_success(self, client):
        """Testa atualização de automação"""
        automation_data = {
            'name': 'Updated Automation',
            'keywords': 'new keywords'
        }
        
        response = client.put(
            '/api/automations/1',
            data=json.dumps(automation_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_delete_automation_success(self, client):
        """Testa remoção de automação"""
        response = client.delete('/api/automations/1')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_toggle_automation_success(self, client):
        """Testa toggle de automação"""
        response = client.post('/api/automations/1/toggle')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    @patch('routes.automations.automation_engine')
    def test_run_automation_not_logged_in(self, mock_engine, client, sample_automation_config):
        """Testa execução de automação sem login"""
        with client.session_transaction() as sess:
            sess.pop('linkedin_manual_connected', None)
        
        response = client.post(
            '/api/automations/run',
            data=json.dumps(sample_automation_config),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Login manual necessário' in data['error']
    
    @patch('routes.automations.automation_engine')
    @patch('routes.automations.asyncio')
    def test_run_automation_success(self, mock_asyncio, mock_engine, client, sample_automation_config, mock_session):
        """Testa execução de automação com sucesso"""
        # Configurar mock do loop assíncrono
        mock_loop = AsyncMock()
        mock_asyncio.new_event_loop.return_value = mock_loop
        mock_asyncio.set_event_loop.return_value = None
        
        # Configurar retorno do engine
        mock_result = {
            'success': True,
            'message': 'Automação executada com sucesso',
            'results': []
        }
        mock_loop.run_until_complete.return_value = mock_result
        
        # Configurar sessão
        with client.session_transaction() as sess:
            sess.update(mock_session)
        
        response = client.post(
            '/api/automations/run',
            data=json.dumps(sample_automation_config),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_run_automation_missing_keywords(self, client, mock_session):
        """Testa execução de automação sem palavras-chave"""
        with client.session_transaction() as sess:
            sess.update(mock_session)
        
        config = {
            'type': 'connection_requests',
            'keywords': '',  # Vazio
            'max_actions': 10
        }
        
        response = client.post(
            '/api/automations/run',
            data=json.dumps(config),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Palavras-chave são obrigatórias' in data['error']
    
    @patch('routes.automations.automation_engine')
    @patch('routes.automations.asyncio')
    def test_get_automation_stats_success(self, mock_asyncio, mock_engine, client):
        """Testa obtenção de estatísticas de automação"""
        # Configurar mock do loop assíncrono
        mock_loop = AsyncMock()
        mock_asyncio.new_event_loop.return_value = mock_loop
        mock_asyncio.set_event_loop.return_value = None
        
        # Configurar retorno do engine
        mock_result = {
            'success': True,
            'stats': {
                'connections_sent': 10,
                'messages_sent': 5,
                'profiles_viewed': 20
            }
        }
        mock_loop.run_until_complete.return_value = mock_result
        
        response = client.get('/api/automations/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'stats' in data
