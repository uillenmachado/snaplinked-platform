import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
import json
from unittest.mock import patch, AsyncMock

class TestAutomationRoutes:
    def test_get_automations_success(self, client, auth_headers):
        response = client.get('/api/automations', headers=auth_headers)
        assert response.status_code == 200

    def test_create_automation_success(self, client, sample_automation_config, auth_headers):
        response = client.post(
            '/api/automations',
            data=json.dumps(sample_automation_config),
            content_type='application/json',
            headers=auth_headers
        )
        assert response.status_code == 201

    @patch('main.LinkedInAutomationEngine')
    def test_run_automation_success(self, mock_engine, client, sample_automation_config, auth_headers):
        mock_instance = mock_engine.return_value
        mock_instance.run_automation = AsyncMock(return_value={
            'success': True,
            'message': 'Automação executada com sucesso',
            'results': []
        })
        mock_instance.close = AsyncMock()

        response = client.post(
            '/api/automations/run',
            data=json.dumps(sample_automation_config),
            content_type='application/json',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    @patch('main.LinkedInAutomationEngine')
    def test_get_automation_stats_success(self, mock_engine, client, auth_headers):
        mock_instance = mock_engine.return_value
        mock_instance.get_stats = AsyncMock(return_value={
            'success': True,
            'stats': {'connections_sent': 10}
        })
        mock_instance.close = AsyncMock()

        response = client.get('/api/automations/stats', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

