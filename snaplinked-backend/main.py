#!/usr/bin/env python3
"""
SnapLinked Backend - Arquivo principal para deploy
Sistema de automação LinkedIn com arquitetura modular
"""

import sys
import os

# Adicionar src ao path para resolver imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Importar aplicação do src
from main import create_app

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
