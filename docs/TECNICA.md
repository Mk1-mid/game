# 🔧 TECNICA.md — Referencia Técnica Completa

**SANGRE POR FORTUNA — v2.2**

Simulador de gestión de gladiadores en la Roma Antigua, en Python puro. El jugador gestiona un equipo de hasta 6 gladiadores: los recluta, entrena, equipa y envía a combatir, administrando dinero, tiempo y salud. Los gladiadores pueden morir permanentemente.

---

## 1. Arquitectura y estructura del proyecto

### Estructura de carpetas

```
game/
├── main.py                 # Punto de entrada (menús y flujo principal)
├── requirements.txt        # Dependencias (pygame, solo música)
├── assets/musica.mp3       # Música
├── src/                    # Código fuente
├── data/                   # users.json, saves/, misiones_<usuario>.json
├── tests/                  # Suite de tests
├── docs/                   # Documentación (TECNICA, ROADMAP, HISTORIAL)
└── legacy/                 # Código v1 (referencia, no se usa)
```

### Módulos de `src/`

| Módulo | Responsabilidad | Elementos clave |
|---|---|---|
| `models.py` | Clases de datos | `Item`, `Weapon`, `Armor`, `Character`, `Gladiador`, `Equipo`, `Barracas`, enemigos; métodos `hp_final()`, `ataque_final()`, `subir_nivel()` |
| `combat.py` | Combate por turnos | `calcular_daño()` (±20%), `calcular_xp_recompensa()`, `combate_arena()`, `verificar_triggers_combate()`, `mostrar_habilidad_activada()` |
| `habilidades.py` | Arquetipos y habilidades | `TipoHabilidad`, `TipoTrigger`, `HABILIDADES_POR_ARQUEOTIPO`, `verificar_y_activar_triggers()`, bonificadores pasivos/activos |
| `misiones.py` | Sistema de misiones | `GestorMisiones`, 23 misiones en 4 capas, auto-tracking, `guardar_estado()`/`cargar_estado()` |
| `facilities.py` | Médico y herrero | Curación progresiva (básica/profunda/completa/rápida), revivir, mejora de armas con % por tier y durabilidad |
| `store.py` | Tienda y mercado | `CATALOGO_ARMAS`, `CATALOGO_ARMADURAS`, pociones, mercado de gladiadores, `comprar_item()`, `vender_item()` |
| `enemies.py` | Generación de enemigos | `generar_enemigo()` (escalado por nivel), `mostrar_info_enemigo()`, 5 tipos de enemigos |
| `auth.py` | Autenticación | `registrar_usuario()`, `iniciar_sesion()` (3 intentos), `cargar_partida()`, `guardar_partida()` |
| `persistence.py` | Serialización | `serializar_equipo()`/`deserializar_equipo()`, guardado de facilities |
| `guia.py` | Ayuda en juego | Guía de estructura y troubleshooting |

### Flujo del programa

```
INICIO → Autenticación (login/registro) → Cargar/crear partida
  → MENÚ PRINCIPAL
      1. Arena        → elegir dificultad → combate_arena() → recompensas/XP
      2. Barracas     → ver equipo, reclutar, entrenar, vender, ampliar
      3. Hospital     → curar / revivir
      4. Mercado      → comprar/vender gladiadores
      5. Armería      → catálogo → comprar → equipar
      6. Ver equipo   → estadísticas
      7. Misiones     → progreso, reclamar recompensas
      8. Guardar
      9. Salir (guardado automático)
```

Dependencias: Python 3.7+, pygame opcional. Ejecución: `python main.py`. Usuario de prueba: `admin/123`.

---

## 2. Modelos de datos

### Clases principales

- **Item / Weapon / Armor**: items (arma = ataque+agilidad; armadura = defensa+HP).
- **Character**: base con `hp`, `attack`, `defense`, `agilidad`, equipo (`weapon`, `armor`) y métodos `*_final()` (base + bonus de equipo).
- **Gladiador**: personaje jugable con progresión independiente — `nivel`, `xp`, `hp_actual`, `estado` (sano/herido/crítico/muerto), `ocupacion` (disponible/ocupado con días), `habilidades`, `contadores_triggers`, historial de combates y `dinero_generado`.
- **Equipo**: lista de gladiadores (máx. según barracas), `dinero`, nivel promedio.
- **EnemyVariant** y derivados: enemigos con escalado por nivel.

### Progresión y escalado

El poder crece **logarítmicamente**: cada nivel cuesta más XP y aporta menos mejora relativa.

- **XP requerida:** `XP_requerido = 100 * (1.1 ^ nivel)`
- **Stats por nivel:** `hp ×1.095`, `attack ×1.085`, `defense ×1.075`, `agilidad ×1.065`

| Nivel | HP | ATK | DEF | SPD |
|---|---|---|---|---|
| 1 | 100 | 20 | 5.0 | 10.0 |
| 5 | 148 | 24 | 5.8 | 10.8 |
| 10 | 218 | 29 | 6.5 | 11.5 |
| 20 | 391 | 42 | 8.5 | 13.5 |
| 30 | 659 | 65 | 11 | 16 |
| 50 | 1.427 | 133 | 18 | 25 |

Nivel 1→20 = 3–4× stats; nivel 40→50 ≈ +5% (rendimientos decrecientes).

**Recompensa de XP** (`calcular_xp_recompensa()`): `50 * (1.15 ^ nivel)` con variación ±10%. `ganar_xp()` encadena subidas de nivel automáticamente.

### Sistema de días y ocupaciones

Cada gladiador realiza **1 acción por día**:

- **Entrenamiento** (1–3 días, 100g/día): +stats, ocupa al gladiador.
- **Curación** (1–3 días, costo según urgencia): restaura HP.
- **Cuartel** (sin ocupación): +10% HP/día.

---

## 3. Sistema de combate

- Combate **automático por turnos** (`combate_arena()`).
- `calcular_daño(ataque, defensa)`: variación aleatoria **±20%**; la defensa reduce el daño recibido; daño mínimo 1.
- La **agilidad** determina el orden de actuación.
- El equipo modifica stats vía métodos `*_final()`.
- Integración de habilidades: bonificadores pasivos + activación por triggers durante el combate.

### Dificultades de arena

| Arena | Enemigo | Multiplicador | Nivel requerido |
|---|---|---|---|
| 🟢 Novato | nivel −2 | ×0.8 | 1 |
| 🟡 Normal | nivel +0 | ×1.0 | 3 |
| 🔴 Experto | nivel +3 | ×1.5 | 10 |
| ⭐ Legendaria | nivel +5 | ×2.0 | 20 |

El menú muestra análisis de riesgo, probabilidad de victoria estimada y recompensas aproximadas. Además, un sistema de **ligas** (Bronce/Plata/Oro/Leyenda) registra puntos, W/L e historial por gladiador.

---

## 4. Habilidades y balance de arquetipos

### Los 5 arquetipos

Mapeo tipo de gladiador → arquetipo (`src/models.py`):

```python
arqueotipos_mapping = {
    "Murmillo":     "Guerrero",   # Fuerte y defensivo
    "Retiarius":    "Velocista",  # Rápido y ágil
    "Secutor":      "Paladín",    # Balanceado
    "Thraex":       "Asesino",    # Ofensivo y crítico
    "Hoplomachus":  "Tanque",     # Defensivo puro
}
```

### Tabla de bonificadores

| Stat | Guerrero | Velocista | Asesino | Tanque | Paladín |
|---|---|---|---|---|---|
| FUERZA | +14% | +5% | +5% | +2% | +12% |
| AGILIDAD | +3% | +15% | +5% | +4% | +5% |
| DEFENSA | +8% | +3% | +1% | +23% | +15% |
| CRÍTICO | +10% | +12% | +26% | +7% | +10% |
| ESQUIVA | +2% | +8% | +10% | +5% | +2% |
| HP MAX | 0% | 0% | 0% | +10% | 0% |
| **Total** | **40%** | **44%** | **43%** | **44%** | **46%** |

Balance: variación total ±10% entre arquetipos.

### Habilidades

- **25 habilidades** (5 por arquetipo): 15 pasivas (siempre activas) + 10 activas (por triggers).
- Definidas en `src/habilidades.py` (`HABILIDADES_POR_ARQUEOTIPO`).
- El `Gladiador` las recibe automáticamente al crearse.

### Triggers (6 tipos)

| Trigger | Condición |
|---|---|
| `SALUD_BAJO` | HP < 30% |
| `ESQUIVAS_CONSECUTIVAS` | 3 esquivas |
| `CRITICOS_RECIBIDOS` | 2+ críticos recibidos |
| `CRITICOS_PROPIOS` | 2+ críticos infligidos |
| `DAÑO_RECIBIDO` | Daño alto en un turno |
| `TURNOS_COMBATE` | Cada X turnos |

### Recomendaciones de uso

- Principiantes: Guerrero o Paladín. Agresivo: Asesino o Guerrero.
- Defensivo: Tanque. Versátil: Velocista o Paladín.

---

## 5. Economía y facilidades

- **Tienda/armería:** 13 armas + 13 armaduras en 4 tiers (50g–1200g), 5 pociones, venta al 50% del precio.
- **Costes de gestión:** reclutamiento ~300g; entrenamiento 100g/día; curación según urgencia (20–100g/día).
- **Ingresos:** victorias según dificultad (base 150–350g, ×multiplicador de arena).
- **Médico:** curación básica/profunda/completa con ocupación en días; curación rápida desbloqueable (inmediata, 1 uso/día); revivir; mejorable en 5 niveles.
- **Herrero:** mejora de armas con **% por tier (+8%/+12%/+15%/+20%)**, coste cuadrático (`base × tipo × nivel²`), **durabilidad** (−5% por mejora, reparable: `(100 − durab) × base / 10`), niveles 1–5 desbloquean tiers.

---

## 6. Guía de desarrollo

### Convenciones

- Clases: PascalCase (`Gladiador`); funciones: snake_case (`calcular_daño`); constantes: UPPER_SNAKE_CASE (`CATALOGO_ARMAS`); privadas: prefijo `_`.
- Docstrings obligatorios (descripción, `Args:`, `Returns:`). Máx. ~100 caracteres/línea. Imports: stdlib → third-party → locales.

### Cómo extender

**Nuevo item** (`src/store.py`):
```python
CATALOGO_ARMAS["XX"] = Weapon("Mi Arma", attack=15, tier=2)
```

**Nuevo enemigo** (`src/enemies.py`): añadir clase con `hp/attack/defense/agilidad` y registrarla en el generador.

**Nueva mecánica**: crear módulo en `src/`, importarlo en `main.py`, añadir opción a `mostrar_menu_principal()` y su rama en `juego_principal()`.

### Testing

```bash
python tests/run_tests_new.py
```

### Troubleshooting

| Problema | Solución |
|---|---|
| `ModuleNotFoundError: No module named 'src'` | Ejecutar desde la raíz del proyecto |
| Usuarios corruptos | Borrar `data/users.json` (se recrea con `admin/123`) |
| Sin música | `pip install pygame` + `assets/musica.mp3` |
| Caracteres raros en consola Windows | Ejecutar con `PYTHONUTF8=1` |
| No inicia | `pip install -r requirements.txt`, `python main.py` |
