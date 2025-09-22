"""
SnapLinked - Serviço OAuth LinkedIn Real
Implementação completa da autenticação OAuth 2.0 do LinkedIn
"""
import os
import requests
import secrets
import logging
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class LinkedInOAuth:
    def __init__(self):
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')
        self.scopes = os.getenv('LINKEDIN_SCOPES', 'openid profile email')
        
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            logger.error("Credenciais LinkedIn OAuth não configuradas")
            raise ValueError("Credenciais LinkedIn OAuth obrigatórias não encontradas")
    
    def generate_auth_url(self, state=None):
        """Gera URL de autorização LinkedIn OAuth"""
        try:
            if not state:
                state = secrets.token_urlsafe(32)
            
            params = {
                'response_type': 'code',
                'client_id': self.client_id,
                'redirect_uri': self.redirect_uri,
                'state': state,
                'scope': self.scopes
            }
            
            auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"
            
            logger.info(f"URL OAuth gerada: {auth_url}")
            return {
                'success': True,
                'auth_url': auth_url,
                'state': state,
                'client_id': self.client_id
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar URL OAuth: {str(e)}")
            return {
                'success': False,
                'error': f"Erro ao gerar URL OAuth: {str(e)}"
            }
    
    def exchange_code_for_token(self, code, state):
        """Troca código de autorização por token de acesso"""
        try:
            token_url = "https://www.linkedin.com/oauth/v2/accessToken"
            
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(token_url, data=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                token_data = response.json()
                logger.info("Token de acesso obtido com sucesso")
                return {
                    'success': True,
                    'access_token': token_data.get('access_token'),
                    'expires_in': token_data.get('expires_in'),
                    'token_type': token_data.get('token_type', 'Bearer')
                }
            else:
                logger.error(f"Erro ao obter token: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f"Erro LinkedIn API: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Erro ao trocar código por token: {str(e)}")
            return {
                'success': False,
                'error': f"Erro ao trocar código por token: {str(e)}"
            }
    
    def get_user_profile(self, access_token):
        """Obtém perfil do usuário LinkedIn"""
        try:
            profile_url = "https://api.linkedin.com/v2/userinfo"
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(profile_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                profile_data = response.json()
                logger.info(f"Perfil obtido: {profile_data.get('name', 'N/A')}")
                return {
                    'success': True,
                    'profile': {
                        'id': profile_data.get('sub'),
                        'name': profile_data.get('name'),
                        'email': profile_data.get('email'),
                        'picture': profile_data.get('picture'),
                        'locale': profile_data.get('locale')
                    }
                }
            else:
                logger.error(f"Erro ao obter perfil: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f"Erro ao obter perfil: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Erro ao obter perfil: {str(e)}")
            return {
                'success': False,
                'error': f"Erro ao obter perfil: {str(e)}"
            }
    
    def validate_token(self, access_token):
        """Valida se o token ainda é válido"""
        try:
            result = self.get_user_profile(access_token)
            return result['success']
        except:
            return False
    
    def revoke_token(self, access_token):
        """Revoga token de acesso"""
        try:
            revoke_url = "https://www.linkedin.com/oauth/v2/revoke"
            
            data = {
                'token': access_token,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(revoke_url, data=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                logger.info("Token revogado com sucesso")
                return {'success': True}
            else:
                logger.warning(f"Erro ao revogar token: {response.status_code}")
                return {'success': False, 'error': 'Erro ao revogar token'}
                
        except Exception as e:
            logger.error(f"Erro ao revogar token: {str(e)}")
            return {'success': False, 'error': str(e)}

# Instância global
linkedin_oauth = LinkedInOAuth()
