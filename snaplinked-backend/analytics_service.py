"""
Serviço de Analytics para SnapLinked
Processa e fornece dados de desempenho das automações
"""

import json
from datetime import datetime, timedelta
from database import db
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self):
        self.db = db
    
    def process_automation_result(self, user_id, automation_type, result_data):
        """Processar resultado de automação e atualizar estatísticas"""
        try:
            # Extrair dados do resultado
            stats_update = {
                'connections_sent': 0,
                'messages_sent': 0,
                'profiles_viewed': 0,
                'likes_given': 0,
                'comments_posted': 0,
                'success_rate': 0.0
            }
            
            if automation_type == 'like_posts' and result_data.get('success'):
                stats_update['likes_given'] = result_data.get('likes_given', 0)
                stats_update['success_rate'] = 100.0 if result_data.get('likes_given', 0) > 0 else 0.0
                
            elif automation_type == 'comment_posts' and result_data.get('success'):
                stats_update['comments_posted'] = result_data.get('comments_posted', 0)
                stats_update['success_rate'] = 100.0 if result_data.get('comments_posted', 0) > 0 else 0.0
                
            elif automation_type == 'send_connections' and result_data.get('success'):
                stats_update['connections_sent'] = result_data.get('connections_sent', 0)
                stats_update['success_rate'] = 100.0 if result_data.get('connections_sent', 0) > 0 else 0.0
            
            # Atualizar estatísticas diárias
            current_stats = self.get_daily_stats(user_id)
            
            for key in stats_update:
                if key != 'success_rate':
                    current_stats[key] = current_stats.get(key, 0) + stats_update[key]
            
            # Calcular nova taxa de sucesso
            total_actions = (current_stats.get('connections_sent', 0) + 
                           current_stats.get('likes_given', 0) + 
                           current_stats.get('comments_posted', 0))
            
            if total_actions > 0:
                current_stats['success_rate'] = min(100.0, (total_actions / max(1, total_actions)) * 100)
            
            # Salvar estatísticas atualizadas
            self.db.update_daily_stats(user_id, current_stats)
            
            # Registrar atividade
            self.db.log_activity(
                user_id, 
                automation_type, 
                f"Automação executada: {automation_type}",
                result_data
            )
            
            logger.info(f"Estatísticas processadas para usuário {user_id}: {automation_type}")
            
        except Exception as e:
            logger.error(f"Erro ao processar resultado de automação: {e}")
    
    def get_daily_stats(self, user_id):
        """Obter estatísticas do dia atual"""
        try:
            stats = self.db.get_user_stats(user_id, days=1)
            return stats['today'] if stats else {
                'connections_sent': 0,
                'messages_sent': 0,
                'profiles_viewed': 0,
                'likes_given': 0,
                'comments_posted': 0,
                'success_rate': 0.0
            }
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas diárias: {e}")
            return {}
    
    def get_dashboard_data(self, user_id):
        """Obter dados completos para o dashboard"""
        try:
            # Estatísticas gerais
            stats = self.db.get_user_stats(user_id, days=30)
            
            # Atividades recentes
            recent_activity = self.db.get_recent_activity(user_id, limit=5)
            
            # Automações ativas
            automations = self.db.get_automations(user_id)
            active_automations = [a for a in automations if a['is_active']]
            
            # Dados de performance dos últimos 7 dias
            performance_data = self.get_performance_chart_data(user_id, days=7)
            
            return {
                'stats': stats,
                'recent_activity': recent_activity,
                'automations': {
                    'total': len(automations),
                    'active': len(active_automations),
                    'list': active_automations[:5]  # Primeiras 5 para o dashboard
                },
                'performance': performance_data,
                'summary': {
                    'total_actions_today': (
                        stats['today']['connections_sent'] + 
                        stats['today']['likes_given'] + 
                        stats['today']['comments_posted']
                    ),
                    'success_rate_trend': self.calculate_success_trend(user_id),
                    'most_active_automation': self.get_most_active_automation(user_id)
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter dados do dashboard: {e}")
            return None
    
    def get_performance_chart_data(self, user_id, days=7):
        """Obter dados para gráfico de performance"""
        try:
            import sqlite3
            
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Dados dos últimos N dias
                cursor.execute('''
                    SELECT date, connections_sent, messages_sent, profiles_viewed,
                           likes_given, comments_posted, success_rate
                    FROM daily_stats 
                    WHERE user_id = ? AND date >= date('now', '-{} days')
                    ORDER BY date ASC
                '''.format(days), (user_id,))
                
                rows = cursor.fetchall()
                
                # Formatar dados para gráfico
                chart_data = []
                for row in rows:
                    chart_data.append({
                        'date': row[0],
                        'connections': row[1],
                        'messages': row[2],
                        'profiles': row[3],
                        'likes': row[4],
                        'comments': row[5],
                        'success_rate': row[6],
                        'total_actions': row[1] + row[2] + row[3] + row[4] + row[5]
                    })
                
                return chart_data
                
        except Exception as e:
            logger.error(f"Erro ao obter dados de performance: {e}")
            return []
    
    def calculate_success_trend(self, user_id):
        """Calcular tendência da taxa de sucesso"""
        try:
            performance_data = self.get_performance_chart_data(user_id, days=7)
            
            if len(performance_data) < 2:
                return 0
            
            # Comparar últimos 3 dias com 3 dias anteriores
            recent_avg = sum(d['success_rate'] for d in performance_data[-3:]) / min(3, len(performance_data[-3:]))
            previous_avg = sum(d['success_rate'] for d in performance_data[-6:-3]) / min(3, len(performance_data[-6:-3]))
            
            if previous_avg == 0:
                return 0
            
            trend = ((recent_avg - previous_avg) / previous_avg) * 100
            return round(trend, 1)
            
        except Exception as e:
            logger.error(f"Erro ao calcular tendência: {e}")
            return 0
    
    def get_most_active_automation(self, user_id):
        """Obter automação mais ativa"""
        try:
            automations = self.db.get_automations(user_id)
            
            if not automations:
                return None
            
            # Ordenar por total executado
            most_active = max(automations, key=lambda x: x['total_executed'])
            
            return {
                'name': most_active['name'],
                'type': most_active['automation_type'],
                'executions': most_active['total_executed'],
                'success_rate': most_active['success_rate']
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter automação mais ativa: {e}")
            return None
    
    def generate_weekly_report(self, user_id):
        """Gerar relatório semanal"""
        try:
            stats = self.db.get_user_stats(user_id, days=7)
            performance_data = self.get_performance_chart_data(user_id, days=7)
            automations = self.db.get_automations(user_id)
            
            # Calcular métricas da semana
            total_actions = (stats['total']['connections_sent'] + 
                           stats['total']['likes_given'] + 
                           stats['total']['comments_posted'])
            
            avg_daily_actions = total_actions / 7 if total_actions > 0 else 0
            
            # Dia mais produtivo
            most_productive_day = max(performance_data, key=lambda x: x['total_actions']) if performance_data else None
            
            report = {
                'period': '7 dias',
                'total_actions': total_actions,
                'avg_daily_actions': round(avg_daily_actions, 1),
                'success_rate': stats['total']['success_rate'],
                'breakdown': {
                    'connections': stats['total']['connections_sent'],
                    'likes': stats['total']['likes_given'],
                    'comments': stats['total']['comments_posted']
                },
                'most_productive_day': most_productive_day['date'] if most_productive_day else None,
                'active_automations': len([a for a in automations if a['is_active']]),
                'performance_trend': self.calculate_success_trend(user_id)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório semanal: {e}")
            return None
    
    def get_automation_insights(self, user_id):
        """Obter insights sobre automações"""
        try:
            automations = self.db.get_automations(user_id)
            
            if not automations:
                return []
            
            insights = []
            
            # Insight sobre automações inativas
            inactive_count = len([a for a in automations if not a['is_active']])
            if inactive_count > 0:
                insights.append({
                    'type': 'warning',
                    'title': 'Automações Inativas',
                    'message': f'Você tem {inactive_count} automações inativas que poderiam estar gerando resultados.',
                    'action': 'Revisar automações inativas'
                })
            
            # Insight sobre performance
            low_performance = [a for a in automations if a['success_rate'] < 50 and a['total_executed'] > 5]
            if low_performance:
                insights.append({
                    'type': 'info',
                    'title': 'Oportunidade de Melhoria',
                    'message': f'{len(low_performance)} automações com baixa taxa de sucesso podem ser otimizadas.',
                    'action': 'Otimizar configurações'
                })
            
            # Insight sobre volume
            stats = self.db.get_user_stats(user_id, days=7)
            if stats['total']['connections_sent'] + stats['total']['likes_given'] + stats['total']['comments_posted'] < 10:
                insights.append({
                    'type': 'tip',
                    'title': 'Aumente sua Atividade',
                    'message': 'Considere aumentar a frequência das automações para melhores resultados.',
                    'action': 'Configurar mais automações'
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Erro ao obter insights: {e}")
            return []

# Instância global do serviço de analytics
analytics = AnalyticsService()
