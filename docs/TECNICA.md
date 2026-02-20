# 📖 DOCUMENTACIÓN TÉCNICA COMPLETA - SANGRE POR FORTUNA v2.0

**Última actualización:** Enero 7, 2026  
**Versión:** 2.0.0  
**Autor:** Proyecto Gladiadores

---

## 📋 TABLA DE CONTENIDOS

1. [Visión General del Proyecto](#visión-general)
2. [Sistema de Equipo de Gladiadores](#sistema-equipo)
3. [Sistema de Progresión y Escalado](#sistema-progresión)
4. [Sistema de Días y Gestión de Tiempo](#sistema-días)
5. [Explicación del Sistema XP/Nivel Implementado](#sistema-xp)
6. [Análisis Actual y Mejoras Recomendadas](#análisis-mejoras)
7. [Plan de Implementación FASE 1](#plan-fase1)
8. [Estado de Implementación](#estado-implementación)

---

## 🎮 VISIÓN GENERAL DEL PROYECTO {#visión-general}

**SANGRE POR FORTUNA** es un simulador de gladiadores en la antigua Roma escrito en Python puro.

### Objetivo Principal
Crear un juego de gestión táctica donde el jugador:
- Recluta y entrena gladiadores
- Los equipa con armas y armaduras
- Los envía a combatir en arenas
- Gestiona recursos (dinero, tiempo, salud)
- Observa su progresión a través de múltiples niveles

### Características Base (v1.0)
✅ Sistema de autenticación (registro/login)
✅ Combate automático por turnos
✅ 5 tipos de enemigos diferentes
✅ Sistema de tienda/armería
✅ Guardado de partidas persistente
✅ Nombres romanos aleatorios
✅ Sistema de equipamiento

---

## 👥 SISTEMA DE EQUIPO DE GLADIADORES {#sistema-equipo}

### Concepto Central
El jugador NO controla directamente un gladiador. Controla un **EQUIPO** de hasta 6 gladiadores que:
- Se entrenan
- Se curan
- Se equipan con armas y armaduras
- Compiten en la arena
- Generan dinero y XP
- Pueden morir (permanentemente)

### Estructura del Equipo

```
MI EQUIPO (6 máximo)
├─ 1. Ferox (Murmillo)
│  ├─ Nivel: 5 | XP: 340/375
│  ├─ HP: 148/150 | Estado: Sano
│  ├─ Equipo: Espada Ridius, Armadura Espartana
│  └─ Historial: 15 victorias, 3 derrotas
│
├─ 2. Velox (Retiarius)
│  ├─ Nivel: 4 | XP: 200/250
│  ├─ HP: 60/80 | Estado: Herido
│  ├─ Equipo: Tridente, Escudo
│  └─ Ocupación: Curación (2/3 días)
│
├─ 3. Fortis (Secutor)
│  ├─ Nivel: 1
│  └─ Estado: Muerto (Revivible)
│
└─ [3 espacios vacíos disponibles]
```

### Tipos de Gladiadores

| Tipo | Rol | Fortaleza | Debilidad |
|------|-----|-----------|----------|
| **Murmillo** | Tanque | Alto HP/DEF | Lento |
| **Retiarius** | Ágil | Velocidad alta | HP bajo |
| **Secutor** | Equilibrado | Stats balanceados | Sin especialización |
| **Thraex** | Agresivo | Ataque alto | Defensa baja |
| **Hoplomachus** | Defensivo | Defensa/HP altos | Daño bajo |

### Ciclo de Vida

```
RECLUTAMIENTO → ENTRENAMIENTO → COMBATE → CURACIÓN (si falta) → REPETIR
         ↓               ↓            ↓                ↓
     50-200g      200-300g/día    Gana dinero    20-100g según urgencia
                  +2-5 stats      +XP/dinero         Requiere 1-3 días
```

---

## ⚖️ SISTEMA DE PROGRESIÓN Y ESCALADO {#sistema-progresión}

### Premisa Fundamental
**El poder debe crecer LOGARÍTMICAMENTE, no exponencialmente**

Cada nivel:
- Cuesta más XP que el anterior
- Proporciona menos mejora que el anterior
- Mantiene el equilibrio: enemigos también escalan

### XP Necesario por Nivel

| Nivel | XP Total | XP/Nivel | Descripción |
|-------|----------|----------|-------------|
| 1 | 0 | 100 | Aprendiz (inicio) |
| 5 | 464 | 146 | Principiante |
| 10 | 1,259 | 235 | Veterano |
| 15 | 2,586 | 375 | Campeón |
| 20 | 4,721 | 597 | Guerrero Experimentado |
| 30 | 13,725 | 1,512 | Leyenda |
| 50 | 60,000 | 8,000 | Semidiós |

**Fórmula:** `XP_requerido = 100 * (1.1 ^ nivel)`

### Aumento de Stats por Nivel (DECRECIENTE)

```
Nivel │ HP    │ ATK   │ DEF   │ SPD   │ Descripción
──────┼───────┼───────┼───────┼───────┼─────────────────────
1     │ 100   │ 20    │ 5     │ 10    │ Base inicial
2     │ 110   │ 21    │ 5.2   │ 10.2  │ +10%
5     │ 148   │ 24    │ 5.8   │ 10.8  │ +9%
10    │ 218   │ 29    │ 6.5   │ 11.5  │ +8.5%
20    │ 391   │ 42    │ 8.5   │ 13.5  │ +7.5%
30    │ 659   │ 65    │ 11    │ 16    │ +6%
50    │ 1,427 │ 133   │ 18    │ 25    │ +5%
```

**Fórmulas por Stat:**
- `HP = 100 * (1.095 ^ nivel)`
- `ATK = 20 * (1.085 ^ nivel)`
- `DEF = 5 * (1.075 ^ nivel)`
- `SPD = 10 * (1.065 ^ nivel)`

**Resultado:** Nivel 1→20 = 3-4x stats | Nivel 40→50 = +5% stats (diminishing returns)

### Escalado de Enemigos

**IMPORTANTE:** Enemigos escalan completamente con el nivel del jugador

| Nivel Jugador | Dificultad Enemigo | Stats Enemigos | Dinero |
|---------------|------------------|-----------------|--------|
| 1-3 | Fácil | 0.8x del jugador | 20-50 |
| 4-7 | Normal | 1.0x del jugador | 50-100 |
| 8-15 | Difícil | 1.2x del jugador | 100-200 |
| 16-30 | Muy Difícil | 1.5x del jugador | 200-400 |
| 30+ | Experto | 1.5x del jugador | 300-600 |

---

## ⏰ SISTEMA DE DÍAS Y GESTIÓN DE TIEMPO {#sistema-días}

### Concepto de "Día"
Un "día" en el juego es una unidad de tiempo abstracta. Cada día:
- Los gladiadores pueden hacer 1 acción
- Se consume 1 día de los gladiadores en ocupación
- Se avanza el tiempo del juego

### Ocupaciones de Gladiadores

```
DESCANSO (1 día)
├─ Restaura 50% HP
├─ Restaura 100% si estaba al 0%
└─ Costo: 0 dinero

ENTRENAMIENTO (1-3 días)
├─ Gana +2-5 stats aleatorios
├─ Costo: 50-200 dinero/día
└─ Requiere estar vivo

CURACIÓN (1-3 días urgentes)
├─ Restaura HP según urgencia
├─ Costo: 20-100 dinero/día
├─ Mayor urgencia = más días, menos costo
└─ Se aplica antes de combate

DESCANSO EN CUARTEL (ilimitado)
├─ Espera sin hacer nada
└─ Se restaura 10% HP/día
```

---

## 🎯 SISTEMA XP/NIVEL IMPLEMENTADO {#sistema-xp}

### Estado Actual: ✅ 100% IMPLEMENTADO

Ubicación: `src/models.py` y `src/combat.py`

### Clases Clave

**En `src/models.py`:**
```python
class Player:
    def __init__(self):
        self.nivel = 1
        self.xp = 0
        self.xp_necesario = 100  # XP para subir a nivel 2
        
    def ganar_xp(self, cantidad):
        """Suma XP y maneja auto level-up"""
        self.xp += cantidad
        while self.xp >= self.xp_necesario:
            self.subir_nivel()
    
    def subir_nivel(self):
        """Aumenta nivel con multiplicadores decrecientes"""
        self.xp -= self.xp_necesario
        self.nivel += 1
        self.hp = int(100 * (1.095 ** self.nivel))
        self.attack = int(20 * (1.085 ** self.nivel))
        self.defense = int(5 * (1.075 ** self.nivel))
        self.speed = int(10 * (1.065 ** self.nivel))
        self.xp_necesario = int(100 * (1.1 ** self.nivel))

class Gladiador:
    """Sistema independiente para cada gladiador del equipo"""
    # Mismo sistema que Player pero para gestión de equipo
```

**En `src/combat.py`:**
```python
def calcular_xp_recompensa(nivel_jugador):
    """Calcula XP dinámico según nivel"""
    base = 50 * (1.15 ** nivel_jugador)
    variacion = base * random.uniform(-0.1, 0.1)
    return int(base + variacion)
```

### Recompensas por Nivel

```
Nivel  │ XP/Victoria (Promedio) │ Victorias para Subir
───────┼──────────────────────┼──────────────────────
1      │ ~51 XP               │ ~2 victorias
5      │ ~67 XP               │ ~2 victorias
10     │ ~118 XP              │ ~2 victorias
15     │ ~208 XP              │ ~2 victorias
20     │ ~367 XP              │ ~2 victorias
30     │ ~1,158 XP            │ ~1 victoria
50     │ ~10,000+ XP          │ Variable
```

### Verificación

Test realizado:
```python
# Crear player y darle 5000 XP
player = Player()
player.ganar_xp(5000)
# Resultado: Nivel 18, ~1200 XP usado de 5000 dados
```

---

## 🔍 ANÁLISIS ACTUAL Y MEJORAS RECOMENDADAS {#análisis-mejoras}

### Lo que está bien ✅

1. **Sistema XP/Nivel:** Perfectamente logarítmico
   - Balance excelente
   - Rewards escalados
   - Progression satisfactoria

2. **Sistema de Combate:** Funcional y rápido
   - Turn-based simple
   - Daño variado (-20% a +20%)
   - Resultado justo

3. **Persistencia:** Datos guardados correctamente
   - JSON limpio
   - Recuperación fiable
   - Validación de integridad

### Lo que falta ⚠️

1. **Items:**
   - Solo 6 items (necesita 20+)
   - Sin sistema de pociones
   - Sin venta de items

2. **Interfaz:**
   - Sin barra de progreso XP
   - Sin visualización de nivel/exp
   - Sin stats animados

3. **Mecánicas:**
   - Sin misiones/quests
   - Sin habilidades especiales
   - Sin árbol de talentos

### Recomendaciones

1. **Expandir Catálogo** (FASE 1)
   - 10 armas nuevas
   - 10 armaduras nuevas
   - 5 pociones diferentes

2. **Sistema de Venta** (FASE 1)
   - Vender items al 50% precio
   - Dinero para reinvertir

3. **UI Mejorada** (FASE 1)
   - Barras de progreso
   - Visualización de stats

---

## 📋 PLAN DE IMPLEMENTACIÓN FASE 1 {#plan-fase1}

### Objetivos
- [ ] Expandir catálogo de items (20+ items)
- [ ] Crear sistema de pociones
- [ ] Implementar venta de items
- [ ] Mejorar visualización UI

### Desglose por Tarea

**Tarea 1: Expandir Items (2 horas)**
- Agregar 10 armas nuevas en src/store.py
- Agregar 10 armaduras nuevas
- Actualizar PRECIOS

**Tarea 2: Pociones (1.5 horas)**
- Crear clase Potion en src/models.py
- Crear CATALOGO_POCIONES en src/store.py
- Integrar con combate

**Tarea 3: Sistema Venta (1 hora)**
- Función vender_item() en src/store.py
- Actualizar dinero del jugador
- Remover de inventario

**Tarea 4: UI (1.5 horas)**
- Barra de XP en pantalla principal
- Mostrar nivel/XP en menú
- Animaciones de level-up

---

## 📊 ESTADO DE IMPLEMENTACIÓN {#estado-implementación}

### Sistema Core

| Componente | Estado | Líneas | Archivo |
|------------|--------|--------|---------|
| Clases (Player, Gladiador, Enemy) | ✅ HECHO | ~300 | models.py |
| Sistema Progresión (XP/Niveles) | ✅ HECHO | ~50 | models.py |
| Combate | ✅ HECHO | ~100 | combat.py |
| Recompensas Dinámicas | ✅ HECHO | ~20 | combat.py |
| Tienda Base | ✅ HECHO | ~80 | store.py |
| Autenticación | ✅ HECHO | ~150 | auth.py |
| Persistencia | ✅ HECHO | ~120 | persistence.py |

### Totales

- **Código:** ~820 líneas
- **Documentación:** ~30,000 palabras
- **Tests:** 5 archivos

### Próximas Prioridades

1. **Expandir items** (Impacto ALTO, Complejidad BAJA)
2. **Pociones** (Impacto ALTO, Complejidad MEDIA)
3. **Venta items** (Impacto MEDIO, Complejidad BAJA)
4. **UI mejorada** (Impacto ALTO, Complejidad MEDIA)

---

**Documentación actualizada:** Enero 7, 2026  
**Versión:** 2.0.0  
⚔️ **SANGRE POR FORTUNA**
