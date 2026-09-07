# 🛣️ ROADMAP.md — Estado y Ruta del Proyecto

**Sangre por Fortuna**

---

## 1. Estado actual — Fase 2.2 completa ✅

Sistemas implementados y funcionales:

- **Habilidades:** 25 habilidades en 5 arquetipos, 6 tipos de triggers, pasivas + activas, visualización pre-combate y durante el combate, persistencia de `habilidades_activas` y `contadores_triggers`.
- **Gladiadores (2.3):** reclutamiento, entrenamiento, curación, ocupación por días, estados (sano/herido/crítico/muerto), hospital, expansión de barracas, vender/liberar.
- **Arenas (2.4):** 4 dificultades (Novato/Normal/Experto/Legendaria) con escalado de enemigos y recompensas ×0.8–×2.0, análisis de riesgo, sistema de ligas con ranking.
- **Contenido (Fase 1):** 31 items (13 armas + 13 armaduras + 5 pociones), venta al 50%, barras HP/XP, animaciones de nivel.
- **Misiones (2.1):** 23 misiones en 4 capas con auto-tracking, notificaciones agregadas y persistencia por usuario.
- **Facilidades:** Médico progresivo (curaciones, revivir, 5 niveles) y Herrero 2.0 (mejora % por tier, durabilidad).
- **Persistencia:** partidas y misiones en JSON multiusuario, guardado automático.

**Tests:** suite `tests/run_tests_new.py` — 51/51 pasando.

---

## 2. Historial de fases

| Fase | Estado | Aporte |
|---|---|---|
| 1 — Contenido básico | ✅ | 26+ items, pociones, venta, UI visual |
| 2.1 — Misiones | ✅ | 23 misiones, auto-tracking, persistencia |
| 2.2 — Habilidades | ✅ | 25 habilidades, triggers, visualización |
| 2.3 — Sistema de gladiadores | ✅ | Gestión de equipo completa |
| 2.4 — Arenas con dificultad | ✅ | 4 arenas, ligas, análisis de riesgo |
| Herrero 2.0 | ✅ | Mejoras %, durabilidad |
| 3.1 — Leaderboards | ✅ | 3 rankings globales Top 10, máximos históricos |
| 3.2 — Eventos, Patricios y Honra | ✅ | 5–7 patricios, honra/redención, 12 eventos, mercado simétrico |

*(Cronología detallada en [HISTORIAL.md](HISTORIAL.md))*

---

## 3. Fase 3 (próxima) — Profundidad

**Objetivo:** pasar de 8.8/10 a 9.2/10. Orden de implementación: 3.1 → 3.2 → 3.3 → 3.4.

### 3.1 — Leaderboards ✅ COMPLETA
- `src/leaderboards.py`: 3 rankings Top 10 (victorias, dinero, nivel) con máximos históricos
- `data/leaderboards_global.json` global compartido entre usuarios
- Actualización automática al guardar partida + menú de visualización (opción 10)
- 6 tests nuevos en `tests/test_leaderboards.py` (suite: 13/13)

### 3.2 — Eventos, Patricios y Honra ✅ COMPLETA
- **Patricios** (`src/patricios.py`): 5–7 patricios generados al crear partida, con equipos propios, afinidad/rivalidad (−100 a +100), honra propia y simulación diaria completa (progreso + combates NPC vs NPC + ranking)
- **Honra** en `Equipo` (0–100, inicio 50): victoria limpia +1 (+2 con racha ≥5); evento turbio −5~−12 y racha=0. Títulos: "El Honorable" ≥80 / "El Respetable" 60–79 / neutro 40–59 / "El Turbio" 20–39 / "El Corrupto de Roma" ≤19. Acceso: eventos honorables ≥70 · participar turbio <40 · organizar <30 · sobreprecio mercado ≤19 · penitencia pública ≤19
- **Redención**: camino lento (racha de victorias limpias, contador visible, resetea con 1 evento turbio) o penitencia pública (600g + fama atada 1 día → +20 honra)
- **Inventario de materiales** en `Equipo` (`materiales: dict`), métodos agregar/consumir/tiene, persistencia
- **12 eventos** (`src/events.py`): mercader ambulante, préstamo a patricio (±afinidad/±honra + préstamo a 3 días), donación de admirador (oro/pociones/materiales), apuesta clandestina, torneo clandestino (participar/apostar/organizar), desafío de patricio rival (ganas: rivalidad −70%, +fama, +3 honra; pierdes: gladiador herido, rivalidad +20%, fama −5), libertad del gladiador famoso (mercado/entrenamiento/mina), relaciones de patricios, epidemia menor, rumor de soborno (gancho bootstrap, flag `habilitado_clandestino`), patrocinio honorable (honra ≥70), penitencia pública
- **Título por honra visible en leaderboards** (3.1)
- **Mercado simétrico**: honra ≥70 = −10% precios; honra ≤19 = +15% precios
- Tests: 6 tests nuevos (`tests/test_events.py`, `tests/test_patricios.py` integrados en `run_tests_new.py`); suite maestra 13/13

### 3.3 — Instalaciones de Recursos ✅ COMPLETA
- **3 instalaciones comprables** (Cantera/Granja/Aserradero), desbloqueadas con **Herrero nivel 2** (prerequisito temático)
- **Precios base:** 2500g c/u · Mejoras 1200/2200/3500/5000g · Total maxear 1 ≈ 14400g
- **Rarezas con clamp duro:** Mítica ≤8% siempre, Común ≥60% siempre, Especial absorbe resto (fórmula normalizar → clamp → redistribuir)
- **Trabajo de gladiadores:** asignación 1/3/5 días → XP (50/150/250), Stat único (+1/+3/+5), Materiales (1/2/3), Riesgo herida 5%/12%/20%
  - Cantera → Fuerza | Granja → Agilidad | Aserradero → Vitalidad (HP)
- **Ingreso pasivo:** 50/75/100/125/150g por nivel/día · Complementa arena, nunca la reemplaza
- **Ocupación:** Reusa `ocupar()`/`pasar_dia()` existente · Persistencia en save del usuario
- Tests: 19 tests nuevos en `tests/test_instalaciones.py` (suite: 51/51)

### 3.4 — Herrería: Construcción y Mejora (~4h)
- **Construcción (forja):** recetas de armas y armaduras desde materiales + dinero, desbloqueadas por nivel de Herrero
- **Mejora de armaduras:** extender el sistema actual (solo armas) a armaduras con % DEF/HP, durabilidad y costos cuadráticos
- Reparación de armaduras; más recetas/materiales ampliables

Cada sistema incluye su suite de tests.

---

## 4. Fase 4 — Árbol de Talentos

Sistema aislado y ampliable (~4h):

- `src/talents.py`: 4 ramas (Fuerza, Resistencia, Agilidad, Técnica) × 5 niveles
- 1 punto por nivel de gladiador; habilidad única en nivel 5 de cada rama
- Integración con `subir_nivel()`, persistencia, menú de asignación
- Extensible luego: más ramas, prestigio/reset, sinergias entre ramas

---

## 5. Visión a largo plazo

**Fase 5 — Pulido final (v4.0+):**

- Interfaz gráfica con Pygame (sprites, animaciones, botones)
- Música por contexto (menú, combate, victoria, derrota)
- Casa/base mejorable (5 mejoras)
- Modo historia (10 capítulos, jefes únicos, recompensas exclusivas)

Meta: juego de calidad casi comercial. Opcional si Fases 3–4 ya son suficientes.
