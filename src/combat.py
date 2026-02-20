"""
Sistema de combate por turnos
============================
"""

import random
from src.habilidades import (
    TipoTrigger, calcular_bonus_pasivo_total,
    aplicar_bonificadores_habilidades, verificar_y_activar_triggers,
    resetear_habilidades_combate, decrementar_duraciones, TipoHabilidad
)


# ============================================
# FUNCIONES DE VISUALIZACIÓN
# ============================================

def mostrar_habilidades_disponibles(gladiador):
    """
    Muestra todas las habilidades disponibles del gladiador antes del combate.
    
    Args:
        gladiador: Objeto Gladiador
    """
    if not hasattr(gladiador, 'habilidades') or not gladiador.habilidades:
        return
    
    print("\n" + "="*60)
    print(f"HABILIDADES DE {gladiador.nombre.upper()} ({gladiador.tipo})")
    print("="*60)
    
    # Separar pasivas y activas
    pasivas = [h for h in gladiador.habilidades if h.tipo == TipoHabilidad.PASIVA]
    activas = [h for h in gladiador.habilidades if h.tipo == TipoHabilidad.ACTIVA]
    
    # Mostrar habilidades pasivas
    if pasivas:
        print("\n[*] HABILIDADES PASIVAS (Siempre Activas):")
        print("-" * 60)
        for hab in pasivas:
            if hasattr(hab, 'bonus_pasivo') and hab.bonus_pasivo:
                bonus_str = ", ".join([f"+{int(v*100)}% {k}" for k, v in hab.bonus_pasivo.items()])
                print(f"  * {hab.nombre}")
                print(f"    -> {hab.descripcion}")
                print(f"    -> {bonus_str}\n")
    
    # Mostrar habilidades activas
    if activas:
        print("\n[+] HABILIDADES ACTIVAS (Se activan en combate):")
        print("-" * 60)
        for hab in activas:
            emoji_trigger = "[T]"
            if hasattr(hab, 'trigger_tipo'):
                if "SALUD" in str(hab.trigger_tipo):
                    emoji_trigger = "[H]"
                elif "CRITICO" in str(hab.trigger_tipo):
                    emoji_trigger = "[*]"
                elif "ESQUIVA" in str(hab.trigger_tipo):
                    emoji_trigger = "[~]"
                elif "DAÑO" in str(hab.trigger_tipo):
                    emoji_trigger = "[!]"
                elif "TURNOS" in str(hab.trigger_tipo):
                    emoji_trigger = "[#]"
            
            print(f"  * {hab.nombre}")
            print(f"    -> {hab.descripcion}")
            if hasattr(hab, 'bonus_activo') and hab.bonus_activo:
                bonus_str = ", ".join([f"+{int(v*100)}% {k}" for k, v in hab.bonus_activo.items()])
                print(f"    -> Efecto: {bonus_str}")
            if hasattr(hab, 'duracion_bonus') and hab.duracion_bonus > 0:
                print(f"    -> Duracion: {hab.duracion_bonus} turno(s)")
            print(f"    -> Se activa: {emoji_trigger}\n")
    
    print("="*60 + "\n")


def mostrar_resumen_combate(gladiador, victoria):
    """
    Muestra un resumen de las habilidades activadas durante el combate.
    
    Args:
        gladiador: Objeto Gladiador
        victoria: bool indicando si gano el combate
    """
    if not hasattr(gladiador, 'habilidades'):
        return
    
    # Contar habilidades activas que fueron usadas
    habilidades_usadas = [h for h in gladiador.habilidades 
                         if h.tipo == TipoHabilidad.ACTIVA and h.veces_usado > 0]
    
    if habilidades_usadas and victoria:
        print("\n" + "="*60)
        print(f"[*] RESUMEN DE COMBATE - {gladiador.nombre}")
        print("="*60)
        print("[*] Habilidades activadas durante el combate:")
        for hab in habilidades_usadas:
            print(f"  [OK] {hab.nombre}")
            if hasattr(hab, 'bonus_activo') and hab.bonus_activo:
                for stat, valor in hab.bonus_activo.items():
                    porcentaje = int(valor * 100)
                    print(f"    -> +{porcentaje}% {stat}")
        print("="*60 + "\n")


# ============================================
# CÁLCULO DE DAÑO CON CRÍTICO Y ESQUIVA
# ============================================

def calcular_ataque(daño_ataque, defensa_enemigo, critico_atacante, esquiva_defensor):
    """
    Calcula resultado de ataque: esquiva, golpe normal o crítico.
    
    Args:
        daño_ataque: Daño base del atacante
        defensa_enemigo: Defensa del defensor
        critico_atacante: Probabilidad de crítico del atacante (%)
        esquiva_defensor: Probabilidad de esquiva del defensor (%)
    
    Returns:
        tuple: (tipo: str, daño: int)
        - tipo: "esquiva", "golpe", "crítico"
        - daño: 0 si esquiva, daño calculado si golpe/crítico
    """
    # Comprobar esquiva primero
    if random.random() * 100 < esquiva_defensor:
        return ("esquiva", 0)
    
    # Variación aleatoria ±20%
    variacion = random.uniform(0.8, 1.2)
    daño_base = int(daño_ataque * variacion)
    
    # La defensa reduce el 50% de su valor
    reduccion = defensa_enemigo * 0.5
    daño_base = max(1, daño_base - reduccion)
    
    # Comprobar crítico
    if random.random() * 100 < critico_atacante:
        daño_final = int(daño_base * 1.8)  # 1.8x daño
        return ("crítico", daño_final)
    
    return ("golpe", daño_base)


def calcular_daño(daño_ataque, defensa_enemigo):
    """
    LEGACY: Calcula el daño sin esquiva/crítico (para compatibilidad).
    """
    tipo, daño = calcular_ataque(daño_ataque, defensa_enemigo, 0, 0)
    return daño


# ============================================
# SISTEMA DE COMBATE
# ============================================

def combate_arena(salud_jugador, daño_jugador, velocidad_jugador, defensa_jugador,
                  salud_enemigo, daño_enemigo, velocidad_enemigo, defensa_enemigo, daño_base,
                  gladiador=None, enemigo=None):
    """
    Simula un combate por turnos entre jugador y enemigo.
    
    Args:
        salud_jugador, daño_jugador, velocidad_jugador, defensa_jugador: Stats del jugador
        salud_enemigo, daño_enemigo, velocidad_enemigo, defensa_enemigo: Stats del enemigo
        daño_base: Daño base para cálculos adicionales
        gladiador: Objeto Gladiador del jugador (opcional, para usar habilidades)
        enemigo: Objeto Enemigo (opcional, para usar habilidades)
    
    Returns:
        tuple: (victoria: bool, salud_jugador_final: int, salud_enemigo_final: int)
    """
    
    salud_simulada_jugador = salud_jugador
    salud_simulada_enemigo = salud_enemigo
    victoria = None
    
    # Mostrar habilidades disponibles al inicio del combate
    if gladiador:
        mostrar_habilidades_disponibles(gladiador)
    
    print("     ⚔️  COMBATE INICIADO ⚔️")
    print(f"Tu gladiador: {salud_simulada_jugador} HP")
    print(f"Enemigo:      {salud_simulada_enemigo} HP")
    input("\nPresiona ENTER para comenzar el combate")

    jugador_primero = velocidad_jugador >= velocidad_enemigo
    
    turno = 1
    while victoria is None:
        print(f"\n Turno {turno} ")
        
        if jugador_primero:
            # PASO 1: Aplicar bonificadores de habilidades si existen
            daño_jugador_bonificado = daño_jugador
            defensa_enemigo_bonificada = defensa_enemigo
            
            if gladiador and hasattr(gladiador, 'habilidades'):
                stats_jugador = aplicar_bonificadores_combate(
                    {"ataque": daño_jugador, "defensa": defensa_jugador},
                    gladiador
                )
                daño_jugador_bonificado = stats_jugador.get("ataque", daño_jugador)
            
            if enemigo and hasattr(enemigo, 'habilidades'):
                stats_enemigo = aplicar_bonificadores_combate(
                    {"ataque": daño_enemigo, "defensa": defensa_enemigo},
                    enemigo
                )
                defensa_enemigo_bonificada = stats_enemigo.get("defensa", defensa_enemigo)
            
            # Jugador ataca
            daño_infligido = calcular_daño(daño_jugador_bonificado, defensa_enemigo_bonificada)
            salud_simulada_enemigo -= daño_infligido
            
            # Mostrar bonificadores si se aplicaron
            if daño_jugador_bonificado != daño_jugador:
                mostrar_bonificadores_aplicados("Tu Gladiador", 
                    {"ataque": daño_jugador}, 
                    {"ataque": daño_jugador_bonificado})
            
            print(f"  ⚔️  Tu gladiador ataca con {daño_infligido} de daño")
            print(f"   💔 Salud enemiga: {salud_simulada_enemigo} HP")
            
            # PASO 2: Verificar triggers
            if gladiador:
                verificar_triggers_combate(gladiador, enemigo, turno, 
                                         resultado_ataque="crítico" if daño_infligido > calcular_daño(daño_jugador_bonificado, defensa_enemigo_bonificada * 0) else "golpe")
            
            if salud_simulada_enemigo <= 0:
                print("   Enemigo derrotado ")
                victoria = True
                break

            input("   Presiona ENTER para continuar")

            # Enemigo ataca
            daño_enemigo_bonificado = daño_enemigo
            defensa_jugador_bonificada = defensa_jugador
            
            if enemigo and hasattr(enemigo, 'habilidades'):
                stats_enemigo = aplicar_bonificadores_combate(
                    {"ataque": daño_enemigo, "defensa": defensa_enemigo},
                    enemigo
                )
                daño_enemigo_bonificado = stats_enemigo.get("ataque", daño_enemigo)
            
            if gladiador and hasattr(gladiador, 'habilidades'):
                stats_jugador = aplicar_bonificadores_combate(
                    {"ataque": daño_jugador, "defensa": defensa_jugador},
                    gladiador
                )
                defensa_jugador_bonificada = stats_jugador.get("defensa", defensa_jugador)
            
            daño_recibido = calcular_daño(daño_enemigo_bonificado, defensa_jugador_bonificada)
            salud_simulada_jugador -= daño_recibido
            
            # Mostrar bonificadores si se aplicaron
            if defensa_jugador_bonificada != defensa_jugador:
                mostrar_bonificadores_aplicados("Tu Gladiador", 
                    {"defensa": defensa_jugador}, 
                    {"defensa": defensa_jugador_bonificada})
            
            print(f"  🗡️  El enemigo ataca con {daño_recibido} de daño")
            print(f"   ❤️  Tu salud: {salud_simulada_jugador} HP")
            
            # PASO 2: Verificar triggers del enemigo
            if enemigo:
                verificar_triggers_combate(enemigo, gladiador, turno,
                                         resultado_ataque="crítico" if daño_recibido > calcular_daño(daño_enemigo_bonificado, defensa_jugador_bonificada * 0) else "golpe")
            
            if salud_simulada_jugador <= 0:
                print("   Has sido derrotado")
                victoria = False
                break
        else:
            # Enemigo ataca primero
            daño_enemigo_bonificado = daño_enemigo
            defensa_jugador_bonificada = defensa_jugador
            
            if enemigo and hasattr(enemigo, 'habilidades'):
                stats_enemigo = aplicar_bonificadores_combate(
                    {"ataque": daño_enemigo, "defensa": defensa_enemigo},
                    enemigo
                )
                daño_enemigo_bonificado = stats_enemigo.get("ataque", daño_enemigo)
            
            if gladiador and hasattr(gladiador, 'habilidades'):
                stats_jugador = aplicar_bonificadores_combate(
                    {"ataque": daño_jugador, "defensa": defensa_jugador},
                    gladiador
                )
                defensa_jugador_bonificada = stats_jugador.get("defensa", defensa_jugador)
            
            daño_recibido = calcular_daño(daño_enemigo_bonificado, defensa_jugador_bonificada)
            salud_simulada_jugador -= daño_recibido
            
            # Mostrar bonificadores si se aplicaron
            if defensa_jugador_bonificada != defensa_jugador:
                mostrar_bonificadores_aplicados("Tu Gladiador", 
                    {"defensa": defensa_jugador}, 
                    {"defensa": defensa_jugador_bonificada})
            
            print(f"  🗡️  El enemigo ataca con {daño_recibido} de daño")
            print(f"   ❤️  Tu salud: {salud_simulada_jugador} HP")
            
            # Verificar triggers del enemigo
            if enemigo:
                verificar_triggers_combate(enemigo, gladiador, turno,
                                         resultado_ataque="crítico" if daño_recibido > calcular_daño(daño_enemigo_bonificado, defensa_jugador_bonificada * 0) else "golpe")
            
            if salud_simulada_jugador <= 0:
                print("   Has sido derrotado")
                victoria = False
                break

            input("   Presiona ENTER para continuar")

            # Jugador ataca
            daño_jugador_bonificado = daño_jugador
            defensa_enemigo_bonificada = defensa_enemigo
            
            if gladiador and hasattr(gladiador, 'habilidades'):
                stats_jugador = aplicar_bonificadores_combate(
                    {"ataque": daño_jugador, "defensa": defensa_jugador},
                    gladiador
                )
                daño_jugador_bonificado = stats_jugador.get("ataque", daño_jugador)
            
            if enemigo and hasattr(enemigo, 'habilidades'):
                stats_enemigo = aplicar_bonificadores_combate(
                    {"ataque": daño_enemigo, "defensa": defensa_enemigo},
                    enemigo
                )
                defensa_enemigo_bonificada = stats_enemigo.get("defensa", defensa_enemigo)
            
            daño_infligido = calcular_daño(daño_jugador_bonificado, defensa_enemigo_bonificada)
            salud_simulada_enemigo -= daño_infligido
            
            # Mostrar bonificadores si se aplicaron
            if daño_jugador_bonificado != daño_jugador:
                mostrar_bonificadores_aplicados("Tu Gladiador", 
                    {"ataque": daño_jugador}, 
                    {"ataque": daño_jugador_bonificado})
            
            print(f"  ⚔️  Tu gladiador ataca con {daño_infligido} de daño")
            print(f"   💔 Salud enemiga: {salud_simulada_enemigo} HP")
            
            # Verificar triggers del jugador
            if gladiador:
                verificar_triggers_combate(gladiador, enemigo, turno,
                                         resultado_ataque="crítico" if daño_infligido > calcular_daño(daño_jugador_bonificado, defensa_enemigo_bonificada * 0) else "golpe")
            
            if salud_simulada_enemigo <= 0:
                print("   Enemigo derrotado ")
                victoria = True
                break
        
        # PASO 3: Decrementar duraciones de habilidades activas
        if gladiador:
            decrementar_habilidades_activas(gladiador)
        if enemigo:
            decrementar_habilidades_activas(enemigo)
        
        turno += 1

    # PASO 4: Resetear habilidades post-combate
    if gladiador:
        resetear_habilidades_para_siguiente_combate(gladiador)
    if enemigo:
        resetear_habilidades_para_siguiente_combate(enemigo)
    
    # Mostrar resumen de habilidades usadas
    if gladiador and victoria:
        mostrar_resumen_combate(gladiador, victoria)

    return victoria, salud_simulada_jugador, salud_simulada_enemigo


def curar_en_base(salud_actual, vida_maxima):
    """
    Cura al jugador completamente en la base.
    
    Args:
        salud_actual: Salud actual
        vida_maxima: Salud máxima
    
    Returns:
        int: Salud restaurada a máximo
    """
    print(f"🏥 Te curas en la base: {salud_actual} → {vida_maxima} HP")
    return vida_maxima


# ============================================
# HABILIDADES EN COMBATE (Fase 2.2)
# ============================================

def aplicar_bonificadores_combate(stats_base, gladiador):
    """
    Aplica bonificadores de habilidades pasivas a los stats del combate.
    
    Args:
        stats_base: Dict con stats básicos
        gladiador: Instancia de Gladiador con habilidades
    
    Returns:
        dict: Stats modificados con bonificadores pasivos y activos
    """
    stats = stats_base.copy()
    
    # Aplicar bonificadores de habilidades
    if hasattr(gladiador, 'habilidades'):
        stats = aplicar_bonificadores_habilidades(stats, gladiador.habilidades)
    
    return stats


def verificar_triggers_combate(gladiador, enemigo, turno, resultado_ataque=None, resultado_defensa=None):
    """
    Verifica y activa triggers de habilidades activas durante el combate.
    
    Args:
        gladiador: Instancia de Gladiador
        enemigo: Instancia de Gladiador/Enemigo
        turno: Número de turno actual
        resultado_ataque: Resultado del ataque ("crítico", "golpe", "esquiva")
        resultado_defensa: Resultado de la defensa
    """
    if not hasattr(gladiador, 'habilidades'):
        return
    
    # Actualizar contadores para triggers
    if resultado_ataque == "crítico":
        gladiador.contadores_triggers["criticos_propios"] += 1
    elif resultado_ataque == "esquiva":
        gladiador.contadores_triggers["esquivas"] = 0  # Reset si es propia
    
    if resultado_defensa == "crítico":
        gladiador.contadores_triggers["criticos_recibidos"] += 1
    elif resultado_defensa == "esquiva":
        gladiador.contadores_triggers["esquivas"] += 1
    
    gladiador.contadores_triggers["turnos"] = turno
    
    # Verificar y activar triggers
    estado_combate = {
        "salud": max(0, gladiador.hp_actual) if hasattr(gladiador, 'hp_actual') else gladiador.hp,
        "salud_maxima": gladiador.hp,
        "esquivas": gladiador.contadores_triggers["esquivas"],
        "criticos_recibidos": gladiador.contadores_triggers["criticos_recibidos"],
        "criticos_propios": gladiador.contadores_triggers["criticos_propios"],
        "turno": turno
    }
    
    # Activar habilidades según triggers y mostrar visualmente
    habilidades_activadas = verificar_y_activar_triggers(gladiador, estado_combate)
    for nombre_habilidad in habilidades_activadas:
        # Buscar la habilidad para mostrar detalles
        for hab in gladiador.habilidades:
            if hab.nombre == nombre_habilidad:
                mostrar_habilidad_activada(gladiador.nombre, hab)
                break


def decrementar_habilidades_activas(gladiador):
    """
    Decrementa la duración de habilidades activas.
    """
    if hasattr(gladiador, 'habilidades'):
        decrementar_duraciones(gladiador.habilidades)


def resetear_habilidades_para_siguiente_combate(gladiador):
    """
    Resetea habilidades al terminar un combate.
    """
    if hasattr(gladiador, 'habilidades'):
        resetear_habilidades_combate(gladiador.habilidades)
        if hasattr(gladiador, 'contadores_triggers'):
            for key in gladiador.contadores_triggers:
                gladiador.contadores_triggers[key] = 0


def mostrar_habilidad_activada(nombre_gladiador, habilidad):
    """
    Muestra visualmente cuando se activa una habilidad durante el combate.
    
    Args:
        nombre_gladiador: Nombre del gladiador
        habilidad: Objeto Habilidad activada
    """
    print(f"\n>>> [!] {nombre_gladiador} ACTIVA [{habilidad.nombre}]!")
    
    # Mostrar descripcion del efecto
    if hasattr(habilidad, 'descripcion') and habilidad.descripcion:
        print(f"   -> {habilidad.descripcion}")
    
    # Mostrar bonificadores si existen
    if hasattr(habilidad, 'bonus_activo') and habilidad.bonus_activo:
        print("   [EFECTOS]:")
        for stat, valor in habilidad.bonus_activo.items():
            if valor != 0:
                signo = "+" if valor > 0 else ""
                porcentaje = int(abs(valor) * 100)
                print(f"      {signo}{porcentaje}% {stat.upper()}")
    
    # Mostrar duracion
    if hasattr(habilidad, 'duracion_bonus') and habilidad.duracion_bonus > 0:
        print(f"   [Duracion: {habilidad.duracion_bonus} turno(s)]")


def mostrar_bonificadores_aplicados(personaje_nombre, stats_originales, stats_modificados):
    """
    Muestra visualmente el cambio de estadísticas por bonificadores.
    
    Args:
        personaje_nombre: Nombre del personaje
        stats_originales: Dict con stats originales
        stats_modificados: Dict con stats después de bonificadores
    """
    cambios = {}
    
    for stat in stats_originales:
        valor_original = stats_originales.get(stat, 0)
        valor_modificado = stats_modificados.get(stat, 0)
        
        if valor_modificado != valor_original:
            cambios[stat] = (valor_original, valor_modificado)
    
    if cambios:
        print(f"\n   🎯 BONIFICADORES APLICADOS A {personaje_nombre}:")
        for stat, (original, modificado) in cambios.items():
            diferencia = modificado - original
            porcentaje_cambio = (diferencia / original * 100) if original > 0 else 0
            
            if "ataque" in stat.lower():
                emoji = "⚔️"
            elif "defensa" in stat.lower():
                emoji = "🛡️"
            else:
                emoji = "⭐"
            
            print(f"      {emoji} {stat.upper()}: {original} → {modificado:.1f} ({porcentaje_cambio:+.0f}%)")


# ============================================
# RECOMPENSAS DE COMBATE (XP)
# ============================================

def calcular_xp_recompensa(nivel_jugador):
    """
    Calcula la XP ganada tras una victoria en función del nivel del jugador.

    La base crece suavemente para mantener progresión sin volverse trivial.
    """
    nivel = max(1, int(nivel_jugador))
    # Base 50 * (1.15 ^ nivel)
    xp = int(50 * (1.15 ** nivel))
    # Pequeña variación aleatoria ±10%
    variacion = random.uniform(0.9, 1.1)
    return int(xp * variacion)
