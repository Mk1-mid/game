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

**Próximo:** Fase 3 (talentos, forja, eventos, leaderboards) — ver [ROADMAP.md](ROADMAP.md).

---

*Nota: los documentos históricos originales mezclaban fechas inconsistentes (2025/2026); se conservan los hechos, no las fechas ambiguas. Todo el historial detallado permanece disponible en git.*
