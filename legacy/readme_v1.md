https://drive.google.com/file/d/1yDryUNF2v6X07LBU_eBcZuSdIddE9ezi/view?usp=sharing 
# 🏛️ SANGRE POR FORTUNA - Juego de Gladiadores

## 📖 Descripción

**Sangre por Fortuna** es un juego de simulación de gladiadores desarrollado en Python puro (consola/terminal). El jugador asume el rol de un entrenador/dueño de gladiadores en la antigua Roma, donde debe gestionar su gladiador, comprar equipo, combatir en la arena y acumular riquezas mientras mantiene vivo a su luchador.

Inspirado en la serie **Domina**, el juego combina estrategia, economía y combate por turnos en un sistema automático donde tu gladiador pelea según sus stats.

---

## 🎮 Características Principales

### ✅ Sistema de Autenticación
- Registro de usuarios con contraseña
- Inicio de sesión con validación (3 intentos)
- Guardado persistente en JSON

### ✅ Sistema de Combate
- Combate por turnos **automático** (estilo entrenador)
- Sistema de velocidad (determina quién ataca primero)
- Daño random (±20% de variación)
- **Defensa activa**: Reduce el 50% del valor de defensa del daño recibido
- Daño simulado vs daño real:
  - **Victoria**: Recibes `daño_base` (desgaste)
  - **Derrota**: Recibes `daño_base * 2` (heridas graves)

### ✅ 5 Tipos de Gladiadores Enemigos
1. **Murmillo**: Tanque pesado (Alto HP y DEF, lento)
2. **Retiarius**: Rápido pero frágil (Alto SPD, bajo HP)
3. **Secutor**: Equilibrado (stats balanceadas)
4. **Thraex**: Agresivo (Alto ATK, baja DEF)
5. **Hoplomachus**: Defensivo (Alta DEF y HP)

### ✅ Sistema de Nombres Aleatorios
# Sangre por Fortuna — Juego de Gladiadores (README limpio)

Resumen
-------
"Sangre por Fortuna" es un juego de consola escrito en Python. El jugador gestiona un gladiador, compra equipo, participa en combates por turnos y administra recursos (dinero y salud). El proyecto está organizado en módulos claros para autenticación, combate, personajes, generación de enemigos y armería.

Relevante para este repositorio
--------------------------------
- Python 3.7 o superior.
- `pygame` es opcional (solo si quieres reproducir música de fondo).

Estructura del proyecto
-----------------------
```
proyecto/
├── main.py            # Entrada del juego y menú principal
├── j.py               # Autenticación y guardado (JSON)
├── combate.py         # Lógica del combate por turnos
├── Character.py       # Clases Player/Enemy/Weapon/Armor
├── enemigo.py         # Generador de enemigos y nombres
├── armeria.py         # Compra, inventario y equipamiento
├── prueba__armeria.py # Script de pruebas de la armería (opcional)
├── users.json         # Usuarios registrados (creado en runtime)
├── save_*.json        # Archivos de partida por usuario
└── readme             # Este archivo
```

Instalación y ejecución
------------------------
1. Asegúrate de tener Python 3.7+.
2. (Opcional) Instala `pygame` si quieres música:

```powershell
pip install pygame
```

3. Ejecuta el juego:

```powershell
python .\main.py
```

Resumen de módulos y responsabilidades
-------------------------------------
- `main.py`: flujo principal, menú, interacción con el jugador y coordinación de módulos.
- `j.py`: autenticación (registro/login), crear/cargar/guardar partidas en JSON.
- `combate.py`: simulador de combate por turnos y cálculo de daño.
- `Character.py`: definiciones de `Item`, `Weapon`, `Armor`, `Character`, `Player` y variantes de enemigo.
- `enemigo.py`: generación de nombres y creación de enemigos con posibles equipamientos.
- `armeria.py`: catálogo, compra, inventario y equipamiento.

Notas sobre el comportamiento (resumen técnico)
---------------------------------------------
- Guardado: las partidas se almacenan en `save_<username>.json` con claves como `dinero`, `salud_jugador`, `inventario_armas`, etc. Usa `dict.get(key, default)` para lecturas seguras.
- Combate: el daño tiene una variación aleatoria aproximada ±20% y la defensa reduce una porción del daño (implementación actual: 50% de la defensa aplicada como reducción). Siempre hay un daño mínimo de 1.
- Velocidad: determina el orden de ataque; en empate el jugador ataca primero.

Casos de prueba recomendados (breve)
-----------------------------------
- Registrar un usuario, iniciar sesión y comenzar una partida.
- Probar comprar y equipar un arma desde `armeria.py`.
- Ejecutar un combate y verificar que la salud y dinero se actualizan y que la partida puede guardarse.

Qué se ha eliminado de este README
---------------------------------
- Se quitaron emoticonos y decoración ASCII innecesaria para mejorar legibilidad.
- Se eliminaron descripciones redundantes y ejemplos demasiado extensos que no aportaban información técnica.

Siguientes pasos sugeridos
-------------------------
- Si quieres, puedo convertir este `readme` en `README.md` (archivo Markdown) y añadir una versión corta en español/inglés.
- Puedo también generar un `requirements.txt` con `pygame` opcional.

Contacto
--------
Para cambios, sugerencias o correcciones de contenido del README dime qué quieres añadir o eliminar.
```bash


