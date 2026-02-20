# 📚 SUPER ÍNDICE - SANGRE POR FORTUNA

**v3.0 - Fase 3 (El Alma del Juego)**  
**Última actualización:** Febrero 2026

---

## � ¿Por dónde empiezo?

### 👤 Soy Jugador
→ Lee **[COMIENZA_AQUI.md](COMIENZA_AQUI.md)**

### 👨‍💻 Soy Desarrollador
→ Empieza por **[ESTRUCTURA.md](ESTRUCTURA.md)**, luego **[MODULOS.md](MODULOS.md)**

### 🗺️ Quiero saber planes futuros
→ Lee **[ROADMAP.md](ROADMAP.md)**

---

## 📖 Los 5 Documentos Maestros

### 1️⃣ 🏗️ **ESTRUCTURA.md** - Arquitectura
Árbol de directorios, módulos src/, fórmulas, estadísticas

### 2️⃣ ⚔️ **FUNCIONALIDADES.md** - Sistemas
Arquetipos, habilidades, efectos, eventos, progresión, fama

### 3️⃣ 📚 **MODULOS.md** - Código
Detalles de cada archivo en src/, clases, funciones

### 4️⃣ 🗺️ **ROADMAP.md** - Planes
Fase 3 (75%), Fase 4, Fase 5, timeline

### 5️⃣ 🎮 **COMIENZA_AQUI.md** - Jugadores
Guía de inicio, menú, estrategias, FAQ

---

## 🗂️ Archivos Legacy (Deprecados pero aún presentes)

Estos archivos pueden servir como referencia histórica pero **NO DEBEN SER USADOS para desarrollo**:

| Archivo | Era | Usar en su lugar |
|---------|-----|------------------|
| ARQUITECTURA.md | Antigua | ESTRUCTURA.md + MODULOS.md |
| TECNICA.md | Fase 2.0 | Outdated |
| COMPARATIVA_ARQUETIPOS.md | Antigua | FUNCIONALIDADES.md |
| ANALISIS_HABILIDADES_ESTADO.md | Antigua | FUNCIONALIDADES.md |
| Carpetas: archivos/, desarrollo/, historial/ | Legacy | Ignorar |

**Acción:** Estos serán archivados en próxima sesión

---

## 📊 ESTADO ACTUAL - FEBRERO 2026

| Aspecto | Status | Archivo Maestro |
|---------|--------|-----------------|
| **Arquitectura** | ✅ 100% | ESTRUCTURA.md |
| **Sistemas** | ✅ 100% | FUNCIONALIDADES.md |
| **Código** | ✅ 100% | MODULOS.md |
| **Planes** | ✅ Actualizado | ROADMAP.md |
| **Duplicación** | ✅ 0% eliminada | Todos |
| **Documentación** | ✅ Consolidada | Este INDICE |

---

**Última revisión:** Febrero 2026  
*Consolidación de 17 archivos a 5 maestros*

---

## 📁 Estructura de Archivos de Documentación

### En `docs/`
```
COMIENZA_AQUI.md          ← Guía para jugadores
ARQUITECTURA.md           ← Descomposición técnica
roadmap-sangre-fortuna.md ← Planes futuros (Fases 3-5)
INDICE.md                 ← Este archivo

archivos/                 ← Documentos legacy (ignorar)
desarrollo/               ← Guías de desarrollo antiguas
historial/                ← Historial de cambios antiguos
```

### En `raíz/`
```
CHANGELOG.md              ← Historial oficial (use este)
main.py                   ← Punto de entrada
README.md                 ← Info del proyecto (con estado)
DOCUMENTACION.md          ← Legacy (DEPRECATED)
```

---

## 🎭 Fase 3: El Alma del Juego (Actual)

### ¿Qué se agregó?

**1. Motor de Narrativa** (`src/narrativa.py`)
- 12 eventos diferentes
- Más de 80 resultados posibles
- Sistema de probabilidades

**2. Sistema de Fama**
- Atributo en Gladiador y Equipo
- Ganancia/Pérdida automática en arena
- Dispara eventos especiales

**3. Paso del Tiempo**
- Opción 8: "Pasar Día"
- Recuperación pasiva
- Procesamiento de eventos

### ¿Cómo funciona?

```
Usuario elige [8] en menú
    ↓
Equipo descansa (pasar_dia)
    ↓
GestorNarrativa intenta disparar evento
    ↓
Evento presentado con decisiones
    ↓
Consecuencias aplicadas al equipo
```

---

## ⚙️ Sistema de Archivos Legacy (Deprecados)

Estos archivos todavía existen pero **NO DEBEN SER USADOS**:

| Archivo | Razón | Alternativa |
|---------|-------|------------|
| `docs/archivos/*` | Documentación fragmentada | Usar `ARQUITECTURA.md` |
| `docs/historial/*` | Cambios antiguos | Usar `CHANGELOG.md` |
| `DOCUMENTACION.md` | Índice antiguo | Usar `docs/INDICE.md` |
| `docs/desarrollo/*` | Guías desactualizadas | Leer `src/` comentado |

**Recomendación**: Considerar eliminar estos en siguiente refactor.

---

## 🔍 Búsqueda por Tema

### "¿Cómo juego?"
→ [COMIENZA_AQUI.md](COMIENZA_AQUI.md)

### "¿Cómo programo?"
→ [ARQUITECTURA.md](ARQUITECTURA.md)

### "¿Qué se cambió?"
→ [../CHANGELOG.md](../CHANGELOG.md)

### "¿Qué viene después?"
→ [roadmap-sangre-fortuna.md](roadmap-sangre-fortuna.md)

### "¿Dónde está X clase?"
→ Buscar en [ARQUITECTURA.md](ARQUITECTURA.md) sección "Núcleo de Modelos"

### "¿Cómo agregar un evento?"
→ [ARQUITECTURA.md](ARQUITECTURA.md) sección "Motor de Narrativa"

---

## 📊 Cobertura de Documentación

| Aspecto | Cobertura | Archivo |
|---------|-----------|---------|
| **Jugabilidad** | ✅ 100% | COMIENZA_AQUI.md |
| **Arquitectura** | ✅ 100% | ARQUITECTURA.md |
| **Eventos/Narrativa** | ✅ 80% | ARQUITECTURA.md + src/narrativa.py |
| **Habilidades** | ✅ 70% | ARQUITECTURA.md + src/habilidades.py |
| **Misiones** | ✅ 60% | ARQUITECTURA.md + src/misiones.py |
| **Persistencia** | ✅ 80% | ARQUITECTURA.md + src/persistence.py |
| **Combate** | ✅ 75% | ARQUITECTURA.md + src/combat.py |

---

## 🚀 Próximas Acciones Recomendadas

1. **Para Jugadores**: Abre `COMIENZA_AQUI.md` y empieza a jugar
2. **Para Devs**: Lee `ARQUITECTURA.md` sección "Núcleo de Modelos"
3. **Para Team**: Comparte `docs/COMIENZA_AQUI.md` y `CHANGELOG.md`
4. **Para Mantenimiento**: Considera limpiar carpetas `archivos/`, `historial/`, `desarrollo/`

---

**Estado**: Fase 3 en progreso (75% completada)  
**Versión**: 3.0
- Timeline estimado

---

## ✨ ESTADO ACTUAL

### 🎉 [PULIDO_FASE_2.2_COMPLETADO.md](PULIDO_FASE_2.2_COMPLETADO.md)
**Reporte final de Fase 2.2 pulida**
- 3 mejoras implementadas
- Tests validados (4/4 ✅)
- Visual output integrado
- Persistencia mejorada
- UI de habilidades agregada

### ✅ [CHECKLIST_FINAL.md](CHECKLIST_FINAL.md)
**Validación completa del proyecto**
- Checklist de implementación
- Estado antes/después
- Métricas finales
- Listo para producción

---

## 📁 CARPETAS ESPECIALIZADAS

### 🛠️ [desarrollo/](desarrollo/)
**Guías para desarrolladores**
- `GUIA_DESARROLLO.md` - Cómo contribuir
- `ESTRUCTURA.md` - Estructura del código

### 📚 [archivos/](archivos/)
**Documentación detallada y archivos legacy**
- Tests y reportes antiguos
- Cambios históricos
- Auditorías y validaciones

### 📜 [historial/](historial/)
**Cambios y evolución**
- `PERSISTENCIA_REPARADA.md` - Historiales de fixes

### 🏛️ [legados/](legados/)
**Archivos antiguos (referencia)**

---

## 🎯 POR CASO DE USO

### Si eres **NUEVO en el proyecto:**
1. Lee: [COMIENZA_AQUI.md](COMIENZA_AQUI.md)
2. Ejecuta: `python main.py`
3. Lee: [roadmap-sangre-fortuna.md](roadmap-sangre-fortuna.md)

### Si eres **DESARROLLADOR:**
1. Lee: [desarrollo/GUIA_DESARROLLO.md](desarrollo/GUIA_DESARROLLO.md)
2. Consulta: [TECNICA.md](TECNICA.md)
3. Revisor: [archivos/](archivos/)

### Si quieres **ENTENDER HABILIDADES:**
1. Lee: [COMPARATIVA_ARQUETIPOS.md](COMPARATIVA_ARQUETIPOS.md)
2. Técnica: [TECNICA.md](TECNICA.md) - Sección Habilidades
3. Status: [PULIDO_FASE_2.2_COMPLETADO.md](PULIDO_FASE_2.2_COMPLETADO.md)

### Si necesitas **VALIDAR ESTADO:**
1. Estado: [PULIDO_FASE_2.2_COMPLETADO.md](PULIDO_FASE_2.2_COMPLETADO.md)
2. Checklist: [CHECKLIST_FINAL.md](CHECKLIST_FINAL.md)
3. Tests: `python tests/test_pulido_simple.py`

---

## 📊 ESTADO ACTUAL - 7 ENERO 2025

| Sistema | Status | Archivo |
|---------|--------|---------|
| **Combate** | ✅ Funcional | TECNICA.md |
| **Habilidades** | ✅ Pulido | PULIDO_FASE_2.2_COMPLETADO.md |
| **Persistencia** | ✅ Mejorado | TECNICA.md |
| **UI** | ✅ Integrada | PULIDO_FASE_2.2_COMPLETADO.md |
| **Tests** | ✅ 4/4 Passing | CHECKLIST_FINAL.md |
| **Documentación** | ✅ Organizada | Este archivo |

---

## 🔗 REFERENCIAS RÁPIDAS

- **Ejecutar juego:** `python main.py`
- **Tests:** `python tests/test_pulido_simple.py`
- **Código fuente:** `src/`
- **Cambios recientes:** Ver [PULIDO_FASE_2.2_COMPLETADO.md](PULIDO_FASE_2.2_COMPLETADO.md)

---

**Este archivo es el punto central. Todos los otros documentos están aquí referenciados.**

Última revisión: 7 de Enero 2025 ✅
