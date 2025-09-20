#!/usr/bin/env python3
"""
WSGI entry point for SnapLinked Backend - Production Deploy
Sistema de automação LinkedIn com arquitetura modular
"""

import os
import sys
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

# Configurar logging para produção
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Importar aplicação
from main import app

# Configurar para produção
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Configurações de produção
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
