"""
Configuração principal do backend
"""
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Configurações de aplicação
APP_NAME = "SnapLinked"
VERSION = "4.2.0"
DEBUG = False

# Import configurações específicas
from .security import SecurityConfig
from .performance import PerformanceConfig

class Config(SecurityConfig, PerformanceConfig):
    """Configuração unificada"""
    
    # Database
    DATABASE_URL = "sqlite:///./snaplinked.db"
    
    # LinkedIn
    LINKEDIN_CLIENT_ID = ""  # Set via env
    LINKEDIN_CLIENT_SECRET = ""  # Set via env
    LINKEDIN_REDIRECT_URI = "http://localhost:3000/auth/linkedin/callback"
    
    # Redis
    REDIS_URL = "redis://localhost:6379/0"
    
    # Upload
    UPLOAD_FOLDER = str(BASE_DIR / "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # CORS
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002"
    ]
    
    @classmethod
    def init_app(cls, app):
        """Inicializa a aplicação com as configurações"""
        app.config.from_object(cls)