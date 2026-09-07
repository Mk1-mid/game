#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests del sistema de Eventos (Fase 3.2)
=======================================

Cubre: tirada de eventos, resolvers, préstamos, honra/racha, persistencia.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import Equipo, Material, CATALOGO_MATERIALES
from src.patricios import GestorPatricios, Patricio
from src.events import (GestorEventos, EVENTOS, PROBABILIDAD_EVENTO,
                        COSTO_HONRA_APUESTA, COSTO_HONRA_TORNEO_PARTICIPAR,
                        GANANCIA_PENITENCIA, COSTO_PENITENCIA_ORO,
                        material_aleatorio, _msg_honra, _msg_material)


def _equipo_base():
    """Equipo con un gladiador disponible y honra 50."""
    e = Equipo()
    e.dinero = 2000
    e.honra = 50
    e.racha_victorias_limpias = 0
    # Gladiador mock simple
    class MockGladiador:
        estado = "sano"
        ocupacion = "disponible"
        combates_ganados = 0
        def puede_luchar(self): return True
        def ganar_xp(self, x): return False
        def aplicar_daño(self, dmg): pass
    e.gladiadores = [MockGladiador()]
    return e


def _patricios_base():
    """GestorPatricios con un patricio amigo y uno rival."""
    gp = GestorPatricios()
    from src.models import Gladiador
    g = Gladiador("TestG", "Murmillo", nivel=1)
    p1 = Patricio("Amigo", 70, [g], afinidad=30)
    p2 = Patricio("Rival", 20, [g], afinidad=-60)
    gp.patricios = [p1, p2]
    return gp


def test_tirar_evento_probabilidad():
    """tirar_evento_dia respeta la probabilidad global."""
    ge = GestorEventos()
    e = _equipo_base()
    pt = _patricios_base()

    # Forzamos semilla para determinismo
    import random
    random.seed(42)
    n_eventos = 0
    for _ in range(1000):
        if ge.tirar_evento_dia(e, pt):
            n_eventos += 1
    # Probabilidad ~35% → 300-400 en 1000 tiradas
    assert 300 < n_eventos < 450
    print(f"  ✓ Probabilidad global OK ({n_eventos}/1000)")


def test_evento_condiciones():
    """Eventos respetan sus condiciones de honra/flags."""
    ge = GestorEventos()
    e = _equipo_base()
    pt = _patricios_base()

    # rumor_soborno solo aparece si no se ha ofrecido
    e.rumor_ofrecido = False
    ev = next((ev for ev in EVENTOS if ev["id"] == "rumor_soborno"), None)
    assert ev is not None
    assert ge.evento_posible(e, pt, ev) is True

    e.rumor_ofrecido = True
    assert ge.evento_posible(e, pt, ev) is False

    # patrocinio_honorable solo con honra >= 70
    e.honra = 70
    ev_patro = next((ev for ev in EVENTOS if ev["id"] == "patrocinio_honorable"), None)
    assert ge.evento_posible(e, pt, ev_patro) is True

    e.honra = 69
    assert ge.evento_posible(e, pt, ev_patro) is False

    # apuesta_clandestina requiere habilitado_clandestino y honra < 40
    e.honra = 39
    e.habilitado_clandestino = False
    ev_ap = next((ev for ev in EVENTOS if ev["id"] == "apuesta_clandestina"), None)
    assert ge.evento_posible(e, pt, ev_ap) is False

    e.habilitado_clandestino = True
    assert ge.evento_posible(e, pt, ev_ap) is True

    print("  ✓ Condiciones de eventos respetadas")


def test_resolver_rumor_soborno():
    """Rumor de soborno activa habilitado_clandestino y baja honra."""
    ge = GestorEventos()
    e = _equipo_base()
    pt = _patricios_base()

    ev = next(ev for ev in EVENTOS if ev["id"] == "rumor_soborno")

    # Opción 1: aceptar
    msgs = ge.resolver_opcion(ev, 1, e, pt)
    assert e.habilitado_clandestino is True
    assert e.honra == 50 - 10  # -10 honra
    assert any("accedes a lo clandestino" in m or "intermediario" in m for m in msgs)

    # Reset
    e.honra = 50
    e.habilitado_clandestino = False
    e.rumor_ofrecido = False

    # Opción 2: rechazar
    msgs = ge.resolver_opcion(ev, 2, e, pt)
    assert e.habilitado_clandestino is False
    assert e.honra == 50 + 2  # +2 honra por rechazar
    print("  ✓ Rumor de soborno (aceptar/rechazar) correcto")


def test_resolver_donacion():
    """Donación da oro y material."""
    ge = GestorEventos()
    e = _equipo_base()
    pt = _patricios_base()
    e.honra = 50  # para que donación no sea la única

    ev = next(ev for ev in EVENTOS if ev["id"] == "donacion_admirador")
    msgs = ge.resolver_opcion(ev, 1, e, pt)

    assert e.dinero > 2000  # recibió oro
    assert len(e.materiales) >= 1  # recibió material
    print("  ✓ Donación da oro y material")


def test_resolver_prestamo():
    """Préstamo crea entrada en prestamos_pendientes con intereses."""
    ge = GestorEventos()
    e = _equipo_base()
    pt = _patricios_base()
    e.honra = 55  # requisito para préstamo

    ev = next(ev for ev in EVENTOS if ev["id"] == "prestamo_patricio")

    # Opción 1: prestar
    msgs = ge.resolver_opcion(ev, 1, e, pt)
    assert len(e.prestamos_pendientes) == 1
    p = e.prestamos_pendientes[0]
    assert p["monto"] == 500
    assert p["devuelve"] == 650  # 30% interés
    assert p["dias_restantes"] == 3
    assert e.dinero == 2000 - 500
    print("  ✓ Préstamo crea deuda con intereses")


def test_procesar_prestamos():
    """procesar_prestamos cobra al vencer el plazo."""
    ge = GestorEventos()
    e = _equipo_base()
    e.prestamos_pendientes = [{"patricio": "Test", "monto": 500,
                                "devuelve": 650, "dias_restantes": 1}]

    msgs = ge.procesar_prestamos(e)
    assert len(e.prestamos_pendientes) == 0
    assert e.dinero == 2000 + 650
    assert any("650g" in m for m in msgs)
    print("  ✓ Préstamo se cobra al vencer")


def test_honra_y_racha():
    """Honra y racha funcionan: victoria limpia sube, evento turbio baja y resetea racha."""
    e = _equipo_base()
    e.honra = 50
    e.racha_victorias_limpias = 0

    # 4 victorias limpias → racha 4, honra +4 (1 c/u)
    for _ in range(4):
        e.registrar_victoria_limpia()
    assert e.honra == 54
    assert e.racha_victorias_limpias == 4

    # 5ta victoria → +2 (racha >=5)
    e.registrar_victoria_limpia()
    assert e.honra == 56
    assert e.racha_victorias_limpias == 5

    # Evento turbio resetea racha y baja honra
    e.registrar_evento_turbio(6)
    assert e.honra == 50
    assert e.racha_victorias_limpias == 0
    print("  ✓ Honra/racha: victoria limpia sube, turbio baja y resetea")


def test_penitencia_publica():
    """Penitencia pública: cuesta oro, da honra, ata fama."""
    ge = GestorEventos()
    e = _equipo_base()
    e.honra = 19  # ≤19 para que aparezca
    e.dinero = 1000

    ev = next(ev for ev in EVENTOS if ev["id"] == "penitencia_publica")

    # Sin dinero suficiente
    e.dinero = 100
    msgs = ge.resolver_opcion(ev, 1, e, None)
    assert e.honra == 19  # no cambia
    assert any("600g" in m for m in msgs)

    # Con dinero
    e.dinero = 1000
    msgs = ge.resolver_opcion(ev, 1, e, None)
    assert e.dinero == 1000 - 600
    assert e.honra == 19 + 20  # +20
    assert e.penitencia_fama_dias == 1
    print("  ✓ Penitencia pública correcta")


def test_titulos_honra():
    """Títulos por banda de honra sin huecos."""
    e = _equipo_base()

    e.honra = 85; assert e.titulo_honra() == "El Honorable"
    e.honra = 70; assert e.titulo_honra() == "El Respetable"
    e.honra = 59; assert e.titulo_honra() is None
    e.honra = 40; assert e.titulo_honra() is None
    e.honra = 39; assert e.titulo_honra() == "El Turbio"
    e.honra = 20; assert e.titulo_honra() == "El Turbio"
    e.honra = 19; assert e.titulo_honra() == "El Corrupto de Roma"
    e.honra = 0;  assert e.titulo_honra() == "El Corrupto de Roma"
    print("  ✓ Títulos por honra sin huecos (incluye 20)")


def test_modificador_mercado():
    """Mercado: −10% honra≥70, +15% honra≤19, normal en medio."""
    e = _equipo_base()

    e.honra = 80; assert e.modificador_mercado() == 0.90
    e.honra = 70; assert e.modificador_mercado() == 0.90
    e.honra = 69; assert e.modificador_mercado() == 1.0
    e.honra = 40; assert e.modificador_mercado() == 1.0
    e.honra = 20; assert e.modificador_mercado() == 1.0
    e.honra = 19; assert e.modificador_mercado() == 1.15
    e.honra = 0;  assert e.modificador_mercado() == 1.15
    print("  ✓ Modificador mercado simétrico correcto")


def test_persistencia_eventos():
    """GestorEventos serializa y deserializa historial."""
    import tempfile, os
    ge = GestorEventos()
    ge.historial = [{"evento": "test", "opcion": 1}]

    archivo = os.path.join(tempfile.gettempdir(), "events_test.json")
    if os.path.exists(archivo):
        os.remove(archivo)

    assert ge.guardar_estado(archivo)
    ge2 = GestorEventos()
    assert ge2.cargar_estado(archivo)
    assert ge2.historial == ge.historial

    os.remove(archivo)
    print("  ✓ Persistencia de eventos correcta")


def test_material_aleatorio():
    """material_aleatorio respeta rareza máxima."""
    for rareza_max in ["comun", "especial", "mitica"]:
        m = material_aleatorio(rareza_max)
        assert m in CATALOGO_MATERIALES
        rareza_real = CATALOGO_MATERIALES[m][0]
        orden = ["comun", "especial", "mitica"]
        assert orden.index(rareza_real) <= orden.index(rareza_max)
    print("  ✓ material_aleatorio respeta rareza máxima")