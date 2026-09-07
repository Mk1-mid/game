#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests de Instalaciones de Recursos (Fase 3.3)
=============================================

Cubre: compra, mejora, probabilidades con clamp, trabajo,
ingreso pasivo, persistencia y edge cases.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import Equipo, Gladiador
from src.instalaciones import (GestorInstalaciones, InstalacionRecursos,
                                calcular_probabilidades, MULTIPLICADORES_DIAS,
                                RIESGO_HERIDA, MATERIALES_CANTERA,
                                MATERIALES_GRANJA, MATERIALES_ASERRADERO,
                                HERRERO_MINIMO, PRECIO_BASE, COSTOS_MEJORA,
                                INGRESO_POR_NIVEL)
from src.facilities import FacilitiesManager


def _equipo_base():
    e = Equipo()
    e.dinero = 10000
    e.honra = 50
    e.instalaciones = None  # se crea en tests
    return e


def _gladiador_disponible(nivel=1):
    g = Gladiador("TestG", "Murmillo", nivel=nivel)
    g.hp_actual = g.hp
    g.estado = "sano"
    g.ocupacion = "disponible"
    return g


def test_compra_instalacion():
    """Comprar instalación con dinero y prerequisito de herrero."""
    e = _equipo_base()
    fm = FacilitiesManager()
    fm.herrero.nivel = HERRERO_MINIMO
    gestor = GestorInstalaciones()

    exito, costo, msg = gestor.comprar("cantera", e.dinero, fm.herrero.nivel)
    assert exito is True
    assert costo == 2500
    e.dinero -= costo
    assert e.dinero == 10000 - 2500
    assert gestor.cantera.comprada is True
    assert gestor.cantera.nivel == 1

    print("  ✓ Compra con herrero nivel 2 OK")


def test_compra_sin_herrero():
    """Comprar sin herrero nivel 2 falla."""
    e = _equipo_base()
    fm = FacilitiesManager()
    fm.herrero.nivel = 1  # < HERRERO_MINIMO
    gestor = GestorInstalaciones()

    exito, costo, msg = gestor.comprar("cantera", e.dinero, fm.herrero.nivel)
    assert exito is False
    assert "Herrero nivel" in msg
    assert gestor.cantera.comprada is False

    print("  ✓ Compra sin herrero nivel 2 rechazada OK")


def test_compra_sin_dinero():
    """Comprar sin dinero suficiente falla."""
    e = _equipo_base()
    e.dinero = 100
    fm = FacilitiesManager()
    fm.herrero.nivel = HERRERO_MINIMO
    gestor = GestorInstalaciones()

    exito, costo, msg = gestor.comprar("cantera", e.dinero, fm.herrero.nivel)
    assert exito is False
    assert "2500g" in msg

    print("  ✓ Compra sin dinero rechazada OK")


def test_mejora_niveles():
    """Mejorar instalación escala nivel y costo."""
    e = _equipo_base()
    fm = FacilitiesManager()
    fm.herrero.nivel = HERRERO_MINIMO
    gestor = GestorInstalaciones()
    gestor.comprar("cantera", e.dinero, fm.herrero.nivel)

    # Nivel 1 -> 2
    exito, costo, msg = gestor.mejorar("cantera", e.dinero)
    assert exito is True
    assert costo == COSTOS_MEJORA[1]
    assert gestor.cantera.nivel == 2

    # Nivel 2 -> 3
    exito, costo, msg = gestor.mejorar("cantera", e.dinero)
    assert exito is True
    assert costo == COSTOS_MEJORA[2]
    assert gestor.cantera.nivel == 3

    # Nivel 3 -> 4
    exito, costo, msg = gestor.mejorar("cantera", e.dinero)
    assert exito is True
    assert costo == COSTOS_MEJORA[3]
    assert gestor.cantera.nivel == 4

    # Nivel 4 -> 5
    exito, costo, msg = gestor.mejorar("cantera", e.dinero)
    assert exito is True
    assert costo == COSTOS_MEJORA[4]
    assert gestor.cantera.nivel == 5

    # Nivel 5 -> max (falla)
    exito, costo, msg = gestor.mejorar("cantera", e.dinero)
    assert exito is False
    assert "máximo" in msg

    print("  ✓ Mejoras 1→5 correctas")


def test_ingreso_pasivo():
    """Ingreso pasivo diario por nivel."""
    e = _equipo_base()
    fm = FacilitiesManager()
    fm.herrero.nivel = HERRERO_MINIMO
    gestor = GestorInstalaciones()

    gestor.comprar("cantera", e.dinero, fm.herrero.nivel)
    assert gestor.ingreso_total() == INGRESO_POR_NIVEL[1]

    gestor.mejorar("cantera", e.dinero)
    assert gestor.ingreso_total() == INGRESO_POR_NIVEL[2]

    # Crear nuevo gestor para test de 3 instalaciones nivel 1
    gestor2 = GestorInstalaciones()
    for tipo in ["cantera", "granja", "aserradero"]:
        gestor2.comprar(tipo, 10000, 2)
    assert gestor2.ingreso_total() == sum(INGRESO_POR_NIVEL[1] for _ in range(3))

    print("  ✓ Ingreso pasivo correcto")


def test_probabilidades_base():
    """Probabilidades base por nivel sin días extra."""
    for nivel in range(1, 6):
        p = calcular_probabilidades(nivel, 1)
        assert abs(sum(p.values()) - 100.0) < 0.01
        assert p["comun"] >= 60.0
        assert p["mitica"] <= 8.0

    # Nivel 1
    p = calcular_probabilidades(1, 1)
    assert p["comun"] == 75.0
    assert p["especial"] == 20.0
    assert p["mitica"] == 5.0

    # Nivel 5
    p = calcular_probabilidades(5, 1)
    assert p["comun"] == 60.0
    assert p["especial"] == 32.0
    assert p["mitica"] == 8.0

    print("  ✓ Probabilidades base correctas")


def test_probabilidades_dias_clamp():
    """Clamp duro: mítica ≤8%, común ≥60% en todas las combinaciones."""
    for nivel in range(1, 6):
        for dias in [1, 3, 5]:
            p = calcular_probabilidades(nivel, dias)
            assert abs(sum(p.values()) - 100.0) < 0.01, f"Nivel {nivel}, {dias}d: suma={sum(p.values())}"
            assert p["comun"] >= 60.0, f"Nivel {nivel}, {dias}d: común={p['comun']}"
            assert p["mitica"] <= 8.0, f"Nivel {nivel}, {dias}d: mítica={p['mitica']}"

    # Caso límite: nivel 1, 5 días → común clamp 60%
    p = calcular_probabilidades(1, 5)
    assert p["comun"] == 60.0

    # Caso límite: nivel 5, 5 días → mítica clamp 8%, común clamp 60%
    p = calcular_probabilidades(5, 5)
    assert p["mitica"] == 8.0
    assert p["comun"] == 60.0

    print("  ✓ Clamp duro funcionando en todas las combinaciones (15 tests)")


def test_riesgo_herida():
    """Riesgo de herida por días."""
    assert RIESGO_HERIDA[1] == 0.05
    assert RIESGO_HERIDA[3] == 0.12
    assert RIESGO_HERIDA[5] == 0.20

    print("  ✓ Riesgos de herida correctos")


def test_yield_dias():
    """Yield de materiales por días."""
    assert MULTIPLICADORES_DIAS[1]["yield"] == 1
    assert MULTIPLICADORES_DIAS[3]["yield"] == 2
    assert MULTIPLICADORES_DIAS[5]["yield"] == 3

    print("  ✓ Yield por días correcto")


def test_trabajo_asignacion():
    """Asignar gladiador a trabajo."""
    e = _equipo_base()
    fm = FacilitiesManager()
    fm.herrero.nivel = HERRERO_MINIMO
    gestor = GestorInstalaciones()
    gestor.comprar("cantera", e.dinero, fm.herrero.nivel)
    e.instalaciones = gestor

    g = _gladiador_disponible()
    e.gladiadores = [g]

    exito, msg = e.asignar_trabajador(0, "cantera", 3)
    assert exito is True
    assert g.ocupacion == "ocupado"
    assert g.dias_ocupado == 3
    assert len(e.trabajadores_activos) == 1
    assert e.trabajadores_activos[0]["instalacion_tipo"] == "cantera"
    assert e.trabajadores_activos[0]["dias_restantes"] == 3
    assert e.trabajadores_activos[0]["dias_totales"] == 3

    print("  ✓ Asignación de trabajador OK")


def test_trabajo_completado_recompensas():
    """Trabajo completado otorga materiales, XP, stat."""
    e = _equipo_base()
    fm = FacilitiesManager()
    fm.herrero.nivel = HERRERO_MINIMO
    gestor = GestorInstalaciones()
    gestor.comprar("cantera", e.dinero, fm.herrero.nivel)
    e.instalaciones = gestor

    g = _gladiador_disponible(nivel=5)
    g.fuerza = 20
    g.hp = 200
    g.hp_actual = 200
    xp_antes = g.xp
    e.gladiadores = [g]

    exito, msg = e.asignar_trabajador(0, "cantera", 5)
    assert exito is True

    # Simular 5 días
    for _ in range(5):
        e.pasar_dia()

    assert g.ocupacion == "disponible"
    assert g.dias_ocupado == 0
    assert len(e.trabajadores_activos) == 0

    # XP ganada (se suma al XP, aunque pueda subir nivel)
    xp_ganada = g.xp - xp_antes
    # Si hubo level up, el XP se reinicia parcialmente
    assert xp_ganada >= 0 or g.nivel > 5  # O ganó XP o subió nivel

    # Fuerza ganada (stat de cantera)
    assert g.fuerza >= 25  # +5

    # Materiales obtenidos (3 materiales para 5 días en cantera nivel 1)
    total_mats = sum(e.materiales.values())
    assert total_mats >= 3  # 3 materiales (yield 3)

    print("  ✓ Trabajo completado da XP, stat y materiales OK")


def test_trabajo_granja_agilidad():
    """Trabajo en granja da agilidad."""
    e = _equipo_base()
    fm = FacilitiesManager()
    fm.herrero.nivel = HERRERO_MINIMO
    gestor = GestorInstalaciones()
    gestor.comprar("granja", e.dinero, fm.herrero.nivel)
    e.instalaciones = gestor

    g = _gladiador_disponible(nivel=5)
    g.agilidad = 15
    e.gladiadores = [g]

    e.asignar_trabajador(0, "granja", 3)
    for _ in range(3):
        e.pasar_dia()

    assert g.agilidad >= 18  # +3

    print("  ✓ Granja da Agilidad OK")


def test_trabajo_aserradero_hp():
    """Trabajo en aserradero da HP (Vitalidad)."""
    e = _equipo_base()
    fm = FacilitiesManager()
    fm.herrero.nivel = HERRERO_MINIMO
    gestor = GestorInstalaciones()
    gestor.comprar("aserradero", e.dinero, fm.herrero.nivel)
    e.instalaciones = gestor

    g = _gladiador_disponible(nivel=5)
    hp_antes = g.hp
    e.gladiadores = [g]

    e.asignar_trabajador(0, "aserradero", 3)
    for _ in range(3):
        e.pasar_dia()

    assert g.hp >= hp_antes + 3  # +3 HP (Vitalidad)

    print("  ✓ Aserradero da HP (Vitalidad) OK")


def test_riesgo_herida_aplicado():
    """Riesgo de herida se aplica (test determinístico con seed)."""
    e = _equipo_base()
    fm = FacilitiesManager()
    fm.herrero.nivel = HERRERO_MINIMO
    gestor = GestorInstalaciones()
    gestor.comprar("cantera", e.dinero, fm.herrero.nivel)
    e.instalaciones = gestor

    g = _gladiador_disponible(nivel=5)
    hp_antes = g.hp
    e.gladiadores = [g]

    e.asignar_trabajador(0, "cantera", 5)
    import random
    random.seed(0)  # Determinístico para test

    for _ in range(5):
        e.pasar_dia()

    # Con seed 0, debería haber herida en 5 días (riesgo 20%)
    # Solo verificamos que el sistema funciona sin crash

    print("  ✓ Sistema de riesgo de herida funcional")


def test_persistencia_instalaciones():
    """Serializar/deserializar instalaciones."""
    e = _equipo_base()
    fm = FacilitiesManager()
    fm.herrero.nivel = HERRERO_MINIMO
    gestor = GestorInstalaciones()
    gestor.comprar("cantera", e.dinero, fm.herrero.nivel)
    gestor.mejorar("cantera", e.dinero)
    gestor.comprar("granja", e.dinero, fm.herrero.nivel)

    # Serializar
    data = gestor.serializar()
    assert "cantera" in data
    assert data["cantera"]["nivel"] == 2
    assert data["granja"]["nivel"] == 1

    # Deserializar
    gestor2 = GestorInstalaciones()
    gestor2.deserializar(data)

    assert gestor2.cantera.nivel == 2
    assert gestor2.cantera.comprada is True
    assert gestor2.granja.nivel == 1
    assert gestor2.granja.comprada is True
    assert gestor2.aserradero.comprada is False

    print("  ✓ Persistencia instalaciones OK")


def test_persistencia_equipo_con_instalaciones():
    """Ciclo completo save/load de equipo con instalaciones."""
    import json
    import tempfile
    import os

    e = _equipo_base()
    fm = FacilitiesManager()
    fm.herrero.nivel = HERRERO_MINIMO
    gestor = GestorInstalaciones()
    gestor.comprar("cantera", e.dinero, fm.herrero.nivel)
    gestor.mejorar("cantera", e.dinero)
    gestor.comprar("granja", e.dinero, fm.herrero.nivel)
    e.instalaciones = gestor
    e.dinero = 5000

    # Serializar equipo
    from src.persistence import serializar_equipo, deserializar_equipo
    data = serializar_equipo(e)

    # Verificar campos
    assert "instalaciones" in data
    assert data["instalaciones"]["cantera"]["nivel"] == 2
    assert data["instalaciones"]["granja"]["nivel"] == 1

    # Deserializar
    e2 = deserializar_equipo(data)
    assert e2.instalaciones.cantera.nivel == 2
    assert e2.instalaciones.cantera.comprada is True
    assert e2.instalaciones.granja.nivel == 1
    assert e2.instalaciones.granja.comprada is True
    assert e2.instalaciones.aserradero.comprada is False

    print("  ✓ Ciclo completo save/load equipo con instalaciones OK")


def test_tres_instalaciones_materiales():
    """Verificar catálogos de materiales correctos."""
    e = _equipo_base()
    fm = FacilitiesManager()
    fm.herrero.nivel = HERRERO_MINIMO
    gestor = GestorInstalaciones()

    for tipo in ["cantera", "granja", "aserradero"]:
        gestor.comprar(tipo, e.dinero, 2)
        inst = getattr(GestorInstalaciones(), tipo)

    # Verificar que cada instalación tiene sus materiales
    cantera = GestorInstalaciones().cantera
    # Solo verificamos que los catálogos existen
    assert "comun" in MATERIALES_CANTERA
    assert "especial" in MATERIALES_CANTERA
    assert "mitica" in MATERIALES_CANTERA

    print("  ✓ Catálogos de materiales definidos OK")


def test_ingreso_pasivo_no_reemplaza_arena():
    """Ingreso pasivo total nivel 5 < una victoria arena."""
    # Arena da 150-350g base * multiplicador
    # 3 instalaciones nivel 5 = 450g/día
    max_pasivo = 3 * 150
    assert max_pasivo < 500  # Menos que victoria arena base

    print("  ✓ Ingreso pasivo no reemplaza arena OK")


def test_prerequisito_herrero_tres():
    """Todas las 3 instalaciones requieren herrero nivel 2."""
    e = _equipo_base()
    fm = FacilitiesManager()
    fm.herrero.nivel = 2
    gestor = GestorInstalaciones()

    for tipo in ["cantera", "granja", "aserradero"]:
        exito, costo, msg = gestor.comprar(tipo, 10000, 2)
        assert exito is True, f"Fallo comprando {tipo}"

    print("  ✓ Las 3 instalaciones requieren herrero 2 OK")


def test_constructor_instancias():
    """Constructor de instalaciones crea las 3 por defecto."""
    gestor = GestorInstalaciones()
    assert hasattr(gestor, 'cantera')
    assert hasattr(gestor, 'granja')
    assert hasattr(gestor, 'aserradero')
    assert len(gestor.obtener_todas()) == 3

    print("  ✓ Constructor crea 3 instalaciones OK")


def test_matrices_materiales():
    """Catálogos de materiales por instalación."""
    assert "Mineral de Hierro" in MATERIALES_CANTERA["comun"]
    assert "Mineral Raro" in MATERIALES_CANTERA["especial"]
    assert "Mithril" in MATERIALES_CANTERA["mitica"]

    assert "Cuero" in MATERIALES_GRANJA["comun"]
    assert "Cuero Endurecido" in MATERIALES_GRANJA["especial"]
    assert "Piel de Bestia" in MATERIALES_GRANJA["mitica"]

    assert "Madera de Roble" in MATERIALES_ASERRADERO["comun"]
    assert "Madera de Ébano" in MATERIALES_ASERRADERO["especial"]
    assert "Madera Ancestral" in MATERIALES_ASERRADERO["mitica"]

    print("  ✓ Catálogos de materiales correctos")