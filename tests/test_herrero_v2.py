#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test completo del Herrero 2.0"""

from src.models import Weapon
from src.facilities import Herrero

print("=" * 70)
print("PRUEBA HERRERO 2.0 - Sistema de Mejora con % ATK + Durabilidad")
print("=" * 70)
print()

# Crear Herrero Nivel 2
herrero = Herrero(nivel=2)
print(f"🏭 Herrero Nivel {herrero.nivel}/5 | Tier desbloqueado: {herrero.obtener_tier_desbloqueado()}")
print()

# Crear armas de diferentes tipos y tiers
armas_test = [
    Weapon("Daga Oxidada", attack=5, tier=1),           # Corta
    Weapon("Espada Gladius", attack=15, tier=2),        # Media
    Weapon("Lanza Corta", attack=12, tier=1),           # Grande
    Weapon("Espada de Marte", attack=30, tier=4),       # Grande legendaria
]

print("=" * 70)
print("1. PRUEBA: MEJORAR ARMAS (% ATK + Costos Cuadráticos)")
print("=" * 70)
print()

dinero = 5000
for arma in armas_test:
    print(f"\n⚔️  {arma.nombre} | Tier {arma.tier} | ATK: {arma.attack}")
    print(f"   Tipo de arma: {herrero._obtener_tipo_arma(arma)}")
    
    # Intenta mejorar hasta que no tenga dinero
    mejoras_hechas = 0
    while dinero > 100:
        exito, costo, msg = herrero.mejorar_arma(arma, dinero)
        if exito:
            dinero -= costo
            mejoras_hechas += 1
            print(f"   ✅ Mejora #{mejoras_hechas}: {msg}")
        else:
            print(f"   ❌ {msg}")
            break
    
    print(f"   💰 Dinero restante: {dinero}g")

print()
print(f"💰 DINERO FINAL: {dinero}g")

print()
print("=" * 70)
print("2. PRUEBA: REPARAR ARMAS (Costo Dinámico por Durabilidad)")
print("=" * 70)
print()

# Arma degradada por mejoras
arma_degradada = armas_test[1]  # Espada Gladius
print(f"⚔️  {arma_degradada.nombre}")
print(f"   Durabilidad: {getattr(arma_degradada, 'durabilidad', 100):.0f}%")
print()

# Intenta reparar
dinero = 500
while dinero > 0:
    exito, costo, msg = herrero.reparar_arma(arma_degradada, dinero)
    if exito:
        dinero -= costo
        print(f"✅ {msg}")
        print(f"   💰 Dinero restante: {dinero}g\n")
        break
    else:
        print(f"❌ {msg}\n")
        break

print()
print("=" * 70)
print("3. ESTADÍSTICAS DEL HERRERO")
print("=" * 70)
stats = herrero.generar_resumen_estadisticas()
print(stats)

print("=" * 70)
print("PRUEBA COMPLETADA ✅")
print("=" * 70)
