#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapLinked v3.0 - Middleware de Segurança
Implementação de headers de segurança, rate limiting e validação
"""

import time
import hashlib
import secrets
from functools import wraps
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from flask import request, jsonify, g, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import structlog

# Configurar logging estruturado
logger = structlog.get_logger(__name__)

# Rate limiter global
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per hour", "100 per minute"]
)


class SecurityMiddleware:
    """Middleware de segurança para Flask"""
    
    def __init__(self, app=None):
        self.app = app
        self.blocked_ips = set()
        self.rate_limit_storage = {}
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializar middleware com aplicação Flask"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        
        # Configurar rate limiter
        limiter.init_app(app)
        
        # Configurar CSP
        self.setup_csp(app)
    
    def before_request(self):
        """Executar antes de cada requisição"""
        # Verificar IP bloqueado
        if self.is_ip_blocked(request.remote_addr):
            logger.warning("Blocked IP attempted access", ip=request.remote_addr)
            return jsonify({'error': 'Access denied'}), 403
        
        # Validar headers de segurança
        if not self.validate_security_headers():
            return jsonify({'error': 'Invalid security headers'}), 400
        
        # Verificar CSRF para métodos não-seguros
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            if not self.validate_csrf_token():
                logger.warning("CSRF validation failed", 
                             ip=request.remote_addr, 
                             endpoint=request.endpoint)
                return jsonify({'error': 'CSRF token invalid'}), 403
        
        # Log da requisição
        g.request_start_time = time.time()
        logger.info("Request started",
                   method=request.method,
                   path=request.path,
                   ip=request.remote_addr,
                   user_agent=request.headers.get('User-Agent', ''))
    
    def after_request(self, response):
        """Executar após cada requisição"""
        # Adicionar headers de segurança
        response = self.add_security_headers(response)
        
        # Log da resposta
        if hasattr(g, 'request_start_time'):
            duration = time.time() - g.request_start_time
            logger.info("Request completed",
                       status_code=response.status_code,
                       duration=f"{duration:.3f}s",
                       content_length=response.content_length)
        
        return response
    
    def add_security_headers(self, response):
        """Adicionar headers de segurança"""
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # XSS Protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response.headers['Permissions-Policy'] = (
            'geolocation=(), microphone=(), camera=(), '
            'payment=(), usb=(), magnetometer=(), gyroscope=()'
        )
        
        # HSTS (apenas em HTTPS)
        if request.is_secure:
            response.headers['Strict-Transport-Security'] = (
                'max-age=31536000; includeSubDomains; preload'
            )
        
        # Content Security Policy
        if not response.headers.get('Content-Security-Policy'):
            response.headers['Content-Security-Policy'] = self.get_csp_header()
        
        return response
    
    def get_csp_header(self) -> str:
        """Gerar header Content Security Policy"""
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.linkedin.com",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com",
            "img-src 'self' data: https: blob:",
            "connect-src 'self' https://api.linkedin.com https://www.linkedin.com",
            "frame-src 'self' https://www.linkedin.com",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "frame-ancestors 'self'",
            "upgrade-insecure-requests"
        ]
        return "; ".join(csp_directives)
    
    def setup_csp(self, app):
        """Configurar Content Security Policy"""
        @app.route('/api/csp-report', methods=['POST'])
        def csp_report():
            """Endpoint para receber relatórios de violação CSP"""
            try:
                report = request.get_json()
                logger.warning("CSP violation reported", report=report)
                return '', 204
            except Exception as e:
                logger.error("Error processing CSP report", error=str(e))
                return '', 400
    
    def validate_security_headers(self) -> bool:
        """Validar headers de segurança obrigatórios"""
        # Verificar User-Agent suspeito
        user_agent = request.headers.get('User-Agent', '')
        suspicious_agents = ['bot', 'crawler', 'spider', 'scraper']
        
        if any(agent in user_agent.lower() for agent in suspicious_agents):
            # Permitir apenas bots conhecidos
            allowed_bots = ['googlebot', 'bingbot', 'slurp']
            if not any(bot in user_agent.lower() for bot in allowed_bots):
                return False
        
        # Verificar Content-Length para uploads
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_length = request.content_length
            if content_length and content_length > 10 * 1024 * 1024:  # 10MB
                logger.warning("Large request detected", 
                             size=content_length, 
                             ip=request.remote_addr)
                return False
        
        return True
    
    def validate_csrf_token(self) -> bool:
        """Validar token CSRF"""
        # Para APIs, verificar header personalizado
        if request.path.startswith('/api/'):
            csrf_header = request.headers.get('X-CSRF-Token')
            if not csrf_header:
                return False
            
            # Verificar se token é válido (implementar lógica específica)
            return self.verify_csrf_token(csrf_header)
        
        # Para formulários, verificar token no corpo
        csrf_token = request.form.get('csrf_token') or request.json.get('csrf_token')
        if not csrf_token:
            return False
        
        return self.verify_csrf_token(csrf_token)
    
    def verify_csrf_token(self, token: str) -> bool:
        """Verificar validade do token CSRF"""
        try:
            # Implementar verificação de token CSRF
            # Por enquanto, aceitar qualquer token não-vazio
            return len(token) > 10
        except Exception:
            return False
    
    def is_ip_blocked(self, ip: str) -> bool:
        """Verificar se IP está bloqueado"""
        return ip in self.blocked_ips
    
    def block_ip(self, ip: str, reason: str = "Security violation"):
        """Bloquear IP"""
        self.blocked_ips.add(ip)
        logger.warning("IP blocked", ip=ip, reason=reason)
    
    def unblock_ip(self, ip: str):
        """Desbloquear IP"""
        self.blocked_ips.discard(ip)
        logger.info("IP unblocked", ip=ip)


class InputValidator:
    """Validador de entrada para APIs"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validar formato de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_string(value: str, min_length: int = 1, max_length: int = 255) -> bool:
        """Validar string"""
        if not isinstance(value, str):
            return False
        return min_length <= len(value.strip()) <= max_length
    
    @staticmethod
    def validate_integer(value: Any, min_val: int = None, max_val: int = None) -> bool:
        """Validar inteiro"""
        try:
            val = int(value)
            if min_val is not None and val < min_val:
                return False
            if max_val is not None and val > max_val:
                return False
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def sanitize_string(value: str) -> str:
        """Sanitizar string removendo caracteres perigosos"""
        import html
        # Escapar HTML
        value = html.escape(value)
        # Remover caracteres de controle
        value = ''.join(char for char in value if ord(char) >= 32 or char in '\t\n\r')
        return value.strip()


def require_valid_input(schema: Dict[str, Any]):
    """Decorator para validar entrada de APIs"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json() or {}
            
            # Validar cada campo do schema
            for field, rules in schema.items():
                value = data.get(field)
                
                # Verificar se campo é obrigatório
                if rules.get('required', False) and value is None:
                    return jsonify({
                        'error': f'Campo "{field}" é obrigatório'
                    }), 400
                
                # Validar tipo
                if value is not None:
                    field_type = rules.get('type', str)
                    if not isinstance(value, field_type):
                        return jsonify({
                            'error': f'Campo "{field}" deve ser do tipo {field_type.__name__}'
                        }), 400
                    
                    # Validações específicas
                    if field_type == str:
                        min_len = rules.get('min_length', 1)
                        max_len = rules.get('max_length', 255)
                        if not InputValidator.validate_string(value, min_len, max_len):
                            return jsonify({
                                'error': f'Campo "{field}" deve ter entre {min_len} e {max_len} caracteres'
                            }), 400
                        
                        # Sanitizar string
                        data[field] = InputValidator.sanitize_string(value)
                    
                    elif field_type == int:
                        min_val = rules.get('min_value')
                        max_val = rules.get('max_value')
                        if not InputValidator.validate_integer(value, min_val, max_val):
                            return jsonify({
                                'error': f'Campo "{field}" deve ser um inteiro válido'
                            }), 400
            
            # Adicionar dados validados ao request
            request.validated_data = data
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def generate_csrf_token() -> str:
    """Gerar token CSRF seguro"""
    return secrets.token_urlsafe(32)


def secure_random_string(length: int = 32) -> str:
    """Gerar string aleatória segura"""
    return secrets.token_urlsafe(length)


def hash_password(password: str) -> str:
    """Hash seguro de senha"""
    import bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verificar senha"""
    import bcrypt
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


# Instância global do middleware
security_middleware = SecurityMiddleware()
