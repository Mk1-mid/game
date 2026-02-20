#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del flujo de main.py - Verifica que las funciones se ejecutan
==================================================================
"""

from src.models import Equipo, Gladiador
import sys
from io import StringIO

# Importar funciones del main
from main import (
    seleccionar_luchador, 
    mostrar_pantalla_equipo,
    hospital_menu
)

def test_seleccionar_luchador_flow():
    """Test: Flujo de selección de luchador"""
    print("=" * 70)
    print("TEST: Seleccionar luchador (simulando entrada)")
    print("=" * 70)
    
    equipo = Equipo()
    g1 = Gladiador("Ferox", "Murmillo", nivel=5)
    g2 = Gladiador("Velox", "Retiarius", nivel=3)
    equipo.dinero = 5000
    equipo.agregar_gladiador(g1)
    equipo.agregar_gladiador(g2)
    
    # Simular que el usuario selecciona opción 1
    original_input = __builtins__.input
    
    def mock_input(prompt):
        print(f"[INPUT SIMULADO]: {prompt}", end="")
        print("1")  # Selecciona al primero
        return "1"
    
    __builtins__.input = mock_input
    
    try:
        gladiador = seleccionar_luchador(equipo)
        print(f"✓ Seleccionado: {gladiador.nombre} (Lvl {gladiador.nivel})")
        print(f"  HP: {gladiador.hp_actual}/{gladiador.hp}")
        print(f"  ATK: {gladiador.ataque_final()}")
    finally:
        __builtins__.input = original_input
    
    print()


def test_mostrar_pantalla_equipo():
    """Test: Mostrar pantalla del equipo"""
    print("=" * 70)
    print("TEST: Mostrar pantalla del equipo")
    print("=" * 70)
    
    equipo = Equipo()
    g1 = Gladiador("Ferox", "Murmillo", nivel=5)
    g2 = Gladiador("Velox", "Retiarius", nivel=3)
    equipo.dinero = 5000
    equipo.agregar_gladiador(g1)
    equipo.agregar_gladiador(g2)
    
    # Dañar a uno
    g2.aplicar_daño(30)
    
    mostrar_pantalla_equipo(equipo, "TestPlayer")
    print()


if __name__ == "__main__":
    try:
        test_mostrar_pantalla_equipo()
        test_seleccionar_luchador_flow()
        
        print("=" * 70)
        print("✅ FUNCIONES DE MAIN.PY FUNCIONAN CORRECTAMENTE")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
