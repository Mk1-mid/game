#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST MAESTRO ACTUALIZADO
========================

Test suite integrado con el nuevo sistema de Critico y Esquiva.
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
from tests.test_forja import (
    test_calcular_stats_forja,
    test_forjar_arma_basica,
    test_forjar_arma_especial,
    test_forjar_arma_mitica,
    test_forjar_sin_herrero,
    test_forjar_sin_dinero,
    test_forjar_sin_materiales,
    test_mejora_arma_comun,
    test_mejora_arma_especial,
    test_mejora_arma_mitica,
    test_mejora_historica_bloqueada,
    test_reparacion_historica_bloqueada,
    test_efecto_falx_dacia,
    test_efecto_rhomphaia,
    test_efecto_katana,
    test_efecto_hacha_dane,
    test_persistencia_arma_forjada,
    test_persistencia_arma_historica,
    test_crear_arma_historica,
    test_efecto_khopesh,
    test_recetas_materiales,
    test_herrero_nivel_bloquea_rareza,
    test_multiplicador_tipo_arma,
    test_costos_forja_base,
    test_costos_mejora_base,
    test_porcentajes_mejora,
    test_armas_historicas_definidas,
)
from tests.test_talents import (
    test_bonus_fuerza,
    test_bonus_resistencia,
    test_bonus_agilidad,
    test_bonus_tecnica,
    test_bonus_completo,
    test_asignar_talento,
    test_asignar_sin_puntos,
    test_asignar_nivel_maximo,
    test_asignar_rama_invalida,
    test_puede_asignar_ok,
    test_puede_asignar_sin_puntos,
    test_puede_asignar_max,
    test_habilidad_unica_fuerza,
    test_habilidades_unicas_completas,
    test_sin_habilidades_unicas,
    test_puntos_subir_nivel,
    test_arbol_vacio_inicial,
    test_seria_talentos,
    test_sin_puntos_persistencia,
    test_compatibilidad_datos_antiguos,
    test_resumen_talentos,
)


def run_all_tests():
    """Ejecuta todos los tests disponibles."""
    
    tests = [
        ("Arquetipos Creacion", test_arquetipos_creacion),
        ("Agilidad Efectiva", test_agilidad_efectiva),
        ("Derivados Correctos", test_derivados_correctos),
        ("Arquetipos Diferenciados", test_arquetipos_diferenciados),
        ("Escalado con Nivel", test_escalado_con_nivel),
        ("Probabilidades Combate", test_probabilidades_combate),
        ("Persistencia Stats", test_persistencia_stats),
        # --- Fase 3.1: Leaderboards Globales ---
        ("Leaderboards: Actualizar y Top", test_actualizar_y_top),
        ("Leaderboards: Maximo historico", test_maximo_historico),
        ("Leaderboards: Limite Top 10", test_limite_top10),
        ("Leaderboards: Entradas invalidas", test_entradas_invalidas),
        ("Leaderboards: Persistencia ciclo completo", test_persistencia_ciclo_completo),
        ("Leaderboards: Posicion de jugador", test_posicion_jugador),
        # --- Fase 3.2: Patricios ---
        ("Patricios: Generacion", test_generar_patricios),
        ("Patricios: Simulacion diaria", test_simular_dia),
        ("Patricios: Serializacion", test_serializacion_patricios),
        ("Patricios: Rival mas fuerte", test_rival_mas_fuerte),
        ("Patricios: Limites afinidad", test_patricio_modificar_afinidad),
        # --- Fase 3.2: Eventos ---
        ("Eventos: Probabilidad global", test_tirar_evento_probabilidad),
        ("Eventos: Condiciones", test_evento_condiciones),
        ("Eventos: Rumor de soborno", test_resolver_rumor_soborno),
        ("Eventos: Donacion", test_resolver_donacion),
        ("Eventos: Prestamo", test_resolver_prestamo),
        ("Eventos: Procesar prestamos", test_procesar_prestamos),
        ("Eventos: Honra y racha", test_honra_y_racha),
        ("Eventos: Penitencia publica", test_penitencia_publica),
        ("Eventos: Titulos honra", test_titulos_honra),
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
        ("Instalaciones: Yield dias", test_yield_dias),
        ("Instalaciones: Trabajo asignacion", test_trabajo_asignacion),
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
        # --- Fase 3.4: Herreria Ampliada (Forja) ---
        ("Forja: Stats forja", test_calcular_stats_forja),
        ("Forja: Arma comun", test_forjar_arma_basica),
        ("Forja: Arma especial", test_forjar_arma_especial),
        ("Forja: Arma mitica", test_forjar_arma_mitica),
        ("Forja: Sin herrero", test_forjar_sin_herrero),
        ("Forja: Sin dinero", test_forjar_sin_dinero),
        ("Forja: Sin materiales", test_forjar_sin_materiales),
        ("Forja: Mejora comun", test_mejora_arma_comun),
        ("Forja: Mejora especial", test_mejora_arma_especial),
        ("Forja: Mejora mitica", test_mejora_arma_mitica),
        ("Forja: Historica no mejora", test_mejora_historica_bloqueada),
        ("Forja: Historica no repara", test_reparacion_historica_bloqueada),
        ("Forja: Falx Dacia", test_efecto_falx_dacia),
        ("Forja: Rhomphaia", test_efecto_rhomphaia),
        ("Forja: Katana", test_efecto_katana),
        ("Forja: Hacha Dane", test_efecto_hacha_dane),
        ("Forja: Persistencia forjada", test_persistencia_arma_forjada),
        ("Forja: Persistencia historica", test_persistencia_arma_historica),
        ("Forja: Crear historica", test_crear_arma_historica),
        ("Forja: Khopesh", test_efecto_khopesh),
        ("Forja: Recetas materiales", test_recetas_materiales),
        ("Forja: Herrero nivel", test_herrero_nivel_bloquea_rareza),
        ("Forja: Mult. tipo", test_multiplicador_tipo_arma),
        ("Forja: Costos forja", test_costos_forja_base),
        ("Forja: Costos mejora", test_costos_mejora_base),
        ("Forja: % mejora", test_porcentajes_mejora),
        ("Forja: Arm. historicas", test_armas_historicas_definidas),
        ("Forja: Khopesh efecto", test_efecto_khopesh),
        ("Forja: Rhomphaia efecto", test_efecto_rhomphaia),
        ("Forja: Katana efecto", test_efecto_katana),
        ("Forja: Hacha Dane efecto", test_efecto_hacha_dane),
        ("Forja: Persistencia forjada", test_persistencia_arma_forjada),
        ("Forja: Persistencia historica", test_persistencia_arma_historica),
        ("Forja: Crear historica", test_crear_arma_historica),
        ("Forja: Recetas materiales", test_recetas_materiales),
        ("Forja: Herrero nivel", test_herrero_nivel_bloquea_rareza),
        ("Forja: Mult. tipo", test_multiplicador_tipo_arma),
        ("Forja: Costos forja", test_costos_forja_base),
        ("Forja: Costos mejora", test_costos_mejora_base),
        ("Forja: % mejora", test_porcentajes_mejora),
        ("Forja: Arm. historicas", test_armas_historicas_definidas),
        ("Forja: Khopesh efecto", test_efecto_khopesh),
        ("Forja: Rhomphaia efecto", test_efecto_rhomphaia),
        ("Forja: Katana efecto", test_efecto_katana),
        ("Forja: Hacha Dane efecto", test_efecto_hacha_dane),
        ("Forja: Persistencia forjada", test_persistencia_arma_forjada),
        ("Forja: Persistencia historica", test_persistencia_arma_historica),
        ("Forja: Crear historica", test_crear_arma_historica),
        ("Forja: Recetas materiales", test_recetas_materiales),
        ("Forja: Herrero nivel", test_herrero_nivel_bloquea_rareza),
        ("Forja: Mult. tipo", test_multiplicador_tipo_arma),
        ("Forja: Costos forja", test_costos_forja_base),
        ("Forja: Costos mejora", test_costos_mejora_base),
        ("Forja: % mejora", test_porcentajes_mejora),
        ("Forja: Arm. historicas", test_armas_historicas_definidas),
        # --- Fase 4: Árbol de Talentos ---
        ("Talentos: Bonus fuerza", test_bonus_fuerza),
        ("Talentos: Bonus resistencia", test_bonus_resistencia),
        ("Talentos: Bonus agilidad", test_bonus_agilidad),
        ("Talentos: Bonus técnica", test_bonus_tecnica),
        ("Talentos: Bonus completo", test_bonus_completo),
        ("Talentos: Asignar punto", test_asignar_talento),
        ("Talentos: Sin puntos", test_asignar_sin_puntos),
        ("Talentos: Nivel máximo", test_asignar_nivel_maximo),
        ("Talentos: Rama inválida", test_asignar_rama_invalida),
        ("Talentos: Puede asignar OK", test_puede_asignar_ok),
        ("Talentos: Puede asignar sin puntos", test_puede_asignar_sin_puntos),
        ("Talentos: Puede asignar máximo", test_puede_asignar_max),
        ("Talentos: Habilidad única fuerza", test_habilidad_unica_fuerza),
        ("Talentos: Habilidades únicas completas", test_habilidades_unicas_completas),
        ("Talentos: Sin habilidades únicas", test_sin_habilidades_unicas),
        ("Talentos: Puntos subir nivel", test_puntos_subir_nivel),
        ("Talentos: Árbol vacío inicial", test_arbol_vacio_inicial),
        ("Talentos: Serializar talentos", test_seria_talentos),
        ("Talentos: Persistencia 0 puntos", test_sin_puntos_persistencia),
        ("Talentos: Compatibilidad datos antiguos", test_compatibilidad_datos_antiguos),
        ("Talentos: Resumen completo", test_resumen_talentos),
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
            print(f"\n[FAIL] FALLO: {name}")
            print(f"   Error: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"RESULTADOS: {passed} Pasados, {failed} Fallidos")
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
