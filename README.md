# 🏛️ SANGRE POR FORTUNA - Juego de Gladiadores

**Versión:** 4.0 (Fase 4 — Árbol de Talentos) | **Estado:** ✅ Funcional

Simulador de gladiadores en la antigua Roma escrito en **Python puro** (consola). Gestiona un equipo de hasta 6 gladiadores: reclútalos, entrénalos, equípalos, cúralos y envíalos a combatir en la arena por dinero y experiencia.

---

## 🚀 Inicio Rápido

### Requisitos
- Python 3.7+
- `pygame` (opcional, solo para música)

### Instalación y ejecución

```bash
pip install -r requirements.txt
python main.py
```

**Usuario de prueba:** `admin` / `123`

### Tests

```bash
python tests/run_tests_new.py
```

---

## 🎮 Características

- **Sistema de progresión:** XP y niveles logarítmicos (`XP = 100 * 1.1^nivel`), stats que escalan con rendimientos decrecientes, **puntos de talento** por nivel
- **Árbol de talentos:** 4 ramas (Fuerza, Resistencia, Agilidad, Técnica) × 5 niveles, habilidades únicas en nivel 5
- **Sistema de equipo:** hasta 6 gladiadores con estado, ocupación (entrenamiento/curación) e historial propios
- **5 arquetipos:** Murmillo, Retiarius, Secutor, Thraex, Hoplomachus — cada uno con 5 habilidades propias
- **Combate:** automático por turnos con habilidades, triggers y dificultades de arena (Novato → Legendaria)
- **Gestión:** barracas, hospital/médico, herrero (mejora de armas), armería, mercado de gladiadores
- **Misiones:** 23 misiones con auto-tracking y notificaciones
- **Sistema de ligas:** ranking y puntos por combate
- **Leaderboards globales:** 3 rankings Top 10 entre todos los jugadores (victorias, fortuna, nivel) con récords históricos
- **Persistencia:** autenticación, partidas guardadas en JSON, multiusuario

## 📁 Estructura del Proyecto

```
game/
├── main.py                # Punto de entrada
├── requirements.txt       # Dependencias (pygame)
├── assets/
│   └── musica.mp3         # Música del juego
├── src/                   # Código fuente
│   ├── models.py          # Gladiador, Equipo, items
│   ├── combat.py          # Combate por turnos
│   ├── habilidades.py     # Habilidades y arquetipos
│   ├── misiones.py        # Sistema de misiones
│   ├── facilities.py      # Médico y herrero
│   ├── store.py           # Tienda y mercado
│   ├── enemies.py         # Generación de enemigos
│   ├── auth.py            # Autenticación
│   ├── persistence.py     # Persistencia JSON
│   └── guia.py            # Guía en juego
├── data/                  # Datos persistentes
│   ├── users.json         # Usuarios
│   ├── saves/             # Partidas guardadas
│   └── misiones_*.json    # Misiones por usuario
├── tests/                 # Suite de tests
├── docs/                  # Documentación (3 documentos)
│   ├── TECNICA.md         # Referencia técnica completa
│   ├── ROADMAP.md         # Estado actual y planes
│   └── HISTORIAL.md       # Historial del desarrollo
└── legacy/                # Código v1 (solo referencia, no se usa)
```

---

## 📚 Documentación

> ⚠️ **Si eres un agente de IA trabajando en este proyecto:** lee primero [AGENTS.md](AGENTS.md) — contiene las convenciones, patrones y reglas obligatorias del proyecto.

| Documento | Contenido |
|-----------|-----------|
| [AGENTS.md](AGENTS.md) | Convenciones del proyecto para agentes de IA (reglas obligatorias) |
| [docs/TECNICA.md](docs/TECNICA.md) | Arquitectura, modelos, combate, habilidades, balance, guía de desarrollo |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Estado actual, fases completadas y plan futuro |
| [docs/HISTORIAL.md](docs/HISTORIAL.md) | Línea de tiempo del desarrollo y changelog |

---

## 🎯 Cómo Jugar

1. **Recluta** gladiadores con nombre y tipo
2. **Entrena** para mejorar stats (cuesta días y oro)
3. **Equipa** armas y armaduras de la armería
4. **Combate** en la arena por dinero y XP (elige dificultad)
5. **Cura** a tus heridos en el médico y **mejora** armas en el herrero
6. **Completa misiones** y sube en el ranking de ligas
7. **Asigna talentos** para especializar a tus gladiadores (4 ramas × 5 niveles)

---

**¡Que comience la batalla!** ⚔️
