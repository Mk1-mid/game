#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST MAESTRO ACTUALIZADO
========================

Test suite integrado con el nuevo sistema de Crítico y Esquiva.
Incluye todos los tests del proyecto.

Ejecutar: python tests/run_tests.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.test_combat_newstats import (
    test_arquetipos_creacion,
    test_agilidad_efectiva,
    test_derivados_correctos,
    test_arquetipos_diferenciados,
    test_escalado_con_nivel,
    test_probabilidades_combate,
    test_persistencia_stats
)


def run_all_tests():
    """Ejecuta todos los tests disponibles."""
    
    tests = [
        ("Arquetipos Creación", test_arquetipos_creacion),
        ("Agilidad Efectiva", test_agilidad_efectiva),
        ("Derivados Correctos", test_derivados_correctos),
        ("Arquetipos Diferenciados", test_arquetipos_diferenciados),
        ("Escalado con Nivel", test_escalado_con_nivel),
        ("Probabilidades Combate", test_probabilidades_combate),
        ("Persistencia Stats", test_persistencia_stats),
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "="*70)
    print("TEST MAESTRO - SUITE COMPLETA".center(70))
    print("="*70)
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ FALLÓ: {name}")
            print(f"   Error: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"RESULTADOS: {passed} Pasados, {failed} Fallidos")
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
