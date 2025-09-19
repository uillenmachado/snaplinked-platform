import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
import json
from unittest.mock import patch

class TestAuthRoutes:
    def test_login_success(self, client, sample_user_data):
        response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': sample_user_data['email'], 'password': sample_user_data['password']}),
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_login_missing_credentials(self, client):
        response = client.post('/api/auth/login', data=json.dumps({}), content_type='application/json')
        assert response.status_code == 400

    def test_register_success(self, client, sample_user_data):
        response = client.post(
            '/api/auth/register',
            data=json.dumps(sample_user_data),
            content_type='application/json'
        )
        assert response.status_code == 201

    def test_logout_success(self, client):
        response = client.post('/api/auth/logout')
        assert response.status_code == 200

    def test_get_current_user_with_token(self, client, auth_headers):
        response = client.get('/api/auth/me', headers=auth_headers)
        assert response.status_code == 200

    def test_linkedin_connect_success(self, client):
        client.application.config['LINKEDIN_CLIENT_ID'] = 'test_client_id'
        client.application.config['LINKEDIN_CLIENT_SECRET'] = 'test_client_secret'
        client.application.config['LINKEDIN_REDIRECT_URI'] = 'http://localhost:5000/callback'

        response = client.get('/api/auth/linkedin/connect')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'authorization_url' in data

