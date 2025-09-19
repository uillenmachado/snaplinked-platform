import re

def validate_email(email):
    """Valida o formato de um e-mail."""
    if not email:
        return False
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is not None and '..' not in email

def validate_password(password):
    """Valida a força de uma senha."""
    errors = []
    if len(password) < 8:
        errors.append("A senha deve ter pelo menos 8 caracteres.")
    if not re.search(r"[A-Z]", password):
        errors.append("A senha deve conter pelo menos uma letra maiúscula.")
    if not re.search(r"[a-z]", password):
        errors.append("A senha deve conter pelo menos uma letra minúscula.")
    if not re.search(r"\d", password):
        errors.append("A senha deve conter pelo menos um número.")
    return {'valid': not errors, 'errors': errors}

def validate_required_fields(data, required_fields):
    """Valida se os campos obrigatórios estão presentes."""
    missing_fields = [field for field in required_fields if not data.get(field)]
    return {'valid': not missing_fields, 'missing_fields': missing_fields}

def validate_automation_config(config):
    """Valida a configuração de uma automação."""
    errors = []
    if not config.get("type") or config.get("type") not in ["connection_requests", "send_messages"]:
        errors.append("Tipo deve ser um de: connection_requests, send_messages")
    if not config.get("keywords"):
        errors.append("Palavras-chave são obrigatórias.")
    if not isinstance(config.get("max_actions"), int) or not 1 <= config.get("max_actions") <= 100:
        errors.append("max_actions deve ser um número entre 1 e 100.")
    if config.get("message") and len(config.get("message")) > 300:
        errors.append("Mensagem não pode exceder 300 caracteres.")
    return {'valid': not errors, 'errors': errors}

def sanitize_string(text, max_length=None):
    """Sanitiza uma string, removendo caracteres de controle."""
    if not isinstance(text, str):
        return ""
    sanitized = "".join(char for char in text if char.isprintable())
    if max_length:
        return sanitized[:max_length].strip()
    return sanitized

def validate_linkedin_credentials(email, password):
    """Valida as credenciais do LinkedIn."""
    errors = []
    if not email:
        errors.append("Email é obrigatório.")
    elif not validate_email(email):
        errors.append("Formato de email inválido.")
    if not password:
        errors.append("Senha é obrigatória.")
    elif len(password) < 6:
        errors.append("Senha deve ter pelo menos 6 caracteres.")
    return {'valid': not errors, 'errors': errors}

