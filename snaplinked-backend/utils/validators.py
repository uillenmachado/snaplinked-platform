"""
Utilitários de validação de dados
"""

import re
from typing import Dict, Any, List, Optional
from functools import wraps
from flask import request, jsonify

def validate_email(email: str) -> bool:
    """Valida formato de email"""
    # Padrão mais restritivo que não permite pontos consecutivos
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9._%-]*[a-zA-Z0-9])?@[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$'
    
    # Verificar se não há pontos consecutivos
    if '..' in email:
        return False
    
    # Verificar se não começa ou termina com ponto
    local_part = email.split('@')[0] if '@' in email else email
    if local_part.startswith('.') or local_part.endswith('.'):
        return False
    
    return re.match(pattern, email) is not None

def validate_password(password: str) -> Dict[str, Any]:
    """Valida força da senha"""
    errors = []
    
    if len(password) < 8:
        errors.append("Senha deve ter pelo menos 8 caracteres")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Senha deve conter pelo menos uma letra maiúscula")
    
    if not re.search(r'[a-z]', password):
        errors.append("Senha deve conter pelo menos uma letra minúscula")
    
    if not re.search(r'\d', password):
        errors.append("Senha deve conter pelo menos um número")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
    """Valida campos obrigatórios"""
    missing_fields = []
    
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    return {
        'valid': len(missing_fields) == 0,
        'missing_fields': missing_fields
    }

def validate_automation_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Valida configuração de automação"""
    errors = []
    
    # Validar tipo de automação
    valid_types = ['connection_requests', 'messages', 'profile_views']
    if config.get('type') not in valid_types:
        errors.append(f"Tipo deve ser um de: {', '.join(valid_types)}")
    
    # Validar palavras-chave
    keywords = config.get('keywords', '').strip()
    if not keywords:
        errors.append("Palavras-chave são obrigatórias")
    elif len(keywords) < 3:
        errors.append("Palavras-chave devem ter pelo menos 3 caracteres")
    
    # Validar limites
    max_actions = config.get('max_actions', 0)
    if not isinstance(max_actions, int) or max_actions < 1:
        errors.append("Número máximo de ações deve ser um inteiro positivo")
    elif max_actions > 100:
        errors.append("Número máximo de ações não pode exceder 100")
    
    # Validar mensagem (se fornecida)
    message = config.get('message', '')
    if message and len(message) > 300:
        errors.append("Mensagem não pode exceder 300 caracteres")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_json_request(required_fields: List[str] = None):
    """Decorator para validar requisições JSON"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar se é JSON
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Content-Type deve ser application/json'
                }), 400
            
            data = request.get_json()
            if not data:
                return jsonify({
                    'success': False,
                    'error': 'Dados JSON são obrigatórios'
                }), 400
            
            # Validar campos obrigatórios
            if required_fields:
                validation = validate_required_fields(data, required_fields)
                if not validation['valid']:
                    return jsonify({
                        'success': False,
                        'error': f"Campos obrigatórios ausentes: {', '.join(validation['missing_fields'])}"
                    }), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def sanitize_string(text: str, max_length: int = None) -> str:
    """Sanitiza string removendo caracteres perigosos"""
    if not isinstance(text, str):
        return ""
    
    # Remover caracteres de controle
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    # Limitar comprimento
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()

def validate_linkedin_credentials(email: str, password: str) -> Dict[str, Any]:
    """Valida credenciais do LinkedIn"""
    errors = []
    
    if not email:
        errors.append("Email é obrigatório")
    elif not validate_email(email):
        errors.append("Formato de email inválido")
    
    if not password:
        errors.append("Senha é obrigatória")
    elif len(password) < 6:
        errors.append("Senha deve ter pelo menos 6 caracteres")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }
