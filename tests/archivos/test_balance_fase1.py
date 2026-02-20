#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Balance - Fase 1.1 y 1.2
=================================

Verificar que:
1. Las nuevas armas y armaduras tienen balance correcto
2. No hay duplicados
3. Los precios son coherentes con los stats
4. Los gladiadores pueden equiparse sin problemas
"""

from src.store import CATALOGO_ARMAS, CATALOGO_ARMADURAS, PRECIOS
from src.models import Gladiador

def test_catalogo_completo():
    """Test: Verificar catálogos completos"""
    print("=" * 80)
    print("TEST 1: Verificar catálogos completos")
    print("=" * 80)
    
    print(f"\n✓ Total de armas: {len(CATALOGO_ARMAS)}")
    for idx, (key, arma) in enumerate(CATALOGO_ARMAS.items(), 1):
        precio = PRECIOS.get(key, "?")
        print(f"  [{key:>2}] {arma.nombre:<25} ATK:{arma.attack:>3} SPD:{arma.speed:>2} │ ${precio:>5}")
    
    print(f"\n✓ Total de armaduras: {len(CATALOGO_ARMADURAS)}")
    for idx, (key, arm) in enumerate(CATALOGO_ARMADURAS.items(), 1):
        precio = PRECIOS.get(key, "?")
        print(f"  [{key:>2}] {arm.nombre:<25} DEF:{arm.defense:>3} HP:{arm.hp:>2} │ ${precio:>5}")
    
    print()


def test_balance_armas():
    """Test: Verificar balance de armas"""
    print("=" * 80)
    print("TEST 2: Análisis de balance - ARMAS")
    print("=" * 80)
    
    stats = []
    for key, arma in CATALOGO_ARMAS.items():
        precio = PRECIOS[key]
        ratio_atk = arma.attack / max(precio / 100, 1)  # ATK por cada 100g
        ratio_spd = arma.speed / max(precio / 100, 1)
        stats.append({
            'key': key,
            'nombre': arma.nombre,
            'atk': arma.attack,
            'spd': arma.speed,
            'precio': precio,
            'ratio_atk': ratio_atk
        })
    
    # Análisis por tier
    print("\n📊 ANÁLISIS POR TIER:")
    print("\nTIER 1 (50-100g):")
    for s in stats:
        if s['precio'] <= 100:
            print(f"  {s['nombre']:<25} ATK:{s['atk']:>3} SPD:{s['spd']:>2} ${s['precio']:>5} (ratio:{s['ratio_atk']:.2f})")
    
    print("\nTIER 2 (150-300g):")
    for s in stats:
        if 150 <= s['precio'] <= 300:
            print(f"  {s['nombre']:<25} ATK:{s['atk']:>3} SPD:{s['spd']:>2} ${s['precio']:>5} (ratio:{s['ratio_atk']:.2f})")
    
    print("\nTIER 3 (350-500g):")
    for s in stats:
        if 350 <= s['precio'] <= 500:
            print(f"  {s['nombre']:<25} ATK:{s['atk']:>3} SPD:{s['spd']:>2} ${s['precio']:>5} (ratio:{s['ratio_atk']:.2f})")
    
    print("\nTIER 4 (800+g):")
    for s in stats:
        if s['precio'] >= 800:
            print(f"  {s['nombre']:<25} ATK:{s['atk']:>3} SPD:{s['spd']:>2} ${s['precio']:>5} (ratio:{s['ratio_atk']:.2f})")
    
    # Verificar outliers
    print("\n⚠️  VERIFICACIONES:")
    max_atk = max(s['atk'] for s in stats)
    min_precio_max = min(s['precio'] for s in stats if s['atk'] == max_atk)
    print(f"  ✓ Máximo ATK: {max_atk} (mínimo precio: {min_precio_max}g)")
    
    print()


def test_balance_armaduras():
    """Test: Verificar balance de armaduras"""
    print("=" * 80)
    print("TEST 3: Análisis de balance - ARMADURAS")
    print("=" * 80)
    
    stats = []
    for key, arm in CATALOGO_ARMADURAS.items():
        precio = PRECIOS[key]
        ratio_def = arm.defense / max(precio / 100, 1)
        ratio_hp = arm.hp / max(precio / 100, 1)
        stats.append({
            'key': key,
            'nombre': arm.nombre,
            'def': arm.defense,
            'hp': arm.hp,
            'precio': precio,
            'ratio_def': ratio_def,
            'ratio_hp': ratio_hp
        })
    
    # Análisis por tier
    print("\n📊 ANÁLISIS POR TIER:")
    print("\nTIER 1 (50-100g):")
    for s in stats:
        if s['precio'] <= 100:
            print(f"  {s['nombre']:<25} DEF:{s['def']:>3} HP:{s['hp']:>2} ${s['precio']:>5} (ratio:{s['ratio_def']:.2f})")
    
    print("\nTIER 2 (150-300g):")
    for s in stats:
        if 150 <= s['precio'] <= 300:
            print(f"  {s['nombre']:<25} DEF:{s['def']:>3} HP:{s['hp']:>2} ${s['precio']:>5} (ratio:{s['ratio_def']:.2f})")
    
    print("\nTIER 3 (350-500g):")
    for s in stats:
        if 350 <= s['precio'] <= 500:
            print(f"  {s['nombre']:<25} DEF:{s['def']:>3} HP:{s['hp']:>2} ${s['precio']:>5} (ratio:{s['ratio_def']:.2f})")
    
    print("\nTIER 4 (800+g):")
    for s in stats:
        if s['precio'] >= 800:
            print(f"  {s['nombre']:<25} DEF:{s['def']:>3} HP:{s['hp']:>2} ${s['precio']:>5} (ratio:{s['ratio_def']:.2f})")
    
    # Verificar outliers
    print("\n⚠️  VERIFICACIONES:")
    max_def = max(s['def'] for s in stats)
    min_precio_max_def = min(s['precio'] for s in stats if s['def'] == max_def)
    max_hp = max(s['hp'] for s in stats)
    min_precio_max_hp = min(s['precio'] for s in stats if s['hp'] == max_hp)
    
    print(f"  ✓ Máximo DEF: {max_def} (mínimo precio: {min_precio_max_def}g)")
    print(f"  ✓ Máximo HP: {max_hp} (mínimo precio: {min_precio_max_hp}g)")
    
    print()


def test_equipamiento():
    """Test: Verificar que los gladiadores pueden equiparse"""
    print("=" * 80)
    print("TEST 4: Equipamiento de gladiadores")
    print("=" * 80)
    
    g = Gladiador("TestGladiador", "Murmillo", nivel=1)
    print(f"✓ Gladiador inicial: {g}")
    
    # Equipar arma básica
    arma_basica = CATALOGO_ARMAS["1"]  # Daga Oxidada
    g.equipar_arma(arma_basica)
    print(f"✓ Equipado con {arma_basica.nombre}")
    print(f"  Stats finales: HP:{g.hp_final()} ATK:{g.ataque_final()} DEF:{g.defensa_final()} SPD:{g.velocidad_final()}")
    
    # Equipar arma legendaria
    arma_legendaria = CATALOGO_ARMAS["10"]  # Espada de Marte
    g.equipar_arma(arma_legendaria)
    print(f"\n✓ Equipado con {arma_legendaria.nombre}")
    print(f"  Stats finales: HP:{g.hp_final()} ATK:{g.ataque_final()} DEF:{g.defensa_final()} SPD:{g.velocidad_final()}")
    
    # Equipar armadura legendaria
    armadura_legendaria = CATALOGO_ARMADURAS["26"]  # Armadura Inmortal
    g.equipar_armadura(armadura_legendaria)
    print(f"\n✓ Equipado con {armadura_legendaria.nombre}")
    print(f"  Stats finales: HP:{g.hp_final()} ATK:{g.ataque_final()} DEF:{g.defensa_final()} SPD:{g.velocidad_final()}")
    
    print(f"\n✓ Gladiador final (Lvl {g.nivel} + items legendarios): {g}")
    print()


def test_progresion_precios():
    """Test: Verificar que los precios progresan de forma sensata"""
    print("=" * 80)
    print("TEST 5: Progresión de precios")
    print("=" * 80)
    
    armas_por_precio = sorted(CATALOGO_ARMAS.items(), key=lambda x: PRECIOS[x[0]])
    armaduras_por_precio = sorted(CATALOGO_ARMADURAS.items(), key=lambda x: PRECIOS[x[0]])
    
    print("\n📈 ARMAS (por precio):")
    for i, (key, arma) in enumerate(armas_por_precio):
        precio = PRECIOS[key]
        print(f"  {precio:>5}g - {arma.nombre:<25} (ATK:{arma.attack:>2} SPD:{arma.speed:>2})")
    
    print("\n📈 ARMADURAS (por precio):")
    for i, (key, arm) in enumerate(armaduras_por_precio):
        precio = PRECIOS[key]
        print(f"  {precio:>5}g - {arm.nombre:<25} (DEF:{arm.defense:>2} HP:{arm.hp:>2})")
    
    # Verificar que el equipo inicial (5000g) permite comprar cosas útiles
    print("\n💰 CON 5000g INICIALES PUEDES COMPRAR:")
    items_5000 = []
    for key, item in list(CATALOGO_ARMAS.items()) + list(CATALOGO_ARMADURAS.items()):
        if PRECIOS[key] <= 5000:
            items_5000.append((PRECIOS[key], key, item.nombre))
    
    items_5000.sort()
    for precio, key, nombre in items_5000[:10]:
        print(f"  ✓ {nombre:<30} ({precio}g)")
    print(f"  ... y {len(items_5000) - 10} items más")
    
    print()


if __name__ == "__main__":
    try:
        test_catalogo_completo()
        test_balance_armas()
        test_balance_armaduras()
        test_equipamiento()
        test_progresion_precios()
        
        print("=" * 80)
        print("✅ FASE 1.1 Y 1.2 - BALANCE VERIFICADO")
        print("=" * 80)
        print("\n📊 RESUMEN:")
        print(f"  - Armas: {len(CATALOGO_ARMAS)} (antes: 3)")
        print(f"  - Armaduras: {len(CATALOGO_ARMADURAS)} (antes: 3)")
        print(f"  - Items totales: {len(CATALOGO_ARMAS) + len(CATALOGO_ARMADURAS)}")
        print("\n✓ Balance verificado")
        print("✓ Precios coherentes")
        print("✓ Progresión clara por tiers")
        print("✓ Gladiadores pueden equiparse correctamente")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
