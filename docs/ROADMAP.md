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

**Tests:** suite `tests/run_tests_new.py` — 7/7 pasando.

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

*(Cronología detallada en [HISTORIAL.md](HISTORIAL.md))*

---

## 3. Fase 3 (próxima) — Profundidad

**Objetivo:** pasar de 8.8/10 a 9.2/10. **Esfuerzo estimado:** 10–12 horas.

| Sistema | Esfuerzo | Detalles clave |
|---|---|---|
| **Árbol de Talentos** (`src/talents.py`) | 4h | 1 punto/nivel; 4 ramas (Fuerza, Resistencia, Agilidad, Técnica) × 5 niveles; habilidad única en nivel 5 de rama |
| **Sistema de Forja** (ampliar `Herrero`) | 3h | Mejora +1 ATK/nivel, −5% durabilidad, costo cuadrático; reparación |
| **Eventos Aleatorios** (`src/events.py`) | 3h | 10 eventos (mercader, apuesta, torneo sorpresa...), 10% de probabilidad, historial |
| **Leaderboards** (`src/leaderboards.py`) | 2h | 3 rankings (victorias, dinero, nivel) Top 10, JSON global compartido |

Cada sistema incluye su suite de tests.

---

## 4. Visión a largo plazo

**Fase 4 — Pulido final (v3.0+):**

- Interfaz gráfica con Pygame (sprites, animaciones, botones)
- Música por contexto (menú, combate, victoria, derrota)
- Casa/base mejorable (5 mejoras)
- Modo historia (10 capítulos, jefes únicos, recompensas exclusivas)

Meta: juego de calidad casi comercial. Opcional si Fase 3 ya es suficiente.
