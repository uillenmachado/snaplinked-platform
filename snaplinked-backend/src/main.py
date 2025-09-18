#!/usr/bin/env python3
"""
SnapLinked Backend - Aplicação Principal para Deploy
Sistema modular de automação LinkedIn com arquitetura limpa
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import logging
from datetime import datetime

# Importar configurações e rotas
from config.settings import Config
from routes import auth_bp, linkedin_bp, automations_bp, analytics_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name=None):
    """Factory function para criar a aplicação Flask"""
    
    # Criar aplicação Flask
    app = Flask(__name__, static_folder='static', static_url_path='')
    
    # Carregar configuração
    config_obj = Config()
    app.config.from_object(config_obj)
    
    # Configurar CORS
    cors_origins = ['*']  # Permitir todas as origens para deploy
    CORS(app, origins=cors_origins)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(linkedin_bp)
    app.register_blueprint(automations_bp)
    app.register_blueprint(analytics_bp)
    
    # Rotas para servir o frontend
    @app.route('/')
    def serve_frontend():
        """Serve the React frontend"""
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_static_files(path):
        """Serve static files or fallback to index.html for SPA routing"""
        try:
            return send_from_directory(app.static_folder, path)
        except:
            return send_from_directory(app.static_folder, 'index.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 by serving frontend"""
        return send_from_directory(app.static_folder, 'index.html')

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return {'error': 'Internal server error'}, 500
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return {
            'status': 'healthy',
            'service': 'SnapLinked API',
            'version': '4.1.0',
            'timestamp': datetime.utcnow().isoformat(),
            'features': {
                'automation_engine': True,
                'linkedin_oauth': True,
                'manual_login': True,
                'real_automation': True,
                'modular_architecture': True,
                'security_improvements': True
            }
        }
    
    logger.info(f"SnapLinked Backend iniciado - Configuração: {config_name or 'default'}")
    logger.info(f"Debug mode: {app.debug}")
    logger.info(f"CORS origins: {cors_origins}")
    
    return app

# Criar aplicação para deploy
app = create_app()

if __name__ == '__main__':
    # Configuração para execução local
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Iniciando servidor na porta {port}")
    logger.info(f"Modo debug: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
