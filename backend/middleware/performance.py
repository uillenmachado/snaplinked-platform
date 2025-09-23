#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapLinked v3.0 - Middleware de Performance
Cache, compressão e otimizações de performance
"""

import time
import gzip
import json
from functools import wraps
from typing import Any, Dict, Optional
from datetime import datetime, timedelta

from flask import request, g, current_app, jsonify
import structlog

# Configurar logging
logger = structlog.get_logger(__name__)


class PerformanceMiddleware:
    """Middleware de performance para Flask"""
    
    def __init__(self, app=None):
        self.app = app
        self.cache = {}
        self.cache_ttl = {}
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializar middleware com aplicação Flask"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        
        # Configurar cache
        self.setup_cache(app)
    
    def before_request(self):
        """Executar antes de cada requisição"""
        g.start_time = time.time()
        
        # Verificar cache para GET requests
        if request.method == 'GET':
            cached_response = self.get_cached_response()
            if cached_response:
                return cached_response
    
    def after_request(self, response):
        """Executar após cada requisição"""
        # Calcular tempo de resposta
        if hasattr(g, 'start_time'):
            response_time = time.time() - g.start_time
            response.headers['X-Response-Time'] = f"{response_time:.3f}s"
            
            # Log performance lenta
            if response_time > 1.0:
                logger.warning("Slow response detected",
                             path=request.path,
                             method=request.method,
                             response_time=response_time,
                             status_code=response.status_code)
        
        # Adicionar headers de cache
        response = self.add_cache_headers(response)
        
        # Comprimir resposta se necessário
        response = self.compress_response(response)
        
        # Cache response para GET requests bem-sucedidas
        if (request.method == 'GET' and 
            response.status_code == 200 and 
            self.is_cacheable(request.path)):
            self.cache_response(response)
        
        return response
    
    def setup_cache(self, app):
        """Configurar sistema de cache"""
        # Configurações de cache por endpoint
        self.cache_config = {
            '/api/health': {'ttl': 60},  # 1 minuto
            '/api/status': {'ttl': 30},  # 30 segundos
            '/static/': {'ttl': 3600},   # 1 hora
        }
    
    def get_cache_key(self, path: str, query_string: str = '') -> str:
        """Gerar chave de cache"""
        return f"cache:{path}:{query_string}"
    
    def get_cached_response(self) -> Optional[Any]:
        """Obter resposta do cache"""
        cache_key = self.get_cache_key(request.path, request.query_string.decode())
        
        if cache_key in self.cache:
            # Verificar TTL
            if cache_key in self.cache_ttl:
                if datetime.now() > self.cache_ttl[cache_key]:
                    # Cache expirado
                    del self.cache[cache_key]
                    del self.cache_ttl[cache_key]
                    return None
            
            cached_data = self.cache[cache_key]
            logger.info("Cache hit", path=request.path, cache_key=cache_key)
            
            # Retornar resposta cached
            response = jsonify(cached_data['data'])
            response.status_code = cached_data['status_code']
            response.headers['X-Cache'] = 'HIT'
            return response
        
        return None
    
    def cache_response(self, response):
        """Armazenar resposta no cache"""
        cache_key = self.get_cache_key(request.path, request.query_string.decode())
        
        # Verificar se deve ser cached
        if not self.is_cacheable(request.path):
            return
        
        # Obter TTL
        ttl = self.get_cache_ttl(request.path)
        if ttl <= 0:
            return
        
        try:
            # Armazenar dados
            cached_data = {
                'data': response.get_json() if response.is_json else response.get_data(as_text=True),
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'cached_at': datetime.now().isoformat()
            }
            
            self.cache[cache_key] = cached_data
            self.cache_ttl[cache_key] = datetime.now() + timedelta(seconds=ttl)
            
            logger.info("Response cached", 
                       path=request.path, 
                       cache_key=cache_key, 
                       ttl=ttl)
            
        except Exception as e:
            logger.error("Error caching response", error=str(e))
    
    def is_cacheable(self, path: str) -> bool:
        """Verificar se path pode ser cached"""
        # Não cachear endpoints de automação
        non_cacheable = [
            '/api/automation/',
            '/api/auth/',
            '/api/stats'
        ]
        
        for pattern in non_cacheable:
            if path.startswith(pattern):
                return False
        
        return True
    
    def get_cache_ttl(self, path: str) -> int:
        """Obter TTL para path"""
        for pattern, config in self.cache_config.items():
            if path.startswith(pattern):
                return config['ttl']
        
        # TTL padrão
        return 300  # 5 minutos
    
    def add_cache_headers(self, response):
        """Adicionar headers de cache"""
        if request.method == 'GET' and response.status_code == 200:
            if self.is_cacheable(request.path):
                ttl = self.get_cache_ttl(request.path)
                response.headers['Cache-Control'] = f'public, max-age={ttl}'
                response.headers['Expires'] = (
                    datetime.now() + timedelta(seconds=ttl)
                ).strftime('%a, %d %b %Y %H:%M:%S GMT')
            else:
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
        
        return response
    
    def compress_response(self, response):
        """Comprimir resposta se suportado"""
        # Verificar se cliente suporta gzip
        accept_encoding = request.headers.get('Accept-Encoding', '')
        if 'gzip' not in accept_encoding:
            return response
        
        # Verificar se resposta deve ser comprimida
        if (response.content_length and response.content_length < 1024):
            return response  # Não comprimir respostas pequenas
        
        content_type = response.headers.get('Content-Type', '')
        compressible_types = [
            'application/json',
            'text/html',
            'text/css',
            'text/javascript',
            'application/javascript'
        ]
        
        if not any(ct in content_type for ct in compressible_types):
            return response
        
        try:
            # Comprimir dados
            data = response.get_data()
            compressed_data = gzip.compress(data)
            
            # Verificar se compressão vale a pena
            if len(compressed_data) >= len(data) * 0.9:
                return response
            
            response.set_data(compressed_data)
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Content-Length'] = len(compressed_data)
            response.headers['Vary'] = 'Accept-Encoding'
            
            logger.debug("Response compressed",
                        original_size=len(data),
                        compressed_size=len(compressed_data),
                        ratio=f"{len(compressed_data)/len(data):.2%}")
            
        except Exception as e:
            logger.error("Error compressing response", error=str(e))
        
        return response
    
    def clear_cache(self, pattern: str = None):
        """Limpar cache"""
        if pattern:
            # Limpar cache específico
            keys_to_remove = [key for key in self.cache.keys() if pattern in key]
            for key in keys_to_remove:
                del self.cache[key]
                if key in self.cache_ttl:
                    del self.cache_ttl[key]
            logger.info("Cache cleared", pattern=pattern, keys_removed=len(keys_to_remove))
        else:
            # Limpar todo o cache
            cache_size = len(self.cache)
            self.cache.clear()
            self.cache_ttl.clear()
            logger.info("All cache cleared", keys_removed=cache_size)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Obter estatísticas do cache"""
        now = datetime.now()
        expired_keys = [
            key for key, expiry in self.cache_ttl.items()
            if now > expiry
        ]
        
        return {
            'total_keys': len(self.cache),
            'expired_keys': len(expired_keys),
            'active_keys': len(self.cache) - len(expired_keys),
            'memory_usage_estimate': sum(
                len(str(data)) for data in self.cache.values()
            )
        }


def cache_response(ttl: int = 300):
    """Decorator para cache de resposta"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar cache
            cache_key = f"func_cache:{f.__name__}:{hash(str(args) + str(kwargs))}"
            
            if hasattr(g, 'performance_middleware'):
                cached = g.performance_middleware.cache.get(cache_key)
                if cached and cache_key in g.performance_middleware.cache_ttl:
                    if datetime.now() <= g.performance_middleware.cache_ttl[cache_key]:
                        return cached
            
            # Executar função
            result = f(*args, **kwargs)
            
            # Armazenar no cache
            if hasattr(g, 'performance_middleware'):
                g.performance_middleware.cache[cache_key] = result
                g.performance_middleware.cache_ttl[cache_key] = (
                    datetime.now() + timedelta(seconds=ttl)
                )
            
            return result
        
        return decorated_function
    return decorator


def measure_time(operation_name: str = None):
    """Decorator para medir tempo de execução"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = f(*args, **kwargs)
                return result
            finally:
                execution_time = time.time() - start_time
                op_name = operation_name or f.__name__
                
                logger.info("Operation completed",
                           operation=op_name,
                           execution_time=f"{execution_time:.3f}s")
                
                # Log operações lentas
                if execution_time > 0.5:
                    logger.warning("Slow operation detected",
                                 operation=op_name,
                                 execution_time=execution_time)
        
        return decorated_function
    return decorator


# Instância global do middleware
performance_middleware = PerformanceMiddleware()
