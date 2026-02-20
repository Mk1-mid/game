# 🗺️ ROADMAP COMPLETO - SANGRE POR FORTUNA v2.0 → v4.0

**Objetivo:** Transformar el juego de 6/10 → 9/10  
**Duración total:** 30-35 horas de trabajo

---

## 📅 FASE 1: CONTENIDO BÁSICO (Semana 1)
**⏱️ Duración:** 3-4 horas | **🔴 Prioridad:** CRÍTICA | **⭐ Impacto:** 5/5

### 🎯 Objetivo
Multiplicar el contenido disponible por 4x y dar razones inmediatas para seguir jugando.

### Tareas

#### ✅ 1.1 Expandir Armas (COMPLETADO ✓)
**Archivo:** `src/store.py`

**10 armas nuevas agregadas en 4 tiers:**
- **Tier 1 (50-100g):** Daga Oxidada, Lanza Corta
- **Tier 2 (150-300g):** Espada Corta, Tridente Romano, Martillo Guerra
- **Tier 3 (350-500g):** Espada Gladius, Gladius Imperial, Hacha Doble
- **Tier 4 (800-900g):** Espada de Marte, Tridente Neptuno, Lanza del Destino

**✅ Resultado:** 13 armas totales (de 3 actuales)
**✅ Balance verificado:** Progresión clara, ratios coherentes, sin OP

---

#### ✅ 1.2 Expandir Armaduras (COMPLETADO ✓)
**Archivo:** `src/store.py`

**10 armaduras nuevas en 4 tiers:**
- **Tier 1 (50-100g):** Ropa Harapienta, Cuero Endurecido
- **Tier 2 (150-300g):** Cota Malla, Armadura Bronce, Peto Hierro, Escudo Imperial, Armadura Espartana
- **Tier 3 (350-500g):** Armadura Centurión, Coraza Reforzada, Armadura Acorazada
- **Tier 4 (900-1200g):** Armadura Júpiter, Peto Divino, Armadura Inmortal

**✅ Resultado:** 13 armaduras totales (de 3 actuales)
**✅ Balance verificado:** Progresión clara, escalado de HP correcto, sin OP

---

#### ✅ 1.3 Sistema de Pociones (COMPLETADO ✓)
**Archivos:** `src/models.py` (líneas 38-67), `src/store.py` (funciones nuevas)

**Clase Potion creada:**
```python
class Potion(Item):
    def __init__(self, nombre, tipo, valor)
    def usar(personaje): aplica efecto y retorna mensaje
```

**5 Pociones implementadas:**
1. ✅ Curación Menor - 30g (restaura 50 HP)
2. ✅ Curación Mayor - 60g (restaura 100 HP)
3. ✅ Fuerza Temporal - 50g (+10 ATK temporal)
4. ✅ Defensa Temporal - 50g (+5 DEF temporal)
5. ✅ Velocidad Temporal - 50g (+5 SPD temporal)

**Funciones en store.py:**
- ✅ `comprar_pocion(opcion, dinero, inventario)` - compra con validación
- ✅ `mostrar_catalogo()` mejorado - ahora muestra todas las 31 items

**Prueba:** ✅ test_pociones_venta.py (PASADO - todo funciona)

---

#### ✅ 1.4 Vender Items (COMPLETADO ✓)
**Archivo:** `src/store.py` (funciones nuevas)

**Funciones implementadas:**
- ✅ `vender_item(opcion, dinero, inventario)` - vende cualquier item al 50%
- ✅ `mostrar_inventario(inventario)` - UI con categorías y precios venta
- ✅ Sistema de 50% de resale value (item sink para economía)

**Características:**
- Funciona para TODAS las 31 items (armas/armaduras/pociones)
- Muestra desglose: ARMAS ⚔️ | ARMADURAS 🛡️ | POCIONES 🧪
- Precio de venta inmediato visible (50% del original)
- Inventario actualizado automáticamente

**Prueba:** ✅ test_pociones_venta.py (PASADO - venta verificada)

---

#### ✅ 1.5 Mejorar UI (COMPLETADO ✓)
**Archivos:** `src/models.py` (métodos en Gladiador), `main.py` (integración)

**Métodos visuales en Gladiador:**
- ✅ `generar_barra_hp()` - barra de 20 chars con % y emojis
- ✅ `generar_barra_xp()` - barra de 20 chars con % y emojis
- ✅ `generar_string_stats()` - stats formateados con emojis
- ✅ `animacion_nivel_up()` - animación ASCII cuando sube de nivel

**UI Implementada:**
```
❤️  HP: 142/142 (100%)
████████████████████

XP: 110/235 (46%)
██████████░░░░░░░░░░

⚔️  ATK: 24  │  🛡️  DEF: 6  │  ⚡ SPD: 13

⭐ ¡SUBISTE DE NIVEL! ⭐
Nivel 8 → Nivel 9
+10 HP  │  +2 ATK  │  +1 DEF  │  +1 SPD
```

**Integración en main.py:**
- ✅ `mostrar_pantalla_equipo()` - ahora muestra barras visuales
- ✅ `combate_equipo()` - muestra animación al subir nivel

**Prueba:** ✅ test_ui_visual.py (PASADO - todas las barras funcionan)

---

### ✅ Checklist Fase 1 - 100% COMPLETADO ✅✅✅✅✅
- [x] 13 armas expandidas (Tier 1-4)
- [x] 13 armaduras expandidas (Tier 1-4)
- [x] 5 pociones funcionales (heal + buffs)
- [x] Sistema venta implementado (50% resale)
- [x] Barra HP visual (20 chars)
- [x] Barra XP visual (20 chars)
- [x] Animación nivel up con detalles
- [x] UI mejorada con emojis
- [x] Inventario visual por categorías
- [x] Balance económico verificado

**📊 Progreso:** 10/10 completadas ✅ (100%)

**📊 Resultado FINAL:** Juego pasa de 6/10 → **7.5/10** ⬆️ +1.5

**Cambios Totales:**
- Items: 6 → 31 (5x expansión)
- Mecánicas: compra + venta + pociones (3 nuevas)
- UI: básica → visual con barras + emojis + animaciones
- Tests: 9 archivos con cobertura completa

**Estructura de Carpetas Organizada:**
- `tests/` - 9 archivos de test centralizados
- `src/` - modelos, tienda, combate, autenticación
- `main.py` - punto de entrada unificado
- `docs/` - documentación técnica

---

## 📅 FASE 2: MECÁNICAS CORE (Semana 2-3)
**⏱️ Duración:** 8-10 horas | **🟡 Prioridad:** IMPORTANTE | **⭐ Impacto:** 5/5

### 🎯 Objetivo
Agregar profundidad con sistemas que den objetivos claros y decisiones tácticas.

### Tareas

#### ✅ 2.1 Sistema de Misiones (3 horas)
**Archivo nuevo:** `src/quests.py`

**Crear clase Mision:**
```python
- tipo: "combate", "nivel", "dinero", "items"
- progreso vs objetivo
- recompensas (dinero + XP)
- estado: activa/completada
```

**11 Misiones iniciales:**
- Combate: Gana 1/5/10/25 combates
- Nivel: Alcanza nivel 5/10/20
- Dinero: Acumula 1000/5000 oro
- Items: Compra 5 items, equipa legendario

**GestorMisiones:**
- Tracking automático
- Actualización por eventos
- Reclamar recompensas

**Integración:** Nuevo menú "Misiones" en juego principal

---

#### ✅ 2.1B Notificaciones + Persistencia (2 horas)
**Archivo:** `src/misiones.py` (métodos nuevos)

**Notificaciones Mejoradas:**
- ✅ Formato visual con bordes y emojis
- ✅ Agregación de múltiples misiones completadas
- ✅ Cálculo de totales (dinero + XP)
- ✅ Información de bonus cuando aplica
- ✅ Deduplicación para eventos simultáneos
- ✅ Hint sobre dónde reclamar recompensas

**Ejemplo:**
```
======================================================================
        ✨ ¡MISIONES COMPLETADAS! ✨
======================================================================

✓ Primer Paso
  💰 100g | 📈 50 XP

✓ Primeras Ganancias
  💰 200g | 📈 100 XP

----------------------------------------------------------------------
📊 TOTAL: 300g + 150 XP
======================================================================
💡 Puedes reclamar recompensas en el menú de Misiones
```

**Sistema de Persistencia:**
- ✅ Guardar estado de misiones en JSON
- ✅ Cargar estado completamente
- ✅ Soporta múltiples usuarios (archivos separados)
- ✅ Restaura progreso, estado y bonus
- ✅ Manejo robusto de errores
- ✅ Reset de misiones a estado inicial

**Integración en main.py:**
- Carga automática al iniciar sesión
- Guardar al presionar "8. Guardar Partida"
- Archivos en `datos/misiones_{usuario}.json`

**Tests:**
- ✅ test_notificaciones_persistencia.py (5 tests)
- ✅ test_integracion_completa.py (sesión simulada)
- ✅ 100% cobertura: formato, totales, persistencia, aislamiento, bonus, reset

#### ✅ 2.2 Habilidades Especiales (3 horas)
**Archivos:** `src/combat.py`, `src/models.py`

**Crear clase Habilidad:**
```python
- nombre, tipo, potencia, cooldown
- usar(): ejecuta efecto
- reducir_cooldown()
```

**5 Habilidades por arquetipo:**
1. **Murmillo:** Muro de Escudos (defense +50%, CD: 3)
2. **Retiarius:** Ataque Rápido (damage x1.5, CD: 2)
3. **Secutor:** Golpe Preciso (damage x2.0, CD: 4)
4. **Thraex:** Furia Bárbara (buff +30% ATK, CD: 3)
5. **Hoplomachus:** Regeneración (heal 30% HP, CD: 5)

**Modificar combate:**
- Opciones: Ataque normal / Habilidad / Poción
- Sistema de cooldowns
- Decisiones tácticas

---

#### ✅ 2.3 Activar Sistema de Gladiadores (4 horas) - COMPLETADO ✅
**Archivo:** `main.py` + mejoras en `src/models.py`

**Estado:** ✅ 100% IMPLEMENTADO + MEJORADO CON UI VISUAL

**Mejoras Implementadas (Fase 2.3):**
- ✅ Barra de Progreso de Ocupación - Visual progress bars
- ✅ Indicador Visual de Entrenamiento - Emojis diferenciados (💪/🏥)
- ✅ Resumen de Cambios Post-Entrenamiento - Antes/Después detallado
- ✅ Animación ASCII de Mejora - Celebración visual
- ✅ Estadísticas del Gladiador - Win rate y stats al seleccionar

**Menu Gestión Equipo:**
```
Ver equipo (estados, niveles, historial) ✓
Reclutar gladiador (200-500g) ✓
Entrenar gladiador (mejora stats, 1-3 días) ✓
Curar gladiador (restaura HP, cuesta dinero) ✓
Asignar a combate ✓
Vender/liberar gladiador ✓
```

**Sistema de Días:**
- ✅ Cada acción consume días
- ✅ Gladiadores en "ocupación" (entrenar/curar/descansar)
- ✅ Contador visual de días hasta disponibilidad

**Estados:**
- ✅ Sano (100-80% HP)
- ✅ Herido (79-30% HP)
- ✅ Crítico (29-1% HP)
- ✅ Muerto (0% HP, revivible con costo alto)

**📊 Completitud: 100% (con mejoras UI)**

---

#### ✅ 2.4 Arenas con Dificultad (2 horas) - COMPLETADO ✅
**Archivo:** `src/enemies.py` + `main.py`

**Estado:** ✅ 100% IMPLEMENTADO + MEJORADO CON UI VISUAL

**Mejoras Implementadas (Fase 2.4):**
- ✅ Análisis de Riesgo Pre-Combate - Evaluación detallada
- ✅ Histórico de Últimos Combates - Tracking automático
- ✅ Estimador de Recompensas - Cálculo visible antes
- ✅ Badges/Logros Desbloqueables - Sistema de tracking
- ✅ Selector Visual Mejorado - Tabla ASCII profesional

**4 Niveles de Arena:**
1. **Novato:** Enemigos nivel -2, recompensa x0.8 ✅
2. **Normal:** Enemigos nivel +0, recompensa x1.0 ✅
3. **Experto:** Enemigos nivel +3, recompensa x1.5 ✅
4. **Legendaria:** Enemigos nivel +5, recompensa x2.0 ✅

**Requisitos de nivel:**
- Novato: Nivel 1+ ✅
- Normal: Nivel 3+ ✅
- Experto: Nivel 10+ ✅
- Legendaria: Nivel 20+ ✅

**Menú Arena mejorado:**
- ✅ Elegir dificultad (tabla visual)
- ✅ Ver recompensas (estimado dinámico)
- ✅ Warning de riesgo (análisis pre-combate)
- ✅ Badges de logros

**📊 Completitud: 100% (con mejoras UI)**

---

### ✅ Checklist Fase 2.1 - Misiones + Notificaciones + Persistencia
- [x] 23 misiones funcionales (4-capas: core, chains, side, auto)
- [x] Auto-tracking de eventos (combate, dinero, nivel, items)
- [x] Notificaciones mejoradas con totales
- [x] Sistema de persistencia JSON
- [x] Carga de partida guardada
- [x] Guardado de partida
- [x] Menú de misiones (5 opciones)
- [x] Tests comprehensivos (22 tests, 100% pass)
- [x] Item purchase auto-tracking en store.py (FIX COMPLETADO 12/02/2026)

**✅ Completitud:** 9/9 (100%) - FASE 2.1 COMPLETADA

**Fix aplicado (12/02/2026):**
- Integrada llamada a `evento_items_comprados()` en `menu_armeria()`
- Ambas misiones de items ("Equipero" + "Coleccionista") se completan automáticamente
- Test de verificación: `tests/test_fix_items_misiones.py` - ✅ 100% PASADO

### ✅ Checklist Fase 2.2 - Habilidades Especiales
- [x] 25 habilidades en 5 arquetipos
- [x] 6 tipos de triggers automáticos
- [x] Output visual de habilidades
- [x] Persistencia de habilidades
- [x] Integración en combate
- [x] Tests completos (100% pass)

**✅ Completitud:** 10/10 (100%)

### ✅ Checklist Fase 2.3 - Sistema de Gladiadores + UI Mejorada
- [x] Sistema de ocupación (días/razón)
- [x] Métodos de entrenamiento
- [x] Métodos de curación
- [x] Menú de gestión equipo (6 opciones)
- [x] Sistema de estados (sano/herido/crítico/muerto)
- [x] Expansión de barracas
- [x] Hospital con revivir
- [x] Validación puede_luchar()
- [x] **MEJORAS UI:**
  - [x] Barra de Progreso de Ocupación
  - [x] Indicador Visual de Entrenamiento
  - [x] Resumen de Cambios Post-Entrenamiento
  - [x] Animación ASCII de Mejora
  - [x] Estadísticas del Gladiador

**✅ Completitud:** 13/13 (100%)

### ✅ Checklist Fase 2.4 - Arenas con Dificultad + UI Mejorada
- [x] 4 niveles de arena (Novato/Normal/Experto/Legendaria)
- [x] Requisitos de nivel por dificultad
- [x] Escalado de nivel de enemigos (-2, +0, +3, +5)
- [x] Escalado de stats de enemigos (multiplicador)
- [x] Recompensas variables (x0.8 a x2.0)
- [x] Menú visual con emojis
- [x] Warning de riesgo
- [x] Validación de requisitos
- [x] Integración en combate
- [x] Sistema de ligas (bonus)
- [x] **MEJORAS UI:**
  - [x] Análisis de Riesgo Pre-Combate
  - [x] Histórico de Últimos Combates
  - [x] Estimador de Recompensas
  - [x] Badges/Logros Desbloqueables
  - [x] Selector Visual Mejorado

**✅ Completitud:** 15/15 (100%)

**📊 Progreso Fase 2:** 10/10 (2.1: 100% ✅ | 2.2: 100% | 2.3: 100% | 2.4: 100%)

**📊 Resultado FINAL:** Juego pasa de 8.0/10 → **8.8/10** ⬆️ +0.8 (FIX COMPLETADA: 9.0/10+)

---

### ⏳ Próximas Tareas - FASE 3

## 📅 FASE 3: PROFUNDIDAD (Semana 4-5)
**⏱️ Duración:** 10-12 horas | **🟢 Prioridad:** MEJORAS | **⭐ Impacto:** 4/5

### 🎯 Objetivo
Agregar sistemas avanzados para jugadores experimentados.

### Tareas

#### ✅ 3.1 Árbol de Talentos (4 horas)
**Archivo nuevo:** `src/talents.py`

**Sistema:**
- 1 punto de talento por nivel
- 4 ramas: Fuerza / Resistencia / Agilidad / Técnica
- 5 niveles por rama (máx 25 puntos)

**Talentos:**
```
FUERZA:
  Nivel 1: +5 ATK
  Nivel 2: +10 ATK
  Nivel 3: +15 ATK, +5% crítico
  Nivel 4: +20 ATK, +10% crítico
  Nivel 5: +30 ATK, +15% crítico, Habilidad "Golpe Devastador"

RESISTENCIA:
  Nivel 1-5: Similar con HP/DEF

AGILIDAD:
  Nivel 1-5: Similar con SPD/evasión

TÉCNICA:
  Nivel 1-5: Similar con XP bonus/mejor loot
```

**UI:** Menú de talentos con árbol visual en ASCII

---

#### ✅ 3.2 Mejora de Items (3 horas)
**Archivo nuevo:** `src/forge.py`

**Herrería/Forja:**
- Mejorar armas: +5 ATK por nivel (máx +5 niveles)
- Mejorar armaduras: +3 DEF, +10 HP por nivel
- Costo incremental: base_precio * nivel²
- Materiales opcionales (futuro)

**Formato:**
```
Espada Gladius +3
  ATK: 20 → 35 (+15)
  Valor: 200g → 600g
```

---

#### ✅ 3.3 Eventos Aleatorios (3 horas)
**Archivo nuevo:** `src/events.py`

**10 Eventos posibles:**
1. Mercader ambulante (items al 70%)
2. Gladiador herido (recluta gratis, HP bajo)
3. Apuesta clandestina (duplica o pierde dinero)
4. Torneo sorpresa (3 combates, triple recompensa)
5. Enfermedad (gladiador -20% stats 3 días)
6. Entrenador legendario (+stats gratis)
7. Sabotaje (enemigo con +stats)
8. Regalo de los dioses (item legendario gratis)
9. Deuda de juego (-dinero o combate forzado)
10. Festival romano (+XP por 5 combates)

**Probabilidad:** 10% cada vez que vuelves al menú

---

#### ✅ 3.4 Leaderboards (2 horas)
**Archivo nuevo:** `src/leaderboards.py`

**3 Tablas:**
1. Top 10 por Victorias
2. Top 10 por Dinero acumulado
3. Top 10 por Nivel máximo

**Persistencia:** JSON global compartido entre usuarios

**UI:** Menú "Rankings" con tabla formateada

---

### ✅ Checklist Fase 3
- [ ] Árbol de talentos (25 puntos)
- [ ] Sistema de mejora de items
- [ ] 10 eventos aleatorios
- [ ] 3 leaderboards funcionales
- [ ] Persistencia global

**📊 Resultado:** Juego pasa de 8.5/10 → **9/10**

---

## 📅 FASE 4: PULIDO FINAL (Semana 6+)
**⏱️ Duración:** 15-20 horas | **🔵 Prioridad:** FUTURO | **⭐ Impacto:** 3/5

### 🎯 Objetivo
Convertir el juego en una experiencia premium pulida.

### Tareas

#### ✅ 4.1 Interfaz Gráfica con Pygame (12 horas)
**Migración completa a ventana gráfica:**
- Sprites de gladiadores
- Animaciones de combate
- Botones y menús visuales
- Barras de HP/XP animadas
- Efectos de partículas

---

#### ✅ 4.2 Sistema de Música (2 horas)
**4 Tracks:**
- Menú principal (épica)
- Combate (intensa)
- Victoria (triunfal)
- Derrota (sombría)

---

#### ✅ 4.3 Casa/Base Mejorable (3 horas)
**5 Mejoras:**
1. Gimnasio (+5% stats entrenamiento)
2. Enfermería (-50% costo curación)
3. Biblioteca (+10% XP combates)
4. Estatua (prestigio, mejor loot)
5. Arena privada (entrena sin riesgo)

---

#### ✅ 4.4 Modo Historia (4 horas)
**10 Capítulos con narrativa:**
- Tutorial integrado
- Jefes únicos
- Recompensas exclusivas
- Cinematics en texto

---

### ✅ Checklist Fase 4
- [ ] UI gráfica completa
- [ ] 4 tracks de música
- [ ] 5 mejoras de base
- [ ] 10 capítulos historia
- [ ] Sprites y animaciones

**📊 Resultado:** Juego pasa de 9/10 → **9.5/10** (Casi comercial)

---

## 📊 RESUMEN EJECUTIVO

| Fase | Tiempo | Calidad Resultante | Prioridad |
|------|--------|-------------------|-----------|
| Fase 1 | 3-4h | 7.5/10 | 🔴 CRÍTICA |
| Fase 2 | 8-10h | 8.5/10 | 🟡 ALTA |
| Fase 3 | 10-12h | 9.0/10 | 🟢 MEDIA |
| Fase 4 | 15-20h | 9.5/10 | 🔵 BAJA |

**Total:** 36-46 horas de desarrollo

---

## 🎯 RECOMENDACIÓN

**Empieza con FASE 1 COMPLETA (4 horas)**

En un fin de semana tendrás:
- 26 items vs 6 actuales
- Sistema de pociones
- Economía funcional (vender)
- UI mejorada

**Resultado:** Un juego 2.5x más divertido

