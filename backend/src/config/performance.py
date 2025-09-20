"""
Configurações de cache e performance
"""

class CacheConfig:
    # Redis para cache
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutos
    
    # Configurações de cache por rota
    CACHE_ROUTES = {
        'api.health': 60,  # 1 minuto
        'api.user_profile': 300,  # 5 minutos
        'api.linkedin_stats': 600,  # 10 minutos
    }
    
class PerformanceConfig:
    # Limites de performance
    SLOW_REQUEST_THRESHOLD = 1.0  # segundos
    MAX_REQUEST_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Configurações de paginação
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Timeouts
    DEFAULT_TIMEOUT = 30  # segundos
    LONG_POLLING_TIMEOUT = 60  # segundos
    
    # Rate limiting por IP
    RATE_LIMIT_DEFAULT = "1000 per hour"
    RATE_LIMIT_DOCS = "2000 per hour"