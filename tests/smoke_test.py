#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke test rápido de los nuevos sistemas Fase 3.2"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.models as models
import src.patricios as patricios
import src.events as events
import src.persistence as persistence
import src.leaderboards as leaderboards
import src.store as store
import main

print("Todos los imports OK")

# Test rápido: crear equipo, patricios, eventos
e = models.Equipo()
e.dinero = 1000
e.honra = 50

gp = patricios.GestorPatricios()
gp.generar_patricios(nivel_referencia=1)
print(f"Patricios: {len(gp.patricios)} generados")

ge = events.GestorEventos()
ev = ge.tirar_evento_dia(e, gp)
print(f"Evento tirado: {ev['id'] if ev else 'None'}")

# Test honra
e.registrar_victoria_limpia()
print(f"Honra tras victoria: {e.honra}")

# Test materiales
e.agregar_material("Mineral de Hierro", 3)
print(f"Materiales: {e.materiales}")

# Test store
mod = e.modificador_mercado()
print(f"Modificador mercado (honra {e.honra}): {mod}")

# Test patricios serialization
import json
data = gp.serializar()
print(f"Patricios serializados: {len(data['patricios'])}")
print("✅ Smoke test completo")