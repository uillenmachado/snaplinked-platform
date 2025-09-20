#!/usr/bin/env python3
"""
Script de inicialização para produção do SnapLinked
Configura o ambiente e inicia o servidor Flask
"""

import os
import sys
import logging
import subprocess
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Configurar ambiente de produção"""
    logger.info("🔧 Configurando ambiente de produção...")
    
    # Definir diretório do projeto
    project_dir = Path(__file__).parent
    backend_dir = project_dir / "snaplinked-backend"
    
    # Mudar para diretório do backend
    os.chdir(backend_dir)
    
    # Verificar se o ambiente virtual existe
    venv_dir = backend_dir / "venv"
    if not venv_dir.exists():
        logger.info("📦 Criando ambiente virtual...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    # Ativar ambiente virtual e instalar dependências
    if os.name == 'nt':  # Windows
        pip_path = venv_dir / "Scripts" / "pip"
        python_path = venv_dir / "Scripts" / "python"
    else:  # Unix/Linux
        pip_path = venv_dir / "bin" / "pip"
        python_path = venv_dir / "bin" / "python"
    
    logger.info("📦 Instalando dependências...")
    subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
    
    # Verificar se os arquivos estáticos existem
    static_dir = backend_dir / "static"
    if not (static_dir / "index.html").exists():
        logger.warning("⚠️ Arquivos estáticos não encontrados. Execute o build do frontend primeiro.")
        return False
    
    logger.info("✅ Ambiente configurado com sucesso!")
    return True, python_path

def check_dependencies():
    """Verificar dependências do sistema"""
    logger.info("🔍 Verificando dependências...")
    
    try:
        # Verificar Playwright
        import playwright
        logger.info("✅ Playwright disponível")
        
        # Verificar Flask
        import flask
        logger.info("✅ Flask disponível")
        
        # Verificar SQLite
        import sqlite3
        logger.info("✅ SQLite disponível")
        
        return True
    except ImportError as e:
        logger.error(f"❌ Dependência faltando: {e}")
        return False

def initialize_database():
    """Inicializar banco de dados"""
    logger.info("🗄️ Inicializando banco de dados...")
    
    try:
        from database import db
        logger.info("✅ Banco de dados inicializado!")
        return True
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar banco: {e}")
        return False

def start_server(python_path, port=5000):
    """Iniciar servidor Flask"""
    logger.info(f"🚀 Iniciando servidor na porta {port}...")
    
    # Configurar variáveis de ambiente
    env = os.environ.copy()
    env['FLASK_ENV'] = 'production'
    env['PORT'] = str(port)
    
    try:
        # Iniciar servidor
        subprocess.run([
            str(python_path), 
            "main.py"
        ], env=env, check=True)
    except KeyboardInterrupt:
        logger.info("🛑 Servidor interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar servidor: {e}")
        return False
    
    return True

def main():
    """Função principal"""
    logger.info("🎯 SnapLinked - Iniciando em modo produção")
    logger.info("=" * 50)
    
    try:
        # 1. Configurar ambiente
        result = setup_environment()
        if not result:
            logger.error("❌ Falha na configuração do ambiente")
            return False
        
        success, python_path = result
        if not success:
            return False
        
        # 2. Verificar dependências
        if not check_dependencies():
            logger.error("❌ Dependências não atendidas")
            return False
        
        # 3. Inicializar banco de dados
        if not initialize_database():
            logger.error("❌ Falha na inicialização do banco")
            return False
        
        # 4. Iniciar servidor
        logger.info("🎉 Tudo pronto! Iniciando SnapLinked...")
        logger.info("📱 Acesse: http://localhost:5000")
        logger.info("🔗 API: http://localhost:5000/api/health")
        logger.info("=" * 50)
        
        return start_server(python_path)
        
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
