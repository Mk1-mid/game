#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests del sistema de Leaderboards Globales (Fase 3.1)
=====================================================

Cubre: caso normal, casos límite, entrada inválida y ciclo
completo de persistencia (guardar/cargar en JSON).

Usa un archivo temporal propio para no tocar data/ real.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.leaderboards import LeaderboardsGlobales, guardar_leaderboards, cargar_leaderboards


def _archivo_temporal():
    """Ruta de archivo temporal para tests (no toca data/ real)."""
    return os.path.join(tempfile.gettempdir(), "leaderboards_test.json")


def _archivo_limpio():
    """Devuelve ruta temporal garantizando que empieza vacía."""
    archivo = _archivo_temporal()
    if os.path.exists(archivo):
        os.remove(archivo)
    return archivo


def test_actualizar_y_top():
    """Caso normal: registrar jugadores y obtener el Top ordenado."""
    archivo = _archivo_limpio()
    lb = LeaderboardsGlobales(archivo)

    lb.actualizar_jugador("ana", victorias=10, dinero=500, nivel_maximo=3)
    lb.actualizar_jugador("beto", victorias=25, dinero=900, nivel_maximo=7)
    lb.actualizar_jugador("carla", victorias=15, dinero=1200, nivel_maximo=5)

    top_victorias = lb.obtener_top("victorias")
    assert top_victorias[0] == ("beto", 25), f"Primer puesto incorrecto: {top_victorias[0]}"
    assert top_victorias[1] == ("carla", 15), f"Segundo puesto incorrecto: {top_victorias[1]}"

    top_dinero = lb.obtener_top("dinero")
    assert top_dinero[0] == ("carla", 1200), f"Dinero top incorrecto: {top_dinero[0]}"

    print("  ✓ Actualización y Top ordenado correctos")


def test_maximo_historico():
    """El leaderboard guarda máximos históricos, no valores actuales."""
    archivo = _archivo_limpio()
    lb = LeaderboardsGlobales(archivo)

    lb.actualizar_jugador("ana", victorias=20, dinero=1000, nivel_maximo=8)
    # Ana "pierde" progreso: su récord NO debe bajar
    lb.actualizar_jugador("ana", victorias=5, dinero=100, nivel_maximo=2)

    assert lb.obtener_top("victorias")[0] == ("ana", 20)
    assert lb.obtener_top("dinero")[0] == ("ana", 1000)
    assert lb.obtener_top("nivel")[0] == ("ana", 8)

    print("  ✓ Máximos históricos preservados")


def test_limite_top10():
    """Caso límite: con más de 10 jugadores, el Top recorta a 10."""
    archivo = _archivo_limpio()
    lb = LeaderboardsGlobales(archivo)

    for i in range(15):
        lb.actualizar_jugador(f"jugador_{i}", victorias=i, dinero=i * 10, nivel_maximo=1)

    top = lb.obtener_top("victorias")
    assert len(top) == 10, f"Top debería tener 10, tiene {len(top)}"
    assert top[0] == ("jugador_14", 14), f"El mejor no está primero: {top[0]}"
    assert ("jugador_0", 0) not in top, "El peor no debería estar en el Top"

    print("  ✓ Límite Top 10 respetado")


def test_entradas_invalidas():
    """Caso de error: usuario inválido y categoría inexistente."""
    archivo = _archivo_limpio()
    lb = LeaderboardsGlobales(archivo)

    exito, _, _ = lb.actualizar_jugador("", victorias=5, dinero=100, nivel_maximo=2)
    assert exito is False, "Usuario vacío debería fallar"

    exito, _, _ = lb.actualizar_jugador(None, victorias=5, dinero=100, nivel_maximo=2)
    assert exito is False, "Usuario None debería fallar"

    assert lb.obtener_top("oro") == [], "Categoría inexistente debe retornar lista vacía"
    assert lb.obtener_posicion("nadie", "victorias") is None
    assert "inválida" in lb.generar_string_ranking("oro").lower()

    print("  ✓ Entradas inválidas rechazadas correctamente")


def test_persistencia_ciclo_completo():
    """Persistencia: guardar y cargar sobrevive el ciclo JSON completo."""
    archivo = _archivo_limpio()

    lb = LeaderboardsGlobales(archivo)
    lb.actualizar_jugador("ana", victorias=12, dinero=800, nivel_maximo=6)
    lb.actualizar_jugador("beto", victorias=4, dinero=2000, nivel_maximo=2)

    # Cargar como si fuera otra sesión (otra instancia desde disco)
    lb_cargado = cargar_leaderboards(archivo)

    assert lb_cargado.obtener_top("victorias")[0] == ("ana", 12)
    assert lb_cargado.obtener_top("dinero")[0] == ("beto", 2000)
    assert lb_cargado.registros == lb.registros

    # Archivo corrupto no debe romper la carga
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write("{ no es json valido")
    lb_corrupto = cargar_leaderboards(archivo)
    assert lb_corrupto.registros == {}, "Archivo corrupto debe dar registros vacíos"

    if os.path.exists(archivo):
        os.remove(archivo)

    print("  ✓ Ciclo completo de persistencia (guardar → cargar → corrupto)")


def test_posicion_jugador():
    """Caso límite: posición de un jugador concreto en el ranking."""
    archivo = _archivo_limpio()
    lb = LeaderboardsGlobales(archivo)

    lb.actualizar_jugador("primero", victorias=30, dinero=0, nivel_maximo=1)
    lb.actualizar_jugador("segundo", victorias=20, dinero=0, nivel_maximo=1)
    lb.actualizar_jugador("tercero", victorias=10, dinero=0, nivel_maximo=1)

    assert lb.obtener_posicion("primero", "victorias") == 1
    assert lb.obtener_posicion("tercero", "victorias") == 3

    print("  ✓ Posiciones calculadas correctamente")
