#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapLinked v3.0 - Middleware de Monitoramento
Métricas, health checks e observabilidade
"""

import time
import psutil
import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, Any, List

from flask import request, g, current_app, jsonify
import structlog

# Configurar logging
logger = structlog.get_logger(__name__)


class MonitoringMiddleware:
    """Middleware de monitoramento para Flask"""
    
    def __init__(self, app=None):
        self.app = app
        self.metrics = defaultdict(lambda: defaultdict(int))
        self.response_times = defaultdict(lambda: deque(maxlen=1000))
        self.error_counts = defaultdict(int)
        self.active_requests = 0
        self.start_time = datetime.now()
        
        # Thread para coleta de métricas do sistema
        self.system_metrics = {}
        self.metrics_thread = None
        self.running = False
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializar middleware com aplicação Flask"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        
        # Registrar endpoints de monitoramento
        self.register_monitoring_endpoints(app)
        
        # Iniciar coleta de métricas do sistema
        self.start_system_monitoring()
    
    def before_request(self):
        """Executar antes de cada requisição"""
        g.request_start_time = time.time()
        self.active_requests += 1
        
        # Incrementar contador de requisições
        self.metrics['requests']['total'] += 1
        self.metrics['requests'][request.method.lower()] += 1
        self.metrics['endpoints'][request.endpoint or 'unknown'] += 1
    
    def after_request(self, response):
        """Executar após cada requisição"""
        if hasattr(g, 'request_start_time'):
            response_time = time.time() - g.request_start_time
            
            # Armazenar tempo de resposta
            endpoint = request.endpoint or 'unknown'
            self.response_times[endpoint].append(response_time)
            
            # Métricas de status
            status_class = f"{response.status_code // 100}xx"
            self.metrics['status_codes'][str(response.status_code)] += 1
            self.metrics['status_classes'][status_class] += 1
            
            # Contar erros
            if response.status_code >= 400:
                self.error_counts[endpoint] += 1
                self.metrics['errors']['total'] += 1
                
                if response.status_code >= 500:
                    self.metrics['errors']['server_errors'] += 1
                else:
                    self.metrics['errors']['client_errors'] += 1
        
        self.active_requests = max(0, self.active_requests - 1)
        return response
    
    def register_monitoring_endpoints(self, app):
        """Registrar endpoints de monitoramento"""
        
        @app.route('/api/metrics')
        def get_metrics():
            """Endpoint para métricas da aplicação"""
            return jsonify(self.get_application_metrics())
        
        @app.route('/api/health/detailed')
        def detailed_health_check():
            """Health check detalhado"""
            return jsonify(self.get_detailed_health())
        
        @app.route('/api/system/stats')
        def system_stats():
            """Estatísticas do sistema"""
            return jsonify(self.get_system_stats())
        
        @app.route('/api/monitoring/dashboard')
        def monitoring_dashboard():
            """Dashboard de monitoramento"""
            return jsonify(self.get_dashboard_data())
    
    def start_system_monitoring(self):
        """Iniciar monitoramento do sistema"""
        if self.metrics_thread and self.metrics_thread.is_alive():
            return
        
        self.running = True
        self.metrics_thread = threading.Thread(target=self._collect_system_metrics)
        self.metrics_thread.daemon = True
        self.metrics_thread.start()
        
        logger.info("System monitoring started")
    
    def stop_system_monitoring(self):
        """Parar monitoramento do sistema"""
        self.running = False
        if self.metrics_thread:
            self.metrics_thread.join(timeout=5)
        
        logger.info("System monitoring stopped")
    
    def _collect_system_metrics(self):
        """Coletar métricas do sistema em background"""
        while self.running:
            try:
                # CPU
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_count = psutil.cpu_count()
                
                # Memória
                memory = psutil.virtual_memory()
                
                # Disco
                disk = psutil.disk_usage('/')
                
                # Rede (se disponível)
                try:
                    network = psutil.net_io_counters()
                    network_stats = {
                        'bytes_sent': network.bytes_sent,
                        'bytes_recv': network.bytes_recv,
                        'packets_sent': network.packets_sent,
                        'packets_recv': network.packets_recv
                    }
                except:
                    network_stats = {}
                
                # Processos
                process_count = len(psutil.pids())
                
                self.system_metrics = {
                    'timestamp': datetime.now().isoformat(),
                    'cpu': {
                        'percent': cpu_percent,
                        'count': cpu_count,
                        'load_avg': list(psutil.getloadavg()) if hasattr(psutil, 'getloadavg') else []
                    },
                    'memory': {
                        'total': memory.total,
                        'available': memory.available,
                        'percent': memory.percent,
                        'used': memory.used,
                        'free': memory.free
                    },
                    'disk': {
                        'total': disk.total,
                        'used': disk.used,
                        'free': disk.free,
                        'percent': disk.percent
                    },
                    'network': network_stats,
                    'processes': {
                        'count': process_count
                    }
                }
                
            except Exception as e:
                logger.error("Error collecting system metrics", error=str(e))
            
            time.sleep(30)  # Coletar a cada 30 segundos
    
    def get_application_metrics(self) -> Dict[str, Any]:
        """Obter métricas da aplicação"""
        uptime = datetime.now() - self.start_time
        
        # Calcular estatísticas de tempo de resposta
        response_time_stats = {}
        for endpoint, times in self.response_times.items():
            if times:
                times_list = list(times)
                response_time_stats[endpoint] = {
                    'count': len(times_list),
                    'avg': sum(times_list) / len(times_list),
                    'min': min(times_list),
                    'max': max(times_list),
                    'p95': self._percentile(times_list, 95),
                    'p99': self._percentile(times_list, 99)
                }
        
        return {
            'uptime_seconds': uptime.total_seconds(),
            'uptime_human': str(uptime),
            'active_requests': self.active_requests,
            'total_requests': self.metrics['requests']['total'],
            'requests_by_method': dict(self.metrics['requests']),
            'requests_by_endpoint': dict(self.metrics['endpoints']),
            'status_codes': dict(self.metrics['status_codes']),
            'status_classes': dict(self.metrics['status_classes']),
            'errors': dict(self.metrics['errors']),
            'error_counts_by_endpoint': dict(self.error_counts),
            'response_times': response_time_stats,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_detailed_health(self) -> Dict[str, Any]:
        """Health check detalhado"""
        health_status = 'healthy'
        checks = {}
        
        # Verificar banco de dados
        try:
            from models import db
            db.session.execute('SELECT 1')
            checks['database'] = {'status': 'healthy', 'message': 'Database connection OK'}
        except Exception as e:
            checks['database'] = {'status': 'unhealthy', 'message': f'Database error: {str(e)}'}
            health_status = 'unhealthy'
        
        # Verificar uso de memória
        if self.system_metrics:
            memory_percent = self.system_metrics.get('memory', {}).get('percent', 0)
            if memory_percent > 90:
                checks['memory'] = {'status': 'warning', 'message': f'High memory usage: {memory_percent}%'}
                if health_status == 'healthy':
                    health_status = 'warning'
            else:
                checks['memory'] = {'status': 'healthy', 'message': f'Memory usage: {memory_percent}%'}
        
        # Verificar CPU
        if self.system_metrics:
            cpu_percent = self.system_metrics.get('cpu', {}).get('percent', 0)
            if cpu_percent > 80:
                checks['cpu'] = {'status': 'warning', 'message': f'High CPU usage: {cpu_percent}%'}
                if health_status == 'healthy':
                    health_status = 'warning'
            else:
                checks['cpu'] = {'status': 'healthy', 'message': f'CPU usage: {cpu_percent}%'}
        
        # Verificar disco
        if self.system_metrics:
            disk_percent = self.system_metrics.get('disk', {}).get('percent', 0)
            if disk_percent > 85:
                checks['disk'] = {'status': 'warning', 'message': f'High disk usage: {disk_percent}%'}
                if health_status == 'healthy':
                    health_status = 'warning'
            else:
                checks['disk'] = {'status': 'healthy', 'message': f'Disk usage: {disk_percent}%'}
        
        # Verificar taxa de erro
        total_requests = self.metrics['requests']['total']
        total_errors = self.metrics['errors']['total']
        if total_requests > 100:  # Só verificar se há requisições suficientes
            error_rate = (total_errors / total_requests) * 100
            if error_rate > 10:
                checks['error_rate'] = {'status': 'warning', 'message': f'High error rate: {error_rate:.2f}%'}
                if health_status == 'healthy':
                    health_status = 'warning'
            else:
                checks['error_rate'] = {'status': 'healthy', 'message': f'Error rate: {error_rate:.2f}%'}
        
        return {
            'status': health_status,
            'timestamp': datetime.now().isoformat(),
            'checks': checks,
            'version': '3.0.0'
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Obter estatísticas do sistema"""
        return self.system_metrics
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Obter dados para dashboard de monitoramento"""
        return {
            'application': self.get_application_metrics(),
            'system': self.get_system_stats(),
            'health': self.get_detailed_health()
        }
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calcular percentil"""
        if not data:
            return 0.0
        
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))
    
    def reset_metrics(self):
        """Resetar métricas"""
        self.metrics.clear()
        self.response_times.clear()
        self.error_counts.clear()
        self.start_time = datetime.now()
        
        logger.info("Metrics reset")
    
    def get_alerts(self) -> List[Dict[str, Any]]:
        """Obter alertas baseados nas métricas"""
        alerts = []
        
        # Alert de alta taxa de erro
        total_requests = self.metrics['requests']['total']
        total_errors = self.metrics['errors']['total']
        if total_requests > 50 and total_errors / total_requests > 0.1:
            alerts.append({
                'type': 'error_rate',
                'severity': 'warning',
                'message': f'High error rate: {(total_errors/total_requests)*100:.1f}%',
                'timestamp': datetime.now().isoformat()
            })
        
        # Alert de tempo de resposta alto
        for endpoint, times in self.response_times.items():
            if times and len(times) > 10:
                avg_time = sum(times) / len(times)
                if avg_time > 2.0:  # 2 segundos
                    alerts.append({
                        'type': 'slow_response',
                        'severity': 'warning',
                        'message': f'Slow response time for {endpoint}: {avg_time:.2f}s',
                        'timestamp': datetime.now().isoformat()
                    })
        
        # Alert de uso de recursos
        if self.system_metrics:
            memory_percent = self.system_metrics.get('memory', {}).get('percent', 0)
            if memory_percent > 85:
                alerts.append({
                    'type': 'high_memory',
                    'severity': 'critical' if memory_percent > 95 else 'warning',
                    'message': f'High memory usage: {memory_percent}%',
                    'timestamp': datetime.now().isoformat()
                })
            
            cpu_percent = self.system_metrics.get('cpu', {}).get('percent', 0)
            if cpu_percent > 80:
                alerts.append({
                    'type': 'high_cpu',
                    'severity': 'warning',
                    'message': f'High CPU usage: {cpu_percent}%',
                    'timestamp': datetime.now().isoformat()
                })
        
        return alerts


# Instância global do middleware
monitoring_middleware = MonitoringMiddleware()
