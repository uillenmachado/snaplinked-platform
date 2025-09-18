"""
Utilitários de segurança
"""

import hashlib
import secrets
import hmac
from typing import Tuple
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

class PasswordManager:
    """Gerenciador de senhas seguro"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Gera hash seguro da senha"""
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verifica se a senha corresponde ao hash"""
        return check_password_hash(password_hash, password)
    
    @staticmethod
    def generate_salt() -> str:
        """Gera salt aleatório"""
        return secrets.token_hex(16)

class TokenManager:
    """Gerenciador de tokens JWT"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def generate_access_token(self, user_id: int, expires_in: timedelta = None) -> str:
        """Gera token de acesso"""
        if expires_in is None:
            expires_in = timedelta(hours=1)
        
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + expires_in,
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def generate_refresh_token(self, user_id: int, expires_in: timedelta = None) -> str:
        """Gera token de refresh"""
        if expires_in is None:
            expires_in = timedelta(days=30)
        
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + expires_in,
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }
        
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> dict:
        """Verifica e decodifica token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return {'valid': True, 'payload': payload}
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'error': 'Token expirado'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'error': 'Token inválido'}

class CSRFProtection:
    """Proteção contra CSRF"""
    
    @staticmethod
    def generate_csrf_token() -> str:
        """Gera token CSRF"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def verify_csrf_token(token: str, expected_token: str) -> bool:
        """Verifica token CSRF"""
        return hmac.compare_digest(token, expected_token)

class RateLimiter:
    """Limitador de taxa de requisições"""
    
    def __init__(self):
        self.attempts = {}
    
    def is_rate_limited(self, identifier: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
        """Verifica se o identificador está limitado por taxa"""
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=window_minutes)
        
        # Limpar tentativas antigas
        if identifier in self.attempts:
            self.attempts[identifier] = [
                attempt for attempt in self.attempts[identifier]
                if attempt > window_start
            ]
        
        # Verificar limite
        attempts_count = len(self.attempts.get(identifier, []))
        return attempts_count >= max_attempts
    
    def record_attempt(self, identifier: str):
        """Registra uma tentativa"""
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        
        self.attempts[identifier].append(datetime.utcnow())

def generate_api_key() -> str:
    """Gera chave de API segura"""
    return f"sk_{secrets.token_urlsafe(32)}"

def hash_api_key(api_key: str) -> str:
    """Gera hash da chave de API"""
    return hashlib.sha256(api_key.encode()).hexdigest()

def verify_api_key(api_key: str, api_key_hash: str) -> bool:
    """Verifica chave de API"""
    return hmac.compare_digest(hash_api_key(api_key), api_key_hash)

def sanitize_filename(filename: str) -> str:
    """Sanitiza nome de arquivo"""
    import re
    # Remover caracteres perigosos
    sanitized = re.sub(r'[^\w\-_\.]', '', filename)
    # Limitar tamanho
    return sanitized[:255]

def generate_secure_random_string(length: int = 32) -> str:
    """Gera string aleatória segura"""
    return secrets.token_urlsafe(length)

# Instâncias globais
password_manager = PasswordManager()
rate_limiter = RateLimiter()
csrf_protection = CSRFProtection()
