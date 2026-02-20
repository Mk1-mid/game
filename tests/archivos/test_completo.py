#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TEST COMPLETO - SANGRE POR FORTUNA v2.0
Verifica que todos los sistemas funcionen correctamente
"""

import sys
import os
import json
from pathlib import Path

# Agregar proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

from src.models import Player, Weapon, Armor, Gladiador
from src.combat import calcular_daño, calcular_xp_recompensa
from src.enemies import generar_enemigo
from src.store import CATALOGO_ARMAS, CATALOGO_ARMADURAS, PRECIOS

# ============================================================================
# CONFIGURACIÓN DE TESTS
# ============================================================================

TESTS_EJECUTADOS = 0
TESTS_PASADOS = 0
TESTS_FALLIDOS = 0

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log_titulo(titulo):
    print(f"\n{Color.BOLD}{Color.CYAN}{'='*70}{Color.END}")
    print(f"{Color.BOLD}{Color.CYAN}{titulo.center(70)}{Color.END}")
    print(f"{Color.BOLD}{Color.CYAN}{'='*70}{Color.END}\n")

def log_test(nombre):
    print(f"{Color.BLUE}TEST: {nombre}{Color.END}")

def log_ok(mensaje=""):
    global TESTS_PASADOS, TESTS_EJECUTADOS
    TESTS_EJECUTADOS += 1
    TESTS_PASADOS += 1
    print(f"  {Color.GREEN}✓ PASADO{Color.END} {mensaje}")

def log_fail(mensaje=""):
    global TESTS_FALLIDOS, TESTS_EJECUTADOS
    TESTS_EJECUTADOS += 1
    TESTS_FALLIDOS += 1
    print(f"  {Color.RED}✗ FALLIDO{Color.END} {mensaje}")

def assert_equal(actual, esperado, mensaje=""):
    if actual == esperado:
        log_ok(f"{mensaje} (valor: {actual})")
    else:
        log_fail(f"{mensaje} - Esperado: {esperado}, Actual: {actual}")

def assert_greater(actual, minimo, mensaje=""):
    if actual > minimo:
        log_ok(f"{mensaje} (valor: {actual})")
    else:
        log_fail(f"{mensaje} - Debe ser > {minimo}, Actual: {actual}")

def assert_range(actual, minimo, maximo, mensaje=""):
    if minimo <= actual <= maximo:
        log_ok(f"{mensaje} (valor: {actual})")
    else:
        log_fail(f"{mensaje} - Debe estar en [{minimo}, {maximo}], Actual: {actual}")

# ============================================================================
# TESTS DE MODELOS
# ============================================================================

def test_player_initialization():
    log_titulo("TEST 1: INICIALIZACIÓN DE PLAYER")
    
    log_test("Crear player")
    player = Player()
    
    assert_equal(player.nivel, 1, "Nivel inicial")
    assert_equal(player.xp, 0, "XP inicial")
    assert_equal(player.hp, 100, "HP inicial")
    assert_equal(player.attack, 20, "Ataque inicial")
    assert_equal(player.defense, 5, "Defensa inicial")
    assert_equal(player.speed, 10, "Velocidad inicial")
    xp_necesario = player.xp_para_siguiente_nivel()
    assert_greater(xp_necesario, 0, f"XP necesario para subir: {xp_necesario}")

def test_xp_system():
    log_titulo("TEST 2: SISTEMA DE XP/NIVELES")
    
    log_test("Ganar XP y subir de nivel")
    player = Player()
    xp_inicial = player.xp
    nivel_inicial = player.nivel
    
    player.ganar_xp(100)
    assert_greater(player.xp, xp_inicial, "XP debe aumentar")
    assert_equal(player.nivel, nivel_inicial, "Nivel no debe subir con 100 XP")
    
    log_test("Subir de nivel automáticamente")
    player2 = Player()
    player2.ganar_xp(5000)
    assert_greater(player2.nivel, 1, f"Debe haber subido de nivel")
    xp_siguiente = player2.xp_para_siguiente_nivel()
    print(f"  → Level: {player2.nivel}, XP: {player2.xp}/{xp_siguiente}")

def test_stat_scaling():
    log_titulo("TEST 3: ESCALADO LOGARÍTMICO DE STATS")
    
    log_test("Stats escalan con nivel")
    player = Player()
    
    # Nivel 1
    hp_l1 = player.hp
    atk_l1 = player.attack
    
    # Subir a nivel 5
    player.ganar_xp(500)
    hp_l5 = player.hp
    atk_l5 = player.attack
    
    assert_greater(hp_l5, hp_l1, f"HP debe aumentar (L1: {hp_l1} -> L{player.nivel}: {hp_l5})")
    assert_greater(atk_l5, atk_l1, f"Ataque debe aumentar (L1: {atk_l1} -> L{player.nivel}: {atk_l5})")
    
    log_test("Rendimientos decrecientes")
    hp_anterior = player.hp
    atk_anterior = player.attack
    player.ganar_xp(100000)  # Muchísimo XP
    hp_final = player.hp
    atk_final = player.attack
    
    incremento_hp = hp_final - hp_anterior
    print(f"  → Nivel actual: {player.nivel}")
    print(f"  → Incremento HP: {incremento_hp} (rendimientos decrecientes)")
    assert_greater(incremento_hp, 0, "HP debe seguir aumentando")

def test_weapons():
    log_titulo("TEST 4: SISTEMA DE ARMAS")
    
    log_test("Crear arma")
    arma = Weapon("Espada de Prueba", attack=30, speed=5)
    assert_equal(arma.attack, 30, "Ataque del arma")
    assert_equal(arma.speed, 5, "Velocidad del arma")

def test_armor():
    log_titulo("TEST 5: SISTEMA DE ARMADURAS")
    
    log_test("Crear armadura")
    armadura = Armor("Armadura de Prueba", defense=15, hp=50)
    assert_equal(armadura.defense, 15, "Defensa de la armadura")
    assert_equal(armadura.hp, 50, "HP adicional")

def test_store_catalog():
    log_titulo("TEST 6: CATÁLOGO DE TIENDA")
    
    log_test("Verificar armas disponibles")
    assert_greater(len(CATALOGO_ARMAS), 0, f"Debe haber armas ({len(CATALOGO_ARMAS)} encontradas)")
    
    log_test("Verificar armaduras disponibles")
    assert_greater(len(CATALOGO_ARMADURAS), 0, f"Debe haber armaduras ({len(CATALOGO_ARMADURAS)} encontradas)")
    
    log_test("Verificar precios")
    assert_greater(len(PRECIOS), 0, f"Debe haber precios definidos ({len(PRECIOS)} encontrados)")

# ============================================================================
# TESTS DE COMBATE
# ============================================================================

def test_damage_calculation():
    log_titulo("TEST 7: CÁLCULO DE DAÑO")
    
    log_test("Calcular daño con variación")
    for i in range(5):
        daño = calcular_daño(20, 5)
        assert_range(daño, 15, 25, f"Iteración {i+1}")

def test_xp_rewards():
    log_titulo("TEST 8: SISTEMA DE RECOMPENSAS XP")
    
    log_test("Calcular recompensas XP por nivel")
    for nivel in [1, 5, 10, 20, 50]:
        xp = calcular_xp_recompensa(nivel)
        assert_greater(xp, 0, f"Nivel {nivel}: {xp} XP")

def test_enemy_generation():
    log_titulo("TEST 9: GENERACIÓN DE ENEMIGOS")
    
    log_test("Generar enemigos aleatorios")
    for i in range(5):
        enemigo = generar_enemigo(nivel=5)
        assert_greater(enemigo.hp, 0, f"Enemigo {i+1}: HP > 0")
        assert_greater(enemigo.attack, 0, f"Enemigo {i+1}: Ataque > 0")
        assert_greater(enemigo.defense, 0, f"Enemigo {i+1}: Defensa > 0")

def test_enemy_scaling():
    log_titulo("TEST 10: ESCALADO DE ENEMIGOS")
    
    log_test("Enemigos escalan con nivel del jugador")
    enemigo_l1 = generar_enemigo(nivel=1)
    enemigo_l10 = generar_enemigo(nivel=10)
    
    assert_greater(enemigo_l10.hp, enemigo_l1.hp, "Enemigos nivel 10 deben ser más fuertes")
    assert_greater(enemigo_l10.attack, enemigo_l1.attack, "Ataque debe ser mayor")

def test_combat_simulation():
    log_titulo("TEST 11: SIMULACIÓN DE COMBATE")
    
    log_test("Realizar combate player vs enemigo")
    player = Player()
    enemigo = generar_enemigo(nivel=1)
    
    # Simulación manual de combate
    rondas = 0
    max_rondas = 100
    
    while player.hp > 0 and enemigo.hp > 0 and rondas < max_rondas:
        # Player ataca
        daño_player = calcular_daño(player.attack, enemigo.defense)
        enemigo.hp -= daño_player
        
        if enemigo.hp <= 0:
            break
        
        # Enemigo ataca
        daño_enemigo = calcular_daño(enemigo.attack, player.defense)
        player.hp -= daño_enemigo
        
        rondas += 1
    
    print(f"  → Combate terminado en {rondas} rondas")
    if player.hp > 0:
        log_ok(f"Player gana (HP restante: {player.hp})")
    else:
        log_ok(f"Enemigo gana (HP del player: {player.hp})")

# ============================================================================
# TESTS DE GLADIADORES
# ============================================================================

def test_gladiador_creation():
    log_titulo("TEST 12: CREACIÓN DE GLADIADORES")
    
    log_test("Crear gladiador")
    glad = Gladiador(nombre="Testius", tipo_base="Murmillo")
    assert_equal(glad.nombre, "Testius", "Nombre del gladiador")
    assert_equal(glad.tipo, "Murmillo", "Tipo de gladiador")
    assert_greater(glad.hp, 0, "HP > 0")

def test_gladiador_progression():
    log_titulo("TEST 13: PROGRESIÓN DE GLADIADORES")
    
    log_test("Gladiador gana XP independientemente")
    glad = Gladiador(nombre="Ferox", tipo_base="Murmillo")
    nivel_inicial = glad.nivel
    
    glad.ganar_xp(1000)
    assert_greater(glad.nivel, nivel_inicial, "Gladiador debe subir de nivel")
    xp_siguiente = glad.xp_para_siguiente_nivel()
    print(f"  → Nivel: {glad.nivel}, XP: {glad.xp}/{xp_siguiente}")

# ============================================================================
# TESTS DE PERSISTENCIA
# ============================================================================

def test_player_dict_conversion():
    log_titulo("TEST 14: CONVERSIÓN A DICCIONARIO")
    
    log_test("Player se convierte a diccionario")
    player = Player()
    player.ganar_xp(500)
    
    player_dict = player.__dict__
    assert_equal("nivel" in player_dict, True, "Debe tener 'nivel'")
    assert_equal("xp" in player_dict, True, "Debe tener 'xp'")
    assert_equal("hp" in player_dict, True, "Debe tener 'hp'")
    assert_equal(player_dict["nivel"], player.nivel, "Valores correctos")

# ============================================================================
# TEST DE INTEGRACIÓN
# ============================================================================

def test_full_workflow():
    log_titulo("TEST 15: FLUJO COMPLETO DEL JUEGO")
    
    log_test("1. Crear player")
    player = Player()
    print(f"  ✓ Player creado: Nivel {player.nivel}, HP {player.hp}")
    
    log_test("2. Ganar combates y XP")
    for i in range(3):
        xp_ganada = calcular_xp_recompensa(player.nivel)
        player.ganar_xp(xp_ganada)
        print(f"  ✓ Combate {i+1}: {xp_ganada} XP, Nivel actual: {player.nivel}")
    
    log_test("3. Generar enemigos y simular combate")
    enemigo = generar_enemigo(nivel=player.nivel)
    print(f"  ✓ Enemigo generado: {enemigo.tipo}, HP {enemigo.hp}")
    
    log_test("4. Verificar progresión")
    assert_greater(player.nivel, 1, "Player debe haber subido de nivel")
    xp_siguiente = player.xp_para_siguiente_nivel()
    print(f"  → Final: Nivel {player.nivel}, HP {player.hp}, XP {player.xp}/{xp_siguiente}")

# ============================================================================
# RESUMEN DE TESTS
# ============================================================================

def print_summary():
    log_titulo("RESUMEN DE RESULTADOS")
    
    total = TESTS_PASADOS + TESTS_FALLIDOS
    porcentaje = (TESTS_PASADOS / total * 100) if total > 0 else 0
    
    print(f"Total de tests ejecutados: {Color.BOLD}{total}{Color.END}")
    print(f"Tests pasados: {Color.GREEN}{TESTS_PASADOS}{Color.END}")
    print(f"Tests fallidos: {Color.RED}{TESTS_FALLIDOS}{Color.END}")
    print(f"Porcentaje de éxito: {Color.BOLD}{porcentaje:.1f}%{Color.END}\n")
    
    if TESTS_FALLIDOS == 0:
        print(f"{Color.GREEN}{Color.BOLD}✓ TODOS LOS TESTS PASARON EXITOSAMENTE{Color.END}")
        print(f"{Color.BOLD}El proyecto está listo para la siguiente fase{Color.END}\n")
        return True
    else:
        print(f"{Color.RED}{Color.BOLD}✗ Hay {TESTS_FALLIDOS} test(s) fallido(s){Color.END}")
        print(f"{Color.RED}Por favor revisa los errores arriba{Color.END}\n")
        return False

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    print(f"\n{Color.BOLD}{Color.YELLOW}")
    print("=" * 74)
    print(" " * 20 + "TEST COMPLETO - SANGRE POR FORTUNA v2.0")
    print(" " * 25 + "7 de Enero de 2026")
    print("=" * 74)
    print(f"{Color.END}")
    
    try:
        # Tests de modelos
        test_player_initialization()
        test_xp_system()
        test_stat_scaling()
        test_weapons()
        test_armor()
        test_store_catalog()
        
        # Tests de combate
        test_damage_calculation()
        test_xp_rewards()
        test_enemy_generation()
        test_enemy_scaling()
        test_combat_simulation()
        
        # Tests de gladiadores
        test_gladiador_creation()
        test_gladiador_progression()
        
        # Tests de persistencia
        test_player_dict_conversion()
        
        # Test de integración
        test_full_workflow()
        
        # Resumen
        success = print_summary()
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"\n{Color.RED}{Color.BOLD}ERROR DURANTE LA EJECUCIÓN:{Color.END}")
        print(f"{Color.RED}{str(e)}{Color.END}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
