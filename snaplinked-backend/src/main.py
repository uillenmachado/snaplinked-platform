"""
SnapLinked Backend - Aplicação Principal Refatorada
Sistema modular de automação LinkedIn com arquitetura limpa
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import logging
from datetime import datetime

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
    
    # Determinar configuração
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    # Criar aplicação Flask
    app = Flask(__name__, static_folder='static', static_url_path='')
    
    # Carregar configuração
    config_obj = Config()
    app.config.from_object(config_obj)
    
    # Configurar CORS
    cors_origins = app.config.get('CORS_ORIGINS', ['http://localhost:3000', 'http://localhost:5173'])
    if isinstance(cors_origins, str):
        cors_origins = cors_origins.split(',')
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
        logger.error(f"Erro interno: {error}")
        return {
            'success': False,
            'message': 'Erro interno do servidor'
        }, 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle uncaught exceptions"""
        logger.error(f"Exceção não tratada: {e}")
        return {
            'success': False,
            'message': 'Erro interno do servidor'
        }, 500
    
    # Log de inicialização
    logger.info(f"SnapLinked Backend iniciado - Configuração: {config_name}")
    logger.info(f"Debug mode: {app.config['DEBUG']}")
    logger.info(f"CORS origins: {app.config['CORS_ORIGINS']}")
    
    return app

# Criar aplicação
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = app.config['DEBUG']
    
    logger.info(f"Iniciando servidor na porta {port}")
    logger.info(f"Modo debug: {debug}")
    
    app.run(
        host='0.0.0.0', 
        port=port, 
        debug=debug
    )
