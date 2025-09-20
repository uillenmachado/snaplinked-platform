"""
Configurações de segurança da aplicação SnapLinked
"""

import os
from datetime import timedelta

class SecurityConfig:
    # Chave secreta gerada automaticamente ou definida via variável de ambiente
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32).hex()
    
    # Configurações JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or os.urandom(32).hex()
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Configurações CORS
    CORS_ORIGINS = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000,http://localhost:3001,http://localhost:3002').split(',')
    
    # Rate Limiting
    RATELIMIT_DEFAULT = "100 per hour"
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    
    # Proteção contra força bruta
    MAX_LOGIN_ATTEMPTS = 5
    LOGIN_TIMEOUT = 300  # 5 minutos
    
    # Configurações de senha
    MIN_PASSWORD_LENGTH = 8
    PASSWORD_REQUIREMENTS = {
        'uppercase': 1,  # mínimo de caracteres maiúsculos
        'lowercase': 1,  # mínimo de caracteres minúsculos
        'numbers': 1,    # mínimo de números
        'special': 1     # mínimo de caracteres especiais
    }
    
    # Headers de segurança
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': "default-src 'self';"
    }