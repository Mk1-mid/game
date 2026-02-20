#!/usr/bin/env python3
"""
Tests para Gladiador, Equipo y Barracas
========================================
"""

from src.models import Gladiador, Equipo, Barracas

print("\n" + "="*70)
print("TEST 1: Crear un Gladiador")
print("="*70)

g1 = Gladiador("Ferox", "Murmillo", nivel=1)
print(f"✓ Gladiador creado: {g1}")
print(f"  Nombre: {g1.nombre}")
print(f"  Tipo: {g1.tipo}")
print(f"  Nivel: {g1.nivel}")
print(f"  HP: {g1.hp_actual}/{g1.hp}")
print(f"  ATK: {g1.attack}")
print(f"  DEF: {g1.defense}")
print(f"  SPD: {g1.speed}")
print(f"  Estado: {g1.estado}")
print(f"  Ocupación: {g1.ocupacion}")

print("\n" + "="*70)
print("TEST 2: Gladiador comienza con nivel > 1")
print("="*70)

g2 = Gladiador("Velox", "Retiarius", nivel=5)
print(f"✓ Gladiador nivel 5: {g2}")
print(f"  HP: {g2.hp}")
print(f"  ATK: {g2.attack}")
print(f"  DEF: {g2.defense}")
print(f"  SPD: {g2.speed}")

print("\n" + "="*70)
print("TEST 3: Daño, Curación y Revivir")
print("="*70)

print(f"HP antes: {g1.hp_actual}/{g1.hp}, Estado: {g1.estado}")
g1.aplicar_daño(50)
print(f"Aplicado 50 daño")
print(f"HP ahora: {g1.hp_actual}/{g1.hp}, Estado: {g1.estado}")

g1.aplicar_daño(100)
print(f"Aplicado 100 daño más (total 150)")
print(f"HP ahora: {g1.hp_actual}/{g1.hp}, Estado: {g1.estado}")

g1.curar(75)
print(f"Curado 75 HP")
print(f"HP ahora: {g1.hp_actual}/{g1.hp}, Estado: {g1.estado}")

g1.aplicar_daño(200)  # Mata el gladiador
print(f"Aplicado 200 daño (matador)")
print(f"HP ahora: {g1.hp_actual}/{g1.hp}, Estado: {g1.estado}")
print(f"¿Puede luchar? {g1.puede_luchar()}")

g1.revivir()
print(f"Revivido")
print(f"HP ahora: {g1.hp_actual}/{g1.hp}, Estado: {g1.estado}")

print("\n" + "="*70)
print("TEST 4: Ocupación (Entrenamiento/Curación)")
print("="*70)

print(f"Estado inicial: {g1.ocupacion}, puede luchar: {g1.puede_luchar()}")
g1.ocupar("entrenamiento", 2)
print(f"Ocupar 2 días por entrenamiento")
print(f"Estado: {g1.ocupacion}, puede luchar: {g1.puede_luchar()}")

g1.pasar_dia()
print(f"Pasó 1 día: dias_ocupado={g1.dias_ocupado}, puede luchar: {g1.puede_luchar()}")

g1.pasar_dia()
print(f"Pasó otro día: dias_ocupado={g1.dias_ocupado}, ocupacion={g1.ocupacion}, puede luchar: {g1.puede_luchar()}")

print("\n" + "="*70)
print("TEST 5: XP y Leveling en Gladiador")
print("="*70)

g3 = Gladiador("Fortis", "Secutor", nivel=1)
print(f"Inicio: Nivel {g3.nivel}, XP {g3.xp}/{g3.xp_para_siguiente_nivel()}")

g3.ganar_xp(55)
print(f"Ganó 55 XP: Nivel {g3.nivel}, XP {g3.xp}/{g3.xp_para_siguiente_nivel()}")

g3.ganar_xp(200)
print(f"Ganó 200 XP más: Nivel {g3.nivel}, XP {g3.xp}/{g3.xp_para_siguiente_nivel()}")

print("\n" + "="*70)
print("TEST 6: Barracas (Housing)")
print("="*70)

barracas = Barracas()
print(f"Estado inicial: {barracas}")
print(f"  Literas: {barracas.literas}")
print(f"  Espacios totales: {barracas.espacios_totales}")
print(f"  Próxima litera cuesta: {barracas.costo_proxima_litera}g")

exito, dinero_nuevo, msg = barracas.comprar_litera(500)
print(f"\nIntento comprar litera (500g disponible):")
print(f"  {msg}")
print(f"  Dinero restante: {dinero_nuevo}g")
print(f"  Ahora: {barracas}")

dinero = 20000
for i in range(4):
    exito, dinero, msg = barracas.comprar_litera(dinero)
    print(f"\nCompra #{i+1}: {msg}")
    if exito:
        print(f"  Dinero restante: {dinero}g")
        print(f"  Barracas: {barracas}")

exito, dinero, msg = barracas.comprar_litera(dinero)
print(f"\nIntento litera #5 (máximo): {msg}")

print("\n" + "="*70)
print("TEST 7: Equipo (Gestión de gladiadores)")
print("="*70)

equipo = Equipo()
print(f"Equipo nuevo: {equipo}")
print(f"Espacios: {equipo.espacios_disponibles}/{equipo.barracas.espacios_totales}")

# Agregar gladiadores
g_list = [
    Gladiador("Ferox", "Murmillo", 5),
    Gladiador("Velox", "Retiarius", 3),
    Gladiador("Fortis", "Secutor", 7),
]

for g in g_list:
    exito, msg = equipo.agregar_gladiador(g)
    print(f"  {msg} → Equipo: {equipo.espacios_disponibles} espacios libres")

print(f"\nNivel promedio: {equipo.calcular_nivel_promedio()}")

print("\n" + "="*70)
print("TEST 8: Seleccionar Luchador")
print("="*70)

exito, msg = equipo.seleccionar_luchador(0)
print(f"Seleccionar índice 0 (puede luchar): {msg}")
print(f"  Luchador activo: {equipo.gladiador_activo}")

# Ocupar el primer gladiador
equipo.gladiadores[0].ocupar("entrenamiento", 1)
exito, msg = equipo.seleccionar_luchador(0)
print(f"\nOcupar primer gladiador, intentar seleccionar: {msg}")

exito, msg = equipo.seleccionar_luchador(1)
print(f"Seleccionar índice 1 (debe estar disponible): {msg}")

print("\n" + "="*70)
print("TEST 9: Fin de día (pasar_dia)")
print("="*70)

equipo.gladiadores[0].ocupar("curacion", 3)
equipo.gladiadores[2].ocupar("entrenamiento", 1)

print("Antes de pasar día:")
for i, g in enumerate(equipo.gladiadores):
    print(f"  [{i}] {g.nombre}: ocupacion={g.ocupacion}, dias={g.dias_ocupado}")

equipo.pasar_dia()
print("\nDespués de pasar 1 día:")
for i, g in enumerate(equipo.gladiadores):
    print(f"  [{i}] {g.nombre}: ocupacion={g.ocupacion}, dias={g.dias_ocupado}")

equipo.pasar_dia()
print("\nDespués de pasar otro día:")
for i, g in enumerate(equipo.gladiadores):
    print(f"  [{i}] {g.nombre}: ocupacion={g.ocupacion}, dias={g.dias_ocupado}")

print("\n" + "="*70)
print("TEST 10: Todos muertos (Game Over check)")
print("="*70)

print(f"Todos muertos (equipo vivo)? {equipo.todos_muertos()}")

for g in equipo.gladiadores:
    g.estado = "muerto"

print(f"Todos muertos (después de matar)? {equipo.todos_muertos()}")

print("\n" + "="*70)
print("✅ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
print("="*70 + "\n")
