#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests del Sistema de Talentos (Fase 4)
=============================================

Cubre: bonus por rama, asignacion, edge cases,
habilidades unicas, subida de nivel y persistencia.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import Gladiador
from src.talents import (
    RAMAS, NIVEL_MAXIMO, crear_arbol_vacio, obtener_bonus_talentos,
    puede_asignar, asignar_talento, verificar_habilidad_unica,
    obtener_nivel_rama, obtener_resumen_talentos,
    NOMBRE_RAMA, NOMBRE_HABILIDAD_UNICA, BONUS_POR_NIVEL,
)


def _gladiador_base(nivel=1):
    g = Gladiador("TestG", "Murmillo", nivel=nivel)
    g.hp_actual = g.hp
    g.estado = "sano"
    g.ocupacion = "disponible"
    return g


# ============================================
# TESTS - BONUSES POR RAMA
# ============================================

def test_bonus_fuerza():
    """3 puntos en fuerza: +24% ATK."""
    g = _gladiador_base()
    g.arbol_talentos = {"fuerza": 3, "resistencia": 0, "agilidad": 0, "tecnica": 0}
    bonus = obtener_bonus_talentos(g.arbol_talentos)
    assert bonus["ATK"] == 0.24, f"Esperaba 0.24, obtuvo {bonus['ATK']}"
    print("  [OK] Bonus fuerza 3 niveles: +24% ATK")


def test_bonus_resistencia():
    """2 puntos en resistencia: +16% DEF."""
    g = _gladiador_base()
    g.arbol_talentos = {"fuerza": 0, "resistencia": 2, "agilidad": 0, "tecnica": 0}
    bonus = obtener_bonus_talentos(g.arbol_talentos)
    assert bonus["DEFENSA"] == 0.16, f"Esperaba 0.16, obtuvo {bonus['DEFENSA']}"
    print("  [OK] Bonus resistencia 2 niveles: +16% DEF")


def test_bonus_agilidad():
    """4 puntos en agilidad: +30% SPD +8% ESQ."""
    g = _gladiador_base()
    g.arbol_talentos = {"fuerza": 0, "resistencia": 0, "agilidad": 4, "tecnica": 0}
    bonus = obtener_bonus_talentos(g.arbol_talentos)
    assert round(bonus["SPD"], 2) == 0.30, f"Esperaba 0.30 SPD, obtuvo {bonus['SPD']}"
    assert round(bonus["ESQUIVA"], 2) == 0.08, f"Esperaba 0.08 ESQ, obtuvo {bonus['ESQUIVA']}"
    print("  [OK] Bonus agilidad 4 niveles: +30% SPD +8% ESQ")


def test_bonus_tecnica():
    """3 puntos en tecnica: +15% CRIT."""
    g = _gladiador_base()
    g.arbol_talentos = {"fuerza": 0, "resistencia": 0, "agilidad": 0, "tecnica": 3}
    bonus = obtener_bonus_talentos(g.arbol_talentos)
    assert round(bonus["CRITICO"], 2) == 0.15, f"Esperaba 0.15 CRIT, obtuvo {bonus['CRITICO']}"
    print("  [OK] Bonus tecnica 3 niveles: +15% CRIT")


def test_bonus_completo():
    """Los 4 arboles a nivel 5: todas las bonuses acumuladas."""
    g = _gladiador_base()
    g.arbol_talentos = {"fuerza": 5, "resistencia": 5, "agilidad": 5, "tecnica": 5}
    bonus = obtener_bonus_talentos(g.arbol_talentos)
    # Fuerza: ATK(0.08+0.08+0.08+0.25) + Técnica ATK(0.05) = 0.54
    # Resistencia: DEF(0.08+0.08+0.08+0.30) = 0.54
    # Agilidad: SPD(0.10+0.10+0.10) + ESQ(0.08+0.40) = 0.78
    # Técnica: CRIT(0.05+0.05+0.05) + ATK(0.05) + XP(0.20) = 0.45
    assert round(bonus["ATK"], 2) == 0.54
    assert round(bonus["DEFENSA"], 2) == 0.54
    assert round(bonus["SPD"], 2) == 0.30
    assert round(bonus["CRITICO"], 2) == 0.25
    assert round(bonus["ESQUIVA"], 2) == 0.48
    assert round(bonus["HP_MAX"], 2) == 0.10
    assert round(bonus["XP_BONUS"], 2) == 0.20
    print("  [OK] Bonus completo 4x5 correcto")


# ============================================
# TESTS - ASIGNACION
# ============================================

def test_asignar_talento():
    """Asignar punto exitoso."""
    g = _gladiador_base()
    g.puntos_talento = 3
    exito, costo, msg = asignar_talento(g, "fuerza")
    assert exito is True
    assert g.arbol_talentos["fuerza"] == 1
    assert g.puntos_talento == 2
    print("  [OK] Asignacion exitosa")


def test_asignar_sin_puntos():
    """Edge: sin puntos disponibles."""
    g = _gladiador_base()
    g.puntos_talento = 0
    g.arbol_talentos = {"fuerza": 2, "resistencia": 0, "agilidad": 0, "tecnica": 0}
    exito, costo, msg = asignar_talento(g, "fuerza")
    assert exito is False
    assert "No tienes puntos" in msg
    assert g.arbol_talentos["fuerza"] == 2
    print("  [OK] Sin puntos: rechazado")


def test_asignar_nivel_maximo():
    """Edge: rama ya al nivel 5."""
    g = _gladiador_base()
    g.puntos_talento = 5
    g.arbol_talentos = {"fuerza": 5, "resistencia": 0, "agilidad": 0, "tecnica": 0}
    exito, costo, msg = asignar_talento(g, "fuerza")
    assert exito is False
    assert "maximo" in msg.lower()
    print("  [OK] Nivel maximo: rechazado")


def test_asignar_rama_invalida():
    """Entrada invalida: rama no existe."""
    g = _gladiador_base()
    g.puntos_talento = 3
    exito, costo, msg = asignar_talento(g, "vuelo")
    assert exito is False
    assert "invalida" in msg.lower()
    print("  [OK] Rama invalida: rechazado")


def test_puede_asignar_ok():
    """puede_asignar retorna True cuando es valido."""
    exito, msg = puede_asignar(3, "fuerza", 2)
    assert exito is True
    assert msg == ""
    print("  [OK] puede_asignar valido")


def test_puede_asignar_sin_puntos():
    """puede_asignar retorna False sin puntos."""
    exito, msg = puede_asignar(0, "fuerza", 2)
    assert exito is False
    print("  [OK] puede_asignar sin puntos")


def test_puede_asignar_max():
    """puede_asignar retorna False a nivel maximo."""
    exito, msg = puede_asignar(3, "fuerza", 5)
    assert exito is False
    print("  [OK] puede_asignar nivel maximo")


# ============================================
# TESTS - HABILIDADES UNICAS
# ============================================

def test_habilidad_unica_fuerza():
    """Gladiador con fuerza 5 desbloquea Furia Gladiatoria."""
    g = _gladiador_base()
    g.arbol_talentos = {"fuerza": 5, "resistencia": 0, "agilidad": 0, "tecnica": 0}
    habilidades = verificar_habilidad_unica(g)
    assert "Furia Gladiatoria" in habilidades
    assert len(habilidades) == 1
    print("  [OK] Furia Gladiatoria desbloqueada")


def test_habilidades_unicas_completas():
    """Las 4 habilidades unicas desbloqueadas con 4x5."""
    g = _gladiador_base()
    g.arbol_talentos = {"fuerza": 5, "resistencia": 5, "agilidad": 5, "tecnica": 5}
    habilidades = verificar_habilidad_unica(g)
    assert len(habilidades) == 4
    assert "Furia Gladiatoria" in habilidades
    assert "Escudo Ancestral" in habilidades
    assert "Reflejo Táctico" in habilidades
    assert "Maestría del Guerrero" in habilidades
    print("  [OK] 4 habilidades unicas desbloqueadas")


def test_sin_habilidades_unicas():
    """Gladiador sin talentos no tiene habilidades unicas."""
    g = _gladiador_base()
    habilidades = verificar_habilidad_unica(g)
    assert len(habilidades) == 0
    print("  [OK] Sin habilidades unicas")


# ============================================
# TESTS - SUBIDA DE NIVEL
# ============================================

def test_puntos_subir_nivel():
    """Después de subir_nivel, puntos_talento += 1."""
    g = _gladiador_base(nivel=1)
    assert g.puntos_talento == 0
    g.subir_nivel()
    assert g.puntos_talento == 1
    g.subir_nivel()
    assert g.puntos_talento == 2
    print("  [OK] subir_nivel otorga puntos de talento")


def test_arbol_vacio_inicial():
    """Gladiador nuevo tiene arbol vacío y 0 puntos."""
    g = _gladiador_base()
    assert g.puntos_talento == 0
    assert g.arbol_talentos == {"fuerza": 0, "resistencia": 0, "agilidad": 0, "tecnica": 0}
    print("  [OK] Arbol vacío inicial")


# ============================================
# TESTS - PERSISTENCIA
# ============================================

def test_seria_talentos():
    """Serializar preserva talentos."""
    from src.persistence import serializar_gladiador, deserializar_gladiador

    g = _gladiador_base(nivel=3)
    g.puntos_talento = 2
    g.arbol_talentos = {"fuerza": 2, "resistencia": 1, "agilidad": 0, "tecnica": 1}

    data = serializar_gladiador(g)
    g2 = deserializar_gladiador(data)

    assert g2.puntos_talento == 2
    assert g2.arbol_talentos == {"fuerza": 2, "resistencia": 1, "agilidad": 0, "tecnica": 1}
    print("  [OK] Persistencia de talentos correcta")


def test_sin_puntos_persistencia():
    """Save con 0 puntos se restaura correctamente."""
    from src.persistence import serializar_gladiador, deserializar_gladiador

    g = _gladiador_base(nivel=1)
    g.puntos_talento = 0
    g.arbol_talentos = {"fuerza": 0, "resistencia": 0, "agilidad": 0, "tecnica": 0}

    data = serializar_gladiador(g)
    g2 = deserializar_gladiador(data)

    assert g2.puntos_talento == 0
    assert g2.arbol_talentos == {"fuerza": 0, "resistencia": 0, "agilidad": 0, "tecnica": 0}
    print("  [OK] Persistencia con 0 puntos")


def test_compatibilidad_datos_antiguos():
    """Deserializar sin campos de talentos (save antiguo) usa defaults."""
    from src.persistence import deserializar_gladiador

    data_antigua = {
        "nombre": "TestG", "tipo": "Murmillo", "nivel": 2, "xp": 50,
        "hp": 119, "hp_actual": 119, "attack": 22, "defense": 5,
        "agilidad": 10, "fuerza": 15, "critico": 12, "esquiva": 8,
        "estado": "sano", "ocupacion": "disponible", "dias_ocupado": 0,
        "razon_ocupacion": None, "combates_ganados": 0, "combates_perdidos": 0,
        "combates_totales": 0, "dinero_generado": 0,
        "weapon": None, "armor": None, "habilidades": None,
    }

    g = deserializar_gladiador(data_antigua)
    assert g.puntos_talento == 0
    assert g.arbol_talentos == {"fuerza": 0, "resistencia": 0, "agilidad": 0, "tecnica": 0}
    print("  [OK] Compatibilidad con datos antiguos")


def test_resumen_talentos():
    """obtener_resumen_talentos retorna dict completo."""
    g = _gladiador_base()
    g.puntos_talento = 2
    g.arbol_talentos = {"fuerza": 1, "resistencia": 1, "agilidad": 0, "tecnica": 0}

    resumen = obtener_resumen_talentos(g)
    assert resumen["puntos_disponibles"] == 2
    assert resumen["arbol"] == {"fuerza": 1, "resistencia": 1, "agilidad": 0, "tecnica": 0}
    assert "FUERZA" in resumen["bonus_total"] or "ATK" in resumen["bonus_total"]
    assert resumen["habilidades_unicas"] == []
    print("  [OK] Resumen de talentos correcto")
