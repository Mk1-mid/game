# 🎮 FUNCIONALIDADES Y SISTEMAS

**v3.0 - Fase 3 (El Alma del Juego)**

---

## 📑 Índice de Sistemas

1. [🎭 Arquetipos (5 tipos)](#arquetipos)
2. [⚔️ Habilidades (25 total)](#habilidades)
3. [✨ Efectos de Estado](#efectos-de-estado)
4. [🎬 Eventos Narrativos (12)](#eventos)
5. [💰 Sistema de Progresión](#progresion)
6. [⭐ Sistema de Fama](#fama)
7. [🎖️ Misiones y Logros](#misiones)
8. [🛡️ Sistema de Equipo](#equipo)

---

## 🎭 ARQUETIPOS

### Descripción General

Cada gladiador tiene un **Arquetipo** que define su fortaleza en combate:

| Arquetipo | Gladiador Romano | Fortaleza | Estadística Principal | Recomendado Para |
|-----------|---|---|---|---|
| ⚔️ **Guerrero** | Murmillo | +14% FUERZA | Daño raw máximo | Agresivos |
| 🏃 **Velocista** | Retiarius | +15% AGILIDAD | Esquiva máxima | Defensivos ágiles |
| 🗡️ **Asesino** | Thraex | +26% CRÍTICO | Daño crítico máximo | Riesgo-recompensa |
| 🛡️ **Tanque** | Hoplomachus | +23% DEFENSA | Defensa máxima | Resistencia pura |
| ⚖️ **Paladín** | Secutor | +12% FUERZA +15% DEFENSA | Balance híbrido | Principiantes |

### Estadísticas Detalladas

#### 1️⃣ GUERRERO (Murmillo)
```
📊 BONIFICADORES
├─ Fuerza:     +14% (MÁXIMO)
├─ Agilidad:   +3%
├─ Defensa:    +8%
├─ Crítico:    +10%
├─ Esquiva:    +2%
└─ HP Máximo:  +0%
______________
   TOTAL:      +37%
```

**Fortalezas:**
- ⚔️ Daño raw más alto
- 💪 Mejor en combates directos
- 🎯 Consistente y predecible

**Debilidades:**
- 🛡️ Defensa media
- ⏱️ Agilidad baja

**Recomendación:** Atacantes puros

---

#### 2️⃣ VELOCISTA (Retiarius)
```
📊 BONIFICADORES
├─ Fuerza:     +5%
├─ Agilidad:   +15% (MÁXIMO)
├─ Defensa:    +3%
├─ Crítico:    +12%
├─ Esquiva:    +8%
└─ HP Máximo:  +0%
______________
   TOTAL:      +43%
```

**Fortalezas:**
- 🏃 Esquivas múltiples
- ⚡ Rápido y versátil
- 🎪 Combates de larga duración

**Debilidades:**
- ⚔️ Daño bajo
- 🎯 Menos predecible

**Recomendación:** Defensivos ágiles

---

#### 3️⃣ ASESINO (Thraex)
```
📊 BONIFICADORES
├─ Fuerza:     +5%
├─ Agilidad:   +5%
├─ Defensa:    +1%
├─ Crítico:    +26% (¡MÁXIMO ABSOLUTO!)
├─ Esquiva:    +10%
└─ HP Máximo:  +0%
______________
   TOTAL:      +47% 🔥
```

**Fortalezas:**
- 💥 Críticos devastadores
- 🎲 Daño variable (muy alto)
- ⚡ Rápido y esquivador

**Debilidades:**
- 🛡️ Defensa crítica (frágil)
- ❌ Bajo HP
- 🎲 Impredecible (suerte-dependiente)

**Recomendación:** Riesgo alto-recompensa alta

---

#### 4️⃣ TANQUE (Hoplomachus)
```
📊 BONIFICADORES
├─ Fuerza:     +2%
├─ Agilidad:   +4%
├─ Defensa:    +23% (MÁXIMO)
├─ Crítico:    +7%
├─ Esquiva:    +5%
└─ HP Máximo:  +10% ⭐
______________
   TOTAL:      +51% 🛡️
```

**Fortalezas:**
- 🛡️ Defensa suprema
- 💪 HP más alto
- 🎪 Ultrarresistente

**Debilidades:**
- ⚔️ Daño muy bajo
- ⏱️ Muy lento

**Recomendación:** Resistencia pura

---

#### 5️⃣ PALADÍN (Secutor)
```
📊 BONIFICADORES
├─ Fuerza:     +12%
├─ Agilidad:   +5%
├─ Defensa:    +15%
├─ Crítico:    +10%
├─ Esquiva:    +2%
└─ HP Máximo:  +0%
______________
   TOTAL:      +44%
```

**Fortalezas:**
- ⚖️ Balance perfecto
- 🎯 Versátil
- 📈 Mejor para principiantes

**Debilidades:**
- ❌ Sin especialidad extrema
- 🔄 Mediocre en todo

**Recomendación:** Principiantes / Versátiles

---

### Matriz de Enfrentamientos

```
          VSS   Guerrero  Velocista  Asesino  Tanque  Paladín
Guerrero   -      IGUAL    PIERDE   PIERDE   PIERDE  PIERDE
Velocista  GANA    -       IGUAL    PIERDE   IGUAL   IGUAL
Asesino    GANA   IGUAL     -       IGUAL    PIERDE  GANA
Tanque     GANA   IGUAL    IGUAL    GANA      -      GANA
Paladín    GANA   GANA     IGUAL    PIERDE   PIERDE   -
```

---

## ⚔️ HABILIDADES

### Sistema de Habilidades

**Estructura:**
```
Habilidad
├─ nombre: str
├─ descripcion: str
├─ tipo: "pasiva" | "activa"
├─ arquetipo: str
├─ trigger: TipoTrigger (si activa)
├─ bonificadores: dict
│   ├─ "ataque": int
│   ├─ "defensa": int
│   ├─ "agilidad": int
│   └─ ...
└─ duracion_bonus: int (turnos)
```

---

### 25 Habilidades Totales

#### ⚔️ GUERRERO (Murmillo)

| # | Nombre | Tipo | Trigger | Efecto | Duración |
|---|--------|------|---------|--------|----------|
| 1 | **Fuerza Bruta** | Pasiva | - | +14% FUERZA | Permanente |
| 2 | **Contraataque** | Activa | Daño Recibido | +8% ATK por 3t | 3 turnos |
| 3 | **Golpe Definitivo** | Activa | 2+ Críticos dados | +20% DMG crítico | 2 turnos |
| 4 | **Resistencia Muscular** | Pasiva | - | +8% DEFENSA | Permanente |
| 5 | **Furia Guerrera** | Activa | Salud < 30% | +25% ATK | 4 turnos |

#### 🏃 VELOCISTA (Retiarius)

| # | Nombre | Tipo | Trigger | Efecto | Duración |
|---|--------|------|---------|--------|----------|
| 1 | **Agilidad Suprema** | Pasiva | - | +15% AGILIDAD | Permanente |
| 2 | **Esquiva en Cadena** | Activa | 3+ Esquivas rend. | +10% DEF por 3t | 3 turnos |
| 3 | **Danza del Combate** | Activa | Turnos pares | +15% ESQUIVA | 2 turnos |
| 4 | **Reflejos** | Pasiva | - | +8% ESQUIVA contra críticos | Permanente |
| 5 | **Velocidad Extrema** | Activa | Sin daño 2 turnos | +30% AGILIDAD | 5 turnos |

#### 🗡️ ASESINO (Thraex)

| # | Nombre | Tipo | Trigger | Efecto | Duración |
|---|--------|------|---------|--------|----------|
| 1 | **Toque Mortal** | Pasiva | - | +26% CRÍTICO | Permanente |
| 2 | **Ejecución** | Activa | 2+ Críticos recibidos | +40% DMG vs salud baja | 3 turnos |
| 3 | **Veneno Mental** | Activa | Ataque fallido | -10% DEF enemigo | 4 turnos |
| 4 | **Destreza Letal** | Pasiva | - | +10% ESQUIVA | Permanente |
| 5 | **Golpe Sorpresa** | Activa | Turno impar | +35% CRÍTICO | 2 turnos |

#### 🛡️ TANQUE (Hoplomachus)

| # | Nombre | Tipo | Trigger | Efecto | Duración |
|---|--------|------|---------|--------|----------|
| 1 | **Defensa Absoluta** | Pasiva | - | +23% DEFENSA | Permanente |
| 2 | **Escudo Reflectante** | Activa | Daño > 50 dmg | Refleja 25% daño | 2 turnos |
| 3 | **Resistencia Férrea** | Activa | Daño recibido x3 | -15% DMG recibido | 5 turnos |
| 4 | **Cuerpo de Piedra** | Pasiva | - | +10% HP Máximo | Permanente |
| 5 | **Fortaleza Inquebrantable** | Activa | Salud < 50% | +50% DEFENSA | 4 turnos |

#### ⚖️ PALADÍN (Secutor)

| # | Nombre | Tipo | Trigger | Efecto | Duración |
|---|--------|------|---------|--------|----------|
| 1 | **Balance Perfecto** | Pasiva | - | +12% FUERZA + +15% DEFENSA | Permanente |
| 2 | **Escudo Justiciero** | Activa | Daño Recibido | +12% DEF + -10% DMG recibido | 3 turnos |
| 3 | **Luz Divina** | Activa | Salud < 50% | Cura 20% HP | Instantáneo |
| 4 | **Equilibrio Táctico** | Pasiva | - | +5% ATK y DEF todos combates | Permanente |
| 5 | **Retribución** | Activa | 2+ Críticos recibidos | Siguiente ataque +50% DMG | 2 turnos |

---

### Sistema de Triggers (6 tipos)

Las habilidades activas se disparan automáticamente cuando ocurre un evento:

#### 1️⃣ SALUD_BAJO
- **Condición:** Salud < 30%
- **Habilidades activadas:** Furia Guerrera, Fortaleza Inquebrantable, Luz Divina
- **Efecto típico:** Buff defensivo o curativo

#### 2️⃣ ESQUIVAS_CONSECUTIVAS
- **Condición:** 3+ esquivas seguidas
- **Habilidades activadas:** Esquiva en Cadena, Danza del Combate
- **Efecto típico:** Buff adicional de esquiva

#### 3️⃣ CRÍTICOS_RECIBIDOS
- **Condición:** Recibe 2+ críticos
- **Habilidades activadas:** Ejecución, Retribución
- **Efecto típico:** Counterattack o buff ofensivo

#### 4️⃣ CRÍTICOS_PROPIOS
- **Condición:** Da 2+ críticos
- **Habilidades activadas:** Golpe Definitivo, Golpe Sorpresa
- **Efecto típico:** Buff de daño crítico adicional

#### 5️⃣ DAÑO_RECIBIDO
- **Condición:** Recibe daño > 50 en un turno
- **Habilidades activadas:** Contraataque, Escudo Reflectante
- **Efecto típico:** Reflejo o contraataque

#### 6️⃣ TURNOS_COMBATE
- **Condición:** Cada X turnos (1, 2, 3, etc.)
- **Habilidades activadas:** Danza del Combate (turnos pares)
- **Efecto típico:** Buff periódico

---

## ✨ EFECTOS DE ESTADO

### Estados Permanentes de Gladiador

```python
class Estado(Enum):
    SANO = "sano"           # Normal
    HERIDO = "herido"       # -20% DEF (rojo visual)
    CRÍTICO = "crítico"     # -40% DEF (rojo oscuro)
    MUERTO = "muerto"       # Fuera de combate
```

### Efectos Temporales (Activos)

Pueden aplicarse por habilidades o eventos narrativos:

| Efecto | Duración | Impacto | Ejemplo |
|--------|----------|---------|---------|
| **🔴 Veneno** | 4 turnos | -10% ATK, -5% DEF | Habilidad Asesino |
| **⚡ Adrenalina** | 3 turnos | +15% ATK, +10% AGILIDAD | Evento Narrativo |
| **❄️ Congelación** | 2 turnos | -20% AGILIDAD, -10% ESQUIVA | Efecto desconocido |
| **🔥 Inflamación** | 3 turnos | +20% Daño CRÍTICO | Combate especial |
| **💚 Regeneración** | 5 turnos | +5% HP por turno | Habilidad Paladín |
| **🛡️ Armadura Extra** | 2 turnos | +30% DEFENSA | Habilidad Tanque |
| **👻 Ceguera** | 3 turnos | -25% CRÍTICO, -15% ATAQUE | Desconocido |

---

## 🎬 EVENTOS NARRATIVOS

Fase 3 introduce **12 eventos** que ocurren aleatoriamente al pasar días:

### Generador de Eventos

**Función:** `GestorNarrativa.intentar_disparar_evento(equipo)`

**Probabilidad base:** 30% cada día

**Factores que afectan:**
- 📈 Fama (+ fama = + probabilidad de eventos positivos)
- 💰 Dinero (poco dinero = problemas económicos)
- ⚔️ Racha de victorias (+ victorias = + eventos)

### 12 Eventos Implementados

#### 1️⃣ 🎪 FESTIVAL DE GLADIADORES
- **Tipo:** Positivo (80% de probabilidad)
- **Condición:** Fama > 500
- **Opciones:**
  - Participar → +250g, +100 XP / gladiador
  - Descansar → +200 XP / gladiador
- **Consecuencia:** Evento de reputación

#### 2️⃣ ⚔️ REBELIÓN DE GLADIADORES
- **Tipo:** Negativo
- **Condición:** Dinero bajo + muchos días parados
- **Opciones:**
  - Pagar bonificación → -500g, -Rebelión
  - Ignorar → -Fama, -1 gladiador
- **Consecuencia:** Económica / Pérdida de gladiador

#### 3️⃣ 💼 PATROCINIO DE NOBLE
- **Tipo:** Positivo
- **Condición:** Fama > 1000 + Racha victorias
- **Opciones:**
  - Aceptar → +1000g, +Fama
  - Rechazar → -Fama pero +200g
- **Consecuencia:** Oro + Fama

#### 4️⃣ 👮 INSPECCIÓN DE ROMA
- **Tipo:** Neutral / Negativo
- **Condición:** (Random)
- **Opciones:**
  - Prepararse bien → -200g, +Reputación
  - Esconder defectos → Riesgo -500g
- **Consecuencia:** Económica

#### 5️⃣ ⚔️ MERCENARIO RIVAL
- **Tipo:** Combate especial
- **Condición:** Fama > 2000
- **Opciones:**
  - Aceptar desafío → Combate vs mercenario fuerte
  - Rechazar → -250 Fama
- **Consecuencia:** Combate o Reputación

#### 6️⃣ 🤒 ENFERMEDAD EN LUDUS
- **Tipo:** Negativo
- **Condición:** (Random)
- **Opciones:**
  - Llamar médico → -300g, Curación rápida
  - Remedios caseros → Curación lenta
- **Consecuencia:** Salud + Económica

#### 7️⃣ 🦅 CAZA FURTIVA DE ESCLAVOS
- **Tipo:** Negativo crítico
- **Condición:** Ludus desprotegido
- **Opciones:**
  - Perseguirlos → 50% éxito
  - Negociar → Pérdida segura
- **Consecuencia:** Pérdida de gladiador

#### 8️⃣ 🤝 AMISTOSO DEPORTIVO
- **Tipo:** Positivo
- **Condición:** Fama > 500 + Dinero > 1000g
- **Opciones:**
  - Participar → +200 XP + +150g
  - Entrenar → +300 XP
- **Consecuencia:** Experiencia + Oro

#### 9️⃣ 🔪 TRAICIÓN DEL GERENTE
- **Tipo:** Negativo
- **Condición:** Dinero bajo + Días sin ganar
- **Opciones:**
  - Pagar silencio → -1000g
  - Descubrirlo → Pierdes gerente pero +Fama
- **Consecuencia:** Económica / Fama

#### 🔟 📝 VISITA DE CRÍTICOS
- **Tipo:** Neutral
- **Condición:** Fama > 1000
- **Opciones:**
  - Impresionarlos → +500 Fama
  - Nada especial → +100 Fama
- **Consecuencia:** Reputación

#### 1️⃣1️⃣ 🗡️ CONSPIRACIÓN POLÍTICA
- **Tipo:** Negativo
- **Condición:** Fama > 2000
- **Opciones:**
  - Involucrarse → Riesgo alto (-500g) pero +1000 Fama
  - Neutral → -200 Fama
- **Consecuencia:** Fama

#### 1️⃣2️⃣ 💭 SUEÑO DE RETIRO
- **Tipo:** Positivo / Existencial
- **Condición:** Cualquier momento
- **Opciones:**
  - Continuar → +Motivación
  - Retirarse → FIN DEL JUEGO
- **Consecuencia:** Narrativa

---

## 💰 SISTEMA DE PROGRESIÓN

### XP y Nivel

```
Nivel: 1-50+

Fórmula XP necesaria para subir:
next_xp = 100 * nivel^1.5

Ejemplo:
├─ Nivel 1 → Nivel 2: 100 XP
├─ Nivel 5 → Nivel 6: 1118 XP
├─ Nivel 10 → Nivel 11: 3162 XP
└─ Nivel 20 → Nivel 21: 8944 XP
```

### Ganancia de XP por Combate

```
Base = 50 XP

Multiplicadores:
├─ Diferencia de nivel (gladiador vs enemigo)
│  ├─ Enemigo es 5+ niveles superior: ×1.5
│  ├─ Enemigo es igual: ×1.0
│  └─ Enemigo es 10+ inferior: ×0.5
├─ Resultado del combate
│  ├─ Victoria: ×1.0
│  ├─ Derrota: ×0.25
│  └─ Fuga: ×0.1
└─ Bonificadores activos
   ├─ Evento booster: ×1.2
   └─ Racha de victorias: ×(1 + racha*0.1)
```

### Stat Progression

```
Por nivel (ejemplo Guerrero):
├─ HP Máximo: +3 por nivel
├─ Ataque: +1.5 por nivel
├─ Defensa: +1 por nivel
├─ Agilidad: +0.5 por nivel
└─ Crítico: +0.2 por nivel
```

---

## ⭐ SISTEMA DE FAMA

**Fama = Reputación del equipo (0 - 99999 puntos)**

### Ganancia de Fama

| Acción | Fama +/- | Condición |
|--------|----------|-----------|
| Victoria en Arena | +50 | Siempre |
| Victoria vs enemigo 5+ niveles | +150 | Escalado |
| Evento Positivo | +250 | Narrativa |
| Evento Negativo | -200 | Narrativa |
| Racha de victorias | +50 × racha | Cada X victorias |
| Derrota | -25 | Siempre |
| Aceptar patrocinio | +500 | Evento |
| Rechazar patrocinio | -100 | Evento |

### Efectos de Fama

```
FAMA BAJA (< 500)
├─ Enemigos más débiles (-20% stats)
├─ Premios más bajos (-30% oro)
└─ Menos eventos positivos

FAMA MEDIA (500-1500)
├─ Equilibrio normal
└─ Mix de eventos

FAMA ALTA (1500-5000)
├─ Enemigos más fuertes (+30% stats)
├─ Premios aumentados (+50% oro)
├─ Más eventos positivos
└─ Desafíos especiales

FAMA MUY ALTA (> 5000)
├─ Enemigos extremos (+80% stats)
├─ Máximos premios
├─ Eventos épicos
└─ Final game content
```

---

## 🎖️ MISIONES Y LOGROS

### Sistema Auto-tracking

**Auto Track 1:** Victorias en Arena
```
Misión: Ganar X combates en la arena
├─ Meta 1: 5 victorias → +200g
├─ Meta 2: 10 victorias → +500g
├─ Meta 3: 20 victorias → +1000g + Logro
└─ Meta secreta: 50 victorias → Acceso a evento especial
```

**Auto Track 2:** Dinero Ganado
```
Misión: Acumular X oro
├─ Meta 1: 2000g → +Skillpoint
├─ Meta 2: 5000g → +Item raro
└─ Meta 3: 10000g → +Acceso tienda premium
```

**Auto Track 3:** Estadísticas de Combate
```
Misión: Alcanzar X críticos
├─ Meta 1: 20 críticos → +50 XP
├─ Meta 2: 50 críticos → +Habilidad crítica
└─ Meta 3: 100 críticos → +Título "Crítico Maestro"
```

### Estados de Misión

```python
class EstadoMision(Enum):
    ACTIVA = "activa"           # En progreso
    COMPLETADA = "completada"   # Meta alcanzada, sin reclamar
    RECLAMADA = "reclamada"     # Recompensa obtenida
```

---

## 🛡️ SISTEMA DE EQUIPO

### Equipo de Combate

Cada gladiador lleva:
- **Arma** (afecta ATK)
- **Armadura** (afecta DEF)
- **Equipo especial** (afecta AGILIDAD o efectos)

### Items Disponibles

```
Armas:
├─ Gladius básico: ATK +5
├─ Gladius mejorado: ATK +10
├─ Espada romana: ATK +18
├─ Lanza de guerra: ATK +25
└─ Arma de leyenda: ATK +35 + Efecto

Armaduras:
├─ Túnica: DEF +2
├─ Coraza: DEF +8
├─ Placas romanas: DEF +15
├─ Armadura completa: DEF +25
└─ Armadura legendaria: DEF +40 + Efecto

Especiales:
├─ Grebas: AGILIDAD +3
├─ Casco: +10% Esquiva críticos
├─ Escudo: DEF +10
└─ Talismanes: Efectos únicos
```

### Peso del Equipo

Mayor peso = Mejor defensa pero menos agilidad

**Bonificador de peso:**
```
peso_defensa = 1 + (peso_equipo * 0.05)
peso_agilidad = 1 - (peso_equipo * 0.03)
```

---

## 📊 RESUMEN DE SISTEMAS

| Sistema | Status | Archivos |
|---------|--------|----------|
| 🎭 Arquetipos | ✅ Implementado | `src/habilidades.py` |
| ⚔️ Habilidades | ✅ Implementado | `src/habilidades.py` |
| ✨ Efectos | ⚠️ Parcial | `src/models.py` |
| 🎬 Narrativa | ✅ Fase 3 | `src/narrativa.py` |
| 💰 Progresión | ✅ Completo | `src/models.py` |
| ⭐ Fama | ✅ Sistema 3.0 | `src/models.py` |
| 🎖️ Misiones | ✅ Auto-track | `src/misiones.py` |
| 🛡️ Equipo | ✅ Tienda | `src/store.py` |

---

*Documento maestro de todas las funcionalidades del juego - Actualizado Fase 3*
