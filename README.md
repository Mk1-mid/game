# ⚔️ SANGRE POR FORTUNA - Simulador de Gladiadores Romanos

**Versión:** 3.0 | **Estado:** 🔄 Fase 3 (El Alma del Juego) - 75% Completada

Simulador de gladiadores en la antigua Roma escrito en **Python puro**. Gestiona tu equipo de gladiadores, combate en la arena, acumula riquezas y ¡observa historias narrativas desarrollarse en tu ludus!

---

## 📚 DOCUMENTACIÓN

**👉 PUNTO DE ENTRADA:** [docs/INDICE.md](docs/INDICE.md)

Desde ahí accedes a toda la documentación organizada de forma clara.

### Acceso Rápido
- **Nuevo en el proyecto?** → [docs/COMIENZA_AQUI.md](docs/COMIENZA_AQUI.md)
- **Desarrollador?** → [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md)
- **Qué cambió?** → [CHANGELOG.md](CHANGELOG.md)
- **Planes futuros?** → [docs/roadmap-sangre-fortuna.md](docs/roadmap-sangre-fortuna.md)

---

## 🎮 Características Principales

### ✅ Fase 1-2: Motor y Mec. Core (100% Completadas)

**Sistema de Progresión**
- Experiencia y Niveles (XP scaling: 100 * 1.1^nivel)
- Stats dinámicos que escalan con cada nivel
- 5 arquetipos con habilidades especiales

**Combate y Recompensas**
- Combate turn-based por turnos
- 4 Dificultades de Arena (Novato-Legendaria)
- Enemigos escalados dinámicamente
- Recompensas proporcionales a dificultad

**Sistemas Secundarios**
- Autenticación y guardado persistente
- Tienda, armería y mercado
- Misiones automáticas
- Ligas competitivas

### 🆕 Fase 3: El Alma (75% Completada - **NUEVO**)

**🎭 Motor de Narrativa**
- 12 eventos únicos (Festival, Rebelión, Patrocinio, etc.)
- 80+ resultados posibles basados en decisiones
- Probabilidades ponderadas según estado del equipo

**⭐ Sistema de Fama y Reputación**
- Atributo `fama` en Gladiador y Equipo
- Ganancia/pérdida automática en arena
- Desbloquea eventos especiales y mejores precios

**⏳ Paso del Tiempo (Días)**
- Opción 8: "Pasar Día" en menú principal
- Recuperación pasiva de HP
- Procesamiento automático de eventos narrativos
- Efectos temporales (buffs/debuffs)

**Ejemplo de Evento:**
```
Festival de Gladiadores
"Se aproxima un evento importante..."
├─ Participar → +Fama, posible herida
└─ Descansar → Sin cambios
```

## 🚀 Inicio Rápido

### Requisitos
- Python 3.7+

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecutar el juego
```bash
python main.py
```

**Usuario de prueba:**
- Usuario: `admin`
- Contraseña: `123`

## 📁 Estructura del Proyecto

```
juego/
├── src/                           Código fuente
│   ├── models.py                  ✅ Clases con progresión
│   ├── combat.py                  ✅ Sistema de combate + XP
│   ├── store.py                   Tienda/armería
│   ├── enemies.py                 Generación de enemigos
│   ├── auth.py                    Autenticación y guardado
│   └── persistence.py             Persistencia de datos
│
├── data/                          Datos persistentes
│   ├── users.json
│   └── saves/
│
├── docs/                          📚 DOCUMENTACIÓN UNIFICADA
│   ├── README.md                  Inicio
│   ├── main/
│   │   ├── INDICE.md              Guía de navegación
│   │   ├── TECNICA.md             Referencia técnica
│   │   └── CHANGELOG.md           Historial
│   ├── desarrollo/
│   │   ├── ESTRUCTURA.md          Detalles técnicos
│   │   └── GUIA_DESARROLLO.md     Cómo extender
│   └── legados/                   Archivos históricos
│
├── main.py                        Punto de entrada
├── test_proyecto.py               Verificación de integridad
└── requirements.txt               Dependencias
```

## 📊 Sistema de Progresión (v2.0)

### XP y Niveles
- Fórmula: `XP_requerido = 100 * (1.1 ^ nivel)`
- Nivel 1→5: ~30 minutos | Nivel 5→15: ~2-3 horas
- Nivel 15→30: ~10+ horas | Nivel 30→50: ~50+ horas

### Escalado de Stats (Rendimientos Decrecientes)
| Nivel | HP | ATK | DEF | SPD |
|-------|-----|------|------|------|
| 1 | 100 | 20 | 5 | 10 |
| 5 | 148 | 24 | 5.8 | 10.8 |
| 10 | 218 | 29 | 6.5 | 11.5 |
| 20 | 391 | 42 | 8.5 | 13.5 |
| 30 | 659 | 65 | 11 | 16 |
| 50 | 1,427 | 133 | 18 | 25 |

### Recompensas Dinámicas
```
Nivel 1:  ~51 XP por victoria
Nivel 5:  ~96 XP por victoria
Nivel 10: ~204 XP por victoria
Nivel 20: ~400+ XP por victoria
```

## 🎯 Sistema de Combate

- **Automático**: El gladiador lucha según sus estadísticas
- **Escalado**: Enemigos escalan dinámicamente con el jugador
- **Velocidad**: Determina orden de ataque
- **Daño**: Variación aleatoria ±20% para realismo
- **Defensa**: Reduce 50% del daño recibido

## 👥 Tipos de Enemigos

1. **Murmillo** - Tanque pesado (Alto HP/DEF, lento)
2. **Retiarius** - Rápido pero frágil (Alto SPD, bajo HP)
3. **Secutor** - Equilibrado (Stats balanceadas)
4. **Thraex** - Agresivo (Alto ATK, baja DEF)
5. **Hoplomachus** - Defensivo (Alta DEF/HP)

*Todos escalan dinámicamente según el nivel del jugador*

## 💰 Economía del Juego

- **Ganar:** 50-5000+ oro por combate (según nivel y dificultad)
- **Gastar:** 150-2000 oro por entrenamientos, items, curación
- **Inversión:** Dinero genera más dinero (equipo → victorias → dinero)

## 🧪 Testing

```bash
python test_proyecto.py
```

Verifica integridad de módulos, clases y funciones.

## 📈 Estado de v2.0

### ✅ Implementado
- [x] Sistema de experiencia y niveles completo
- [x] Clase Gladiador con progresión independiente
- [x] Cálculo de recompensas XP dinámico
- [x] Fórmulas de escalado logarítmico
- [x] Guardado/carga de progresión

### 🔶 En Progreso
- [ ] Expandir catálogo de items (20+ items)
- [ ] Sistema de pociones/consumibles
- [ ] Vender items del inventario
- [ ] Mostrar progresión en UI

### ❌ Próximo (v2.1+)
- [ ] Arenas con 5 dificultades
- [ ] Misiones/quests con objetivos
- [ ] Habilidades especiales
- [ ] Árbol de talentos
- [ ] Tablas de clasificación

## 🎓 ¿Cómo Jugar?

### Conceptos Básicos
1. **Recluta gladiadores** → Les das nombre y tipo
2. **Entrena** → Mejoran stats diariamente
3. **Equipa** → Compra armas y armaduras en la tienda
4. **Combate** → Envíalos a la arena por dinero y XP
5. **Repite** → El ciclo continúa indefinidamente

### Estrategia
- Nivel 1-5: Acumula dinero inicial
- Nivel 5-15: Diversifica equipo
- Nivel 15-30: Optimiza recompensas
- Nivel 30+: Competencia y minmax

## 💡 Próximas Mejoras Planeadas

**v2.1 (1-2 semanas):** Items + Pociones + UI
**v2.2 (2-3 semanas):** Misiones + Habilidades + Arenas
**v3.0 (3-4 semanas):** Profundidad + Balance
**v4.0 (1+ mes):** GUI gráfica + Eventos

*Ver [documentacion/CHANGELOG.md](documentacion/CHANGELOG.md) para detalles completos*

## 🎮 Características Destacadas

✨ **Progresión Logarítmica:** No te vuelves overpowered nunca
✨ **Equipo Independiente:** 6 gladiadores con progresión propia
✨ **Economía Balanceada:** Dinero nunca es trivial
✨ **Recompensas Dinámicas:** XP y oro escalan con nivel
✨ **Diseño Modular:** Fácil de extender

## 📧 Notas de Desarrollo

- Juego 100% Python - sin dependencias gráficas requeridas
- Persistencia JSON - fácil de debuguear
- Arquitectura OOP - escalable
- Balance de dificultad - 50% winrate mantenido en escalado

---

## 🔗 Enlaces Principales

- 📖 **Documentación Completa:** [documentacion/DOCUMENTACION_COMPLETA.md](documentacion/DOCUMENTACION_COMPLETA.md)
- 📝 **Historial de Cambios:** [documentacion/CHANGELOG.md](documentacion/CHANGELOG.md)
- 🏗️ **Arquitectura Técnica:** [docs/ESTRUCTURA.md](docs/ESTRUCTURA.md)
- 🛠️ **Guía de Desarrollo:** [docs/GUIA_DESARROLLO.md](docs/GUIA_DESARROLLO.md)

---

**¡Que comience la batalla!** ⚔️

*Última actualización: 7 de Enero de 2026*  
*Versión: 2.0.0*
