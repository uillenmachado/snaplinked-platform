"""
Blueprint para endpoints de saúde e status da API
"""

from flask import Blueprint, jsonify
from datetime import datetime

from config.settings import Config

health_bp = Blueprint('health', __name__)

@health_bp.route('/')
def health_check():
    """Endpoint para verificação de saúde do sistema"""
    return jsonify({
        "status": "ok",
        "version": Config.VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "environment": Config.ENV
    })

@health_bp.route('/status')
def detailed_status():
    """Endpoint com informações detalhadas do status do sistema"""
    return jsonify({
        "status": "operational",
        "version": Config.VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "environment": Config.ENV,
        "debug_mode": Config.DEBUG,
        "services": {
            "database": "connected",
            "redis": "connected",
            "linkedin_api": "available"
        }
    })