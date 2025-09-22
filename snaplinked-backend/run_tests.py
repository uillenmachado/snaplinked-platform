#!/usr/bin/env python3
"""
Script para executar testes do SnapLinked Backend
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(command, description):
    """Executa comando e exibe resultado"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.stdout:
            print(result.stdout)
        
        print(f"✅ {description} - SUCESSO")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FALHOU")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Função principal"""
    print("🚀 Iniciando testes do SnapLinked Backend")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('src/main.py'):
        print("❌ Execute este script do diretório snaplinked-backend")
        sys.exit(1)
    
    # Lista de comandos de teste
    test_commands = [
        {
            'command': 'python -m pytest tests/unit/ -v --tb=short',
            'description': 'Executando testes unitários'
        },
        {
            'command': 'python -m pytest tests/integration/ -v --tb=short',
            'description': 'Executando testes de integração'
        },
        {
            'command': 'python -m pytest tests/ --cov=src --cov-report=term-missing',
            'description': 'Executando testes com cobertura'
        }
    ]
    
    # Executar testes
    success_count = 0
    total_count = len(test_commands)
    
    for test in test_commands:
        if run_command(test['command'], test['description']):
            success_count += 1
    
    # Relatório final
    print(f"\n{'='*60}")
    print(f"📊 RELATÓRIO FINAL")
    print(f"{'='*60}")
    print(f"✅ Sucessos: {success_count}/{total_count}")
    print(f"❌ Falhas: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 Todos os testes passaram!")
        sys.exit(0)
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")
        sys.exit(1)

if __name__ == '__main__':
    main()
