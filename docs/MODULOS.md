# 📚 MÓDULOS Y COMPONENTES

**v3.0 - Documentación detallada por archivo fuente**

---

## 📑 Índice de Módulos

1. [main.py](#mainpy) - Punto de entrada
2. [models.py](#modelspy) - Entidades core
3. [narrativa.py](#narrativapdy) - Motor de eventos (NUEVO)
4. [combat.py](#combatpy) - Sistema de combate
5. [enemies.py](#enemiespy) - Generación de enemigos
6. [habilidades.py](#habilidadespy) - Arquetipos y skills
7. [facilities.py](#facilitiespy) - Hospital y Herrero
8. [auth.py](#authpy) - Autenticación
9. [persistence.py](#persistencepy) - Guardado/carga
10. [store.py](#storepy) - Tienda y comercio
11. [misiones.py](#misionespy) - Sistema de misiones
12. [guia.py](#guiapdy) - Ayuda en juego

---

## 🎮 main.py

**Líneas:** 2278  
**Responsabilidad:** Punto de entrada y loop principal del juego

### Estructura

```
1. IMPORTACIONES (todas las librerías)
2. FUNCIONES AUXILIARES
   ├─ animar_titulo()
   ├─ mostrar_menu()
   ├─ procesar_opcion_arena()
   ├─ procesar_opcion_barracas()
   └─ ... (más opciones)
3. FUNCIÓN PRINCIPAL
   └─ juego_principal()
4. ENTRY POINT
   └─ if __name__ == "__main__"
```

### Funciones Principales

#### `juego_principal()`
```python
def juego_principal():
    """
    Loop principal del juego:
    
    1. Muestra título y ubicación
    2. Pide usuario
    3. Carga/crea equipo
    4. Loop: mostrar menú → procesar opción
    5. Guardar al salir
    """
```

**Subprocesos:**
- `procesar_opcion_arena()` → Combate
- `procesar_opcion_barracas()` → Entrenamiento
- `procesar_opcion_hospital()` → Curación
- `procesar_opcion_mercado()` → Comprar gladiadores
- `procesar_opcion_armeria()` → Comprar items
- `procesar_opcion_ver_equipo()` → Estadísticas
- `procesar_opcion_misiones()` → Logros
- `procesar_opcion_pasar_dia()` → Narrativa 🆕
- `procesar_opcion_guardar()` → Persistencia

#### Menú Principal

```
┌─────────────────────────────────┐
│  ⚔️ LUDUS DE SANGRE Y FORTUNA ⚔️ │
│                                 │
│ [1] 🗣️ Arena                    │
│ [2] 🏋️ Barracas                │
│ [3] 🏥 Hospital                 │
│ [4] 🛍️ Mercado                  │
│ [5] ⚔️ Armería                  │
│ [6] 📊 Ver Equipo               │
│ [7] 🎖️ Misiones                │
│ [8] ⏰ Pasar Día 🆕             │
│ [9] 💾 Guardar                  │
│ [0] 🚪 Salir                    │
└─────────────────────────────────┘
```

### Flujo de Datos

```
Usuario → Opción → Función específica → Modifica equipo → Necesita guardar
```

---

## 📊 models.py

**Líneas:** 1033  
**Responsabilidad:** Definición de todas las entidades del juego

### Clases Principales

#### `Character` (Base)
```python
class Character:
    # Atributos base
    nombre: str
    hp: int
    hp_actual: int
    attack: int
    defense: int
    agilidad: int
    
    # Métodos
    def ataque_final() -> int
    def defensa_final() -> int
    def agilidad_final() -> int
    def calcular_stats_finales()
```

**Propósito:** Base para Gladiador y Enemigos. Define cálculo de stats finales.

---

#### `Gladiador(Character)` - ⭐ CORE
```python
class Gladiador(Character):
    # Progresión
    nivel: int                          # 1-50+
    xp: int                             # Experiencia actual
    xp_necesaria_proxima: int
    
    # Combate
    tipo_nombre: str                    # Murmillo, Retiarius, etc.
    arqueotipo: str                     # Guerrero, Velocista, etc.
    fuerza: int
    crítico: int
    esquiva: int
    heridas: int
    
    # Estado
    estado: str                         # sano/herido/crítico/muerto
    ocupacion: str                      # disponible/ocupado/<fecha>
    
    # ⭐ FASE 3
    fama: int                           # Reputación personal
    efectos_activos: List[dict]         # Buffs temporales
    
    # Historial
    combates_ganados: int
    combates_perdidos: int
    dinero_generado: int
    
    # Equipo
    weapon: Weapon
    armor: Armor
    
    # Habilidades
    habilidades: List[Habilidad]
    habilidades_activas: Dict
    contadores_triggers: Dict
    
    # Métodos
    def ganar_xp(xp: int)
    def subir_nivel()
    def puede_combatir() -> bool
    def pasar_dia()
    def aplicar_efecto(efecto: dict)
    def calcular_stats_finales()
    def animar_nivel_up()
```

**Responsabilidades:**
- Gestión de progresión (XP, nivel)
- Cálculo de stats con equipo
- Control de estado (sano/herido/muerto)
- Aplicación de efectos temporales
- Rastreo de habilidades

---

#### `Equipo` (Gestor del Ludus)
```python
class Equipo:
    nombre: str
    gladiadores: List[Gladiador]       # Lista de tus gladiadores
    dinero: int
    barracas: Barracas
    
    # ⭐ FASE 3
    fama: int                           # Reputación del ludus
    victoria_reciente: bool
    dias_con_poco_oro: int
    racha_victorias: int
    xp_bonus_activos: List[dict]
    
    # Métodos
    def agregar_gladiador(glad: Gladiador)
    def vender_gladiador(glad: Gladiador)
    def pasar_dia()                     # Procesa efectos
    def calcular_nivel_promedio()
    
    # Propiedades
    @property
    def espacios_disponibles() -> int
    
    @property
    def todos_muertos() -> bool
```

**Responsabilidades:**
- Gestión de gladiadores
- Gestión de oro
- Procesamiento diario (efectos, narrativa)
- Cálculo de recompensas escaladas

---

#### `Barracas`
```python
class Barracas:
    espacios_totales: int = 6
    gladiadores_alojados: int
    precio_por_espacio: int = 500
    
    def renovar_alojamiento()
```

---

#### `Weapon` y `Armor`
```python
class Weapon:
    nombre: str
    attack: int
    precio: int
    
class Armor:
    nombre: str
    defense: int
    peso: float                         # Afecta agilidad
    precio: int
```

---

#### `SistemaLigas`
```python
class SistemaLigas:
    """Sistema de ranking de gladiadores"""
    rankings: Dict[str, int]            # nombre -> puntos
    
    def registrar_victoria(glad: Gladiador)
    def obtener_top10() -> List[tuple]
```

---

### Fórmulas Clave

**XP para siguiente nivel:**
```python
xp_necesario = int(100 * (1.1 ** (nivel - 1)))
```

**Escalado de stats por nivel:**
```python
multiplicador = 1.095 ^ niveles_ganados
```

---

## 🎭 narrativa.py (NUEVO - Fase 3)

**Líneas:** ~350  
**Responsabilidad:** Sistema de eventos narrativos

### Clases Principales

#### `GestorNarrativa`
```python
class GestorNarrativa:
    eventos: Dict[str, Evento]
    
    def intentar_disparar_evento(equipo: Equipo) -> bool:
        """
        Intenta disparar un evento con:
        1. Cálculo de probabilidad base (30%)
        2. Ajuste por fama, dinero, racha
        3. Selección ponderada
        4. Presentación al jugador
        5. Ejecución de consecuencias
        """
    
    def calcular_probabilidad(equipo: Equipo) -> float
```

---

#### `Evento`
```python
class Evento:
    nombre: str
    descripcion: str
    disparadores: List[str]             # Condiciones
    opciones: List[Opcion]              # 2-3 decisiones
    probabilidad_base: float
```

**Eventos disponibles:**
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

#### `Opcion` y `Resultado`
```python
class Opcion:
    texto: str
    descripcion: str
    resultado: Resultado

class Resultado:
    cambios_dinero: int
    cambios_xp: int
    efectos_activos: List[dict]
    estado_narrativo: str
```

---

### Integración en main.py

```python
# En juego_principal():
gestor_narrativa = GestorNarrativa()

# En loop principal:
if opcion == 8:  # Pasar día
    equipo.pasar_dia()
    if gestor_narrativa.intentar_disparar_evento(equipo):
        # Evento disparado y procesado
        pass
```

---

## ⚔️ combat.py

**Líneas:** ~400  
**Responsabilidad:** Sistema de combate automático

### Función Principal

#### `combate_arena(gladiador, enemigo, dificultad)`
```python
def combate_arena(gladiador: Gladiador, enemigo: Character, 
                 dificultad: int = 0) -> tuple[bool, dict]:
    """
    Ejecuta combate automático:
    
    Returns:
        (victoria: bool, recompensas: dict)
    
    Recompensas incluyen:
    - oro_ganado
    - xp_ganado
    - fama_ganada
    - estado_gladiador (actualizado)
    """
```

**Flujo de combate:**
```
1. Inicializar estados
2. Presentar combatientes
3. Loop de turnos:
   ├─ Calcular daño gladiador
   ├─ Calcular daño enemigo
   ├─ Aplicar habilidades
   ├─ Procesar esquivas/críticos
   └─ Mostrar resultado turno
4. Determinar ganador
5. Calcular recompensas
6. Actualizar gladiador
```

---

#### `calcular_daño(ataque, defensa)`
```python
def calcular_daño(ataque: int, defensa: int) -> int:
    """
    daño_base = ataque - (defensa * 0.5)
    daño_final = daño_base * factor_crítico * factor_esquiva
    """
```

---

#### `calcular_xp_recompensa(gladiador, enemigo, dificultad)`
```python
def calcular_xp_recompensa(glad: Gladiador, enemigo: Character, 
                          dif: int) -> int:
    """
    base_xp = 50
    multiplicador_dificultad = 1 + (dif * 0.3)
    multiplicador_nivel = 1 + (diferencia_nivel * 0.1)
    """
```

---

## 👾 enemies.py

**Líneas:** ~200  
**Responsabilidad:** Generación de enemigos escalados

### Función Principal

#### `generar_enemigo(nivel_promedio, dificultad)`
```python
def generar_enemigo(nivel_promedio: int, dificultad: int = 0) -> Character:
    """
    Crea enemigo con:
    1. Nombre romano random
    2. Nivel ajustado por dificultad
    3. Stats escalados
    4. Equipo apropiado
    
    dificultad:
        -2: Novato (nivel - 2)
        0: Normal (nivel)
        3: Experto (nivel + 3)
        5: Legendaria (nivel + 5)
    """
```

---

#### `generar_nombre_romano()`
```python
# Genera nombres de gladiadores romanos realistas
# Ejemplos: Maximus, Titus, Brutus, Severus, etc.
```

---

## ⚡ habilidades.py

**Líneas:** ~600  
**Responsabilidad:** Arquetipos y sistema de habilidades

### Clases/Funciones Clave

#### `TipoTrigger(Enum)`
```python
class TipoTrigger(Enum):
    SALUD_BAJO = "salud_bajo"
    ESQUIVAS_CONSECUTIVAS = "esquivas_consecutivas"
    CRITICOS_RECIBIDOS = "criticos_recibidos"
    CRITICOS_PROPIOS = "criticos_propios"
    DAÑO_RECIBIDO = "daño_recibido"
    TURNOS_COMBATE = "turnos_combate"
```

---

#### `obtener_habilidades_arqueotipo(arqueotipo)`
```python
def obtener_habilidades_arqueotipo(arquetipo: str) -> List[Habilidad]:
    """
    Retorna lista de 5 habilidades para el arqueotipo.
    
    Ejemplos:
    ├─ obtener_habilidades_arqueotipo("Guerrero")
    │  └─ [Fuerza Bruta, Contraataque, Golpe Definitivo, ...]
    └─ obtener_habilidades_arqueotipo("Tanque")
       └─ [Defensa Absoluta, Escudo Reflectante, ...]
    """
```

---

#### `aplicar_bonificadores_combate(stats, gladiador)`
```python
def aplicar_bonificadores_combate(stats: dict, glad: Gladiador) -> dict:
    """
    Aplica bonificadores pasivos de habilidades a stats.
    
    Ejemplo:
    stats = {"ataque": 20, "defensa": 15}
    glad.habilidades[0].bonificadores = {"ataque": 0.14}
    
    Retorna: {"ataque": 22.8, "defensa": 15}
    """
```

---

## 🏥 facilities.py

**Líneas:** ~300  
**Responsabilidad:** Hospital y Herrero

### Clases/Funciones

#### `hospital_opcion_curacion_rapida(equipo)`
```python
# Costo: 100g
# Efecto: Cura 75% HP en 1 día
```

#### `hospital_opcion_revivir(equipo)`
```python
# Costo: 100g
# Efecto: Revive gladiador con 75% HP
```

#### `herrero_opcion_vender_items(equipo)`
```python
# Muestra catálogo de items premium
# Precios según calidad
```

---

## 🔐 auth.py

**Líneas:** ~100  
**Responsabilidad:** Autenticación de usuarios

### Funciones

#### `registrar_usuario(usuario, password)`
```python
# Crea nuevo usuario en data/users.json
# Criptografía básica
```

#### `verificar_login(usuario, password)`
```python
# Valida contra data/users.json
```

---

## 💾 persistence.py

**Líneas:** ~250  
**Responsabilidad:** Guardado y carga de datos

### Funciones Principales

#### `serializar_equipo(equipo) -> dict`
```python
def serializar_equipo(equipo: Equipo) -> dict:
    """
    Convierte equipo a diccionario JSON-serializable.
    
    Incluye:
    - Datos del equipo (oro, fama, etc.)
    - Lista de gladiadores (cada uno serializado)
    - Historial de misiones
    - Barracas
    """
```

---

#### `deserializar_equipo(data) -> Equipo`
```python
def deserializar_equipo(data: dict) -> Equipo:
    """
    Restaura Equipo desde diccionario.
    (Inverso de serializar_equipo)
    """
```

---

#### `guardar_partida(usuario, datos)`
```python
def guardar_partida(usuario: str, datos: dict):
    """
    Guarda datos en data/users.json bajo clave usuario.
    """
```

#### `cargar_partida(usuario) -> Equipo`
```python
def cargar_partida(usuario: str) -> Equipo:
    """
    Carga y deserializa equipo del usuario.
    """
```

---

## 🛍️ store.py

**Líneas:** ~350  
**Responsabilidad:** Tienda y sistemas de compra

### Catálogos

#### `CATALOGO_GLADIADORES`
```python
[
    {"nombre": "Murmillo", "arquetipo": "Guerrero", "precio": 500},
    {"nombre": "Retiarius", "arquetipo": "Velocista", "precio": 500},
    # ... 5 arquetipos
]
```

#### `CATALOGO_ARMAS`
```python
[
    {"nombre": "Gladius Básico", "ataque": 5, "precio": 50},
    {"nombre": "Espada Romana", "ataque": 18, "precio": 300},
    # ... escalado
]
```

#### `CATALOGO_ARMADURAS`
```python
[
    {"nombre": "Túnica", "defensa": 2, "precio": 30},
    {"nombre": "Placas Romanas", "defensa": 15, "precio": 250},
    # ... escalado
]
```

---

### Funciones

#### `comprar_gladiador(equipo, tipo)`
```python
# Valida oro disponible
# Crea nuevo Gladiador
# Añade a equipo
```

#### `comprar_item(equipo, item_id)`
```python
# Valida oro
# Equipar a gladiador seleccionado
```

---

## 🎖️ misiones.py

**Líneas:** ~200  
**Responsabilidad:** Rastreo automático de misiones

### Clases

#### `Mision`
```python
class Mision:
    id: int
    nombre: str
    descripcion: str
    objetivo: str                       # "Ganar 5 combates"
    progreso: int
    objetivo_cantidad: int
    recompensa_xp: int
    recompensa_oro: int
    estado: str                         # ACTIVA, COMPLETADA, RECLAMADA
    
    def puede_reclamarse() -> bool
    def reclamar_recompensas(equipo)
```

---

#### `GestorMisiones`
```python
class GestorMisiones:
    misiones_activas: List[Mision]
    
    def actualizar_progreso(evento: str, valor: int)
    def check_completadas() -> List[Mision]
```

**Tipos de misiones:**
1. Ganar X combates
2. Acumular X oro
3. Alcanzar X críticos
4. Subir nivel a X
5. Obtener X objetos

---

## 📖 guia.py

**Líneas:** ~150  
**Responsabilidad:** Sistema de ayuda en juego

### Funciones

#### `mostrar_guia_rapida()`
```python
# Tutorial básico

# Cubre:
# - Cómo ganar gold
# - Cómo subir nivel
# - Cómo mejorar equipmidero
# - Tips balance
```

#### `mostrar_faq()`
```python
# Preguntas frecuentes
# Respuestas de balance
```

---

## 🔗 Gráfico de Dependencias

```
main.py (ENTRY POINT)
├── models.py (Gladiador, Equipo, Character)
├── narrativa.py (GestorNarrativa) ← NUEVO
├── combat.py
│   ├── enemies.py (generar_enemigo)
│   ├── habilidades.py (aplicar_bonificadores)
│   └── models.py
├── facilities.py
├── auth.py
├── persistence.py
│   └── models.py
├── store.py
│   └── models.py
├── misiones.py
│   └── models.py
└── guia.py
```

---

## 📊 Estadísticas de Código

| Archivo | Líneas | Clases | Funciones |
|---------|--------|--------|-----------|
| main.py | 2278 | 0 | 8 principales |
| models.py | 1033 | 8 | 40+ |
| narrativa.py | 350 | 4 | 20+ |
| combat.py | 400 | 0 | 15+ |
| enemies.py | 200 | 2 | 10+ |
| habilidades.py | 600 | 3 | 25+ |
| facilities.py | 300 | 2 | 20+ |
| auth.py | 100 | 0 | 5 |
| persistence.py | 250 | 0 | 8 |
| store.py | 350 | 0 | 15+ |
| misiones.py | 200 | 2 | 12+ |
| guia.py | 150 | 0 | 6 |
| **TOTAL** | **~6500** | **~21** | **~175** |

---

*Documento actualizado a Fase 3 - referencia para desarrollo y debugging*
