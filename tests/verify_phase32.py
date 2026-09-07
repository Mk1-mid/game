#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificación exhaustiva Fase 3.2"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.models as models
import src.patricios as patricios
import src.events as events
import src.persistence as persistence
import src.leaderboards as leaderboards
import src.store as store

print("=== VERIFICACION FASE 3.2 ===")
print()

# 1. Material y catalogo
print("1. Materiales y catalogo:")
for nombre, (rareza, valor) in models.CATALOGO_MATERIALES.items():
    print(f"   {nombre}: {rareza}, {valor}g")
print(f"   Total: {len(models.CATALOGO_MATERIALES)} materiales")
print()

# 2. Equipo con honra, materiales, titulos
print("2. Equipo - Honra, materiales, titulos:")
e = models.Equipo()
e.dinero = 5000
e.honra = 50
print(f"   Honra inicial: {e.honra}")
print(f"   Titulo: {e.titulo_honra()}")
print(f"   Modificador mercado: {e.modificador_mercado()}")

# Test racha
for _ in range(5):
    e.registrar_victoria_limpia()
print(f"   Tras 5 victorias limpias: honra={e.honra}, racha={e.racha_victorias_limpias}")

e.registrar_evento_turbio(6)
print(f"   Tras evento turbio: honra={e.honra}, racha={e.racha_victorias_limpias}")

# Materiales
e.agregar_material("Mineral de Hierro", 5)
print(f"   Materiales: {e.materiales}")
print(f"   Tiene 3 Mineral: {e.tiene_material('Mineral de Hierro', 3)}")
ok, cant, msg = e.consumir_material("Mineral de Hierro", 2)
print(f"   Consumir 2: {msg}, quedan: {e.materiales}")
print()

# 3. Patricios
print("3. Patricios:")
gp = patricios.GestorPatricios()
gp.generar_patricios(nivel_referencia=2, cantidad=6)
print(f"   Generados: {len(gp.patricios)} patricios")
for p in gp.patricios:
    print(f"   {p.nombre}: honra={p.honra}, afinidad={p.afinidad}, glads={len(p.gladiadores)}")
log = gp.simular_dia()
print(f"   Simulacion dia: {len(log)} eventos")
print(f"   Ranking: {[(p.nombre, p.victorias) for p in gp.obtener_ranking()[:3]]}")
print()

# 4. Eventos
print("4. Eventos:")
ge = events.GestorEventos()
print(f"   Eventos en catalogo: {len(events.EVENTOS)}")
for ev in events.EVENTOS:
    print(f"   - {ev['id']}: {ev['nombre']} (tipo {ev['tipo']})")
print()

# 5. Condiciones de eventos
print("5. Condiciones de eventos (test):")
e2 = models.Equipo()
e2.dinero = 2000
e2.honra = 35
e2.habilitado_clandestino = True
pt = patricios.GestorPatricios()
from src.models import Gladiador
g = Gladiador("Test", "Murmillo", nivel=1)
pt.patricios = [patricios.Patricio("Rival", 20, [g], afinidad=-60)]
candidatos = ge._candidatos(e2, pt)
print(f"   Eventos disponibles con honra 35 + clandestino: {len(candidatos)}")
for c in candidatos:
    print(f"   - {c['id']}")
print()

# 6. Leaderboards con titulo
print("6. Leaderboards con titulo de honra:")
lb = leaderboards.LeaderboardsGlobales()
lb.actualizar_jugador("test_user", victorias=10, dinero=5000, nivel_maximo=5, titulo="El Honorable")
top = lb.obtener_top("victorias")
print(f"   Top: {top}")
print("   Ranking string:")
print(lb.generar_string_ranking("victorias"))
print()

# 7. Store con modificador
print("7. Store con modificador de honra:")
e3 = models.Equipo()
e3.honra = 80
print(f"   Honra 80: modificador {e3.modificador_mercado()}")
e3.honra = 19
print(f"   Honra 19: modificador {e3.modificador_mercado()}")
e3.honra = 50
print(f"   Honra 50: modificador {e3.modificador_mercado()}")
print()

# 8. Persistencia completa
print("8. Persistencia (save/load):")
# Guardar equipo
data = persistence.serializar_equipo(e)
print(f"   Equipo serializado keys: {list(data.keys())}")
print(f"   Honra guardada: {data.get('honra')}")
print(f"   Materiales guardados: {data.get('materiales')}")
print(f"   Raacha guardada: {data.get('racha_victorias_limpias')}")
print(f"   Habilitado clandestino: {data.get('habilitado_clandestino')}")
print(f"   Rumor ofrecido: {data.get('rumor_ofrecido')}")
print(f"   Fama: {data.get('fama')}")
print(f"   Prestamos: {data.get('prestamos_pendientes')}")
print(f"   Penitencia dias: {data.get('penitencia_fama_dias')}")

# Deserializar
e_loaded = persistence.deserializar_equipo(data)
print(f"   Cargado: honra={e_loaded.honra}, materiales={e_loaded.materiales}, racha={e_loaded.racha_victorias_limpias}")

# Patricios persist
pat_data = gp.serializar()
print(f"   Patricios serializados: {len(pat_data['patricios'])} patricios, {len(pat_data['historial_npc'])} historial")
gp2 = patricios.GestorPatricios()
gp2.deserializar(pat_data)
print(f"   Patricios cargados: {len(gp2.patricios)}")

# Eventos persist
ge.historial = [{"evento": "test", "opcion": 1}]
ev_data = ge.serializar()
print(f"   Eventos serializados: {len(ev_data['historial'])} entradas")
ge2 = events.GestorEventos()
ge2.deserializar(ev_data)
print(f"   Eventos cargados: {len(ge2.historial)}")
print()

print("=== VERIFICACION COMPLETA ===")