"""
Módulo de rotas da aplicação
"""

from .auth import auth_bp
from .linkedin import linkedin_bp
from .automations import automations_bp
from .analytics import analytics_bp

__all__ = ['auth_bp', 'linkedin_bp', 'automations_bp', 'analytics_bp']
