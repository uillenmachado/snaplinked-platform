#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapLinked v3.0 - Executor de Testes
Script para executar todos os testes automatizados
"""

import unittest
import sys
import os
from io import StringIO

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_tests(verbose=True):
    """Executar todos os testes"""
    print("🧪 Executando testes SnapLinked v3.0...")
    print("=" * 50)
    
    # Descobrir e carregar todos os testes
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Configurar runner
    stream = StringIO() if not verbose else sys.stderr
    runner = unittest.TextTestRunner(
        stream=stream,
        verbosity=2 if verbose else 1,
        descriptions=True,
        failfast=False
    )
    
    # Executar testes
    result = runner.run(suite)
    
    # Mostrar resultados
    print(f"\n📊 Resultados dos Testes:")
    print(f"✅ Testes executados: {result.testsRun}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"⚠️ Erros: {len(result.errors)}")
    print(f"⏭️ Pulados: {len(result.skipped)}")
    
    if result.failures:
        print(f"\n❌ Falhas ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\n⚠️ Erros ({len(result.errors)}):")
        for test, traceback in result.errors:
            error_msg = traceback.split('\n')[-2] if traceback.split('\n') else 'Erro desconhecido'
            print(f"  - {test}: {error_msg}")
    
    if result.skipped:
        print(f"\n⏭️ Testes Pulados ({len(result.skipped)}):")
        for test, reason in result.skipped:
            print(f"  - {test}: {reason}")
    
    # Calcular taxa de sucesso
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"\n📈 Taxa de Sucesso: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🎉 Todos os testes passaram!")
    elif success_rate >= 80:
        print("✅ Maioria dos testes passou, mas há algumas questões para resolver.")
    else:
        print("⚠️ Muitos testes falharam. Revisão necessária.")
    
    return result.wasSuccessful()


def run_specific_test(test_name):
    """Executar um teste específico"""
    print(f"🧪 Executando teste específico: {test_name}")
    print("=" * 50)
    
    try:
        # Carregar teste específico
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(test_name)
        
        # Executar teste
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except Exception as e:
        print(f"❌ Erro ao executar teste: {str(e)}")
        return False


def list_tests():
    """Listar todos os testes disponíveis"""
    print("📋 Testes Disponíveis:")
    print("=" * 30)
    
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    def extract_tests(test_suite):
        tests = []
        for test in test_suite:
            if hasattr(test, '_tests'):
                tests.extend(extract_tests(test))
            else:
                tests.append(test)
        return tests
    
    all_tests = extract_tests(suite)
    
    current_module = None
    for test in all_tests:
        module_name = test.__class__.__module__
        if module_name != current_module:
            current_module = module_name
            print(f"\n📁 {module_name}:")
        
        test_name = test._testMethodName
        print(f"  - {test_name}")
    
    print(f"\n📊 Total: {len(all_tests)} testes")


def check_coverage():
    """Verificar cobertura de código (se coverage.py estiver disponível)"""
    try:
        import coverage
        print("📊 Executando análise de cobertura...")
        
        cov = coverage.Coverage()
        cov.start()
        
        # Executar testes
        run_tests(verbose=False)
        
        cov.stop()
        cov.save()
        
        print("\n📈 Relatório de Cobertura:")
        cov.report()
        
    except ImportError:
        print("⚠️ Módulo 'coverage' não encontrado. Instale com: pip install coverage")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Executar testes SnapLinked')
    parser.add_argument('--test', '-t', help='Executar teste específico')
    parser.add_argument('--list', '-l', action='store_true', help='Listar todos os testes')
    parser.add_argument('--coverage', '-c', action='store_true', help='Executar com análise de cobertura')
    parser.add_argument('--quiet', '-q', action='store_true', help='Modo silencioso')
    
    args = parser.parse_args()
    
    if args.list:
        list_tests()
    elif args.test:
        success = run_specific_test(args.test)
        sys.exit(0 if success else 1)
    elif args.coverage:
        check_coverage()
    else:
        success = run_tests(verbose=not args.quiet)
        sys.exit(0 if success else 1)
