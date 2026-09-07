# 📜 HISTORIAL.md — Historial del Desarrollo

> Registro único y consolidado del desarrollo de **Sangre por Fortuna**. Condensa todos los reportes de sesiones, fases, auditorías y changelogs antiguos.

---

## Análisis inicial del juego

El juego partía de una base sólida: combate automático por turnos, 5 tipos de enemigos, autenticación, tienda básica y guardado. Debilidades: solo 3 armas y 3 armaduras, sin progresión XP, sin habilidades ni objetivos, penalización mínima por perder. Valoración original: Calidad 4/5, Diversión 3/5, Rejugabilidad 2/5, **Potencial 5/5**.

---

## Línea de tiempo

### 🟦 v2.0 — Sistema de progresión (Enero 2026)

- Sistema XP/Niveles: `XP_requerido = 100 * (1.1^nivel)`, escalado logarítmico (HP ×1.095, ATK ×1.085, DEF ×1.075, SPD ×1.065 por nivel).
- Recompensas dinámicas: `50 * (1.15^nivel)` XP por combate, variación ±10%.
- Clase `Gladiador` mejorada: equipo de hasta 6, estado, ocupación por días, historial W/L.
- Tests: 57 ejecutados, 56 pasados (98.2%); único fallo por aleatoriedad estadística.

### 🟩 Fase 1 — Contenido básico

- Catálogo expandido: 3→13 armas, 3→13 armaduras (4 tiers, 50–1200g) + pociones; venta al 50%.
- Balance verificado (`test_balance_fase1.py`): progresión por tier coherente, sin items rotos.

### 🟨 Fase 2.1 + Sesión 3 — Misiones, notificaciones y persistencia (Enero 2025)

- **Misiones:** 4 capas (CORE, CHAINS, SIDE, AUTO), 23 misiones en `src/misiones.py`; auto-tracking de combate/dinero/nivel; menú de misiones integrado.
- **Notificaciones mejoradas:** agregación de misiones completadas con totales (dinero + XP), deduplicación.
- **Persistencia de misiones:** `guardar_estado()`/`cargar_estado()` en JSON por usuario.
- **Fix crítico:** las partidas se guardaban pero nunca se restauraban; reparado con `serializar_equipo()`/`deserializar_equipo()` + auto-guardado al salir.
- 11 tests nuevos, 100% pasando.

### 🟧 Fase 2.2 — Habilidades especiales (Enero 2026)

- 25 habilidades (5 arquetipos × 5): 15 pasivas + 10 activas con 6 tipos de triggers.
- `mostrar_habilidad_activada()` en combate; `mostrar_habilidades_gladiador()` pre-combate.
- Persistencia de `habilidades_activas` y `contadores_triggers` en partidas.
- UX de habilidades: 5/10 → 9.5/10 según reporte de la sesión.

### 🟥 Fase 2.3 + 2.4 — Gladiadores, arenas y pulido UI (Enero 2026)

- 10 mejoras UI/UX: barras de progreso de ocupación, indicadores 💪/🏥, resumen antes/después de entrenar, análisis de riesgo pre-combate, badges de arena, selector visual de dificultad.
- ~300 líneas nuevas en main.py con 7 funciones auxiliares de UI.
- Puntuación del juego reportada: 6/10 → 8.8/10.

### ⚒️ Herrero 2.0

- Mejora de armas de bonus fijos a **% por tier (+8%/+12%/+15%/+20%)**; costos cuadráticos (`base × tipo × nivel²`).
- **Durabilidad**: −5% por mejora; reparación `(100 − durab) × base / 10`.
- Niveles de herrero 1–5 desbloquean tiers (600g → 4000g).

### 🌐 Fase 3.1 — Leaderboards Globales (Septiembre 2026)

- Nuevo módulo `src/leaderboards.py`: `LeaderboardsGlobales` con 3 rankings Top 10 (victorias, fortuna, nivel máximo) compartidos entre TODOS los usuarios.
- Registra **máximos históricos** (no valores actuales): un jugador que llegó a 5000g conserva ese récord aunque luego gaste el dinero.
- Archivo global `data/leaderboards_global.json` (fuera del save de cada usuario, para que nadie sobreescriba los récords de otro); tolerante a archivo corrupto.
- Integración en `main.py`: opción 10 del menú principal (Top victorias / fortuna / nivel + posición propia) y actualización automática al guardar (opciones 8 y 9).
- Infraestructura de proyecto: creado `AGENTS.md` con las convenciones y reglas de desarrollo; README apunta a él.
- Tests: 6 tests nuevos en `tests/test_leaderboards.py` (caso normal, máximos, límite Top 10, entradas inválidas, posición, ciclo completo de persistencia); suite maestra 7/7 → 13/13.

### 🏛️ Fase 3.2 — Eventos, Patricios y Honra (Septiembre 2026)

- **Patricios** (`src/patricios.py`): 5–7 patricios generados al crear partida, con equipos propios (2–4 gladiadores reales), afinidad/rivalidad (−100 a +100), honra propia y simulación diaria completa (progreso de equipos + combates NPC vs NPC + ranking local).
- **Honra** en `Equipo` (0–100, inicio 50): victoria limpia +1 (+2 con racha ≥5); evento turbio −5~−12 y racha=0. Títulos: "El Honorable" ≥80 / "El Respetable" 60–79 / neutro 40–59 / "El Turbio" 20–39 / "El Corrupto de Roma" ≤19.
- **Redención**: camino lento (racha de victorias limpias, contador visible, resetea con 1 evento turbio) o penitencia pública (600g + fama atada 1 día → +20 honra).
- **Inventario de materiales** en `Equipo` (`materiales: dict`), métodos agregar/consumir/tiene, persistencia.
- **12 eventos** (`src/events.py`): mercader ambulante, préstamo a patricio (±afinidad/±honra + préstamo a 3 días), donación de admirador (oro/pociones/materiales), apuesta clandestina, torneo clandestino (participar/apostar/organizar), desafío de patricio rival (ganas: rivalidad −70%, +fama, +3 honra; pierdes: gladiador herido, rivalidad +20%, fama −5), libertad del gladiador famoso (mercado/entrenamiento/mina), relaciones de patricios, epidemia menor, rumor de soborno (gancho bootstrap, flag `habilitado_clandestino`), patrocinio honorable (honra ≥70), penitencia pública.
- **Título por honra visible en leaderboards** (Fase 3.1).
- **Mercado simétrico**: honra ≥70 = −10% precios; honra ≤19 = +15% precios.
- Hook de "fin de día" tras cada combate: avanza ocupación, resetea facilities, simula patricios, tira evento, procesa préstamos, reduce fama atada, actualiza honra/racha.
- Tests: 6 tests nuevos (`tests/test_events.py`, `tests/test_patricios.py`) integrados en `run_tests_new.py`; suite maestra 13/13 → 30/30.

### 🏛️ Fase 3.3 — Instalaciones de Recursos (Septiembre 2026)

- **3 instalaciones comprables** (Cantera, Granja, Aserradero) con **prerequisito de Herrero nivel 2** (los materiales no tienen uso sin Forja).
- **Precios:** 2500g base · mejoras 1200/2200/3500/5000g · total maxear 1 ≈ 14400g.
- **Rarezas con clamp duro:** mítica ≤8% siempre, común ≥60% siempre, especial absorbe resto (fórmula: normalizar → clamp mítica≤8% → clamp común≥60% → especial absorbe).
- **Trabajo de gladiadores:** 1/3/5 días → XP 50/150/250, stat +1/+3/+5, 1/2/3 materiales, riesgo herida 5%/12%/20%.
  - Cantera → Fuerza | Granja → Agilidad | Aserradero → Vitalidad (HP).
- **Ingreso pasivo:** 50/75/100/125/150g por nivel/día (complementa arena, nunca la reemplaza).
- **Ocupación:** reusa `ocupar()`/`pasar_dia()` existente.
- **Prerequisito Herrero 2:** coherencia temática (materiales sin forja no sirven).
- Tests: 19 tests nuevos en `tests/test_instalaciones.py`; suite maestra 30/30 → 51/51.

### ✅ Auditorías y validación global

- 25 archivos Python compilando sin errores, 0 imports rotos, 100% docstrings.
- Suites históricas: misiones 7/7, auto-tracking 7/7, notificaciones/persistencia 5/5, integración 2/2, pulido 2.2 4/4.
- Rendimiento: guardar/cargar ~1ms; notificación ~0.1ms.

### 🧹 Reorganizaciones del proyecto

1. **Unificación de documentación v1:** fusión de `/docs` y `/documentacion`, de 18 archivos con ~30% duplicación a estructura organizada.
2. **Depuración (Enero 2025):** 27 → 8 documentos principales; limpieza de raíz y tests.
3. **Reorganización final:** código v1 movido a `legacy/`, tests unificados en `tests/`, datos en `data/`, música en `assets/`, documentación comprimida a 4 archivos (README + docs/TECNICA + docs/ROADMAP + docs/HISTORIAL).

---

## Changelog de versiones

| Versión | Cambios clave |
|---|---|
| **1.0.0** | Auth, combate por turnos, 5 enemigos, tienda (6 items), guardado JSON. Sin progresión. |
| **2.0.0** | Sistema XP/Niveles logarítmico, Gladiador con estado completo, recompensas dinámicas. |
| **2.1** | Sistema de misiones (23 misiones), notificaciones, persistencia de misiones. |
| **2.2** | Habilidades especiales (25), triggers, visualización, contenido Fase 1 (31 items). |
| **2.3–2.4** | Sistema de gladiadores (equipo completo), arenas con 4 dificultades, ligas, pulido UI. |
| Herrero 2.0 | Mejoras % por tier, durabilidad, niveles de herrero. |
| **3.1** | Leaderboards globales (3 rankings Top 10 multiusuario, máximos históricos). |
| **3.2** | Eventos, patricios, honra/redención, 12 eventos, mercado simétrico. |
| **3.3** | Instalaciones de recursos (Cantera/Granja/Aserradero, trabajo gladiadores, clamp rareza, prereq herrero 2). |

**Próximo:** Fase 3.4 (herrería ampliada/forja) — ver [ROADMAP.md](ROADMAP.md).

---

*Nota: los documentos históricos originales mezclaban fechas inconsistentes (2025/2026); se conservan los hechos, no las fechas ambiguas. Todo el historial detallado permanece disponible en git.*
