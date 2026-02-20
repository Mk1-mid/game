# 📋 FASE 3: PROFUNDIDAD - PLAN DETALLADO

**Fecha de Inicio:** 12 de Febrero 2026  
**Duración Estimada:** 10-12 horas  
**Objetivo Final:** Llevar el juego de 8.8/10 → 9.2/10  
**Prioridad:** 🟢 ALTA (mejoras de valor)

---

## 🎯 RESUMEN EJECUTIVO

Fase 3 añade **4 sistemas avanzados** que multiplican la jugabilidad:

1. **Árbol de Talentos** (4h) - Personalización profunda de gladiadores
2. **Sistema de Forja** (3h) - Mejora y reparación de armas
3. **Eventos Aleatorios** (3h) - Variabilidad y surpresas
4. **Leaderboards Global** (2h) - Competencia y objetivo a largo plazo

**Impacto por sistema:**
- Árbol de Talentos: +0.4 (decisiones tácticas)
- Forja: +0.2 (profundidad económica)
- Eventos: +0.3 (replayability)
- Leaderboards: +0.1 (competencia)

---

## 📅 3.1 - ÁRBOL DE TALENTOS (4 HORAS)

### 🎯 Concepto
Cada gladiador gana **1 punto de talento por nivel**. Distribuye en 4 ramas con 5 niveles cada una (máx 25 puntos totales a nivel 25).

### 📋 Tareas

#### 3.1.1 - Crear `src/talents.py`
**Clases necesarias:**

```python
class TalentBranch(Enum):
    FUERZA = "fuerza"
    RESISTENCIA = "resistencia"
    AGILIDAD = "agilidad"
    TECNICA = "tecnica"

class TalentNode:
    def __init__(self, branch, level, name, description, stats_bonus)
    effect()  # Aplica los bonos

class TalentTree:
    def __init__(self, gladiador)
    add_point(branch, level) -> bool
    get_available_points() -> int
    get_all_bonuses() -> dict
```

**Definición de talentos:**

```
FUERZA (Aumenta ATK + Crítico):
  Nivel 1: +5 ATK
  Nivel 2: +10 ATK
  Nivel 3: +15 ATK, +5% Crítico
  Nivel 4: +20 ATK, +10% Crítico
  Nivel 5: +30 ATK, +15% Crítico, Habilidad "Golpe Devastador"

RESISTENCIA (Aumenta HP + DEF):
  Nivel 1: +30 HP
  Nivel 2: +50 HP
  Nivel 3: +50 HP, +5 DEF
  Nivel 4: +50 HP, +10 DEF
  Nivel 5: +100 HP, +15 DEF, Habilidad "Escudo Inquebrantable"

AGILIDAD (Aumenta SPD + Evasión):
  Nivel 1: +5 SPD
  Nivel 2: +10 SPD
  Nivel 3: +15 SPD, +5% Evasión
  Nivel 4: +20 SPD, +10% Evasión
  Nivel 5: +25 SPD, +15% Evasión, Habilidad "Fantasma"

TÉCNICA (Aumenta XP + Loot):
  Nivel 1: +5% XP ganado
  Nivel 2: +10% XP ganado
  Nivel 3: +15% XP ganado, +10% Oro
  Nivel 4: +20% XP ganado, +15% Oro
  Nivel 5: +25% XP ganado, +20% Oro, Acceso a items especiales
```

#### 3.1.2 - Integrar en `src/models.py`
Añadir a clase `Gladiador`:

```python
class Gladiador:
    def __init__(self, ...):
        ...
        self.talent_tree = TalentTree(self)
        self.puntos_talento_disponibles = 0
    
    def ganar_nivel(self, ...):
        ...
        self.puntos_talento_disponibles += 1  # 1 punto por nivel
```

#### 3.1.3 - Crear menú en `main.py`
**Función: `menu_talentos(gladiador)`**

```
═════════════════════════════════════════════════════════════
🌳 ÁRBOL DE TALENTOS - {Gladiador.nombre}
═════════════════════════════════════════════════════════════

Puntos Disponibles: 3/5

🔴 FUERZA (3/5 niveles desbloqueados)
   [1] Nivel 1: +5 ATK (COMPLETADO ✓)
   [2] Nivel 2: +10 ATK (COMPLETADO ✓)
   [3] Nivel 3: +15 ATK, +5% Crítico (COMPLETADO ✓)
   [4] Nivel 4: +20 ATK, +10% Crítico (Bloqueado - Requiere 4 puntos)
   [5] Nivel 5: +30 ATK, +15% Crítico (Bloqueado - Requiere 5 puntos)

🟡 RESISTENCIA (1/5)
   [1] Nivel 1: +30 HP (COMPLETADO ✓)

🟢 AGILIDAD (0/5)
   [1] Nivel 1: +5 SPD (Requiere 1 punto)

🔵 TÉCNICA (0/5)
   [1] Nivel 1: +5% XP (Requiere 1 punto)

═════════════════════════════════════════════════════════════
[F/R/A/T] Selecciona rama | [V] Ver resumen | [0] Salir
```

#### 3.1.4 - Testing
**Test file:** `tests/test_talent_tree.py`

**Coverage:**
- ✅ Creación de árbol para nuevo gladiador
- ✅ Ganar punto al subir nivel
- ✅ Aplicar talento correctamente
- ✅ Bloquear si no hay puntos
- ✅ Bloquear si requisitos no cumplidos
- ✅ Persistencia del árbol en JSON

---

## 📅 3.2 - SISTEMA DE FORJA (3 HORAS)

### 🎯 Concepto
El Herrero ahora puede mejorar armas y armaduras. Cada mejora:
- Aumenta stats
- Reduce durabilidad
- Cuesta más cada mejora

También existe reparación para restaurar durabilidad.

### 📋 Tareas

#### 3.2.1 - Modificar `src/facilities.py`
Expandir clase `Herrero`:

```python
class Herrero:
    def __init__(self, nivel=1):
        ...
        self.estadisticas = {
            "armas_mejoradas": 0,
            "ataque_total_otorgado": 0,
            "reparaciones": 0,
            "dinero_ganado": 0
        }
    
    def mejorar_arma(self, weapon, gladiador) -> (bool, str, cost):
        """Mejora arma en +1 ATK, reduce 5% durabilidad, cuesta base × tipo × nivel²"""
        pass
    
    def reparar_arma(self, weapon) -> (bool, str, cost):
        """Repara completamente arma, costo = (100 - durabilidad) × base / 10"""
        pass
    
    def obtener_costo_mejora(self, weapon):
        """Calcula costo de próxima mejora"""
        pass
```

**Fórmulas:**

```
MEJORA:
  Costo = base_price × tipo_multiplier × nivel_mejora²
  
  Ejemplos (Tier 2, base 200g, tipo_medio=1.0):
    Mejora 1: 200 × 1.0 × 1² = 200g       (+12% ATK)
    Mejora 2: 200 × 1.0 × 2² = 800g       (+12% ATK más)
    Mejora 3: 200 × 1.0 × 3² = 1800g      (+12% ATK más)
    Mejora 5: 200 × 1.0 × 5² = 5000g      (muy caro)

DURABILIDAD:
  -5% por mejora
  Ejemplo:
    Arma +0: 100% durabilidad
    Arma +3: 85% durabilidad
    Arma +5: 75% durabilidad

REPARACIÓN:
  Costo = (100 - durabilidad_actual) × precio_base / 10
  
  Ejemplos:
    Reparar de 95% → 100%: 5 × 20 = 100g
    Reparar de 50% → 100%: 50 × 20 = 1000g
    Reparar de 0% → 100%: 100 × 20 = 2000g
```

#### 3.2.2 - Expandir menú Herrero en `main.py`
**Función: `herrero_menu(equipo, herrero)`**

```
═════════════════════════════════════════════════════════════
⚒️  HERRERO - NIVEL 3/5
═════════════════════════════════════════════════════════════

Dinero disponible: 2500g

[1] Mejorar Arma
    Selecciona gladiador → Selecciona arma
    Muestra: Costo, próximo stats, durabilidad
    
[2] Reparar Arma
    Selecciona gladiador → Selecciona arma
    Muestra: Durabilidad actual, costo, resultado

[3] Ver Estadísticas del Herrero
    • Armas mejoradas: 12
    • ATK total otorgado: 145
    • Reparaciones realizadas: 8
    • Dinero ganado: 3200g

[4] Ver Catálogo de Armas
    Muestra todas y sus costos de mejora

[0] Salir
```

#### 3.2.3 - Testing
**Test file:** `tests/test_forge_system.py`

**Coverage:**
- ✅ Mejora aumenta ATK correctamente
- ✅ Durabilidad disminuye -5% por mejora
- ✅ Costo escala cuadráticamente
- ✅ Reparación restaura durabilidad
- ✅ Estadísticas del Herrero se actualizan
- ✅ Persistencia de armas mejoradas

---

## 📅 3.3 - EVENTOS ALEATORIOS (3 HORAS)

### 🎯 Concepto
10 eventos que ocurren aleatoriamente (10% de chance cada vez que accedes al menú principal). Generan variabilidad y decisiones difíciles.

### 📋 Tareas

#### 3.3.1 - Crear `src/events.py`

```python
class Evento(Enum):
    MERCADER_AMBULANTE = "mercader"
    GLADIADOR_HERIDO = "herido"
    APUESTA = "apuesta"
    TORNEO_SORPRESA = "torneo"
    ENFERMEDAD = "enfermedad"
    ENTRENADOR_LEGENDARIO = "entrenador"
    SABOTAJE = "sabotaje"
    REGALO_DIOSES = "regalo"
    DEUDA_JUEGO = "deuda"
    FESTIVAL_ROMANO = "festival"

class EventoManager:
    def __init__(self):
        self.historial_eventos = []
    
    def generar_evento_aleatorio(self) -> Evento or None:
        """10% de chance, retorna evento aleatorio"""
        pass
    
    def procesar_evento(self, evento, equipo) -> (success, message):
        """Aplica los efectos del evento"""
        pass
```

**Definición de eventos:**

```
1. MERCADER AMBULANTE
   - Vende 6 items especiales al 70% del precio
   - Items de tiers altos disponibles
   - Chance: Una sola vez por sesión

2. GLADIADOR HERIDO
   - Te encuentras un gladiador herido
   - Lo recluta GRATIS pero con 30% HP
   - Requiere hospital inmediato

3. APUESTA CLANDESTINA
   - Apunta dinero (100g - 1000g)
   - 50% chance ganar el doble
   - 50% chance perder todo

4. TORNEO SORPRESA
   - 3 combates obligatorios consecutivos
   - Si ganas 3: Triple dinero + XP
   - Si pierdes 1: Pierdes un gladiador (muerto)

5. ENFERMEDAD
   - Gladiador aleatorio -20% stats por 3 días
   - Hospital intenta curar (costo doble)

6. ENTRENADOR LEGENDARIO
   - +10 stats en 1 atributo (eliges cuál) GRATIS
   - El gladiador sube de nivel sin costo

7. SABOTAJE
   - Próximo combate: Enemigo tiene +50% stats
   - Aviso previo: "Alguien saboteó tu equipo"

8. REGALO DE LOS DIOSES
   - Recibe 1 item legendario al azar
   - Arma Tier 4 o Armadura Tier 4
   - 100% gratis

9. DEUDA DE JUEGO
   - Pierdes 500-1000g por apuestas anteriores
   - O realizas 1 combate obligatorio sin recompensa

10. FESTIVAL ROMANO
    - +15% XP en los próximos 5 combates
    - Evento cosmético pero positivo
```

#### 3.3.2 - Integrar en `main.py`
**En el loop principal:**

```python
while juego_activo:
    # Cada turno, 10% chance de evento
    if random.random() < 0.1:
        evento = evento_manager.generar_evento_aleatorio()
        if evento:
            success, message = evento_manager.procesar_evento(evento, equipo)
            print(message)  # Mostrar con estilo visual
            if not success:
                print("(Puedes continuar jugando)")
    
    # Mostrar menú normal
    mostrar_menu_principal()
```

#### 3.3.3 - Testing
**Test file:** `tests/test_events.py`

**Coverage:**
- ✅ Cada evento ocurre y se procesa
- ✅ Efectos se aplican correctamente
- ✅ Dinero/stats/gladiadores se actualizan
- ✅ Mensajes visuales se generan
- ✅ Eventos no ocurren en combate

---

## 📅 3.4 - LEADERBOARDS GLOBAL (2 HORAS)

### 🎯 Concepto
Sistema de rankings compartido entre todos los usuarios. 3 tablas: Victorias, Dinero, Nivel máximo.

### 📋 Tareas

#### 3.4.1 - Crear `src/leaderboards.py`

```python
class LeaderboardEntry:
    def __init__(self, usuario, gladiador_principal, valor):
        self.usuario = usuario
        self.gladiador = gladiador_principal
        self.valor = valor
        self.fecha = today()

class GlobalLeaderboard:
    def __init__(self):
        self.top_victorias = []  # Máx 10
        self.top_dinero = []     # Máx 10
        self.top_nivel = []      # Máx 10
    
    def update_entry(self, usuario, gladiador, tipo) -> None:
        """Actualiza entry si está en top 10"""
        pass
    
    def obtener_ranking(self, tipo) -> List[LeaderboardEntry]:
        """Retorna top 10"""
        pass
    
    def obtener_posicion(self, usuario, tipo) -> int:
        """Retorna la posición del usuario en ranking"""
        pass
    
    def cargar_desde_json(self, path):
        """Carga leaderboards desde JSON compartido"""
        pass
    
    def guardar_a_json(self, path):
        """Guarda leaderboards en JSON"""
        pass
```

**Estructura JSON:**

```json
{
  "top_victorias": [
    {"usuario": "admin", "gladiador": "Ferox", "valor": 150, "fecha": "2026-02-12"},
    {"usuario": "player1", "gladiador": "Velox", "valor": 120, "fecha": "2026-02-10"},
    ...
  ],
  "top_dinero": [...],
  "top_nivel": [...]
}
```

#### 3.4.2 - Crear menú en `main.py`
**Función: `mostrar_leaderboards(leaderboard)`**

```
═════════════════════════════════════════════════════════════
🏆 LEADERBOARDS GLOBAL
═════════════════════════════════════════════════════════════

[1] TOP VICTORIAS
    🥇 Ferox (admin) - 150 victorias
    🥈 Velox (player1) - 120 victorias
    🥉 Marcus (player2) - 98 victorias

[2] TOP DINERO ACUMULADO
    🥇 admin - 50,000g
    🥈 player1 - 35,000g
    🥉 player2 - 28,000g

[3] TOP NIVEL MÁXIMO ALCANZADO
    🥇 Ferox (admin) - Nivel 35
    🥈 Velox (player1) - Nivel 28
    🥉 Marcus (player2) - Nivel 25

[0] Volver

═════════════════════════════════════════════════════════════
Tu posición actual:
  • Victorias: #5 (95 victorias)
  • Dinero: #7 (18,000g)
  • Nivel: #8 (Nivel 22)
═════════════════════════════════════════════════════════════
```

#### 3.4.3 - Integración con persistencia
**En `main.py` - Guardar/cargar:**

```python
# Al cargar usuario
leaderboards.cargar_desde_json("datos/leaderboards.json")

# Después de cada combate, nivel-up, dinero
leaderboards.update_entry(usuario, equipo.obtener_gladiador_principal(), "victorias")
leaderboards.guardar_a_json("datos/leaderboards.json")
```

#### 3.4.4 - Testing
**Test file:** `tests/test_leaderboards.py`

**Coverage:**
- ✅ Crear entries correctamente
- ✅ Ranking se ordena por valor (descendente)
- ✅ Top 10 se mantiene
- ✅ Posición del usuario se calcula
- ✅ Persistencia JSON funciona
- ✅ Múltiples usuarios no interfieren

---

## 📊 RESUMEN DE TAREAS

### Primera Semana - Talentos + Forja (7h)
```
Lunes:      3.1.1 + 3.1.2 (Crear TalentTree) - 2.5h
Martes:     3.1.3 + 3.1.4 (Menu + testing) - 1.5h
Miércoles:  3.2.1 + 3.2.2 (Sistema forja) - 1.5h
Jueves:     3.2.3 (Testing forja) - 1.5h
```

### Segunda Semana - Eventos + Leaderboards (5h)
```
Viernes:    3.3.1 + 3.3.2 (Eventos) - 2h
Lunes:      3.3.3 (Testing eventos) - 1h
Martes:     3.4.1 + 3.4.2 (Leaderboards) - 1.5h
Miércoles:  3.4.3 + 3.4.4 (Integración + testing) - 0.5h
```

---

## ✅ CHECKLIST FINAL FASE 3

- [ ] 3.1 Árbol de Talentos completo + testing
  - [ ] TalentTree creado
  - [ ] Menu integrado
  - [ ] 4 ramas × 5 niveles = 20 opciones
  - [ ] Test: test_talent_tree.py (100%)

- [ ] 3.2 Sistema de Forja completo + testing
  - [ ] Mejora de armas
  - [ ] Durabilidad implementada
  - [ ] Reparación de armas
  - [ ] Test: test_forge_system.py (100%)

- [ ] 3.3 Eventos Aleatorios + testing
  - [ ] 10 eventos diferentes
  - [ ] Integración en loop principal
  - [ ] Efectos se aplican correctamente
  - [ ] Test: test_events.py (100%)

- [ ] 3.4 Leaderboards Global + testing
  - [ ] 3 tablas de ranking
  - [ ] Persistencia JSON
  - [ ] Menu visual
  - [ ] Test: test_leaderboards.py (100%)

- [ ] Documentación actualizada
  - [ ] Roadmap con resultados finales
  - [ ] Documentación técnica de Fase 3
  - [ ] Guía de uso

---

## 📊 IMPACTO FINAL

**Antes de Fase 3:** 8.8/10  
**Después de Fase 3:** 9.2/10  
**Incremento:** +0.4

El juego pasa a ser una experiencia **muy completa y replayable**, con sistemas que dan objetivos a largo plazo y decisiones tácticas profundas.

**Siguiente paso:** Fase 4 (Interfaz Gráfica) sería opcional para llevar a 9.5/10, pero con Fase 3 ya tendremos un juego **de calidad producción** listo.
