# 🏛️ SANGRE POR FORTUNA - Juego de Gladiadores

**Versión:** 2.2 (Fase 2.2 - Sistema de Habilidades Pulido) | **Estado:** ✅ Funcional

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

- **Sistema de progresión:** XP y niveles logarítmicos (`XP = 100 * 1.1^nivel`), stats que escalan con rendimientos decrecientes
- **Sistema de equipo:** hasta 6 gladiadores con estado, ocupación (entrenamiento/curación) e historial propios
- **5 arquetipos:** Murmillo, Retiarius, Secutor, Thraex, Hoplomachus — cada uno con 5 habilidades propias
- **Combate:** automático por turnos con habilidades, triggers y dificultades de arena (Novato → Legendaria)
- **Gestión:** barracas, hospital/médico, herrero (mejora de armas), armería, mercado de gladiadores
- **Misiones:** 23 misiones con auto-tracking y notificaciones
- **Sistema de ligas:** ranking y puntos por combate
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

| Documento | Contenido |
|-----------|-----------|
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

---

**¡Que comience la batalla!** ⚔️
