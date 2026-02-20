# 🗓️ ROADMAP - SANGRE Y FORTUNA

**Planes de desarrollo Fase 3 a Fase 6**

---

## 📊 Resumen Ejecutivo

| Fase | Tema | Status | Progreso | Impacto | Objetivo |
|------|------|--------|----------|---------|----------|
| ✅ **1** | Motor Base | Completada | 100% | ⭐⭐⭐ | Funcionamiento básico |
| ✅ **2** | Mecánicas Core | Completada | 100% | ⭐⭐⭐⭐ | Sistema de combate sólido |
| 🔄 **3** | El Alma del Juego | En Progreso | 75% | ⭐⭐⭐⭐⭐ | Narrativa + Fama |
| ⏳ **4** | Expansión Mecánica | No iniciada | 0% | ⭐⭐⭐⭐ | Combate sin armas + Habilidades |
| ⏳ **5** | Interfaz Visual (JUEGO FUNCIONAL) | No iniciada | 0% | ⭐⭐⭐⭐⭐ | Desktop Flet + UI polida |
| ⏳ **6** | Horizontes de Sangre (Expansión Global) | No iniciada | 0% | ⭐⭐⭐⭐⭐ | Navegante + Culturas mundiales |

**Timeline:** Fases 1-3 completadas. Fases 4-5 son el "MVP Pulido". Fase 6 es el "Post-Launch"

---

## 🎭 FASE 3: EL ALMA DEL JUEGO

**Duración:** 6-8 horas | **Prioridad:** CRÍTICA | **Impacto:** 5/5

**Objetivo:** Transformar simulador técnico en experiencia de rol con identidad narrativa y consecuencias reales.

### 3.1 ✅ Sistema de Reputación y Fama

**Status:** ✅ COMPLETADO

**Implementado:**
- Atributo `fama` en `Gladiador` y `Equipo`
- Ganancia en arena (proporcional a dificultad)
- Pérdida en derrota (pequeña)
- Efectos en probabilidad de eventos

**Características:**
- Rango: 0 - 99999 puntos
- Efectos visuales en mens ú
- Modificadores de dificultad según fama
- Incremento de oro por victorias

**Archivo:** `src/models.py` (líneas ~150-200)

---

### 3.2 ✅ Retiro de Veteranos / Sistema de Instructores

**Status:** ⚠️ PARCIAL (Framework existe, instructores no aplican bonus)

**Implementado:**
- Requisito: Nivel 20+
- Opción "Retirar" en menú
- Guardado de instructor retirado

**Falta:**
- Aplicación de bonos pasivos (+5% XP equipo)
- Visualización de instructores
- Beneficio real en progresión

**Archivo:** `src/models.py` (líneas ~300-330)

---

### 3.3 ✅ Eventos Narrativos Diarios

**Status:** ✅ COMPLETADO

**Implementado:**
- 12 eventos únicos
- 80+ resultados posibles
- Sistema de probabilidades ponderadas
- Aplicación de efectos (oro, XP, heridas)

**Eventos:**
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

**Archivo:** `src/narrativa.py` (completamente nuevo)

---

### 3.4 ✅ Casa/Base Mejorable (v1)

**Status:** ✅ FRAMEWORK (sin UI expandida)

**Implementado:**
- `Barracas` con espacios (máx 6)
- Costo de mantenimiento (500g por espacio)
- Sistema de ocupación

**Falta:**
- Expansión dinámica de barracas
- Hospital propio mejorable
- Arena personal
- Mejoras visuales

**Archivo:** `src/models.py` (Barracas clase)

---

### 3.5 ⚠️ Sistema de Efectos Temporales

**Status:** ⚠️ IMPLEMENTADO pero VISUAL INCOMPLETO

**Lo que funciona:**
- Estructura en `Gladiador.efectos_activos[]`
- Aplicación de buffs/debuffs
- Duración en días
- Integración en combate

**Lo que falta:**
- Visualización clara de efectos activos
- Descripción de qué hace cada efecto
- Animación en combate
- Balance de valores numéricos

**Archivo:** `src/models.py`, `main.py`

---

### 3.6 ⚠️ Paso del Tiempo (Días)

**Status:** ✅ IMPLEMENTADO

**Implementado:**
- Botón "Pasar Día" (opción 8)
- Recuperación de HP pasiva
- Curación de heridas
- Procesamiento de efectos
- Disparo de eventos narrativos

**Falta:** Animación visual mejorada

**Archivo:** `src/models.py` (Equipo.pasar_dia()), `main.py`

---

## 📈 ESTADO DETALLADO - FASE 3

### Completado (75%)

✅ Motor de narrativa (100%)
✅ Sistema de fama (100%)
✅ 12 eventos dinámicos (100%)
✅ Paso diario de tiempo (95%)
✅ Framework de efectos (90%)
✅ Barracas mejorable (50%)
✅ Instructores veteranos (20%)

### En Progreso (20%)

🔄 Visualización de efectos (60%)
🔄 Balance de eventos (70%)
🔄 Integración de habilidades (50%)

### Prueba Pendiente (5%)

⏳ E2E de narrativa completa
⏳ Balance económico
⏳ Testing multijugador local

---

## ⚙️ FASE 4: EXPANSIÓN MECÁNICA

**Duración:** 10-12 horas | **Prioridad:** ALTA | **Impacto:** 4/5

**Objetivo:** Agregar sistemas avanzados y preparar base para Fase 6

### 4.1 Sistema de Combate sin Armas (Pankration + Lucha)

**Status:** No iniciado

**Concepto:** Los gladiadores pueden pelear sin equipo, usando solo Fuerza + Agilidad pura

**Mecánicas Nuevas:**
```
Modo Sin Armas:
├─ Se activa al seleccionar "Desarmado" en lugar de arma
├─ Stats base sin bonificadores de equipo
├─ Nuevas acciones de combate
│  ├─ Golpes (Puño)
│  ├─ Patadas (Agilidad)
│  ├─ Llaves de Sumisión (Bloqueo + Daño)
│  ├─ Esquivas Acrobáticas (+30% evasión)
│  └─ Sangrado de Nariz (Efecto de estado)
└─ Habilidades específicas para Sin Armas
   ├─ Pankration Clásico (Grecorromano)
   ├─ Pugilismo (Boxeo griego)
   └─ Lucha Libre (Wrestling romano)
```

**Implementación:**
- Modificar `combat.py`: Detectar si el arma es "None" o "Desarmado"
- Crear `habilidades_pankration.py`: 15 nuevas habilidades
- Expandir `models.py`: Atributo `modo_combate` en Gladiador

**Triggers Específicos:**
- Sangrados acumulados (3+ sangrados = efecto de estado persistente)
- Esquivas consecutivas sin armas (4+ = contrataque automático)
- Combates largos (+20 turnos = fatiga del enemigo)

**Recompensas:**
- Gladiadores que ganan sin armas ganan +50% XP (maestría)
- Desbloquean habilidades híbridas (Arma + Sin Armas)

---

### 4.2 Árbol de Talentos (4 horas)

**Status:** No iniciado

**Sistema:** 1 punto por nivel en 4 ramas (Fuerza, Resistencia, Agilidad, Técnica)

**Detalles:**
```
Árbol de Talentos
├─ RAMA FUERZA (+2 ATK por punto)
├─ RAMA RESISTENCIA (+3 DEF por punto)
├─ RAMA AGILIDAD (+2 ESQUIVA por punto)
└─ RAMA TÉCNICA (+2 CRÍTICO por punto)
```

---

### 4.3 Forja y Mejora de Items (3 horas)

**Status:** No iniciado

**Sistema:** Herrer ería para +1, +2, +3 equipamiento

---

### 4.4 Leaderboards & Torneos Regionales (3 horas)

**Status:** No iniciado

**Sistema:** Rankings globales y eventos temporales

---

## 🎨 FASE 5: EL SALTO VISUAL (JUEGO FUNCIONAL)

**Duración:** 15-20 horas | **Prioridad:** CRÍTICA | **Impacto:** 5/5

**Objetivo:** Migrar a aplicación desktop moderna con Flet. **Este es el "Release Candidate" del juego.**

### 5.1 Refactorización Core (5 horas)

**Tarea:** Separar lógica de UI de lógica de juego

```
ANTES (acoplado):
src/main.py
├─ print() [UI]
├─ input() [UI]
└─ lógica de juego [Lógica]

DESPUÉS (separado):
src/main.py (solo lógica)
src/ui_console.py (UI consola - mantener)
src/ui_flet.py (UI Flet - nueva)
```

**Impacto:**
- Permite múltiples interfaces
- Facilita testing
- Código más limpio

**Archivos:**
- Refactorizar `main.py`
- Crear `src/ui_console.py` (move print/input)
- Crear `src/ui_flet.py` (nueva)

---

### 5.2 Interfaz Desktop con FLET (12 horas)

**Concepto:** App moderna con:
- 🎴 Tarjetas interactivas
- 📊 Logs de combate animados
- 🎨 Menúes visuales
- 📱 Responsive design

**Pantallas Principales:**
1. Login / Crear Equipo
2. Menú Principal (Hub Central)
3. Arena (selección dificultad, combate en vivo)
4. Barracas (entrenamientos + talento)
5. Mercado (compra de gladiadores)
6. Armería (equipamiento + forja)
7. Estadísticas (visualización detallada)
8. Eventos Narrativos (cinemáticas)
9. Misiones (tracking visual)

**Stack:**
- Framework: Flet (UI multiplataforma)
- Language: Python 3.8+
- Datos: JSON persistente (ya existe)

**Archivos:** Crear `src/ui_flet.py` (~2000 líneas)

---

### ✅ FIN DE FASE 5 = JUEGO COMPLETO 1.0

**En este punto:**
- ✅ Toda mecánica de Fases 1-4 funcional
- ✅ UI pulida y jugable
- ✅ Listo para "Release"
- ✅ Base sólida para expansiones futuras

---

## 🌍 FASE 6: HORIZONTES DE SANGRE (Expansión Global Post-Launch)

**Duración:** 20-25 horas | **Prioridad:** Post-Launch | **Impacto:** 5/5

**Objetivo:** Transformar juego local en imperio global de entretenimiento y exploración comercial.

### 6.1 Sistema Base: El Navegante Misterioso (5 horas)

**Status:** No iniciado

**Concepto:** Un navegante aparece ofreciendo rutas comerciales a cambio de oro

**Mecánicas:**
```
El Navegante:
├─ Aparece como evento oculto (1% chance cada día, si fama > 500 y oro > 5000)
├─ Sistema de "Doble o Nada"
│  ├─ Inviertes 10,000 oro
│  ├─ Navega 20+ días
│  ├─ Regresa con ganancias o NADA
│  └─ Tensión de incertidumbre (cada 5 días: un mensaje de progreso)
└─ Escalas progresivas
   ├─ Escala 1 (Cercana): Bajo riesgo, bajo reward
   ├─ Escala 2 (Media): Riesgo moderado, reward mediano
   ├─ Escala 3 (Lejana): Alto riesgo, reward alto
   └─ Escala 4 (Extrema): Riesgo crítico, reward épico
```

**Archivo Nuevo:** `src/expeditions.py`

---

### 6.2 Ruta Continental: Egipto (4 horas)

**Primer destino:** Cercano, introducción amigable

**Desbloqueos:**
- Mercado de Alejandría (armas exóticas + gladiadores)
- Posibilidad de construir Coliseo en Egipto (generador de oro pasivo)
- Arquetipos: Maestro del Nilo (híbrido de defensa/agilidad)
- Items: Khopesh, Escudo de Piedra, Vendas de Lino

---

### 6.3 Ruta Marítima: Asia Insólita (8 horas)

**Destinos Múltiples:**
```
India:
├─ Elefantes de Guerra (eventos de arena únicos)
├─ Especias y Medicinas (buffs permanentes)
└─ Arquetipos: Rajá Legendario

China:
├─ Maestro de Kung Fu (combate sin armas puro)
├─ Nuevas habilidades: Postura del Tigre, Postura de la Grulla
├─ Arma: Bastón de Guerra
└─ Mayor chance de fracaso (40%)

Japón:
├─ Katana (arma rota si no se balancea bien)
├─ Iaijutsu (primer ataque crítico automático)
├─ Arquetipos: Samurai/Ronin
└─ Mayor chance de fracaso (50%)
```

---

### 6.4 Gran Travesía: El Nuevo Mundo (7 horas)

**El Destino Legendario:** Riesgo 80%, Reward 5x

**Culturas Implementadas:**
```
Aztecas/Mexicas:
├─ Arquetipo: Guerrero Jaguar
├─ Arma: Macuahuitl (ignora armaduras pesadas)
├─ Habilidad: Sacrificio de Sangre (5% HP → +20% ATK)
└─ Arena: Selva peligrosa (trampas, animales)

Mayas:
├─ Especialidad: Navegación de calendario (predict eventos)
├─ Item: Obsidiana tallada (cuchillas de precisión)
└─ Bonus: +15% XP ganado

Diné/Apaches:
├─ Especialidad: Emboscadas (ataque gratuito antes de combate)
├─ Arma: Tomahawk (arma de corta distancia)
└─ Arena: Cañones y mesas (topografía variable)
```

**Ambiente Único:**
- 🐆 Jaguares, Osos Grizzly, Caimanes
- 🌿 Selva peligrosa (triggers de daño ambiental)
- 💊 Medicinas chamánicas (regeneración "mágica")
- 🏛️ Arenas de piedra volcánica (visual disruptivo)

---

### 6.5 Infraestructura Global (3 horas)

**Inversión en Rutas Comerciales:**

```
Fase de Desarrollo de Ruta:
├─ Fase 1: Primer Viaje (Riesgo total)
├─ Fase 2: Pagas Protección (Reduce riesgo -20%)
├─ Fase 3: Estableces Ruta (Descuento en items)
└─ Fase 4: Coliseo Regional (Generador de oro pasivo)
```

**Archivo Expandido:** `src/expeditions.py` + `models.py`

---

### 6.6 Sistemas de Hibridación (3 horas)

**Concepto:** Los gladiadores pueden mezclar estilos

```
Ejemplos:
├─ Murmillo Japonés (Katana + Escudo Romano)
├─ Thraex Chino (Sin armas + Movimiento de Posturas)
├─ Paladín Azteca (Macuahuitl + Sacrificio de Sangre)
└─ Gladiador "Cosmopolita" (múltiples culturas)
```

**Mecánica:** Atributo `estilos_dominados` en Gladiador

---

## ❌ LO QUE NO ENTRA EN ESTA LISTA

- Interfaz gráfica tridimensional (Godot/Unity sería Fase 7+)
- Multijugador en tiempo real (requiere servidor)
- Blockchain/NFTs (out of scope total)
- VR/Metaverso (no es la visión del proyecto)

---

## 🎯 Próximos Pasos Inmediatos

### Prioridad CRÍTICA (Esta semana)

- [ ] Completar Fase 3 (narrativa al 100%)
- [ ] Testing E2E de Fase 3
- [ ] Documentación de Fase 3 final

### Prioridad ALTA (Próximas 2 semanas)

- [ ] Iniciar Fase 4.1 (Pankration sin armas)
- [ ] Crear `src/pankration.py`
- [ ] Modificar combate para soportar "No Weapon"

### Prioridad MEDIA (Próximas 4 semanas)

- [ ] Fases 4.2, 4.3, 4.4 (Talentos, Forja, Ligas)
- [ ] Refactorización UI para Flet
- [ ] Primeros prototipos Flet

### Prioridad BAJA (Después de Fase 5)

- [ ] Iniciar Fase 6 (Horizontes de Sangre)
- [ ] Crear `src/expeditions.py`
- [ ] Diseño de culturas mundiales

---

## 📋 Historial de Cambios

### Fase 3.0 (Actual)
- ✅ Motor narrativo completo
- ✅ Sistema de fama integrado
- ✅ 12 eventos únicos
- ✅ Paso del tiempo diario
- ✅ Efectos temporales framework
- ✅ Consolidación de documentación

### Fase 2.4
- ✅ Sistema de ligas automáticas

### Fase 2.3
- ✅ Dificultades dinámicas de arena

### Fase 2.2
- ✅ Sistema de habilidades (25 total)
- ✅ 5 arquetipos balanceados

### Fase 2.1
- ✅ Sistema de combate mejorado

### Fase 2.0
- ✅ Items y equipamiento

### Fase 1.0
- ✅ Motor base del juego

---

## 💡 Notas Técnicas

### Principios de Diseño

1. **Balance First**: Todos los arquetipos deben ser viables
2. **Narrativa + Mecánica**: Evento debe tener impacto real
3. **Escalabilidad**: Sistema preparado para Fase 4-5
4. **Polish**: Código comentado, documentado, testeado

### Deuda Técnica Conocida

- [ ] Refactorizar `main.py` (2278 líneas, demasiado grande)
- [ ] Separar UI de lógica
- [ ] Mejorar nombres de variables en combate
- [ ] Más cobertura de tests

### Testing

```
tests/
├─ test_habilidades.py (25 tests)
├─ test_combat_newstats.py (15 tests)
├─ test_fase_4.py (20 tests)
└─ test_completo.py (50+ tests)
```

---

## 🚀 Estimación de Timeline

```
HOY (Fase 3 - 75%):
└─ 3-4 horas: Completar y pulir

SEMANA 1 (Fase 4 Init):
├─ 5 horas: Árbol de Talentos (4.1)
├─ 3 horas: Forja de Items (4.2)
└─ 2 horas: Ligas Expandidas (4.3)

SEMANA 2-3 (Fase 5 Init):
├─ 5 horas: Refactorización Core (5.1)
├─ 10 horas: Prototipo Flet inicial (5.2)
└─ 3 horas: Testing y ajustes

SEMANA 4+ (Fase 5 Polish):
├─ 10 horas: UI completa Flet
├─ 5 horas: Animaciones
└─ 5 horas: Balance final

TOTAL ESTIMADO: 36-42 horas de desarrollo
```

---

## 📞 Contacto / Soporte

Para reportar bugs o sugerir features en el roadmap:
1. Crear issue en el repositorio
2. Seguir template de feature request
3. Reference la fase y componente

---

*Documento de planificación actualizado a Fase 3 - EL ALMA DEL JUEGO*

**Última actualización:** Febrero 2026  
**Próxima revisión:** Cuando Fase 3 alcance 95%
