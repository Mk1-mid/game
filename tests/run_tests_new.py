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
from tests.test_leaderboards import (
    test_actualizar_y_top,
    test_maximo_historico,
    test_limite_top10,
    test_entradas_invalidas,
    test_persistencia_ciclo_completo,
    test_posicion_jugador
)
from tests.test_patricios import (
    test_generar_patricios,
    test_simular_dia,
    test_serializacion_patricios,
    test_rival_mas_fuerte,
    test_patricio_modificar_afinidad
)
from tests.test_events import (
    test_tirar_evento_probabilidad,
    test_evento_condiciones,
    test_resolver_rumor_soborno,
    test_resolver_donacion,
    test_resolver_prestamo,
    test_procesar_prestamos,
    test_honra_y_racha,
    test_penitencia_publica,
    test_titulos_honra,
    test_modificador_mercado,
    test_persistencia_eventos,
    test_material_aleatorio
)
from tests.test_instalaciones import (
    test_compra_instalacion,
    test_compra_sin_herrero,
    test_compra_sin_dinero,
    test_mejora_niveles,
    test_ingreso_pasivo,
    test_probabilidades_base,
    test_probabilidades_dias_clamp,
    test_riesgo_herida,
    test_yield_dias,
    test_trabajo_asignacion,
    test_trabajo_completado_recompensas,
    test_trabajo_granja_agilidad,
    test_trabajo_aserradero_hp,
    test_riesgo_herida_aplicado,
    test_persistencia_instalaciones,
    test_persistencia_equipo_con_instalaciones,
    test_tres_instalaciones_materiales,
    test_ingreso_pasivo_no_reemplaza_arena,
    test_prerequisito_herrero_tres,
    test_constructor_instancias,
    test_matrices_materiales,
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
        # --- Fase 3.1: Leaderboards Globales ---
        ("Leaderboards: Actualizar y Top", test_actualizar_y_top),
        ("Leaderboards: Máximo histórico", test_maximo_historico),
        ("Leaderboards: Límite Top 10", test_limite_top10),
        ("Leaderboards: Entradas inválidas", test_entradas_invalidas),
        ("Leaderboards: Persistencia ciclo completo", test_persistencia_ciclo_completo),
        ("Leaderboards: Posición de jugador", test_posicion_jugador),
        # --- Fase 3.2: Patricios ---
        ("Patricios: Generación", test_generar_patricios),
        ("Patricios: Simulación diaria", test_simular_dia),
        ("Patricios: Serialización", test_serializacion_patricios),
        ("Patricios: Rival más fuerte", test_rival_mas_fuerte),
        ("Patricios: Límites afinidad", test_patricio_modificar_afinidad),
        # --- Fase 3.2: Eventos ---
        ("Eventos: Probabilidad global", test_tirar_evento_probabilidad),
        ("Eventos: Condiciones", test_evento_condiciones),
        ("Eventos: Rumor de soborno", test_resolver_rumor_soborno),
        ("Eventos: Donación", test_resolver_donacion),
        ("Eventos: Préstamo", test_resolver_prestamo),
        ("Eventos: Procesar préstamos", test_procesar_prestamos),
        ("Eventos: Honra y racha", test_honra_y_racha),
        ("Eventos: Penitencia pública", test_penitencia_publica),
        ("Eventos: Títulos honra", test_titulos_honra),
        ("Eventos: Modificador mercado", test_modificador_mercado),
        ("Eventos: Persistencia", test_persistencia_eventos),
        ("Eventos: Material aleatorio", test_material_aleatorio),
        # --- Fase 3.3: Instalaciones de Recursos ---
        ("Instalaciones: Compra con herrero", test_compra_instalacion),
        ("Instalaciones: Compra sin herrero", test_compra_sin_herrero),
        ("Instalaciones: Compra sin dinero", test_compra_sin_dinero),
        ("Instalaciones: Mejoras niveles", test_mejora_niveles),
        ("Instalaciones: Ingreso pasivo", test_ingreso_pasivo),
        ("Instalaciones: Probabilidades base", test_probabilidades_base),
        ("Instalaciones: Probabilidades clamp", test_probabilidades_dias_clamp),
        ("Instalaciones: Riesgo herida", test_riesgo_herida),
        ("Instalaciones: Yield días", test_yield_dias),
        ("Instalaciones: Trabajo asignación", test_trabajo_asignacion),
        ("Instalaciones: Trabajo recompensas", test_trabajo_completado_recompensas),
        ("Instalaciones: Granja agilidad", test_trabajo_granja_agilidad),
        ("Instalaciones: Aserradero HP", test_trabajo_aserradero_hp),
        ("Instalaciones: Riesgo herida aplicado", test_riesgo_herida_aplicado),
        ("Instalaciones: Persistencia instalaciones", test_persistencia_instalaciones),
        ("Instalaciones: Persistencia equipo completo", test_persistencia_equipo_con_instalaciones),
        ("Instalaciones: 3 instalaciones materiales", test_tres_instalaciones_materiales),
        ("Instalaciones: Ingreso no reemplaza arena", test_ingreso_pasivo_no_reemplaza_arena),
        ("Instalaciones: Prerequisito herrero 3", test_prerequisito_herrero_tres),
        ("Instalaciones: Constructor 3 instancias", test_constructor_instancias),
        ("Instalaciones: Matrices materiales", test_matrices_materiales),
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
