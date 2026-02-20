#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST MAESTRO - TODAS LAS VERSIONES
===================================

Agrega y ejecuta TODOS los tests del proyecto:
- Versión 1: Fase 1 (Contenido básico) - 19 tests
- Versión 2: Fase 2 (Misiones + Notificaciones) - 30 tests

Total: 49+ tests

Ejecutar: python tests/test_maestro.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ============================================================================
# IMPORTS TESTS V1 Y V2 (DESDE ARCHIVOS INDIVIDUALES)
# ============================================================================

# Importar desde tests/archivos/ (donde están los tests individuales)

from tests.archivos.test_balance_fase1 import (
    test_catalogo_completo,
    test_balance_armas,
    test_balance_armaduras,
    test_equipamiento,
    test_progresion_precios
)

from tests.archivos.test_sistema_equipos import (
    test_sistema_equipos,
    test_equipo_completo
)

from tests.archivos.test_equipo import (
    test_crear_gladiador,
    test_armar_gladiador,
    test_progresion_xp
)

from tests.archivos.test_mercado import (
    test_compra_items,
    test_venta_items,
    test_restricciones_compra
)

from tests.archivos.test_pociones_venta import (
    test_compra_pociones,
    test_uso_pociones
)

from tests.archivos.test_ui_visual import (
    test_barras_hp_xp,
    test_emojis
)

from tests.archivos.test_main_functions import (
    test_main_menu,
    test_navegacion
)

from tests.archivos.test_misiones import (
    test_gestor_misiones,
    test_misiones_core,
    test_misiones_encadenadas,
    test_misiones_automaticas,
    test_misiones_secundarias,
    test_generador_progreso,
    test_balance as test_balance_misiones
)

from tests.archivos.test_autotracking_misiones import (
    test_evento_combate_ganado,
    test_evento_dinero_acumulado,
    test_evento_nivel_up,
    test_evento_items_comprados,
    test_cadena_con_auto_tracking,
    test_notificaciones,
    test_multiples_eventos_simultaneos
)

from tests.archivos.test_notificaciones_persistencia import (
    test_notificaciones_mejoradas,
    test_persistencia_guardar_cargar,
    test_persistencia_multiples_usuarios,
    test_persistencia_con_bonus,
    test_resetear_misiones
)

from tests.archivos.test_integracion_misiones import (
    test_integracion_equipo_misiones,
    test_flujo_completo_cadena,
    test_chain_unlocking,
    test_multiples_cadenas_simultaneas
)

from tests.archivos.test_integracion_completa import (
    simular_sesion_completa,
    test_carga_partida_no_existente
)

# ============================================================================
# TEST MAESTRO - TODAS LAS VERSIONES
# ============================================================================

def ejecutar_test_maestro():
    """Ejecuta TODOS los tests (V1 + V2)"""
    
    print("\n" + "="*80)
    print("🎮 TEST MAESTRO - TODAS LAS VERSIONES")
    print("="*80)
    print("\n📋 Ejecutando todos los tests del proyecto...")
    print("   - Versión 1 (Fase 1): 19 tests")
    print("   - Versión 2 (Fase 2): 30 tests")
    print("   - Total: 49+ tests\n")
    
    # Agrupación por versión
    tests_v1 = [
        ("V1: Balance Catálogo", test_catalogo_completo),
        ("V1: Balance Armas", test_balance_armas),
        ("V1: Balance Armaduras", test_balance_armaduras),
        ("V1: Equipamiento", test_equipamiento),
        ("V1: Progresión Precios", test_progresion_precios),
        ("V1: Sistema Equipos", test_sistema_equipos),
        ("V1: Equipo Completo", test_equipo_completo),
        ("V1: Crear Gladiador", test_crear_gladiador),
        ("V1: Armar Gladiador", test_armar_gladiador),
        ("V1: Progresión XP", test_progresion_xp),
        ("V1: Compra Items", test_compra_items),
        ("V1: Venta Items", test_venta_items),
        ("V1: Restricciones Compra", test_restricciones_compra),
        ("V1: Compra Pociones", test_compra_pociones),
        ("V1: Uso Pociones", test_uso_pociones),
        ("V1: Barras HP/XP", test_barras_hp_xp),
        ("V1: Emojis", test_emojis),
        ("V1: Menu Principal", test_main_menu),
        ("V1: Navegación", test_navegacion),
    ]
    
    tests_v2 = [
        ("V2: Gestor Misiones", test_gestor_misiones),
        ("V2: Misiones CORE", test_misiones_core),
        ("V2: Misiones Encadenadas", test_misiones_encadenadas),
        ("V2: Misiones Automáticas", test_misiones_automaticas),
        ("V2: Misiones Secundarias", test_misiones_secundarias),
        ("V2: Generador Progreso", test_generador_progreso),
        ("V2: Balance Misiones", test_balance_misiones),
        ("V2: Evento - Combate Ganado", test_evento_combate_ganado),
        ("V2: Evento - Dinero Acumulado", test_evento_dinero_acumulado),
        ("V2: Evento - Nivel Up", test_evento_nivel_up),
        ("V2: Evento - Items Comprados", test_evento_items_comprados),
        ("V2: Cadena + Auto-Tracking", test_cadena_con_auto_tracking),
        ("V2: Notificaciones", test_notificaciones),
        ("V2: Eventos Simultáneos", test_multiples_eventos_simultaneos),
        ("V2: Notificaciones Mejoradas", test_notificaciones_mejoradas),
        ("V2: Persistencia: Guardar/Cargar", test_persistencia_guardar_cargar),
        ("V2: Persistencia: Multi-usuario", test_persistencia_multiples_usuarios),
        ("V2: Persistencia: Con Bonus", test_persistencia_con_bonus),
        ("V2: Persistencia: Reset", test_resetear_misiones),
        ("V2: Integración: Equipo + Misiones", test_integracion_equipo_misiones),
        ("V2: Integración: Flujo Cadena", test_flujo_completo_cadena),
        ("V2: Integración: Chain Unlocking", test_chain_unlocking),
        ("V2: Integración: Múltiples Cadenas", test_multiples_cadenas_simultaneas),
        ("V2: Integración: Sesión Completa", simular_sesion_completa),
        ("V2: Integración: Partida No Existente", test_carga_partida_no_existente),
    ]
    
    todos_tests = tests_v1 + tests_v2
    passed_v1, failed_v1 = 0, 0
    passed_v2, failed_v2 = 0, 0
    
    # Ejecutar V1
    print("\n" + "-"*80)
    print("VERSIÓN 1 - FASE 1 (Contenido Básico)")
    print("-"*80)
    for nombre, test_func in tests_v1:
        try:
            print(f"  ▶ {nombre:<35}", end=" ")
            test_func()
            print("✅")
            passed_v1 += 1
        except Exception as e:
            print(f"❌ {str(e)[:40]}")
            failed_v1 += 1
    
    # Ejecutar V2
    print("\n" + "-"*80)
    print("VERSIÓN 2 - FASE 2 (Misiones + Notificaciones)")
    print("-"*80)
    for nombre, test_func in tests_v2:
        try:
            print(f"  ▶ {nombre:<35}", end=" ")
            test_func()
            print("✅")
            passed_v2 += 1
        except Exception as e:
            print(f"❌ {str(e)[:40]}")
            failed_v2 += 1
    
    # Resumen total
    total_passed = passed_v1 + passed_v2
    total_failed = failed_v1 + failed_v2
    total_tests = total_passed + total_failed
    
    print("\n" + "="*80)
    print("📊 RESUMEN GENERAL")
    print("="*80)
    print(f"\n📦 VERSIÓN 1:")
    print(f"   ✅ Pasados:  {passed_v1}")
    print(f"   ❌ Fallidos: {failed_v1}")
    print(f"   📈 Tasa:     {passed_v1}/{passed_v1+failed_v1} ({100*passed_v1//(passed_v1+failed_v1) if passed_v1+failed_v1 > 0 else 0}%)")
    
    print(f"\n📦 VERSIÓN 2:")
    print(f"   ✅ Pasados:  {passed_v2}")
    print(f"   ❌ Fallidos: {failed_v2}")
    print(f"   📈 Tasa:     {passed_v2}/{passed_v2+failed_v2} ({100*passed_v2//(passed_v2+failed_v2) if passed_v2+failed_v2 > 0 else 0}%)")
    
    print(f"\n🎯 TOTAL:")
    print(f"   ✅ Pasados:  {total_passed}")
    print(f"   ❌ Fallidos: {total_failed}")
    print(f"   📈 Tasa:     {total_passed}/{total_tests} ({100*total_passed//total_tests if total_tests > 0 else 0}%)")
    print("="*80)
    
    return total_passed, total_failed


if __name__ == "__main__":
    ejecutar_test_maestro()
