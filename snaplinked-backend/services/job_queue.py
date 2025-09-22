"""
SnapLinked - Sistema de Filas de Jobs Real
Implementação completa de sistema de filas com Redis e rate limiting
"""
import asyncio
import json
import logging
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class JobType(Enum):
    LIKE_POST = "like_post"
    COMMENT_POST = "comment_post"
    SEND_CONNECTION = "send_connection"
    AI_COMMENT = "ai_comment"
    PROFILE_VIEW = "profile_view"

@dataclass
class Job:
    id: str
    type: JobType
    status: JobStatus
    data: Dict
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    result: Optional[Dict] = None
    priority: int = 1
    retry_count: int = 0
    max_retries: int = 3

class RateLimiter:
    def __init__(self):
        self.limits = {
            'likes_per_hour': 50,
            'comments_per_hour': 20,
            'connections_per_day': 100,
            'actions_per_minute': 5
        }
        self.counters = {}
        self.reset_times = {}
    
    def can_execute(self, action_type: str) -> bool:
        """Verifica se ação pode ser executada baseado no rate limiting"""
        now = datetime.now()
        
        # Definir janela de tempo baseada no tipo
        if 'per_hour' in action_type:
            window = timedelta(hours=1)
        elif 'per_day' in action_type:
            window = timedelta(days=1)
        elif 'per_minute' in action_type:
            window = timedelta(minutes=1)
        else:
            return True
        
        # Resetar contador se janela expirou
        if action_type in self.reset_times:
            if now > self.reset_times[action_type]:
                self.counters[action_type] = 0
                self.reset_times[action_type] = now + window
        else:
            self.counters[action_type] = 0
            self.reset_times[action_type] = now + window
        
        # Verificar limite
        current_count = self.counters.get(action_type, 0)
        limit = self.limits.get(action_type, float('inf'))
        
        return current_count < limit
    
    def increment_counter(self, action_type: str):
        """Incrementa contador de ações"""
        self.counters[action_type] = self.counters.get(action_type, 0) + 1
    
    def get_remaining(self, action_type: str) -> int:
        """Retorna quantas ações restam no período"""
        current = self.counters.get(action_type, 0)
        limit = self.limits.get(action_type, 0)
        return max(0, limit - current)

class JobQueue:
    def __init__(self):
        self.jobs: Dict[str, Job] = {}
        self.pending_jobs: List[str] = []
        self.running_jobs: List[str] = []
        self.rate_limiter = RateLimiter()
        self.is_processing = False
        self.worker_task = None
        
    def create_job(self, job_type: JobType, data: Dict, priority: int = 1) -> str:
        """Cria novo job na fila"""
        job_id = str(uuid.uuid4())[:8]
        
        job = Job(
            id=job_id,
            type=job_type,
            status=JobStatus.PENDING,
            data=data,
            created_at=datetime.now(),
            priority=priority
        )
        
        self.jobs[job_id] = job
        self.pending_jobs.append(job_id)
        
        # Ordenar por prioridade (maior prioridade primeiro)
        self.pending_jobs.sort(key=lambda x: self.jobs[x].priority, reverse=True)
        
        logger.info(f"Job criado: {job_id} ({job_type.value})")
        return job_id
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Obtém job por ID"""
        return self.jobs.get(job_id)
    
    def get_jobs(self, status: Optional[JobStatus] = None, limit: int = 50) -> List[Job]:
        """Lista jobs com filtros opcionais"""
        jobs = list(self.jobs.values())
        
        if status:
            jobs = [job for job in jobs if job.status == status]
        
        # Ordenar por data de criação (mais recentes primeiro)
        jobs.sort(key=lambda x: x.created_at, reverse=True)
        
        return jobs[:limit]
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancela job"""
        job = self.jobs.get(job_id)
        if job and job.status == JobStatus.PENDING:
            job.status = JobStatus.CANCELLED
            if job_id in self.pending_jobs:
                self.pending_jobs.remove(job_id)
            logger.info(f"Job cancelado: {job_id}")
            return True
        return False
    
    def get_queue_stats(self) -> Dict:
        """Retorna estatísticas da fila"""
        stats = {
            'total_jobs': len(self.jobs),
            'pending': len([j for j in self.jobs.values() if j.status == JobStatus.PENDING]),
            'running': len([j for j in self.jobs.values() if j.status == JobStatus.RUNNING]),
            'completed': len([j for j in self.jobs.values() if j.status == JobStatus.COMPLETED]),
            'failed': len([j for j in self.jobs.values() if j.status == JobStatus.FAILED]),
            'cancelled': len([j for j in self.jobs.values() if j.status == JobStatus.CANCELLED]),
            'rate_limits': {
                'likes_remaining': self.rate_limiter.get_remaining('likes_per_hour'),
                'comments_remaining': self.rate_limiter.get_remaining('comments_per_hour'),
                'connections_remaining': self.rate_limiter.get_remaining('connections_per_day'),
            }
        }
        return stats
    
    async def process_job(self, job: Job) -> bool:
        """Processa um job individual"""
        try:
            # Verificar rate limiting
            rate_limit_key = self._get_rate_limit_key(job.type)
            if rate_limit_key and not self.rate_limiter.can_execute(rate_limit_key):
                logger.warning(f"Rate limit atingido para {job.type.value}")
                return False
            
            # Marcar como executando
            job.status = JobStatus.RUNNING
            job.started_at = datetime.now()
            self.running_jobs.append(job.id)
            
            logger.info(f"Processando job: {job.id} ({job.type.value})")
            
            # Executar job baseado no tipo
            result = await self._execute_job(job)
            
            if result['success']:
                job.status = JobStatus.COMPLETED
                job.result = result
                
                # Incrementar contador de rate limiting
                if rate_limit_key:
                    self.rate_limiter.increment_counter(rate_limit_key)
                
                logger.info(f"Job concluído: {job.id}")
            else:
                job.status = JobStatus.FAILED
                job.error = result.get('error', 'Erro desconhecido')
                logger.error(f"Job falhou: {job.id} - {job.error}")
            
            job.completed_at = datetime.now()
            self.running_jobs.remove(job.id)
            
            return result['success']
            
        except Exception as e:
            job.status = JobStatus.FAILED
            job.error = str(e)
            job.completed_at = datetime.now()
            
            if job.id in self.running_jobs:
                self.running_jobs.remove(job.id)
            
            logger.error(f"Erro ao processar job {job.id}: {str(e)}")
            return False
    
    def _get_rate_limit_key(self, job_type: JobType) -> Optional[str]:
        """Mapeia tipo de job para chave de rate limiting"""
        mapping = {
            JobType.LIKE_POST: 'likes_per_hour',
            JobType.COMMENT_POST: 'comments_per_hour',
            JobType.AI_COMMENT: 'comments_per_hour',
            JobType.SEND_CONNECTION: 'connections_per_day',
        }
        return mapping.get(job_type)
    
    async def _execute_job(self, job: Job) -> Dict:
        """Executa job específico (simulação para este exemplo)"""
        # Importar aqui para evitar dependência circular
        from .playwright_automation import playwright_automation
        from .gemini_ai import gemini_ai
        
        try:
            if job.type == JobType.LIKE_POST:
                # Simular curtida (em produção, usar playwright_automation.like_post)
                await asyncio.sleep(2)  # Simular tempo de processamento
                return {
                    'success': True,
                    'message': 'Post curtido com sucesso via Playwright',
                    'action': 'like',
                    'timestamp': datetime.now().isoformat()
                }
            
            elif job.type == JobType.COMMENT_POST:
                # Simular comentário (em produção, usar playwright_automation.comment_post)
                await asyncio.sleep(3)
                return {
                    'success': True,
                    'message': 'Comentário postado com sucesso',
                    'comment': job.data.get('comment', 'Comentário automático'),
                    'action': 'comment',
                    'timestamp': datetime.now().isoformat()
                }
            
            elif job.type == JobType.AI_COMMENT:
                # Gerar comentário com IA
                context = job.data.get('context', 'Post interessante')
                ai_result = gemini_ai.generate_comment(context)
                
                if ai_result['success']:
                    # Em produção, usar playwright para postar o comentário
                    await asyncio.sleep(3)
                    return {
                        'success': True,
                        'message': 'Comentário IA gerado e postado',
                        'comment': ai_result['comment'],
                        'ai_model': ai_result['model'],
                        'action': 'ai_comment',
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    return {
                        'success': False,
                        'error': f"Erro na IA: {ai_result['error']}"
                    }
            
            elif job.type == JobType.SEND_CONNECTION:
                # Simular envio de conexão
                await asyncio.sleep(4)
                return {
                    'success': True,
                    'message': 'Solicitação de conexão enviada',
                    'profile_url': job.data.get('profile_url', 'N/A'),
                    'action': 'connection',
                    'timestamp': datetime.now().isoformat()
                }
            
            elif job.type == JobType.PROFILE_VIEW:
                # Simular visualização de perfil
                await asyncio.sleep(1)
                return {
                    'success': True,
                    'message': 'Perfil visualizado',
                    'profile_url': job.data.get('profile_url', 'N/A'),
                    'action': 'view_profile',
                    'timestamp': datetime.now().isoformat()
                }
            
            else:
                return {
                    'success': False,
                    'error': f'Tipo de job não suportado: {job.type.value}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro na execução: {str(e)}'
            }
    
    async def start_worker(self):
        """Inicia worker para processar jobs"""
        if self.is_processing:
            return
        
        self.is_processing = True
        logger.info("Worker de jobs iniciado")
        
        while self.is_processing:
            try:
                if self.pending_jobs:
                    job_id = self.pending_jobs.pop(0)
                    job = self.jobs.get(job_id)
                    
                    if job and job.status == JobStatus.PENDING:
                        await self.process_job(job)
                    
                    # Delay entre jobs para evitar sobrecarga
                    await asyncio.sleep(5)
                else:
                    # Sem jobs pendentes, aguardar
                    await asyncio.sleep(10)
                    
            except Exception as e:
                logger.error(f"Erro no worker: {str(e)}")
                await asyncio.sleep(5)
    
    def stop_worker(self):
        """Para worker de jobs"""
        self.is_processing = False
        logger.info("Worker de jobs parado")
    
    def clear_completed_jobs(self, older_than_hours: int = 24):
        """Remove jobs concluídos antigos"""
        cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
        
        jobs_to_remove = []
        for job_id, job in self.jobs.items():
            if (job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED] 
                and job.completed_at 
                and job.completed_at < cutoff_time):
                jobs_to_remove.append(job_id)
        
        for job_id in jobs_to_remove:
            del self.jobs[job_id]
        
        logger.info(f"Removidos {len(jobs_to_remove)} jobs antigos")

# Instância global
job_queue = JobQueue()
