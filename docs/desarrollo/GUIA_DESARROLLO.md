# Guía de Desarrollo - SANGRE POR FORTUNA

## 📋 Tabla de Contenidos
1. [Arquitectura](#arquitectura)
2. [Convenciones de Código](#convenciones-de-código)
3. [Guía de Extensiones](#guía-de-extensiones)
4. [Testing](#testing)
5. [Troubleshooting](#troubleshooting)

---

## 🏗️ Arquitectura

El proyecto está organizado en una arquitectura modular donde cada módulo en `src/` tiene una responsabilidad clara:

```
src/
├── models.py       ← Objetos y lógica de datos
├── combat.py       ← Mecánica de combate
├── store.py        ← Sistema de compra/venta
├── enemies.py      ← Generación de enemigos
└── auth.py         ← Persistencia y autenticación
```

### Flujo de Datos

```
Usuario (main.py)
    ↓
Auenticación (auth.py)
    ↓
Menú Principal
    ├→ Combate (combat.py)
    │  ├→ Generar Enemigo (enemies.py)
    │  └→ Calcular Daño (models.py)
    │
    ├→ Tienda (store.py)
    │  ├→ Comprar Item (models.py)
    │  └→ Equipar Item (models.py)
    │
    └→ Guardar Partida (auth.py)
```

---

## 📝 Convenciones de Código

### Nombres
- **Clases**: PascalCase (ej: `Player`, `Murmillo`)
- **Funciones**: snake_case (ej: `calcular_daño`, `generar_enemigo`)
- **Constantes**: UPPER_SNAKE_CASE (ej: `NOMBRES_ROMANOS`, `PRECIOS`)
- **Variables privadas**: Comienzan con `_` (ej: `_stats_base`)

### Documentación
Todos los módulos, clases y funciones deben tener docstrings:

```python
def mi_funcion(param1, param2):
    """
    Descripción breve de qué hace la función.
    
    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2
    
    Returns:
        Descripción del valor retornado
    """
    pass
```

### Estilo
- Máximo 100 caracteres por línea
- Usa espacios en blanco (4 espacios por indentación)
- Agrupa imports en este orden:
  1. Standard library
  2. Third-party libraries
  3. Local imports

---

## 🔧 Guía de Extensiones

### Agregar Nuevo Tipo de Enemigo

1. **En `src/enemies.py`:**

```python
class MiEnemigo(EnemyVariant):
    """Descripción del tipo de enemigo."""
    
    def __init__(self):
        super().__init__(
            nombre=generar_nombre_gladiador(),
            hp=100,           # Puntos de vida
            attack=20,        # Daño base
            defense=10,       # Defensa base
            speed=12          # Velocidad
        )
        self.tipo = "Mi Enemigo"
```

2. **Agregar a la lista de tipos:**

```python
TIPOS_ENEMIGOS = [Murmillo, Retiarius, Secutor, Thraex, Hoplomachus, MiEnemigo]
```

### Agregar Nuevo Item a la Tienda

1. **En `src/store.py`:**

```python
# Agregar al catálogo
CATALOGO_ARMAS["7"] = Weapon("Mi Nueva Arma", attack=30, speed=2)

# Agregar el precio
PRECIOS["7"] = 400

# Actualizar mostrar_catalogo()
# Agregar línea visual al menú
```

### Agregar Nueva Mecánica de Juego

1. **Crear nuevo módulo en `src/`** (ej: `src/quests.py`)
2. **Importar en `main.py`**
3. **Agregar opción al menú principal**

Ejemplo:

```python
# main.py
from src.quests import menu_quests

# En mostrar_menu_principal()
print("  7. Misiones Especiales")

# En juego_principal()
elif opcion == "7":
    menu_quests(usuario_logueado, dinero, victorias)
```

---

## 🧪 Testing

### Ejecutar Pruebas

```bash
python -m pytest tests/
```

### Escribir Pruebas

Ejemplo: `tests/test_combat.py`

```python
import unittest
from src.combat import calcular_daño

class TestCombat(unittest.TestCase):
    def test_calcular_daño_basico(self):
        daño = calcular_daño(20, 5)
        self.assertGreater(daño, 0)
        self.assertLess(daño, 30)
    
    def test_daño_minimo(self):
        daño = calcular_daño(1, 100)  # Defensa muy alta
        self.assertEqual(daño, 1)

if __name__ == '__main__':
    unittest.main()
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'src'"

**Solución:** Asegúrate de:
1. Ejecutar `python main.py` desde la raíz del proyecto
2. Que exista `src/__init__.py`

### "Archivo de usuarios corrupto"

**Solución:** Elimina o corrige `data/users.json`

```bash
rm data/users.json
# O reinicia con usuario admin/123
```

### Música no se reproduce

**Solución:** 
1. Instala pygame: `pip install pygame`
2. Coloca `musica.mp3` en la raíz del proyecto

### Stats del enemigo no se actualizan con equipo

**Verificar:**
```python
# En enemies.py - generar_enemigo()
# Los métodos hp_final(), ataque_final(), etc. en models.py
```

---

## 📊 Estadísticas del Código

- **Total de líneas**: ~1500
- **Módulos**: 6
- **Clases**: 12+
- **Funciones**: 30+

---

## 🚀 Próximas Mejoras Sugeridas

- [ ] Sistema de niveles para el jugador
- [ ] Mejor IA para enemigos
- [ ] Sistema de quests/misiones
- [ ] Tienda con más variedad
- [ ] Sistema de habilidades especiales
- [ ] Multiplayer (servidor local)
- [ ] Persistencia de equipo

---

¡Happy Coding! ⚔️
