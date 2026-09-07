#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests del sistema de Patricios (Fase 3.2)
=========================================

Cubre: generación, simulación diaria, serialización.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.patricios import GestorPatricios, Patricio
from src.models import Gladiador
from src.persistence import serializar_gladiador, deserializar_gladiador


def test_generar_patricios():
    """Los patricios se generan con equipos y stats válidos."""
    gestor = GestorPatricios()
    gestor.generar_patricios(nivel_referencia=1, cantidad=5)

    assert len(gestor.patricios) == 5
    for p in gestor.patricios:
        assert p.nombre
        assert 0 <= p.honra <= 100
        assert -100 <= p.afinidad <= 100
        assert 2 <= len(p.gladiadores) <= 4
        for g in p.gladiadores:
            assert isinstance(g, Gladiador)
            assert g.nivel >= 1

    print("  ✓ Generación de patricios correcta")


def test_simular_dia():
    """simular_dia() avanza el mundo sin romper."""
    gestor = GestorPatricios()
    gestor.generar_patricios(nivel_referencia=2, cantidad=6)

    vict_total_antes = sum(p.victorias for p in gestor.patricios)
    log = gestor.simular_dia()

    # No debe lanzar excepción
    assert isinstance(log, list)
    vict_total_despues = sum(p.victorias for p in gestor.patricios)

    # Las victorias pueden haber subido (combate NPC)
    assert vict_total_despues >= vict_total_antes

    print("  ✓ Simulación diaria sin errores")


def test_serializacion_patricios():
    """Ciclo completo: serializar → deserializar mantiene datos."""
    gestor = GestorPatricios()
    gestor.generar_patricios(nivel_referencia=3, cantidad=4)

    # Añadir historial
    gestor.historial_npc.append("Test combate")

    data = gestor.serializar()
    assert "patricios" in data
    assert "historial_npc" in data
    assert len(data["patricios"]) == 4

    # Deserializar en gestor nuevo
    gestor2 = GestorPatricios()
    gestor2.deserializar(data)

    assert len(gestor2.patricios) == 4
    assert gestor2.historial_npc == ["Test combate"]
    for p1, p2 in zip(gestor.patricios, gestor2.patricios):
        assert p1.nombre == p2.nombre
        assert p1.honra == p2.honra
        assert p1.afinidad == p2.afinidad
        assert len(p1.gladiadores) == len(p2.gladiadores)

    print("  ✓ Serialización/deserialización de patricios correcta")


def test_rival_mas_fuerte():
    """rival_mas_fuerte() detecta al patricio que más te odia."""
    gestor = GestorPatricios()
    # Crear manualmente para controlar afinidades
    g1 = Gladiador("Test1", "Murmillo", nivel=1)
    g2 = Gladiador("Test2", "Retiarius", nivel=1)

    p_amigo = Patricio("Amigo", 70, [g1], afinidad=50)
    p_neutral = Patricio("Neutral", 50, [g2], afinidad=0)
    p_rival1 = Patricio("Rival1", 20, [g1], afinidad=-60)
    p_rival2 = Patricio("Rival2", 10, [g2], afinidad=-80)  # El que más odia

    gestor.patricios = [p_amigo, p_neutral, p_rival1, p_rival2]

    rival = gestor.rival_mas_fuerte()
    assert rival is not None
    assert rival.nombre == "Rival2"  # afinidad -80 es la más baja

    # Sin rivales
    gestor.patricios = [p_amigo, p_neutral]
    assert gestor.rival_mas_fuerte() is None

    print("  ✓ Detección de rival más fuerte correcta")


def test_patricio_modificar_afinidad():
    """modificar_afinidad() respeta límites -100..100."""
    g = Gladiador("Test", "Murmillo", nivel=1)
    p = Patricio("Test", 50, [g], afinidad=0)

    p.modificar_afinidad(150)
    assert p.afinidad == 100

    p.modificar_afinidad(-300)
    assert p.afinidad == -100

    p.modificar_afinidad(50)
    assert p.afinidad == -50

    print("  ✓ Límites de afinidad respetados")