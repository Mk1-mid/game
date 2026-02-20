# 🎮 GUÍA DE USO: NOTIFICACIONES Y PERSISTENCIA

## Para Usuarios (Jugadores)

### Guardando tu Partida

1. **Durante el juego**, presiona `8` en el menú principal:
   ```
   ║════════════════════════════════════════╗
   ║  MENÚ PRINCIPAL - SANGRE POR FORTUNA  ║
   ║════════════════════════════════════════║
   ║  1. ⚔️  Equipo                        ║
   ║  2. 🏛️  Arena                         ║
   ║  3. 🛒 Mercado                        ║
   ║  4. 📚 Guía                           ║
   ║  5. 🎖️  Historial                     ║
   ║  6. 🗺️  Mapa (Próximamente)           ║
   ║  7. 📋 Misiones                       ║
   ║  8. 💾 Guardar Partida  ← AQUÍ       ║
   ║  9. 🚪 Salir                          ║
   ║════════════════════════════════════════║
   ```

2. **Recibirás confirmación:**
   ```
   💾 Guardando partida...
   ✓ Misiones guardadas exitosamente
   ✓ Partida guardada correctamente
   ```

3. **¡Listo!** Tu progreso se guardó en `datos/misiones_{tuusuario}.json`

### Cargando tu Partida Guardada

1. **Al iniciar el juego**, selecciona tu usuario
2. **Si tienes partida guardada**, verás:
   ```
   💾 Partida guardada encontrada
   ✓ Misiones restauradas desde partida anterior
   ```

3. **Todas tus misiones aparecerán exactamente donde las dejaste:**
   - Progreso restaurado
   - Estado restaurado
   - Bonus restaurados

### Entendiendo las Notificaciones

Cuando completas misiones durante combate, verás:

```
======================================================================
        ✨ ¡MISIONES COMPLETADAS! ✨
======================================================================

✓ Primer Paso
  💰 100g | 📈 50 XP

✓ Primeras Ganancias
  💰 200g | 📈 100 XP

----------------------------------------------------------------------
📊 TOTAL: 300g + 150 XP
======================================================================
💡 Puedes reclamar recompensas en el menú de Misiones
```

**Qué significa:**
- `✓ Nombre` = Misión completada
- `💰 100g` = Dinero que recibirás
- `📈 50 XP` = Experiencia que recibirás
- `📊 TOTAL` = Suma de todas las misiones completadas en este evento
- El hint te invita a ir al menú de Misiones para reclamar

---

## Para Desarrolladores

### Usando el Sistema de Misiones en Código

#### Guardar Misiones

```python
from src.misiones import GestorMisiones

# Crear gestor
gestor = GestorMisiones()

# ... usuario juega ...

# Guardar cuando presiona "Guardar"
if gestor.guardar_estado(f"datos/misiones_{usuario}.json"):
    print("✓ Partida guardada")
else:
    print("❌ Error al guardar")
```

#### Cargar Misiones

```python
# Crear nuevo gestor
gestor = GestorMisiones()

# Cargar estado guardado
if gestor.cargar_estado(f"datos/misiones_{usuario}.json"):
    print("✓ Partida restaurada")
else:
    print("⚠️  No hay partida guardada, comenzando nueva")
```

#### Generar Notificación

```python
# Cuando ocurre evento de combate
misiones_completadas = gestor.evento_combate_ganado()

# Generar y mostrar notificación
notif = gestor.generar_notificacion_misiones(misiones_completadas)
if notif:  # Solo mostrar si hay misiones completadas
    print(notif)
```

#### Agregación de Múltiples Eventos

```python
# Un combate genera múltiples eventos
misiones_combate = gestor.evento_combate_ganado()      # Evento 1
misiones_dinero = gestor.evento_dinero_acumulado(250)  # Evento 2
misiones_nivel = gestor.evento_gladiador_sube_nivel()  # Evento 3

# Agregar sin duplicados
todas = list(set(misiones_combate + misiones_dinero + misiones_nivel))

# Una sola notificación con todas
notif = gestor.generar_notificacion_misiones(todas)
print(notif)
```

### Estructura del Archivo JSON Guardado

```json
{
  "misiones": {
    "combate_1": {
      "id": "combate_1",
      "nombre": "Primer Paso",
      "progreso": 1,
      "objetivo": 1,
      "estado": "completada",
      "tipo": "combate",
      "capa": "core",
      "dificultad": "tier_1",
      "recompensas": {
        "dinero": 100,
        "xp": 50
      },
      "mision_padre_id": null,
      "misiones_hijo_ids": ["cadena_gloria_1"],
      "tiene_bonus": false,
      "descripcion_bonus": "",
      "bonus_extra_recompensa": 0
    }
  },
  "activas": ["dinero_1", "nivel_1"],
  "completadas": ["combate_1"],
  "timestamp": "2025-01-07 14:23:45.123456"
}
```

### Métodos Disponibles

#### `guardar_estado(archivo: str) -> bool`

Guarda estado de todas las misiones en JSON.

**Parámetros:**
- `archivo` (str): Ruta del archivo a guardar. Por defecto `datos/misiones.json`

**Retorna:**
- `True` si se guardó exitosamente
- `False` si ocurrió error

**Ejemplo:**
```python
exito = gestor.guardar_estado("datos/misiones_player1.json")
if exito:
    print("✓ Guardado")
```

---

#### `cargar_estado(archivo: str) -> bool`

Carga estado de misiones desde archivo JSON.

**Parámetros:**
- `archivo` (str): Ruta del archivo a cargar

**Retorna:**
- `True` si se cargó exitosamente
- `False` si no existe archivo o error

**Ejemplo:**
```python
if gestor.cargar_estado("datos/misiones_player1.json"):
    print("✓ Partida restaurada")
else:
    print("⚠️  Partida nueva")
```

**Nota:** No retorna error si archivo no existe, solo retorna False.

---

#### `generar_notificacion_misiones(misiones_ids: List[str]) -> str`

Genera notificación visual para misiones completadas.

**Parámetros:**
- `misiones_ids` (List[str]): Lista de IDs de misiones completadas

**Retorna:**
- `str`: Notificación formateada (vacía si no hay misiones)

**Ejemplo:**
```python
notif = gestor.generar_notificacion_misiones(["combate_1", "dinero_1"])
print(notif)
# Output:
# ======================================================================
#         ✨ ¡MISIONES COMPLETADAS! ✨
# ======================================================================
# 
# ✓ Primer Paso
#   💰 100g | 📈 50 XP
# ... etc
```

**Características:**
- Calcula totales automáticamente
- Muestra información de bonus si aplica
- Incluye hint sobre dónde reclamar
- Retorna string vacío si lista vacía

---

#### `resetear_misiones()`

Reinicia todas las misiones a estado inicial (0 progreso, bloqueadas).

**Parámetros:** Ninguno

**Retorna:** Nada

**Ejemplo:**
```python
gestor.resetear_misiones()
# Después: todos los progreso en 0, misiones bloqueadas
# Luego: guardar si deseas persistir el reset
gestor.guardar_estado("datos/misiones.json")
```

**Nota:** Reactiva automáticamente las misiones CORE que se activan solas.

---

### Casos de Uso Comunes

#### Caso 1: Nuevo Jugador - Comenzar Partida

```python
# En juego_principal()
usuario = "nuevo_jugador"
gestor_misiones = GestorMisiones()

# No hay partida anterior, continuar con estado inicial
print(f"✓ {len(gestor_misiones.misiones)} misiones cargadas")
```

#### Caso 2: Jugador Retornando - Cargar Partida

```python
# En juego_principal()
usuario = "jugador_anterior"
gestor_misiones = GestorMisiones()

if gestor_misiones.cargar_estado(f"datos/misiones_{usuario}.json"):
    print("✓ Partida anterior restaurada")
    print(f"  {len(gestor_misiones.misiones_activas)} misiones activas")
else:
    print("⚠️  Partida nueva")
```

#### Caso 3: Guardar Partida Actual

```python
# Cuando usuario presiona "8. Guardar"
if gestor_misiones.guardar_estado(f"datos/misiones_{usuario}.json"):
    print("✓ Misiones guardadas exitosamente")
    print("✓ Partida guardada correctamente")
else:
    print("❌ Error al guardar las misiones")
```

#### Caso 4: Combate con Múltiples Eventos

```python
# En combate_equipo(), después de victoria
recompensa = 250  # Dinero ganado

# Evento 1: Combate ganado
misiones_cb = gestor_misiones.evento_combate_ganado()
notif = gestor_misiones.generar_notificacion_misiones(misiones_cb)
if notif:
    print(notif)

# Evento 2: Dinero acumulado
misiones_d = gestor_misiones.evento_dinero_acumulado(recompensa)
notif = gestor_misiones.generar_notificacion_misiones(misiones_d)
# Solo mostrar si es diferente a anterior
if notif and misiones_d != misiones_cb:
    print(notif)

# Evento 3: Nivel up (si aplica)
if gladiador.subio_nivel:
    misiones_n = gestor_misiones.evento_gladiador_sube_nivel()
    notif = gestor_misiones.generar_notificacion_misiones(misiones_n)
    if notif:
        print(notif)
```

#### Caso 5: Admin Reset

```python
# Si necesitas resetear para debugging
gestor_misiones.resetear_misiones()

# Verificar estado
print(f"Misiones activas: {len(gestor_misiones.misiones_activas)}")
print(f"Misiones completadas: {len(gestor_misiones.misiones_completadas)}")
```

---

### Testing

#### Ejecutar Tests de Notificaciones

```bash
python tests/test_notificaciones_persistencia.py
```

**Output esperado:**
```
✅ Test notificaciones mejoradas: PASADO
✅ Test persistencia: PASADO
✅ Test aislamiento de usuarios: PASADO
✅ Test resetear misiones: PASADO
✅ TODOS LOS TESTS DE NOTIFICACIONES Y PERSISTENCIA PASARON
```

#### Ejecutar Tests de Integración

```bash
python tests/test_integracion_completa.py
```

**Output esperado:**
```
SESIÓN 1: Jugar y Guardar Partida
  ✓ Equipo creado
  ✓ 23 misiones cargadas
  ✓ Eventos simulados
  ✓ Misiones guardadas

SESIÓN 2: Cargar Partida y Continuar
  ✓ Misiones restauradas
  ✓ Integridad verificada
  ✓ Continuando juego
  ✓ Partida actualizada

✅ TODOS LOS TESTS DE INTEGRACIÓN PASARON
```

---

### Troubleshooting

#### Problema: "No puedo cargar mi partida guardada"

**Posibles causas:**
1. Archivo JSON corrompido
2. Ruta incorrecta
3. Permiso de lectura denegado

**Soluciones:**
```python
# Verificar archivo existe
import os
archivo = "datos/misiones_usuario.json"

if os.path.exists(archivo):
    print("✓ Archivo existe")
    
    # Intentar cargar
    if not gestor.cargar_estado(archivo):
        print("❌ Archivo corrupto o formato inválido")
        # Solución: Deletear archivo y comenzar nuevo
else:
    print("❌ Archivo no encontrado")
    # Solución: Crear partida nueva
```

#### Problema: "Las misiones no se guardan"

**Verificar:**
```python
# 1. Directorio existe
os.makedirs("datos", exist_ok=True)

# 2. Permiso de escritura
archivo = "datos/test.json"
try:
    gestor.guardar_estado(archivo)
    print("✓ Escritura OK")
except:
    print("❌ Sin permiso de escritura")

# 3. Espacio en disco
import os
stat = os.statvfs("datos")
libres = stat.f_bavail * stat.f_frsize
print(f"Espacio libre: {libres / 1024 / 1024:.2f} MB")
```

#### Problema: "Las notificaciones no aparecen"

**Verificar:**
```python
# 1. Misiones están completándose
misiones = gestor.evento_combate_ganado()
print(f"Misiones completadas: {misiones}")

# 2. Generar notificación
notif = gestor.generar_notificacion_misiones(misiones)
print(f"Notificación generada: {len(notif)} caracteres")

# 3. Mostrar
if notif:
    print(notif)
else:
    print("⚠️  Notificación vacía (sin misiones completadas)")
```

---

### Performance Tips

1. **Guardar solo cuando necesario**
   ```python
   # ❌ Malo: Guardar cada evento
   for evento in eventos:
       gestor.evento_combate_ganado()
       gestor.guardar_estado(archivo)  # Lento
   
   # ✅ Bueno: Guardar una vez al final
   for evento in eventos:
       gestor.evento_combate_ganado()
   gestor.guardar_estado(archivo)  # Rápido
   ```

2. **Cache notificaciones agregadas**
   ```python
   # En lugar de generar múltiples notificaciones
   notificaciones = []
   for mision_id in misiones_completadas:
       notif = gestor.generar_notificacion_misiones([mision_id])
       notificaciones.append(notif)
   
   # Hacer una sola
   notif_única = gestor.generar_notificacion_misiones(misiones_completadas)
   ```

---

### FAQ Técnico

**P: ¿Qué pasa si dos usuarios guardan simultáneamente?**
R: No hay problema. Cada usuario tiene archivo separado (`misiones_usuario1.json` vs `misiones_usuario2.json`).

**P: ¿Puedo editar manualmente el JSON?**
R: Sí, pero con cuidado. Mantén estructura exacta. El sistema validará al cargar.

**P: ¿Cuánto espacio ocupa una partida guardada?**
R: ~12-15 KB. Trivial incluso con miles de partidas.

**P: ¿Qué pasa si corrompo el JSON?**
R: `cargar_estado()` retorna False. Puedes deletear archivo y comenzar nuevo.

**P: ¿Puedo exportar/compartir una partida?**
R: Sí. Solo copia el archivo JSON. Otro usuario puede cargarlo.

---

**Última actualización:** 7 de Enero 2025  
**Versión:** 1.0  
**Status:** ✅ Producción Ready
