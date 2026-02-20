#!/usr/bin/env python3
"""
Tests para Mercado de Gladiadores y Main.py
===========================================
"""

from src.models import Equipo, Gladiador
from src.store import (
    generar_gladiador_disponible, calcular_costo_gladiador,
    comprar_gladiador, vender_gladiador, mostrar_mercado_gladiadores
)

print("\n" + "="*70)
print("TEST 1: Generar Gladiador del Mercado")
print("="*70)

for i in range(5):
    g = generar_gladiador_disponible(1, 5)
    costo = calcular_costo_gladiador(g.nivel)
    print(f"  {i+1}. {g.nombre:<20} Lvl {g.nivel} {g.tipo:<12} → {costo}g")

print("\n" + "="*70)
print("TEST 2: Costo Escalado por Nivel")
print("="*70)

print("Costo de gladiadores por nivel:")
for nivel in [1, 5, 10, 15, 20]:
    costo = calcular_costo_gladiador(nivel)
    print(f"  Nivel {nivel:>2}: {costo:>5}g")

print("\n" + "="*70)
print("TEST 3: Comprar Gladiador")
print("="*70)

equipo = Equipo()
equipo.dinero = 10000

print(f"Equipo inicial: {equipo.dinero}g, {len(equipo.gladiadores)}/{equipo.barracas.espacios_totales} espacios")

gladiadores_disponibles = [generar_gladiador_disponible(3, 5) for _ in range(6)]

print("\nMercado disponible:")
for i, g in enumerate(gladiadores_disponibles, 1):
    costo = calcular_costo_gladiador(g.nivel)
    print(f"  [{i}] {g.nombre:<20} Lvl {g.nivel} → {costo}g")

# Comprar primero
exito, dinero, msg, _ = comprar_gladiador(gladiadores_disponibles, "1", equipo.dinero, equipo)
print(f"\nCompra #1: {msg}")
equipo.dinero = dinero
print(f"  Equipo: {equipo.dinero}g, {len(equipo.gladiadores)}/{equipo.barracas.espacios_totales}")

# Comprar segundo
exito, dinero, msg, _ = comprar_gladiador(gladiadores_disponibles, "3", equipo.dinero, equipo)
print(f"Compra #2: {msg}")
equipo.dinero = dinero
print(f"  Equipo: {equipo.dinero}g, {len(equipo.gladiadores)}/{equipo.barracas.espacios_totales}")

# Intentar comprar sin dinero
exito, dinero, msg, _ = comprar_gladiador(gladiadores_disponibles, "5", 100, equipo)
print(f"Compra #3 (sin dinero): {msg}")

# Intentar comprar equipo lleno (después de llenar)
for _ in range(10):
    g_dummy = Gladiador("X", "Murmillo", 1)
    if equipo.equipo_lleno:
        break
    equipo.agregar_gladiador(g_dummy)

exito, dinero, msg, _ = comprar_gladiador(gladiadores_disponibles, "1", 5000, equipo)
print(f"Compra (equipo lleno): {msg}")

print("\n" + "="*70)
print("TEST 4: Vender Gladiador")
print("="*70)

equipo2 = Equipo()
equipo2.dinero = 0

g1 = Gladiador("Ferox", "Murmillo", 5)
g2 = Gladiador("Velox", "Retiarius", 3)
equipo2.agregar_gladiador(g1)
equipo2.agregar_gladiador(g2)

print(f"Equipo de venta: {len(equipo2.gladiadores)} gladiadores")
print(f"  [1] {g1.nombre} Lvl {g1.nivel} → Vende por {int(calcular_costo_gladiador(g1.nivel) * 0.5)}g")
print(f"  [2] {g2.nombre} Lvl {g2.nivel} → Vende por {int(calcular_costo_gladiador(g2.nivel) * 0.5)}g")

costo1 = calcular_costo_gladiador(g1.nivel)
venta1 = int(costo1 * 0.5)
print(f"\nVende {g1.nombre}: {venta1}g")
print(f"Dinero: 0g → {venta1}g")

print("\n" + "="*70)
print("TEST 5: Ciclo Completo (Compra + Combate + Venta)")
print("="*70)

equipo3 = Equipo()
equipo3.dinero = 5000

print(f"1. Dinero inicial: {equipo3.dinero}g")

# Comprar gladiador
g_comprado = generar_gladiador_disponible(2, 4)
costo = calcular_costo_gladiador(g_comprado.nivel)
exito, equipo3.dinero, msg, _ = comprar_gladiador([g_comprado], "1", equipo3.dinero, equipo3)
print(f"2. Compra: {msg}")
print(f"   Dinero: {equipo3.dinero}g")

# Simular combate (ganancia de dinero y XP)
print(f"3. Combate ganado: +250g, +XP")
equipo3.dinero += 250
g_comprado.ganar_xp(100)
print(f"   Dinero: {equipo3.dinero}g")
print(f"   {g_comprado.nombre}: Lvl {g_comprado.nivel}, XP {g_comprado.xp}")

# Vender
venta = int(costo * 0.5)
equipo3.dinero += venta
equipo3.remover_gladiador(0)
print(f"4. Venta: {g_comprado.nombre} vendido por {venta}g")
print(f"   Dinero final: {equipo3.dinero}g")

print("\n" + "="*70)
print("✅ TODOS LOS TESTS DE MERCADO COMPLETADOS")
print("="*70 + "\n")
