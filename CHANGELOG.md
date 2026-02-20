# 📝 CHANGELOG

**Sangre por Fortuna - Historial de Desarrollo**

---

## [3.0] - 2026-02-20 🎭 **EL ALMA DEL JUEGO**

### Agregado
- ✅ **Motor de Narrativa Completo** (`src/narrativa.py`)
  - 12 eventos únicos con 80+ resultados posibles
  - Sistema de probabilidades ponderadas
  - Efectos mecánicos (Oro, XP, Heridas, Buffs temporales)
  
- ✅ **Sistema de Fama y Reputación**
  - Atributo `fama` en Gladiador y Equipo
  - Ganancia de fama en arena (proporcional a dificultad)
  - Pérdida de fama en derrota
  - Fama como disparador de eventos

- ✅ **Paso del Tiempo (Días)**
  - Nuevo botón "Pasar Día" en menú (opción 8)
  - Recuperación pasiva de HP al descansar
  - Curación de estado crítico/herido
  - Procesamiento de efectos temporales

- ✅ **Sistema de Efectos Temporales**
  - Buffs/Debuffs con duración en días
  - Aplicación automática al passar día
  - Integración con eventos narrativos

### Modificado
- 📊 `src/models.py`
  - `Gladiador`: +`fama`, +`efectos_activos`
  - `Equipo`: +`fama`, +`victoria_reciente`, +`dias_con_poco_oro`, +`racha_victorias`, +`xp_bonus_activos`
  - `Equipo.pasar_dia()`: Mejorado con lógica de rastreo y efectos

- 🎮 `main.py`
  - Integración de `GestorNarrativa` en loop principal
  - Opción 8: "PASAR DÍA" con eventos narrativos
  - Menú principal simplificado para evitar errores de codificación
  - Incremento de fama en victoria (proporcional a dificultad)
  - Pérdida de fama en derrota

### Técnico
- Importación de `GestorNarrativa` en main
- Instanciación de narrativa en `juego_principal()`
- Integración con sistema de guardado existente

---

## [2.4] - 2026-02-15 🏆 **LIGAS AUTOMÁTICAS**

### Agregado
- ✅ **Sistema de Ligas Automáticas** 
  - Puntuación por combate
  - Ranking de temporada
  - Recompensas automáticas
  - Historial de temporadas

### Modificado
- 📊 `src/models.py`: `SistemaLigas`, `LigasAutomaticas`
- 🎮 `main.py`: Integración en menú de Arena

---

## [2.3] - 2026-02-10 🎯 **DIFICULTADES DINÁMICAS**

### Agregado
- ✅ **4 Niveles de Arena**
  - Novato 🟢 (nivel -2)
  - Normal 🟡 (nivel +0)
  - Experto 🔴 (nivel +3)
  - Legendaria ⭐ (nivel +5)

- ✅ **Análisis Pre-Combate**
  - Estimación de recompensas
  - Probabilidad de victoria
  - Análisis de riesgo

### Modificado
- 🎮 `main.py`: Menú de Arena con selector de dificultad

---

## [2.2] - 2026-02-05 ⚡ **SISTEMA DE HABILIDADES**

### Agregado
- ✅ **Arquetipos y Habilidades**
  - 5 arquetipos (Guerrero, Velocista, Paladín, Asesino, Tanque)
  - 24+ habilidades especiales
  - Sistema de triggers (esquivas, críticos, etc.)

- ✅ **Combate Mejorado**
  - Habilidades se activan en combate
  - Duración y cooldowns
  - Bonificadores a stats

### Modificado
- 🎮 `src/combat.py`: Integración de habilidades
- 📊 `src/models.py`: Sistema de contadores

---

## [2.1] - 2026-02-01 🏥 **SISTEMA DE FACILIDADES**

### Agregado
- ✅ **Hospital con Médico**
  - Curación rápida (100g → 75% HP)
  - Revivir muertos (100g)
  - Curaciones lentas gratis

- ✅ **Herrerería Mejorada**
  - Compra de items potentes
  - Reparación de equipo
  - Descuentos por fama

---

## [2.0] - 2026-01-25 🎮 **SEGUNDA FASE: MECÁNICAS CORE**

### Agregado
- ✅ Autenticación de usuario
- ✅ Persistencia completa (JSON)
- ✅ Sistema de Misiones automáticas
- ✅ Sistema de Items y Equipo
- ✅ Tienda y Mercado
- ✅ Barracas (compra de espacios)

### Modificado
- 📊 Arqeuitura completa de models
- 🎮 Loop principal estable

---

## [1.0] - 2026-01-10 ⚔️ **PRIMERA FASE: MOTOR BASE**

### Agregado
- ✅ Sistema de Combate turn-based
- ✅ Generador de Enemigos
- ✅ Arquetipos de Gladiadores
- ✅ Progresión de Niveles (XP)
- ✅ Stats Base y Derivados
- ✅ Equipo y Armas

### Concepto
- Juego de gestión de ludus romana
- Combate táctica en arena
- Progresión de gladiadores

---

## Roadmap Futuro

| Fase | Tema | ETA | Prioridad |
|------|------|-----|-----------|
| 4 | Deep Play (Talentos, Forja) | Q2 2026 | Media |
| 5 | Flet UI (Desktop) | Q3 2026 | Alta |
| 6 | Expansión de Contenido | Q4 2026 | Baja |

---

*Última revisión: 2026-02-20*
