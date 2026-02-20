# 🏗️ ESTRUCTURA DEL PROYECTO

**v3.0 - Fase 3 (El Alma del Juego)**

---

## 📦 Árbol de Directorios

```
juego/
├── 📄 main.py                          ← Punto de entrada (2278 líneas)
├── 📄 requirements.txt                 ← Dependencias Python
├── 📄 README.md                        ← Info del proyecto
├── 📄 CHANGELOG.md                     ← Historial de versiones
│
├── 🗂️ src/                             ← Código fuente (11 módulos)
│   ├── __init__.py
│   ├── models.py                       ← CORE: Gladiador, Equipo, Barracas (1033 líneas)
│   ├── narrativa.py                    ← NUEVO: Motor narrativo + eventos
│   ├── combat.py                       ← Sistema de combate automático
│   ├── enemies.py                      ← Generador de enemigos escalados
│   ├── habilidades.py                  ← Arquetipos y habilidades (24+ skills)
│   ├── facilities.py                   ← Hospital + Herrero
│   ├── auth.py                         ← Autenticación de usuarios
│   ├── persistence.py                  ← Guardado/carga (JSON)
│   ├── store.py                        ← Tienda y armería
│   ├── misiones.py                     ← Sistema de misiones
│   └── guia.py                         ← Ayuda en juego
│
├── 🗂️ tests/                           ← Suite de pruebas
│   ├── run_tests.py
│   ├── run_tests_new.py
│   └── 15+ archivos test específicos
│
├── 🗂️ data/                            ← Datos persistentes
│   ├── users.json                      ← Registro de usuarios
│   └── saves/                          ← Partidas guardadas por usuario
│
├── 🗂️ datos/                           ← Definiciones de contenido
│   └── misiones_admin.json             ← Definiciones de misiones
│
└── 🗂️ docs/                            ← Documentación (5 maestros)
    ├── INDICE.md                       ← Super índice (navegación)
    ├── ESTRUCTURA.md                   ← Este archivo
    ├── MODULOS.md                      ← Detalle por módulo src/
    ├── FUNCIONALIDADES.md              ← Arquetipos, habilidades, efectos
    ├── ROADMAP.md                      ← Planes Fase 3-5
    ├── COMIENZA_AQUI.md                ← Guía rápida para jugadores
    └── CHANGELOG.md                    ← Historial de cambios
```

---

## 🧩 Módulos Principales (src/)

### 1️⃣ **models.py** - NÚCLEO DEL JUEGO (1033 líneas)

**Responsabilidad**: Definición de todas las entidades del juego.

**Clases Principales**:

#### `Character` (Base)
- `hp, attack, defense, agilidad`
- `weapon, armor` (equipo)
- Métodos: `ataque_final()`, `defensa_final()`, `agilidad_final()`

#### `Gladiador` (Hereda de Character)
```
- nivel (1-50+)
- xp, experiencia
- fuerza, crítico, esquiva
- hp_actual, estado (sano/herido/crítico/muerto)
- ocupación (disponible/ocupado)
- ⭐ fama (reputación)
- ⭐ efectos_activos[] (buffs/debuffs)
- habilidades, habilidades_activas
- combates_ganados, combates_perdidos, dinero_generado
```

**Métodos Clave**:
- `ganar_xp(xp)` - Gana experiencia, sube nivel
- `pasar_dia()` - Avanza estado (ocupación, efectos)
- `calcular_stats_finales()` - Recalcula stats con equipo
- `animar_nivel_up()` - Visual de subida de nivel

#### `Equipo` (Gestor de equipo)
```
- gladiadores[] (lista de Gladiador)
- dinero (oro disponible)
- barracas (espacios para gladiadores)
- fama (reputación del equipo)
- victoria_reciente (bool)
- dias_con_poco_oro (int)
- racha_victorias (int)
- xp_bonus_activos[] (bonificadores pasivos)
```

**Métodos Clave**:
- `agregar_gladiador(gladiador)`
- `pasar_dia()` - Avanza día + procesa efectos
- `calcular_nivel_promedio()` - Para escalado de enemigos
- Propiedades: `espacios_disponibles`, `todos_muertos()`

#### `Barracas`
```
- espacios_totales (capacidad, max 6)
- gladiadores_alojados
- precio_por_espacio (500g)
```

#### `Weapon` y `Armor`
```
- hp, attack, defense, agilidad
- peso (afecta velocidad)
```

#### Otras Clases:
- `SistemaLigas` - Ranking de gladiadores
- `LigasAutomaticas` - Ligas por temporada
- `Item` - Objeto genérico

---

### 2️⃣ **narrativa.py** - MOTOR DE EVENTOS (NUEVO - Fase 3)

**Responsabilidad**: Generar eventos narrativos y aplicar consecuencias.

**Clases Principales**:

#### `GestorNarrativa`
- 12 eventos predefinidos
- `intentar_disparar_evento(equipo)` - Selecticiona evento por probabilidad
- `calcular_probabilidad()` - Basada en estado (fama, oro, etc.)

#### `Evento`
```
- nombre (ej: "Festival de Gladiadores")
- descripcion
- disparadores (condiciones)
- opciones[] (decisiones disponibles)
- probabilidad_base
```

#### `Opcion`
```
- texto (ej: "Participar")
- descripcion
- resultado (qué ocurre)
```

#### `Resultado`
```
- cambios_dinero (int)
- cambios_xp (int)
- estado_gladiador (cambio)
- efectos_activos[] (buffs)
```

**Eventos Implementados** (12 total):
1. Festival de Gladiadores
2. Rebelión de Gladiadores
3. Patrocinio de Noble
4. Inspección de Roma
5. Mercenario Rival
6. Enfermedad en Ludus
7. Caza Furtiva de Esclavos
8. Amistoso Deportivo
9. Traición del Gerente
10. Visita de Críticos
11. Conspiración Política
12. Sueño de Retiro

---

### 3️⃣ **combat.py** - COMBATE

**Responsabilidad**: Lógica de combate automático.

**Funciones Principales**:
- `combate_arena()` - Flujo de combate
- `calcular_xp_recompensa()` - Escala por (nivel, dificultad)
- Sistema de turnos automático

**Features**:
- Defensa mitiga daño
- Crítico x1.5 daño
- Esquiva evita daño (probabilidad)
- Integración con habilidades

---

### 4️⃣ **habilidades.py** - SISTEMA DE HABILIDADES

**Responsabilidad**: Arquetipos, habilidades y triggers.

**Arquetipos** (5 disponibles):
- **Guerrero** - Fuerza + Defensa
- **Velocista** - Agilidad + Esquiva
- **Asesino** - Crítico + Daño
- **Paladín** - Equilibrio
- **Tanque** - Defensa pura

**Habilidades**: 24+ total
- Trigger automático en combate
- Duración de efectos
- Cooldowns

---

### 5️⃣ **enemies.py** - GENERACIÓN DE ENEMIGOS

**Responsabilidad**: Crear enemigos equilibrados.

- Escalado automático por nivel
- Nombres romanos aleatorios
- Stats variados

---

### 6️⃣ **facilities.py** - HOSPITAL Y HERRERO

## Médico (Hospital)
- Curación rápida: 100g → 75% HP
- Revivir: 100g → 75% HP
- Curación lenta: gratis

## Herrero
- Venta de items potentes
- Reparación de equipo

---

### 7️⃣ **auth.py** - AUTENTICACIÓN

- Registro/Login
- Encriptación básica
- Separación de usuarios

---

### 8️⃣ **persistence.py** - GUARDADO/CARGA

- JSON persistente
- Serialización de objetos
- `serializar_equipo()` → dict
- `deserializar_equipo()` ← dict

---

### 9️⃣ **store.py** - TIENDA Y ARMERÍA

- Catálogo de items
- Compra/Venta
- Equipamiento

---

### 🔟 **misiones.py** - SISTEMA DE MISIONES

- Auto-tracking de logros
- Estados: ACTIVA, COMPLETADA, RECLAMADA
- Recompensas automáticas

---

### 1️⃣1️⃣ **guia.py** - AYUDA EN JUEGO

- Tutoriales
- Tips de balance

---

## 🔗 Dependencias Internas

```
main.py (2278 líneas)
  ├─ models.py
  ├─ narrativa.py      ← NUEVO
  ├─ combat.py
  ├─ enemies.py
  ├─ habilidades.py
  ├─ facilities.py
  ├─ auth.py
  ├─ persistence.py
  ├─ misiones.py
  ├─ store.py
  └─ guia.py
```

---

## ⚙️ Ciclo de Vida de la Partida

```
1. INICIO
   └─ main.py llama a juego_principal()

2. AUTENTICACIÓN
   └─ auth.py (login/registro)

3. CARGA DE EQUIPO
   └─ persistence.py (JSON → Equipo)

4. LOOP PRINCIPAL (while juego_activo)
   ├─ Mostrar menú (8 opciones)
   ├─ [1] Arena
   │   ├─ Seleccionar gladiador
   │   ├─ enemies.py (generar enemigo)
   │   ├─ combat.py (combate)
   │   ├─ habilidades.py (skills activan)
   │   ├─ models.py (actualizar stats)
   │   └─ Recompensas (oro, XP, fama)
   ├─ [2] Barracas (entrenar)
   ├─ [3] Hospital (curar)
   ├─ [4] Mercado (comprar gladiadores)
   ├─ [5] Armería (comprar items)
   ├─ [6] Ver equipo
   ├─ [7] Misiones
   ├─ [8] PASAR DÍA
   │   ├─ models.py → equipo.pasar_dia()
   │   ├─ narrativa.py → GestorNarrativa.intentar_disparar_evento()
   │   └─ Aplicar consecuencias
   ├─ [9] Guardar
   └─ [0] Salir

5. GUARDADO
   └─ persistence.py (Equipo → JSON)
```

---

## 📊 Estadísticas de Código

| Componente | Líneas | Tipo |
|-----------|--------|------|
| main.py | 2278 | Principal |
| models.py | 1033 | Core |
| narrativa.py | 350 | Nuevo |
| combat.py | 400 | Sistema |
| habilidades.py | 600 | Sistema |
| Otros + helpers | 1500 | Código |
| **Total src/** | **~6500** | **Código Python** |

---

## 🚀 Escalabilidad

- **Límites actuales**: 6 gladiadores, 50 niveles, 12 eventos
- **Fácil expandir**: Más arquetipos, más eventos, más items
- **Datos**: JSON permitemayor contenido sin cambios

---

*Este documento es referencia para cualquier cambio estructural en el código.*
