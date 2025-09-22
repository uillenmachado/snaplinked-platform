"""
SnapLinked Backend - Configurações
Versão 4.2.0 - Sistema de configuração centralizado e otimizado
"""

import os
from datetime import timedelta

class Config:
    """Configuração base da aplicação"""
    
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY', 'snaplinked-secret-key-2025-v4.2.0')
    DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    ENV = os.environ.get('FLASK_ENV', 'production')
    VERSION = '4.2.0'
    
    # Configurações de banco de dados
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///snaplinked.db')
    
    # Configurações JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', '1')))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', '30')))
    
    # Configurações LinkedIn OAuth
    LINKEDIN_CLIENT_ID = os.environ.get('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.environ.get('LINKEDIN_CLIENT_SECRET')
    LINKEDIN_REDIRECT_URI = os.environ.get('LINKEDIN_REDIRECT_URI', 'http://localhost:3000/auth/linkedin/callback')
    LINKEDIN_SCOPES = os.environ.get('LINKEDIN_SCOPES', 'openid profile email')
    
    # Configurações Gemini API
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    # Configurações Redis
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Configurações de email
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    SMTP_USE_TLS = os.environ.get('SMTP_USE_TLS', 'true').lower() == 'true'
    
    # Configurações de segurança
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configurações CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    
    # Configurações de rate limiting
    RATE_LIMIT_STORAGE_URL = os.environ.get('RATE_LIMIT_STORAGE_URL', 'redis://localhost:6379/3')
    
    # Configurações de upload
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', '16777216'))  # 16MB
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads/')
    
    # Configurações de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/snaplinked.log')

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    ENV = 'production'
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Mapeamento de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
