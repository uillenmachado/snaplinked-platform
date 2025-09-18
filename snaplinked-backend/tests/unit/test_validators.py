"""
Testes unitários para utilitários de validação
"""

import pytest
import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from utils.validators import (
    validate_email,
    validate_password,
    validate_required_fields,
    validate_automation_config,
    sanitize_string,
    validate_linkedin_credentials
)

class TestValidators:
    """Testes para funções de validação"""
    
    def test_validate_email_valid(self):
        """Testa validação de email válido"""
        valid_emails = [
            'test@example.com',
            'user.name@domain.co.uk',
            'user+tag@example.org',
            'user123@test-domain.com'
        ]
        
        for email in valid_emails:
            assert validate_email(email) is True
    
    def test_validate_email_invalid(self):
        """Testa validação de email inválido"""
        invalid_emails = [
            'invalid-email',
            '@example.com',
            'user@',
            'user@.com',
            'user..name@example.com',
            ''
        ]
        
        for email in invalid_emails:
            assert validate_email(email) is False
    
    def test_validate_password_strong(self):
        """Testa validação de senha forte"""
        strong_password = 'StrongPass123'
        result = validate_password(strong_password)
        
        assert result['valid'] is True
        assert len(result['errors']) == 0
    
    def test_validate_password_weak(self):
        """Testa validação de senha fraca"""
        weak_passwords = [
            'weak',  # Muito curta
            'weakpassword',  # Sem maiúscula e número
            'WEAKPASSWORD',  # Sem minúscula e número
            'WeakPassword',  # Sem número
            'weakpass123'  # Sem maiúscula
        ]
        
        for password in weak_passwords:
            result = validate_password(password)
            assert result['valid'] is False
            assert len(result['errors']) > 0
    
    def test_validate_required_fields_valid(self):
        """Testa validação de campos obrigatórios válidos"""
        data = {
            'name': 'Test',
            'email': 'test@example.com',
            'password': 'password123'
        }
        required_fields = ['name', 'email', 'password']
        
        result = validate_required_fields(data, required_fields)
        
        assert result['valid'] is True
        assert len(result['missing_fields']) == 0
    
    def test_validate_required_fields_missing(self):
        """Testa validação com campos obrigatórios ausentes"""
        data = {
            'name': 'Test',
            'email': ''  # Campo vazio
            # password ausente
        }
        required_fields = ['name', 'email', 'password']
        
        result = validate_required_fields(data, required_fields)
        
        assert result['valid'] is False
        assert 'email' in result['missing_fields']
        assert 'password' in result['missing_fields']
    
    def test_validate_automation_config_valid(self):
        """Testa validação de configuração de automação válida"""
        config = {
            'type': 'connection_requests',
            'keywords': 'desenvolvedor python',
            'max_actions': 25,
            'message': 'Olá! Gostaria de conectar.'
        }
        
        result = validate_automation_config(config)
        
        assert result['valid'] is True
        assert len(result['errors']) == 0
    
    def test_validate_automation_config_invalid_type(self):
        """Testa validação com tipo de automação inválido"""
        config = {
            'type': 'invalid_type',
            'keywords': 'desenvolvedor python',
            'max_actions': 25
        }
        
        result = validate_automation_config(config)
        
        assert result['valid'] is False
        assert any('Tipo deve ser um de' in error for error in result['errors'])
    
    def test_validate_automation_config_missing_keywords(self):
        """Testa validação sem palavras-chave"""
        config = {
            'type': 'connection_requests',
            'keywords': '',
            'max_actions': 25
        }
        
        result = validate_automation_config(config)
        
        assert result['valid'] is False
        assert any('Palavras-chave são obrigatórias' in error for error in result['errors'])
    
    def test_validate_automation_config_invalid_max_actions(self):
        """Testa validação com max_actions inválido"""
        configs = [
            {
                'type': 'connection_requests',
                'keywords': 'test',
                'max_actions': 0  # Muito baixo
            },
            {
                'type': 'connection_requests',
                'keywords': 'test',
                'max_actions': 150  # Muito alto
            },
            {
                'type': 'connection_requests',
                'keywords': 'test',
                'max_actions': 'invalid'  # Tipo inválido
            }
        ]
        
        for config in configs:
            result = validate_automation_config(config)
            assert result['valid'] is False
    
    def test_validate_automation_config_long_message(self):
        """Testa validação com mensagem muito longa"""
        config = {
            'type': 'connection_requests',
            'keywords': 'test',
            'max_actions': 25,
            'message': 'x' * 301  # Muito longa
        }
        
        result = validate_automation_config(config)
        
        assert result['valid'] is False
        assert any('Mensagem não pode exceder 300 caracteres' in error for error in result['errors'])
    
    def test_sanitize_string_normal(self):
        """Testa sanitização de string normal"""
        text = "Normal text with spaces"
        result = sanitize_string(text)
        
        assert result == text
    
    def test_sanitize_string_with_control_chars(self):
        """Testa sanitização removendo caracteres de controle"""
        text = "Text\x00with\x1fcontrol\x7fchars"
        result = sanitize_string(text)
        
        assert result == "Textwithcontrolchars"
    
    def test_sanitize_string_max_length(self):
        """Testa sanitização com limite de comprimento"""
        text = "This is a very long text that should be truncated"
        result = sanitize_string(text, max_length=20)
        
        assert len(result) <= 20
        assert result == "This is a very long"
    
    def test_sanitize_string_non_string(self):
        """Testa sanitização de não-string"""
        result = sanitize_string(123)
        assert result == ""
        
        result = sanitize_string(None)
        assert result == ""
    
    def test_validate_linkedin_credentials_valid(self):
        """Testa validação de credenciais LinkedIn válidas"""
        result = validate_linkedin_credentials('test@example.com', 'password123')
        
        assert result['valid'] is True
        assert len(result['errors']) == 0
    
    def test_validate_linkedin_credentials_invalid_email(self):
        """Testa validação com email inválido"""
        result = validate_linkedin_credentials('invalid-email', 'password123')
        
        assert result['valid'] is False
        assert any('Formato de email inválido' in error for error in result['errors'])
    
    def test_validate_linkedin_credentials_short_password(self):
        """Testa validação com senha muito curta"""
        result = validate_linkedin_credentials('test@example.com', '123')
        
        assert result['valid'] is False
        assert any('Senha deve ter pelo menos 6 caracteres' in error for error in result['errors'])
    
    def test_validate_linkedin_credentials_empty_fields(self):
        """Testa validação com campos vazios"""
        result = validate_linkedin_credentials('', '')
        
        assert result['valid'] is False
        assert any('Email é obrigatório' in error for error in result['errors'])
        assert any('Senha é obrigatória' in error for error in result['errors'])
