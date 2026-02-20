#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para visualizar habilidades en combate
"""

import sys
import os
sys.path.insert(0, 'c:\\Users\\USUARIO\\Desktop\\juego')

# Configurar codificación UTF-8 para Windows
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from src.models import Gladiador, Character
from src.enemies import Retiarius
from src.combat import combate_arena

# Crear un gladiador de prueba
print("Creando gladiador de prueba...")
gladiador = Gladiador("Ferox", "Murmillo")
print(f"OK Gladiador creado: {gladiador.nombre} ({gladiador.tipo})")
print(f"  - HP: {gladiador.hp}")
print(f"  - ATK: {gladiador.attack}")
print(f"  - DEF: {gladiador.defense}")
print(f"  - AGI: {gladiador.agilidad}")

# Crear enemigo de prueba
print("\nCreando enemigo de prueba...")
enemigo = Retiarius()
print(f"OK Enemigo creado: {enemigo.nombre} ({enemigo.tipo})")
print(f"  - HP: {enemigo.hp}")
print(f"  - ATK: {enemigo.attack}")
print(f"  - DEF: {enemigo.defense}")
print(f"  - AGI: {enemigo.agilidad}")

# Iniciar combate
print("\n" + "="*60)
print("INICIANDO COMBATE DE PRUEBA")
print("="*60)

victoria, salud_final_jugador, salud_final_enemigo = combate_arena(
    salud_jugador=gladiador.hp,
    daño_jugador=gladiador.attack,
    velocidad_jugador=gladiador.agilidad,
    defensa_jugador=gladiador.defense,
    salud_enemigo=enemigo.hp,
    daño_enemigo=enemigo.attack,
    velocidad_enemigo=enemigo.agilidad,
    defensa_enemigo=enemigo.defense,
    daño_base=5,
    gladiador=gladiador,
    enemigo=enemigo
)

# Mostrar resultado
print("\n" + "="*60)
print("RESULTADO DEL COMBATE")
print("="*60)
if victoria:
    print("VICTORIA!")
else:
    print("DERROTA")
print(f"Salud final del jugador: {salud_final_jugador} HP")
print(f"Salud final del enemigo: {salud_final_enemigo} HP")
print("="*60)
