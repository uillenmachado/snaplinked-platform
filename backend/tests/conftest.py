"""
Configuração global para testes
"""
import os
import sys
from pathlib import Path

# Adiciona o diretório src ao PYTHONPATH
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))