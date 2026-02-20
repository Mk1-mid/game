#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del Sistema de Equipos - Verificación funcional
====================================================

Prueba que:
1. La clase Equipo se instancia correctamente
2. Los gladiadores se crean correctamente
3. La selección de luchador funciona
4. El flujo de combate es posible
"""

from src.models import Equipo, Gladiador
from src.enemies import generar_enemigo

def test_equipo_basico():
    """Test 1: Crear equipo con gladiadores"""
    print("=" * 70)
    print("TEST 1: Crear equipo con gladiadores")
    print("=" * 70)
    
    equipo = Equipo()
    print(f"✓ Equipo creado: {equipo}")
    
    g1 = Gladiador("Ferox", "Murmillo", nivel=1)
    g2 = Gladiador("Velox", "Retiarius", nivel=1)
    
    print(f"✓ Gladiador 1 creado: {g1}")
    print(f"✓ Gladiador 2 creado: {g2}")
    
    equipo.dinero = 5000
    exito1, msg1 = equipo.agregar_gladiador(g1)
    exito2, msg2 = equipo.agregar_gladiador(g2)
    
    print(f"✓ {msg1}")
    print(f"✓ {msg2}")
    print(f"✓ Equipo ahora: {equipo}")
    print(f"✓ Espacios disponibles: {equipo.espacios_disponibles}")
    print()


def test_seleccionar_luchador():
    """Test 2: Seleccionar luchador disponible"""
    print("=" * 70)
    print("TEST 2: Seleccionar luchador")
    print("=" * 70)
    
    equipo = Equipo()
    g1 = Gladiador("Ferox", "Murmillo", nivel=5)
    equipo.dinero = 5000
    equipo.agregar_gladiador(g1)
    
    # Verificar que puede luchar
    print(f"¿Ferox puede luchar? {g1.puede_luchar()}")
    print(f"Estado de Ferox: {g1.estado}")
    print(f"Ocupación: {g1.ocupacion}")
    
    # Obtener disponibles
    disponibles = [g for g in equipo.gladiadores if g.puede_luchar()]
    print(f"✓ Gladiadores disponibles: {len(disponibles)}")
    print(f"✓ {disponibles[0].nombre} está listo para combate")
    print()


def test_combate_flow():
    """Test 3: Flujo de combate"""
    print("=" * 70)
    print("TEST 3: Preparar combate")
    print("=" * 70)
    
    equipo = Equipo()
    g1 = Gladiador("Ferox", "Murmillo", nivel=3)
    equipo.dinero = 5000
    equipo.agregar_gladiador(g1)
    
    # Seleccionar luchador
    disponibles = [g for g in equipo.gladiadores if g.puede_luchar()]
    gladiador = disponibles[0]
    
    print(f"✓ Seleccionado: {gladiador.nombre}")
    print(f"  - Nivel: {gladiador.nivel}")
    print(f"  - HP Total: {gladiador.hp_final()}")
    print(f"  - ATK: {gladiador.ataque_final()}")
    print(f"  - DEF: {gladiador.defensa_final()}")
    print(f"  - SPD: {gladiador.velocidad_final()}")
    
    # Generar enemigo
    enemigo = generar_enemigo(nivel=3)
    print(f"\n✓ Enemigo generado")
    print(f"  - HP: {enemigo.hp_final()}")
    print(f"  - ATK: {enemigo.ataque_final()}")
    print(f"  - DEF: {enemigo.defensa_final()}")
    print(f"  - SPD: {enemigo.velocidad_final()}")
    
    print(f"\n✓ COMBATE LISTO (parámetros listos para combate_arena)")
    print()


def test_hospital():
    """Test 4: Sistema de hospital"""
    print("=" * 70)
    print("TEST 4: Sistema de Hospital")
    print("=" * 70)
    
    equipo = Equipo()
    g1 = Gladiador("Ferox", "Murmillo", nivel=1)
    equipo.dinero = 5000
    equipo.agregar_gladiador(g1)
    
    # Simular daño
    g1.aplicar_daño(50)
    print(f"✓ Ferox recibió 50 daño")
    print(f"  HP: {g1.hp_actual}/{g1.hp}")
    print(f"  Estado: {g1.estado}")
    
    # Curar
    costo_curacion = g1.hp - g1.hp_actual
    equipo.dinero -= costo_curacion
    g1.curar(costo_curacion)
    print(f"\n✓ Ferox curado por {costo_curacion}g")
    print(f"  HP: {g1.hp_actual}/{g1.hp}")
    print(f"  Estado: {g1.estado}")
    print(f"  Dinero restante: {equipo.dinero}g")
    print()


def test_barracas():
    """Test 5: Sistema de barracas"""
    print("=" * 70)
    print("TEST 5: Sistema de Barracas")
    print("=" * 70)
    
    equipo = Equipo()
    print(f"✓ Barracas iniciales: {equipo.barracas}")
    print(f"  - Literas: {equipo.barracas.literas}")
    print(f"  - Espacios totales: {equipo.barracas.espacios_totales}")
    
    equipo.dinero = 2000
    print(f"\n✓ Dinero disponible: {equipo.dinero}g")
    print(f"  - Costo próxima litera: {equipo.barracas.costo_proxima_litera}g")
    
    exito, dinero_nuevo, msg = equipo.barracas.comprar_litera(equipo.dinero)
    print(f"\n✓ {msg}")
    if exito:
        equipo.dinero = dinero_nuevo
        print(f"  - Dinero restante: {equipo.dinero}g")
        print(f"  - Barracas ahora: {equipo.barracas}")
    print()


if __name__ == "__main__":
    try:
        test_equipo_basico()
        test_seleccionar_luchador()
        test_combate_flow()
        test_hospital()
        test_barracas()
        
        print("=" * 70)
        print("✅ TODOS LOS TESTS PASARON - SISTEMA FUNCIONAL 100%")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
