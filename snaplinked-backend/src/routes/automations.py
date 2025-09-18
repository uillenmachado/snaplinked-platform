"""
Rotas de automações da aplicação SnapLinked
"""

from flask import Blueprint, request, jsonify, session
from datetime import datetime
import logging
import asyncio

from services.linkedin_automation import automation_engine

logger = logging.getLogger(__name__)

automations_bp = Blueprint('automations', __name__, url_prefix='/api/automations')

@automations_bp.route('', methods=['GET'])
def get_automations():
    """Lista automações configuradas"""
    try:
        return jsonify({
            'success': True,
            'automations': [
                {
                    'id': 1,
                    'name': 'Conexões Tech',
                    'type': 'connection_requests',
                    'status': 'active',
                    'keywords': 'desenvolvedor, programador, tech',
                    'daily_limit': 50,
                    'used_today': 23,
                    'success_rate': 78.5,
                    'automation_type': 'real_browser',
                    'created_at': '2024-01-15',
                    'last_run': '2024-01-20 15:30'
                },
                {
                    'id': 2,
                    'name': 'Mensagens Follow-up',
                    'type': 'messages',
                    'status': 'paused',
                    'keywords': 'CEO, founder, startup',
                    'daily_limit': 25,
                    'used_today': 0,
                    'success_rate': 82.1,
                    'automation_type': 'real_browser',
                    'created_at': '2024-01-10',
                    'last_run': '2024-01-19 14:20'
                }
            ]
        })
        
    except Exception as e:
        logger.error(f"Erro ao listar automações: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@automations_bp.route('/run', methods=['POST'])
def run_automation():
    """Executa automação LinkedIn"""
    try:
        if not session.get('linkedin_manual_connected'):
            return jsonify({
                'success': False,
                'error': 'Login manual necessário para automações'
            }), 400
        
        data = request.get_json()
        automation_config = {
            'type': data.get('type', 'connection_requests'),
            'keywords': data.get('keywords', ''),
            'max_actions': data.get('max_actions', 25),
            'message': data.get('message', '')
        }
        
        # Validar configuração
        if not automation_config['keywords']:
            return jsonify({
                'success': False,
                'error': 'Palavras-chave são obrigatórias'
            }), 400
        
        # Executar automação
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(automation_engine.run_automation(automation_config))
            return jsonify(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Erro na automação: {e}")
        return jsonify({
            'success': False,
            'error': f'Erro na automação: {str(e)}'
        }), 500

@automations_bp.route('/stats', methods=['GET'])
def get_automation_stats():
    """Obtém estatísticas de automação"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(automation_engine.get_stats())
            return jsonify(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Erro ao buscar stats: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno'
        }), 500

@automations_bp.route('', methods=['POST'])
def create_automation():
    """Cria nova automação"""
    try:
        data = request.get_json()
        
        # Validação básica
        required_fields = ['name', 'type', 'keywords']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Campo {field} é obrigatório'
                }), 400
        
        # Simular criação
        new_automation = {
            'id': len([]) + 1,  # Simular ID
            'name': data['name'],
            'type': data['type'],
            'status': 'active',
            'keywords': data['keywords'],
            'daily_limit': data.get('daily_limit', 50),
            'used_today': 0,
            'success_rate': 0,
            'automation_type': 'real_browser',
            'created_at': datetime.now().strftime('%Y-%m-%d'),
            'last_run': None
        }
        
        return jsonify({
            'success': True,
            'message': 'Automação criada com sucesso',
            'automation': new_automation
        }), 201
        
    except Exception as e:
        logger.error(f"Erro ao criar automação: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@automations_bp.route('/<int:automation_id>', methods=['PUT'])
def update_automation(automation_id):
    """Atualiza automação existente"""
    try:
        data = request.get_json()
        
        # Simular atualização
        return jsonify({
            'success': True,
            'message': 'Automação atualizada com sucesso'
        })
        
    except Exception as e:
        logger.error(f"Erro ao atualizar automação: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@automations_bp.route('/<int:automation_id>', methods=['DELETE'])
def delete_automation(automation_id):
    """Remove automação"""
    try:
        # Simular remoção
        return jsonify({
            'success': True,
            'message': 'Automação removida com sucesso'
        })
        
    except Exception as e:
        logger.error(f"Erro ao remover automação: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@automations_bp.route('/<int:automation_id>/toggle', methods=['POST'])
def toggle_automation(automation_id):
    """Ativa/desativa automação"""
    try:
        # Simular toggle
        return jsonify({
            'success': True,
            'message': 'Status da automação alterado com sucesso'
        })
        
    except Exception as e:
        logger.error(f"Erro ao alterar status: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500
