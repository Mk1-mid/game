# SANGRE POR FORTUNA - Estructura del Proyecto Reorganizado

## 📁 Estructura de Carpetas

```
juego/
├── src/                      # Código fuente principal
│   ├── __init__.py          # Inicialización del módulo
│   ├── models.py            # Clases de personajes, armas y armaduras
│   ├── combat.py            # Sistema de combate por turnos
│   ├── store.py             # Sistema de tienda/armería
│   ├── enemies.py           # Generación de enemigos
│   └── auth.py              # Autenticación y guardado de partidas
│
├── data/                    # Datos persistentes
│   ├── users.json           # Base de datos de usuarios
│   └── saves/               # Archivos de partidas guardadas
│       ├── save_admin.json
│       ├── save_usuario.json
│       └── ...
│
├── docs/                    # Documentación del proyecto
│   ├── README.md            # Inicio
│   ├── main/
│   │   ├── INDICE.md        # Índice de documentación
│   │   ├── TECNICA.md       # Referencia técnica
│   │   └── CHANGELOG.md     # Historial de versiones
│   ├── desarrollo/
│   │   ├── ESTRUCTURA.md    # Este archivo
│   │   └── GUIA_DESARROLLO.md
│   └── legados/             # Archivos históricos
│
├── tests/                   # Pruebas unitarias
│   ├── test_combat.py
│   ├── test_models.py
│   └── test_store.py
│
├── main.py                  # Punto de entrada del juego
├── requirements.txt         # Dependencias de Python
└── README.md                # Información general del proyecto
```

## 🎮 Módulos Principales

### `src/models.py`
Define las clases fundamentales del juego:
- **Item**: Clase base para todos los items
- **Weapon**: Armas (ataque + velocidad)
- **Armor**: Armaduras (defensa + HP)
- **Character**: Clase base para personajes
- **Player**: El gladiador del jugador con progresión XP
- **Gladiador**: Gestión de equipo con estadísticas independientes
- **EnemyBasic, EnemyChampion**: Enemigos básicos y campeones
- Variantes de enemigos: Murmillo, Retiarius, Secutor, Thraex, Hoplomachus

### `src/combat.py`
Sistema de combate automático:
- `calcular_daño()`: Calcula daño con variación ±20%
- `calcular_xp_recompensa()`: XP dinámico según nivel
- `combate_arena()`: Simula un combate por turnos
- `curar_en_base()`: Restaura salud del jugador

### `src/store.py`
Sistema de tienda:
- `CATALOGO_ARMAS`: Diccionario de armas disponibles
- `CATALOGO_ARMADURAS`: Diccionario de armaduras
- `PRECIOS`: Precios de todos los items
- `mostrar_catalogo()`: Muestra items disponibles
- `comprar_item()`: Realiza compra de item
- `menu_armeria()`: Interfaz interactiva de tienda
- `equipar_item()`: Equipa items del inventario

### `src/enemies.py`
Generación de enemigos:
- `generar_nombre_gladiador()`: Crea nombres romanos aleatorios
- Clases de enemigos con diferentes arquetipos
- `generar_enemigo()`: Factory para crear enemigos
- `mostrar_info_enemigo()`: Muestra stats del enemigo

### `src/auth.py`
Gestión de usuarios y partidas:
- `registrar_usuario()`: Crea nueva cuenta
- `iniciar_sesion()`: Login con validación (3 intentos)
- `mostrar_menu_autenticacion()`: Menú de auth
- `crear_nueva_partida()`: Inicializa partida nueva
- `cargar_partida()`: Carga partida guardada
- `guardar_partida()`: Persiste progreso del jugador

### `main.py`
Punto de entrada y bucle principal del juego:
- `mostrar_titulo()`: Pantalla de bienvenida
- `mostrar_menu_principal()`: Menú de opciones
- `mostrar_estadisticas()`: Visualiza progreso del jugador
- `juego_principal()`: Bucle principal del gameplay

## 🎯 Flujo del Juego

```
1. INICIO
   ├── Pantalla de bienvenida
   ├── Autenticación (login/registro)
   └── Cargar/crear partida

2. MENÚ PRINCIPAL
   ├── 1. IR A LA ARENA
   │   ├── Generar enemigo
   │   ├── Iniciar combate
   │   └── Procesar recompensas/daño
   │
   ├── 2. ARMERÍA
   │   ├── Ver catálogo
   │   ├── Comprar items
   │   └── Equipar items
   │
   ├── 3. DESCANSAR
   │   └── Restaurar salud
   │
   ├── 4. ESTADÍSTICAS
   │   └── Ver progreso
   │
   ├── 5. GUARDAR PARTIDA
   │   └── Persistir datos
   │
   └── 6. SALIR

3. FIN
   └── Guardado automático
```

## 🔄 Mejoras Implementadas

✅ **Organización modular**: Código separado por responsabilidad  
✅ **Documentación**: Docstrings en todas las funciones  
✅ **Nombres corregidos**: 'deffense' → 'defense'  
✅ **Estructura de carpetas**: Separación clara entre código, datos y docs  
✅ **Error handling**: Manejo de excepciones en operaciones críticas  
✅ **Código limpio**: Variables y funciones con nombres descriptivos  
✅ **Flexibilidad**: Fácil de extender y mantener  
✅ **Sistema XP/Niveles**: Implementación logarítmica balanceada  

## 📦 Dependencias

- Python 3.7+
- pygame (opcional, solo para música)

Instalar:
```bash
pip install -r requirements.txt
```

## 🚀 Cómo Ejecutar

```bash
python main.py
```

## 👨‍💻 Agregar Nuevas Características

### Nuevo tipo de enemigo:
```python
# En src/enemies.py
class MiEnemigo(EnemyVariant):
    def __init__(self):
        super().__init__(
            nombre=generar_nombre_gladiador(),
            hp=100,
            attack=20,
            defense=10,
            speed=12
        )
        self.tipo = "Mi Enemigo"

# Agregar a TIPOS_ENEMIGOS
TIPOS_ENEMIGOS = [Murmillo, Retiarius, MiEnemigo, ...]
```

### Nuevo item en la tienda:
```python
# En src/store.py
CATALOGO_ARMAS["7"] = Weapon("Nueva Arma", attack=30, speed=2)
PRECIOS["7"] = 400
```

## 📝 Notas

- Los archivos guardados se almacenan en `data/saves/`
- La base de datos de usuarios está en `data/users.json`
- Usuario de prueba: admin / 123
- El dinero se recompensa/pierde según victorias/derrotas
