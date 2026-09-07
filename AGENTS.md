# AGENTS.md — Convenciones del proyecto "Sangre por Fortuna"

## 1. 🎮 Descripción del proyecto

Simulador de gestión de gladiadores en la antigua Roma, escrito en **Python puro**, jugado por **consola**, multiusuario, con persistencia en JSON.

- **Punto de entrada:** `main.py`
- **Tests:** `python tests/run_tests_new.py`
- **Estado actual:** ver `docs/ROADMAP.md` para el estado actual de fases (no se duplica aquí, para evitar contradicciones).

---

## 2. ✅ Cómo verificar que algo funciona

Antes de tocar código, y **antes de dar cualquier tarea por terminada**, corre:

```bash
python tests/run_tests_new.py
```

Reglas no negociables sobre esto:

- **Ninguna tarea se considera terminada si `run_tests_new.py` no pasa al 100%.** Si un test falla, el trabajo sigue abierto — no se reporta como completo, no se actualiza `ROADMAP.md`/`HISTORIAL.md` como si lo estuviera.
- **Toda función o sistema nuevo debe venir acompañado de su propia suite de tests** en `tests/`, escrita en el mismo momento en que se escribe la funcionalidad (no después, no "al final de la fase"). Los tests nuevos se integran a `run_tests_new.py` (no quedan como scripts sueltos) para que el comando único de la sección 2 siga siendo la puerta de validación de todo el proyecto.
- Los tests nuevos deben cubrir al menos: caso normal, un caso límite (edge case) y un caso de entrada inválida/error esperado.
- Si una función nueva modifica o depende de datos persistidos (JSON), el test debe verificar también que la serialización/deserialización sobrevive un ciclo completo de guardado y carga.

---

## 3. 🔍 Revisión de compatibilidad entre archivos (obligatoria)

Este proyecto ha tenido errores recurrentes por cambios en un módulo que rompen otro sin que se note de inmediato. Antes de dar por escrita cualquier función nueva o modificada:

1. **Buscar todos los usos existentes** de cualquier función/clase que se esté modificando (`grep`/búsqueda de texto en `src/` y `main.py`) antes de cambiar su firma, su tipo de retorno, o su comportamiento.
2. **Verificar el contrato de datos compartido**: si una función lee o escribe un diccionario/JSON que también usa otro módulo (por ejemplo, el estado de un `Gladiador` usado por `combat.py`, `habilidades.py` y `persistence.py` a la vez), confirmar que la nueva estructura sigue siendo compatible con **todos** los consumidores, no solo con el módulo donde se hizo el cambio.
3. **Confirmar que los patrones de retorno se mantienen** (ver sección 4) — un cambio que rompe la forma `(éxito, costo, mensaje)` en un solo lugar puede romper cualquier código que llame a esa función esperando esa forma.
4. **Si una función nueva depende de otro módulo, declarar esa dependencia explícitamente** (import claro, sin acoplamientos ocultos vía variables globales no documentadas).
5. Si tras esta revisión se detecta una incompatibilidad real entre módulos, **no se resuelve en silencio decidiendo unilateralmente cuál módulo tiene razón** — se reporta como bloqueo y se pregunta antes de decidir el enfoque.

Este paso se hace **antes** de escribir el test, no después — el objetivo es no descubrir la incompatibilidad con un test rojo, sino evitarla desde el diseño de la función.

---

## 4. 📜 Convenciones de código

- **Idioma:** código y documentación en español. Comentarios explican el **por qué**, no el qué (el código ya dice el qué).
- **Estilo:** Python puro; tipos documentados en docstrings (no type hints por ahora, para mantener consistencia con el código existente).
- **Emojis:** se usan en salidas de usuario (menús, mensajes de consola), no en nombres de variables/funciones ni en comentarios de código.
- **Patrones establecidos — seguir, no reinventar:**
  - Funciones de persistencia: `serializar_<entidad>()` / `deserializar_<entidad>()`, `guardar_<algo>()` / `cargar_<algo>()`.
  - Retorno de operaciones con costo/resultado: tupla `(éxito: bool, costo: int, mensaje: str)`. Ejemplo real del patrón, tomado de `facilities.py` (`Herrero.mejorar_arma()`):
    ```python
    def mejorar_arma(self, arma, dinero):
        """
        Mejora un arma aumentando su ATK por porcentaje
        Retorna: (exito, costo, mensaje)
        """
        if not hasattr(arma, 'tier'):
            return False, 0, "❌ Este arma no puede mejorarse"

        costo = self._calcular_costo_mejora(arma)

        if dinero < costo:
            return False, 0, f"💰 Mejora cuesta {costo}g (no tienes suficiente)"

        # ... aplica la mejora ...

        return True, costo, f"⚔️  {arma.nombre} mejorado! [...] | Costo: {costo}g"
    ```
    Nota deliberada: cuando falla por dinero insuficiente, el `costo` retornado es `0` (no el costo real calculado, que solo aparece en el mensaje). Este es el comportamiento real del código — se deja tal cual, no se "corrige" al replicar el patrón en funciones nuevas, salvo que se decida cambiarlo explícitamente como su propia tarea.
- **Cambios mínimos:** no refactorizar código existente al añadir una feature nueva. Si una función nueva no encaja limpio en los patrones existentes, **prioriza consistencia con el código existente sobre elegancia**. Si eso genera una duda real de diseño (no solo estética), pregunta antes de implementar — no decidas en silencio romper el patrón.
- **Persistencia:** todo dato que deba sobrevivir entre sesiones pasa por `persistence.py` + `auth.py`, siguiendo el patrón de serialización ya establecido.

---

## 5. 🔄 Proceso de desarrollo por fases

- Trabajar **una subfase a la vez**, según el orden definido en `docs/ROADMAP.md`.
- **Definición de "fase terminada" (Definition of Done)** — todos estos puntos, no solo el primero:
  1. `python tests/run_tests_new.py` pasa al 100%, incluyendo los tests nuevos de la fase.
  2. Se hizo la revisión de compatibilidad de la sección 3 para cada función tocada.
  3. Docstrings completos en las funciones nuevas (descripción, `Args:`, `Returns:`).
  4. `docs/ROADMAP.md` actualizado moviendo la subfase a completada.
  5. `docs/HISTORIAL.md` actualizado con una entrada de la fase (qué se agregó, qué se tocó).
  6. `README.md` actualizado **solo si** cambió algo visible para el usuario final (nueva mecánica jugable, nuevo comando, etc.).
- **No se hace `git commit` ni `git push` sin confirmación explícita del usuario**, sin excepción.
- El estado de qué fase está en progreso, completada o pendiente **vive únicamente en `docs/ROADMAP.md`** — no se asume estado de fases desde conversaciones anteriores ni se duplica ese resumen en este archivo.

---

## 6. 📁 Arquitectura (mapa rápido)

| Módulo (`src/`) | Responsabilidad |
|---|---|
| `models.py` | Clases de datos: `Item`, `Weapon`, `Armor`, `Character`, `Gladiador`, `Equipo`, `Barracas`, enemigos |
| `combat.py` | Combate por turnos, cálculo de daño y XP, triggers de combate |
| `habilidades.py` | Arquetipos, habilidades pasivas/activas, activación por triggers |
| `misiones.py` | Sistema de misiones (4 capas), auto-tracking, persistencia de progreso |
| `facilities.py` | Médico (curación/revivir) y herrero (mejora de armas, durabilidad) |
| `store.py` | Catálogo de armas/armaduras/pociones, mercado, compra/venta |
| `enemies.py` | Generación y escalado de enemigos |
| `auth.py` | Registro, login, carga/guardado de partida |
| `persistence.py` | Serialización/deserialización de equipo y facilities |
| `leaderboards.py` | Rankings globales multiusuario (Top 10, máximos históricos) |
| `guia.py` | Ayuda en juego |

`data/` guarda `users.json`, `saves/` (partidas) y `misiones_<usuario>.json`.

Para detalle de arquitectura, modelos y balance: `docs/TECNICA.md`.

---

## 7. ⚠️ Advertencias y límites

- `legacy/` no se toca — es código v1, solo de referencia.
- `data/` contiene partidas reales de usuarios — no borrar ni sobrescribir archivos manualmente.
- Entorno de desarrollo: Windows / PowerShell.
- No hacer commit/push sin confirmación explícita del usuario (repetido aquí a propósito: es la regla que más se pasa por alto).
