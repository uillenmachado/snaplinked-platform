#!/usr/bin/env python3
"""
SnapLinked Backend - Arquivo principal
Sistema de automação LinkedIn com arquitetura modular
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    """
    Cria e configura a aplicação Flask
    """
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/')
    def index():
        return jsonify({
            "message": "SnapLinked API v4.2.0",
            "status": "operational"
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    
    print(f"🚀 Iniciando SnapLinked Backend na porta {port}")
    print(f"🔧 Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
