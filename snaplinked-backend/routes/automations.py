"""
Rotas de automações da aplicação SnapLinked
"""

from flask import Blueprint, request, jsonify, session
from datetime import datetime
import logging
import asyncio
import json

# Import correto do engine de automação
from linkedin_automation_engine import automation_engine

logger = logging.getLogger(__name__)

automations_bp = Blueprint('automations', __name__, url_prefix='/api/automations')

# Armazenamento temporário de automações (em produção usar banco de dados)
automations_storage = []

@automations_bp.route('', methods=['GET'])
def get_automations():
    """Lista automações configuradas"""
    try:
        # Retornar automações reais do storage
        return jsonify({
            'success': True,
            'automations': automations_storage
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
            'message': data.get('message', ''),
            'comment_templates': data.get('comment_templates', [])
        }
        
        # Validar configuração baseada no tipo
        if automation_config['type'] in ['connection_requests', 'profile_views']:
            if not automation_config['keywords']:
                return jsonify({
                    'success': False,
                    'error': 'Palavras-chave são obrigatórias para este tipo de automação'
                }), 400
        
        # Executar automação real
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

@automations_bp.route('/feed/interact', methods=['POST'])
def interact_with_feed():
    """Executa interações no feed (curtidas e comentários)"""
    try:
        if not session.get('linkedin_manual_connected'):
            return jsonify({
                'success': False,
                'error': 'Login manual necessário para automações'
            }), 400
        
        data = request.get_json()
        max_interactions = data.get('max_interactions', 15)
        like_probability = data.get('like_probability', 0.7)
        comment_probability = data.get('comment_probability', 0.3)
        
        # Executar interação com feed
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                automation_engine.interact_with_feed(
                    max_interactions, 
                    like_probability, 
                    comment_probability
                )
            )
            return jsonify(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Erro na interação com feed: {e}")
        return jsonify({
            'success': False,
            'error': f'Erro na interação com feed: {str(e)}'
        }), 500

@automations_bp.route('/feed/like', methods=['POST'])
def like_feed_posts():
    """Curte posts no feed"""
    try:
        if not session.get('linkedin_manual_connected'):
            return jsonify({
                'success': False,
                'error': 'Login manual necessário para automações'
            }), 400
        
        data = request.get_json()
        max_likes = data.get('max_likes', 10)
        
        # Executar curtidas no feed
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(automation_engine.like_posts_in_feed(max_likes))
            return jsonify(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Erro ao curtir posts: {e}")
        return jsonify({
            'success': False,
            'error': f'Erro ao curtir posts: {str(e)}'
        }), 500

@automations_bp.route('/feed/comment', methods=['POST'])
def comment_feed_posts():
    """Comenta em posts do feed"""
    try:
        if not session.get('linkedin_manual_connected'):
            return jsonify({
                'success': False,
                'error': 'Login manual necessário para automações'
            }), 400
        
        data = request.get_json()
        max_comments = data.get('max_comments', 5)
        comment_templates = data.get('comment_templates', [])
        
        # Executar comentários no feed
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                automation_engine.comment_on_posts(max_comments, comment_templates)
            )
            return jsonify(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Erro ao comentar posts: {e}")
        return jsonify({
            'success': False,
            'error': f'Erro ao comentar posts: {str(e)}'
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
        required_fields = ['name', 'type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Campo {field} é obrigatório'
                }), 400
        
        # Validar tipo de automação
        valid_types = [
            'connection_requests', 
            'profile_views', 
            'feed_interactions', 
            'feed_likes', 
            'feed_comments'
        ]
        
        if data['type'] not in valid_types:
            return jsonify({
                'success': False,
                'error': f'Tipo de automação inválido. Tipos válidos: {", ".join(valid_types)}'
            }), 400
        
        # Validar campos específicos por tipo
        if data['type'] in ['connection_requests', 'profile_views']:
            if not data.get('keywords'):
                return jsonify({
                    'success': False,
                    'error': 'Palavras-chave são obrigatórias para este tipo de automação'
                }), 400
        
        # Criar nova automação
        new_automation = {
            'id': len(automations_storage) + 1,
            'name': data['name'],
            'type': data['type'],
            'status': 'active',
            'keywords': data.get('keywords', ''),
            'daily_limit': data.get('daily_limit', 50),
            'used_today': 0,
            'success_rate': 0,
            'automation_type': 'real_browser',
            'created_at': datetime.now().strftime('%Y-%m-%d'),
            'last_run': None,
            'message': data.get('message', ''),
            'comment_templates': data.get('comment_templates', [])
        }
        
        # Adicionar ao storage
        automations_storage.append(new_automation)
        
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

@automations_bp.route('/<int:automation_id>/execute', methods=['POST'])
def execute_automation(automation_id):
    """Executa uma automação específica"""
    try:
        if not session.get('linkedin_manual_connected'):
            return jsonify({
                'success': False,
                'error': 'Login manual necessário para automações'
            }), 400
        
        # Encontrar automação
        automation = None
        for auto in automations_storage:
            if auto['id'] == automation_id:
                automation = auto
                break
        
        if not automation:
            return jsonify({
                'success': False,
                'error': 'Automação não encontrada'
            }), 404
        
        # Configurar automação
        automation_config = {
            'type': automation['type'],
            'keywords': automation.get('keywords', ''),
            'max_actions': automation.get('daily_limit', 25),
            'message': automation.get('message', ''),
            'comment_templates': automation.get('comment_templates', [])
        }
        
        # Executar automação
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(automation_engine.run_automation(automation_config))
            
            # Atualizar estatísticas da automação
            if result.get('success'):
                automation['last_run'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                automation['used_today'] += result.get('total_interactions', 1)
            
            return jsonify(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Erro ao executar automação: {e}")
        return jsonify({
            'success': False,
            'error': f'Erro ao executar automação: {str(e)}'
        }), 500

@automations_bp.route('/<int:automation_id>', methods=['PUT'])
def update_automation(automation_id):
    """Atualiza automação existente"""
    try:
        data = request.get_json()
        
        # Encontrar automação
        automation = None
        for auto in automations_storage:
            if auto['id'] == automation_id:
                automation = auto
                break
        
        if not automation:
            return jsonify({
                'success': False,
                'error': 'Automação não encontrada'
            }), 404
        
        # Atualizar campos
        updatable_fields = ['name', 'keywords', 'daily_limit', 'message', 'comment_templates', 'status']
        for field in updatable_fields:
            if field in data:
                automation[field] = data[field]
        
        return jsonify({
            'success': True,
            'message': 'Automação atualizada com sucesso',
            'automation': automation
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
        # Encontrar e remover automação
        global automations_storage
        automations_storage = [auto for auto in automations_storage if auto['id'] != automation_id]
        
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
        # Encontrar automação
        automation = None
        for auto in automations_storage:
            if auto['id'] == automation_id:
                automation = auto
                break
        
        if not automation:
            return jsonify({
                'success': False,
                'error': 'Automação não encontrada'
            }), 404
        
        # Alternar status
        automation['status'] = 'paused' if automation['status'] == 'active' else 'active'
        
        return jsonify({
            'success': True,
            'message': f'Automação {"ativada" if automation["status"] == "active" else "pausada"} com sucesso',
            'automation': automation
        })
        
    except Exception as e:
        logger.error(f"Erro ao alterar status: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@automations_bp.route('/types', methods=['GET'])
def get_automation_types():
    """Lista tipos de automação disponíveis"""
    try:
        automation_types = [
            {
                'id': 'connection_requests',
                'name': 'Solicitações de Conexão',
                'description': 'Envia solicitações de conexão para perfis encontrados por palavras-chave',
                'requires_keywords': True,
                'supports_message': True
            },
            {
                'id': 'profile_views',
                'name': 'Visualização de Perfis',
                'description': 'Visualiza perfis encontrados por palavras-chave',
                'requires_keywords': True,
                'supports_message': False
            },
            {
                'id': 'feed_interactions',
                'name': 'Interações no Feed',
                'description': 'Curte e comenta posts no feed do LinkedIn',
                'requires_keywords': False,
                'supports_message': False
            },
            {
                'id': 'feed_likes',
                'name': 'Curtidas no Feed',
                'description': 'Curte posts no feed do LinkedIn',
                'requires_keywords': False,
                'supports_message': False
            },
            {
                'id': 'feed_comments',
                'name': 'Comentários no Feed',
                'description': 'Comenta em posts do feed do LinkedIn',
                'requires_keywords': False,
                'supports_message': False
            }
        ]
        
        return jsonify({
            'success': True,
            'types': automation_types
        })
        
    except Exception as e:
        logger.error(f"Erro ao listar tipos: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500
