#!/usr/bin/env python3
"""
SnapLinked Backend - Arquivo principal para deploy
Sistema de automação LinkedIn com arquitetura modular
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importar aplicação
from src.main import create_app

# Criar aplicação
app = create_app()

if __name__ == '__main__':
    # Configuração para produção
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"🚀 Iniciando SnapLinked Backend na porta {port}")
    print(f"🔧 Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
