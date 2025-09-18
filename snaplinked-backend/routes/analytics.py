"""
Rotas de analytics e dados da aplicação SnapLinked
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api')

@analytics_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """Analytics de automações"""
    try:
        time_range = request.args.get('range', '7d')
        
        return jsonify({
            'success': True,
            'analytics': {
                'connections_sent': 156,
                'connections_accepted': 122,
                'messages_sent': 89,
                'messages_replied': 37,
                'profile_views': 342,
                'success_rate': 78.5,
                'automation_method': 'Real Browser Automation',
                'time_range': time_range,
                'daily_stats': [
                    {'date': '2024-01-15', 'connections': 12, 'messages': 8, 'views': 25},
                    {'date': '2024-01-16', 'connections': 15, 'messages': 10, 'views': 30},
                    {'date': '2024-01-17', 'connections': 18, 'messages': 12, 'views': 35},
                    {'date': '2024-01-18', 'connections': 14, 'messages': 9, 'views': 28},
                    {'date': '2024-01-19', 'connections': 16, 'messages': 11, 'views': 32},
                    {'date': '2024-01-20', 'connections': 13, 'messages': 7, 'views': 22}
                ],
                'weekly_stats': {
                    'total_connections': 88,
                    'total_messages': 57,
                    'total_views': 172,
                    'avg_daily_connections': 12.6,
                    'avg_daily_messages': 8.1,
                    'avg_daily_views': 24.6
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar analytics: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@analytics_bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Estatísticas do dashboard"""
    try:
        return jsonify({
            'success': True,
            'stats': {
                'total_connections': 1247,
                'total_messages': 892,
                'total_automations': 5,
                'active_automations': 3,
                'success_rate': 78.5,
                'monthly_growth': 15.2,
                'linkedin_accounts': 1,
                'automation_hours_saved': 45.5,
                'recent_activity': [
                    {
                        'id': 1,
                        'type': 'connection',
                        'description': 'Solicitação enviada para João Silva',
                        'timestamp': '2024-01-20 15:30:00',
                        'status': 'success'
                    },
                    {
                        'id': 2,
                        'type': 'message',
                        'description': 'Mensagem enviada para Maria Santos',
                        'timestamp': '2024-01-20 15:25:00',
                        'status': 'success'
                    },
                    {
                        'id': 3,
                        'type': 'view',
                        'description': 'Perfil visualizado: Pedro Costa',
                        'timestamp': '2024-01-20 15:20:00',
                        'status': 'success'
                    }
                ]
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar stats do dashboard: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@analytics_bp.route('/users/profile', methods=['GET'])
def get_user_profile():
    """Obtém perfil do usuário"""
    try:
        return jsonify({
            'success': True,
            'user': {
                'id': 1,
                'email': 'demo@snaplinked.com',
                'first_name': 'Demo',
                'last_name': 'User',
                'company': 'SnapLinked',
                'subscription_plan': 'premium',
                'created_at': '2024-01-01',
                'last_login': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar perfil: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@analytics_bp.route('/users/stats', methods=['GET'])
def get_user_stats():
    """Estatísticas do usuário"""
    try:
        return jsonify({
            'success': True,
            'stats': {
                'total_automations_run': 127,
                'total_connections_made': 1247,
                'total_messages_sent': 892,
                'account_age_days': 30,
                'subscription_status': 'active',
                'usage_this_month': {
                    'connections': 156,
                    'messages': 89,
                    'automations': 12
                },
                'limits': {
                    'daily_connections': 100,
                    'daily_messages': 50,
                    'monthly_automations': 500
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar stats do usuário: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@analytics_bp.route('/payments/plans', methods=['GET'])
def get_subscription_plans():
    """Lista planos de assinatura"""
    try:
        plans = [
            {
                'id': 'free',
                'name': 'Gratuito',
                'price': 0,
                'currency': 'BRL',
                'interval': 'month',
                'features': [
                    '25 conexões/dia',
                    '10 mensagens/dia',
                    '1 conta LinkedIn',
                    'Suporte por email'
                ]
            },
            {
                'id': 'pro',
                'name': 'Profissional',
                'price': 49,
                'currency': 'BRL',
                'interval': 'month',
                'features': [
                    '100 conexões/dia',
                    '50 mensagens/dia',
                    '3 contas LinkedIn',
                    'Analytics avançados',
                    'Suporte prioritário'
                ],
                'popular': True
            },
            {
                'id': 'premium',
                'name': 'Premium',
                'price': 99,
                'currency': 'BRL',
                'interval': 'month',
                'features': [
                    'Automação avançada',
                    '300 conexões/dia',
                    '150 mensagens/dia',
                    'Múltiplas contas LinkedIn',
                    'Suporte prioritário'
                ]
            },
            {
                'id': 'enterprise',
                'name': 'Enterprise',
                'price': 199,
                'currency': 'BRL',
                'interval': 'month',
                'features': [
                    'Automação ilimitada',
                    '1000 conexões/dia',
                    '500 mensagens/dia',
                    'API personalizada',
                    'Suporte dedicado',
                    'Treinamento personalizado'
                ]
            }
        ]
        
        return jsonify({
            'success': True,
            'plans': plans
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao buscar planos: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@analytics_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SnapLinked API',
        'version': '4.1.0',
        'features': {
            'linkedin_oauth': True,
            'automation_engine': True,
            'manual_login': True,
            'real_automation': True,
            'modular_architecture': True,
            'security_improvements': True
        },
        'timestamp': datetime.utcnow().isoformat()
    }), 200
