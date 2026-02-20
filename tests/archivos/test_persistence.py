#!/usr/bin/env python3
"""
Tests para Persistencia (Guardar/Cargar Equipo)
===============================================
"""

from src.models import Equipo, Gladiador, Barracas
from src.persistence import (
    serializar_gladiador, deserializar_gladiador,
    serializar_equipo, deserializar_equipo,
    guardar_equipo_partida, cargar_equipo_partida
)

import json
import os

print("\n" + "="*70)
print("TEST 1: Serializar Gladiador")
print("="*70)

g1 = Gladiador("Ferox", "Murmillo", nivel=5)
g1.hp_actual = 150
g1.estado = "herido"
g1.combates_ganados = 10
g1.combates_perdidos = 2
g1.ganar_xp(500)

print(f"Gladiador original:")
print(f"  Nombre: {g1.nombre}")
print(f"  Nivel: {g1.nivel}, XP: {g1.xp}")
print(f"  HP: {g1.hp_actual}/{g1.hp}")
print(f"  Estado: {g1.estado}")
print(f"  Record: {g1.combates_ganados}W-{g1.combates_perdidos}L")

# Serializar
datos_g1 = serializar_gladiador(g1)
print(f"\nSerializado (dict):")
print(json.dumps(datos_g1, indent=2, ensure_ascii=False))

print("\n" + "="*70)
print("TEST 2: Deserializar Gladiador")
print("="*70)

g1_recuperado = deserializar_gladiador(datos_g1)

print(f"Gladiador recuperado:")
print(f"  Nombre: {g1_recuperado.nombre}")
print(f"  Nivel: {g1_recuperado.nivel}, XP: {g1_recuperado.xp}")
print(f"  HP: {g1_recuperado.hp_actual}/{g1_recuperado.hp}")
print(f"  Estado: {g1_recuperado.estado}")
print(f"  Record: {g1_recuperado.combates_ganados}W-{g1_recuperado.combates_perdidos}L")

# Verificar que son iguales
assert g1_recuperado.nombre == g1.nombre
assert g1_recuperado.nivel == g1.nivel
assert g1_recuperado.xp == g1.xp
assert g1_recuperado.hp_actual == g1.hp_actual
assert g1_recuperado.estado == g1.estado
assert g1_recuperado.combates_ganados == g1.combates_ganados

print("\n✓ Gladiador deserializado correctamente")

print("\n" + "="*70)
print("TEST 3: Serializar Equipo")
print("="*70)

equipo = Equipo()
equipo.dinero = 15000
equipo.barracas.literas = 3
equipo.barracas.espacios_totales = 6

g_a = Gladiador("Ferox", "Murmillo", 5)
g_b = Gladiador("Velox", "Retiarius", 3)
g_c = Gladiador("Fortis", "Secutor", 7)

equipo.agregar_gladiador(g_a)
equipo.agregar_gladiador(g_b)
equipo.agregar_gladiador(g_c)

print(f"Equipo original:")
print(f"  Dinero: {equipo.dinero}g")
print(f"  Barracas: {equipo.barracas.literas} literas, {equipo.barracas.espacios_totales} espacios")
print(f"  Gladiadores: {len(equipo.gladiadores)}")
for g in equipo.gladiadores:
    print(f"    - {g.nombre} (Lvl {g.nivel})")

# Serializar
datos_equipo = serializar_equipo(equipo)
print(f"\nSerializado (mostrando estructura):")
print(f"  dinero: {datos_equipo['dinero']}")
print(f"  literas: {datos_equipo['literas']}")
print(f"  gladiadores: {len(datos_equipo['gladiadores'])}")
for gdata in datos_equipo['gladiadores']:
    print(f"    - {gdata['nombre']} (Lvl {gdata['nivel']})")

print("\n" + "="*70)
print("TEST 4: Deserializar Equipo")
print("="*70)

equipo_recuperado = deserializar_equipo(datos_equipo)

print(f"Equipo recuperado:")
print(f"  Dinero: {equipo_recuperado.dinero}g")
print(f"  Barracas: {equipo_recuperado.barracas.literas} literas, {equipo_recuperado.barracas.espacios_totales} espacios")
print(f"  Gladiadores: {len(equipo_recuperado.gladiadores)}")
for g in equipo_recuperado.gladiadores:
    print(f"    - {g.nombre} (Lvl {g.nivel})")

# Verificar
assert equipo_recuperado.dinero == equipo.dinero
assert equipo_recuperado.barracas.literas == equipo.barracas.literas
assert len(equipo_recuperado.gladiadores) == len(equipo.gladiadores)

print("\n✓ Equipo deserializado correctamente")

print("\n" + "="*70)
print("TEST 5: Guardar y Cargar Partida (JSON)")
print("="*70)

usuario_test = "test_persistence_user"

# Crear equipo con datos
equipo_a_guardar = Equipo()
equipo_a_guardar.dinero = 50000
equipo_a_guardar.barracas.literas = 4
equipo_a_guardar.barracas.espacios_totales = 8

g_1 = Gladiador("Héroe", "Secutor", 10)
g_1.hp_actual = 250
g_1.combates_ganados = 25
g_1.ganar_xp(1000)

g_2 = Gladiador("Guardián", "Hoplomachus", 8)
g_2.ocupacion = "ocupado"
g_2.dias_ocupado = 2
g_2.razon_ocupacion = "curacion"

equipo_a_guardar.agregar_gladiador(g_1)
equipo_a_guardar.agregar_gladiador(g_2)

print(f"Equipo a guardar:")
print(f"  Dinero: {equipo_a_guardar.dinero}g")
print(f"  Gladiadores: {len(equipo_a_guardar.gladiadores)}")

# Guardar
guardar_equipo_partida(usuario_test, equipo_a_guardar)

# Cargar
equipo_cargado = cargar_equipo_partida(usuario_test)

if equipo_cargado:
    print(f"\nEquipo cargado:")
    print(f"  Dinero: {equipo_cargado.dinero}g")
    print(f"  Gladiadores: {len(equipo_cargado.gladiadores)}")
    
    for g in equipo_cargado.gladiadores:
        print(f"    - {g.nombre} (Lvl {g.nivel})")
        if g.nombre == "Héroe":
            print(f"      HP: {g.hp_actual}/{g.hp}, Combates: {g.combates_ganados}W-{g.combates_perdidos}L")
        if g.nombre == "Guardián":
            print(f"      Ocupación: {g.ocupacion} ({g.dias_ocupado} días)")
    
    # Verificar datos
    assert equipo_cargado.dinero == equipo_a_guardar.dinero
    assert len(equipo_cargado.gladiadores) == len(equipo_a_guardar.gladiadores)
    assert equipo_cargado.gladiadores[0].combates_ganados == 25
    assert equipo_cargado.gladiadores[1].ocupacion == "ocupado"
    
    print("\n✓ Partida guardada y cargada correctamente")
else:
    print("❌ Error al cargar partida")

# Limpiar
archivo_test = os.path.join("data/saves", f"save_{usuario_test}.json")
if os.path.exists(archivo_test):
    os.remove(archivo_test)
    print("✓ Archivo de prueba eliminado")

print("\n" + "="*70)
print("TEST 6: JSON Inspection")
print("="*70)

# Crear y guardar para inspeccionar
equipo_inspect = Equipo()
equipo_inspect.dinero = 12345

g_inspect = Gladiador("Inspección", "Murmillo", 3)
g_inspect.ganar_xp(250)
equipo_inspect.agregar_gladiador(g_inspect)

datos_inspect = serializar_equipo(equipo_inspect)
json_str = json.dumps(datos_inspect, indent=2, ensure_ascii=False)

print("JSON generado:")
print(json_str)

print("\n" + "="*70)
print("✅ TODOS LOS TESTS DE PERSISTENCIA COMPLETADOS")
print("="*70 + "\n")
