from functools import wraps
import time
import logging
from flask import request, g
from config.settings import Config

logger = logging.getLogger(__name__)

def performance_monitor(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Marca tempo inicial
        start_time = time.time()
        
        # Executa função
        result = f(*args, **kwargs)
        
        # Calcula duração
        duration = time.time() - start_time
        
        # Log de performance
        logger.info(
            f"Performance: {request.endpoint} - {duration:.2f}s",
            extra={
                'duration': duration,
                'endpoint': request.endpoint,
                'method': request.method,
                'path': request.path,
                'status_code': getattr(result, 'status_code', None)
            }
        )
        
        # Alertas se duração exceder limites
        if duration > Config.SLOW_REQUEST_THRESHOLD:
            logger.warning(
                f"Slow request detected: {request.endpoint} - {duration:.2f}s"
            )
        
        return result
    return decorated_function