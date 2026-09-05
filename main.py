#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SANGRE POR FORTUNA - Juego de Gladiadores
==========================================

Sistema de gestión de equipo de gladiadores estilo Pokémon.
Usa múltiples gladiadores, gestiona barracas, hospital, mercado.

Uso: python main.py
"""

from src.models import Equipo, Gladiador
from src.combat import combate_arena, calcular_xp_recompensa
from src.store import (
    mostrar_catalogo, comprar_item, menu_armeria, equipar_item,
    mostrar_mercado_gladiadores, comprar_gladiador, vender_gladiador,
    mostrar_catalogo_herrero, comprar_item_herrero
)
from src.enemies import generar_enemigo, mostrar_info_enemigo
from src.auth import mostrar_menu_autenticacion, cargar_partida, guardar_partida
from src.persistence import serializar_equipo, deserializar_equipo, guardar_facilities, cargar_facilities
from src.misiones import GestorMisiones, EstadoMision
from src.facilities import FacilitiesManager

import random

try:
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load("assets/musica.mp3")
    pygame.mixer.music.play(-1)
except:
    pass  # Música no disponible


# ============================================
# FUNCIONES AUXILIARES DE UI
# ============================================

def generar_barra_progreso(actual, total, largo=10, emoji="▓"):
    """Genera barra de progreso visual."""
    llenos = int((actual / total) * largo)
    barra = emoji * llenos + "░" * (largo - llenos)
    porcentaje = int((actual / total) * 100)
    return barra, porcentaje

def generar_barra_ocupacion(dias_ocupado, dias_totales):
    """Barra visual para ocupación (entrenamiento/curación)."""
    dias_restantes = dias_totales - dias_ocupado
    barra, porcentaje = generar_barra_progreso(dias_restantes, dias_totales, largo=10, emoji="█")
    return f"{barra} ({dias_restantes}/{dias_totales}d)"

def analizar_riesgo_combate(nivel_jugador, nivel_enemigo):
    """Retorna análisis de riesgo de combate."""
    diferencia = nivel_enemigo - nivel_jugador
    
    if diferencia <= -2:
        return "MUY FÁCIL 👶", "🟢", 95
    elif diferencia <= -1:
        return "FÁCIL 😊", "🟢", 80
    elif diferencia <= 0:
        return "BALANCEADO ⚔️", "🟡", 65
    elif diferencia <= 2:
        return "DIFÍCIL 😰", "🔴", 40
    elif diferencia <= 4:
        return "MUY DIFÍCIL 💀", "🔴", 20
    else:
        return "EXTREMO ☠️", "⭐", 5

def calcular_estimacion_recompensas(nivel_base, multiplicador, victoria=True):
    """Calcula estimación de recompensas."""
    if not victoria:
        return 0, 0
    
    recompensa_base = random.randint(150, 350)
    xp_base = int(calcular_xp_recompensa(nivel_base))
    
    recompensa_final = int(recompensa_base * multiplicador)
    xp_final = int(xp_base * multiplicador)
    
    return recompensa_final, xp_final

def obtener_historico_combates(gladiador):
    """Retorna histórico de últimos combates con estadísticas."""
    total = gladiador.combates_totales
    ganados = gladiador.combates_ganados
    perdidos = gladiador.combates_perdidos
    
    if total == 0:
        return "Sin combates aún"
    
    winrate = int((ganados / total) * 100)
    return f"{ganados}W-{perdidos}L ({winrate}% win rate)"

def generar_badges_arena(gladiador, dificultad_name):
    """Retorna badges/logros basados en estadísticas."""
    badges = {
        "novato": {"emoji": "🟢", "nombre": "Novato Master", "requisito": lambda g: getattr(g, 'combates_novato', 0) >= 10},
        "normal": {"emoji": "🟡", "nombre": "Normal Champion", "requisito": lambda g: getattr(g, 'combates_normal', 0) >= 15},
        "experto": {"emoji": "🔴", "nombre": "Experto Legend", "requisito": lambda g: getattr(g, 'combates_experto', 0) >= 5},
        "legendaria": {"emoji": "⭐", "nombre": "Legendario Hero", "requisito": lambda g: getattr(g, 'combates_legendaria', 0) >= 1},
    }
    
    resultado = []
    for dif, badge_info in badges.items():
        logrado = badge_info["requisito"](gladiador)
        emoji = "✅" if logrado else "❌"
        contador = getattr(gladiador, f'combates_{dif}', 0)
        requisito_valor = badge_info["requisito"].__code__.co_consts[1]
        resultado.append(f"  {emoji} {badge_info['emoji']} {badge_info['nombre']:<20} ({contador}/? combates)")
    
    return "\n".join(resultado)

def mostrar_animacion_mejora(stats_antes, stats_despues):
    """Muestra animación ASCII de mejora de stats."""
    print("\n╭─────────────────────────────╮")
    print("│     💪 ¡MEJORADO!           │")
    for stat_name in stats_antes:
        delta = stats_despues[stat_name] - stats_antes[stat_name]
        if delta > 0:
            print(f"│  +{delta} {stat_name:<15} ⬆️│")
    print("╰─────────────────────────────╯\n")


# ============================================
# PANTALLAS
# ============================================

def mostrar_titulo():
    """Muestra el título del juego."""
    print("""
╔══════════════════════════════════════════╗
║                                          ║
║      🏛️  BIENVENIDO AL COLISEO  🏛️         ║
║       SISTEMA DE EQUIPOS (Pokémon)       ║
║                                          ║
╚══════════════════════════════════════════╝
""")


def mostrar_pantalla_equipo(equipo, usuario):
    """Pantalla principal del equipo con UI visual mejorada."""
    print("\n" + "="*70)
    print(f"         ⚔️  {usuario.upper()}  ⚔️")
    print("="*70)
    print(f"💰 Dinero: {equipo.dinero}g  |  📊 Nivel Promedio: {equipo.calcular_nivel_promedio()}")
    print(f"🏠 Barracas: {len(equipo.gladiadores)}/{equipo.barracas.espacios_totales} ")
    print(f"   (Espacios: {equipo.espacios_disponibles} libres)")
    print("="*70)
    print("\nTU EQUIPO DE GLADIADORES:\n")
    
    if not equipo.gladiadores:
        print("  ❌ No tienes gladiadores. ¡Compra algunos en el mercado!")
        return
    
    for i, g in enumerate(equipo.gladiadores, 1):
        estado_icon = {
            "sano": "✓",
            "herido": "⚠️",
            "critico": "🔴",
            "muerto": "☠️"
        }.get(g.estado, "?")
        
        ocupacion_str = ""
        if g.ocupacion == "ocupado":
            ocupacion_str = f" ({g.razon_ocupacion.upper()} {g.dias_ocupado}d)"
        
        print(f"  [{i}] {g.nombre:<15} Lvl {g.nivel:>2} {estado_icon} {g.estado:<8}{ocupacion_str}")
        print(f"       {g.tipo}")
        print(f"       {g.generar_barra_hp()}")
        print(f"       {g.generar_barra_xp()}")
        print(f"       {g.generar_string_stats()}")
        print(f"       Record: {g.combates_ganados}W-{g.combates_perdidos}L")
        print()
    
    print("="*70)


def mostrar_menu_principal():
    """Menú principal."""
    print("""
╔════════════════════════════════════════════╗
║       ⚔️  SANGRE POR FORTUNA  ⚔️  (Equipo)   ║
╠════════════════════════════════════════════╣
║  1. 🏟️  Ir a la Arena (Combate)           ║
║  2. 🏛️  Barracas (Ver/Comprar espacio)    ║
║  3. 🏥 Hospital (Curar/Revivir)           ║
║  4. 🛍️  Mercado de Gladiadores            ║
║  5. ⚔️  Armería                            ║
║  6. 📊 Ver Equipo Completo                ║
║  7. � Misiones                           ║
║  8. 💾 Guardar Partida                    ║
║  9. 🚪 Salir del Juego                    ║
╚════════════════════════════════════════════╝
    """)


# ============================================
# COMBAT FLOW
# ============================================

def seleccionar_luchador(equipo):
    """Menú para seleccionar qué gladiador va a combatir."""
    print("\n" + "="*70)
    print("SELECCIONA A TU LUCHADOR")
    print("="*70 + "\n")
    
    disponibles = [(i, g) for i, g in enumerate(equipo.gladiadores) if g.puede_luchar()]
    
    if not disponibles:
        print("❌ No tienes gladiadores disponibles para combatir")
        return None
    
    for idx, (i, g) in enumerate(disponibles, 1):
        print(f"  [{idx}] {g.nombre} (Lvl {g.nivel}) - {g.tipo} - HP: {g.hp_actual}/{g.hp}")
    
    print("  [0] Cancelar")
    
    opcion = input("\n¿Quién va a pelear? [0-{}]: ".format(len(disponibles))).strip()
    
    try:
        idx = int(opcion)
        if idx == 0:
            return None
        if 1 <= idx <= len(disponibles):
            _, gladiador = disponibles[idx - 1]
            return gladiador
    except ValueError:
        pass
    
    print("❌ Opción inválida")
    return None


def mostrar_habilidades_gladiador(gladiador):
    """Muestra las habilidades disponibles del gladiador antes del combate."""
    if not hasattr(gladiador, 'habilidades') or not gladiador.habilidades:
        return
    
    print("\n" + "="*70)
    print(f"HABILIDADES DE {gladiador.nombre} ({gladiador.tipo})")
    print("="*70 + "\n")
    
    # Separar pasivas y activas
    pasivas = [h for h in gladiador.habilidades if hasattr(h, 'tipo') and h.tipo.name == "PASIVA"]
    activas = [h for h in gladiador.habilidades if hasattr(h, 'tipo') and h.tipo.name == "ACTIVA"]
    
    if pasivas:
        print("🟡 HABILIDADES PASIVAS (Activas siempre):")
        for hab in pasivas:
            desc = hab.descripcion if hasattr(hab, 'descripcion') else "Sin descripción"
            print(f"   • {hab.nombre}: {desc}")
    
    if activas:
        print("\n🔵 HABILIDADES ACTIVAS (Se activan por triggers):")
        for hab in activas:
            desc = hab.descripcion if hasattr(hab, 'descripcion') else "Sin descripción"
            trigger_text = ""
            if hasattr(hab, 'triggers'):
                trigger_names = [t.name if hasattr(t, 'name') else str(t) for t in hab.triggers]
                trigger_text = f" - Trigger: {', '.join(trigger_names)}"
            print(f"   • {hab.nombre}: {desc}{trigger_text}")
    
    print()


def arena_menu(equipo, sistema_ligas=None):
    """🏛️ Menú de Arena con Dificultades (Fase 2.3 - MEJORADO)."""
    print("\n" + "="*70)
    print("🏛️  ARENA - SELECCIONA DIFICULTAD")
    print("="*70)
    
    # Información del equipo
    nivel_promedio = equipo.calcular_nivel_promedio()
    print(f"Nivel promedio del equipo: {nivel_promedio}")
    print(f"Dinero disponible: {equipo.dinero}g\n")
    
    dificultades = {
        "1": {
            "nombre": "NOVATO",
            "descripcion": "Enemigos nivel -2",
            "multiplicador_dificultad": 0.8,
            "recompensa_mult": 0.8,
            "req_nivel": 1,
            "emoji": "🟢",
            "label": "🟢 NOVATO",
            "recom_minimo": 1,
            "recom_maximo": 3
        },
        "2": {
            "nombre": "NORMAL",
            "descripcion": "Enemigos nivel +0",
            "multiplicador_dificultad": 1.0,
            "recompensa_mult": 1.0,
            "req_nivel": 3,
            "emoji": "🟡",
            "label": "🟡 NORMAL",
            "recom_minimo": 3,
            "recom_maximo": 8
        },
        "3": {
            "nombre": "EXPERTO",
            "descripcion": "Enemigos nivel +3",
            "multiplicador_dificultad": 1.5,
            "recompensa_mult": 1.5,
            "req_nivel": 10,
            "emoji": "🔴",
            "label": "🔴 EXPERTO",
            "recom_minimo": 10,
            "recom_maximo": 15
        },
        "4": {
            "nombre": "LEGENDARIA",
            "descripcion": "Enemigos nivel +5",
            "multiplicador_dificultad": 2.0,
            "recompensa_mult": 2.0,
            "req_nivel": 20,
            "emoji": "⭐",
            "label": "⭐ LEGENDARIA",
            "recom_minimo": 20,
            "recom_maximo": 999
        }
    }
    
    # IDEA 10: Selector visual mejorado con indicadores
    print("┌─ DIFICULTAD ─────────────────────────────────────────┐")
    
    for key, dif in dificultades.items():
        bloqueado = ""
        bloqueado_marca = ""
        
        if nivel_promedio < dif["req_nivel"]:
            bloqueado = f" 🔒 (Requiere Nivel {dif['req_nivel']})"
            bloqueado_marca = " [BLOQUEADO]"
        
        # Recomendación de nivel
        recom_texto = f"Nivel recom: {dif['recom_minimo']}-{dif['recom_maximo']}"
        
        # Análisis de dificultad
        if nivel_promedio >= dif["req_nivel"]:
            _, riesgo_color, win_prob = analizar_riesgo_combate(nivel_promedio, nivel_promedio + (int(dif["descripcion"].split()[-1]) if "+" in dif["descripcion"] else 0))
        else:
            riesgo_color = "🔒"
            win_prob = 0
        
        # Estimación de recompensas
        recompensa_est, xp_est = calcular_estimacion_recompensas(nivel_promedio, dif["recompensa_mult"])
        
        print(f"│                                                       │")
        print(f"│ [{key}] {dif['emoji']} {dif['nombre']:<15} [{recom_texto}]{bloqueado_marca}")
        print(f"│     Recompensa: {recompensa_est}g + {xp_est} XP (x{dif['recompensa_mult']}) │")
        print(f"│     Riesgo: {riesgo_color} {int(dif['multiplicador_dificultad']*100)}% | Win prob: {win_prob}%     │")
    
    print("│                                                       │")
    print("│ [0] SALIR                                             │")
    print("└─────────────────────────────────────────────────────────┘")
    
    opcion = input("\n➤ Elige dificultad [0-4]: ").strip()
    
    if opcion not in dificultades:
        if opcion == "0":
            return
        print("❌ Opción inválida")
        return
    
    dif = dificultades[opcion]
    
    # Validar nivel requerido
    if nivel_promedio < dif["req_nivel"]:
        print(f"\n❌ Nivel insuficiente (tienes {nivel_promedio}, necesitas {dif['req_nivel']})")
        return
    
    # IDEA 6: Análisis de riesgo pre-combate
    print(f"\n" + "="*70)
    print("📊 ANÁLISIS DE RIESGO PRE-COMBATE:")
    print("="*70)
    nivel_enemigo_est = nivel_promedio + (int(dif["descripcion"].split()[-1]) if "+" in dif["descripcion"] else int(dif["descripcion"].split()[-1]))
    riesgo_nombre, riesgo_emoji, win_prob = analizar_riesgo_combate(nivel_promedio, nivel_enemigo_est)
    print(f"Tu Nivel Promedio: {nivel_promedio}")
    print(f"Enemigo Aproximado: Nivel {nivel_enemigo_est}")
    print(f"Dificultad: {riesgo_emoji} {riesgo_nombre}")
    print(f"Probabilidad de Victoria: ~{win_prob}%")
    print("="*70)
    
    print(f"\n✓ Entrando a Arena {dif['nombre']}...")
    combate_equipo(equipo, dificultad=dif, multiplicador=dif["multiplicador_dificultad"], 
                   sistema_ligas=sistema_ligas, dificultad_label=dif["label"])


def combate_equipo(equipo, usuario=None, dificultad=None, multiplicador=1.0, sistema_ligas=None, dificultad_label="🟡 NORMAL"):
    """Flujo de combate con equipo (con soporte a dificultades Fase 2.3)."""
    print("\n🏛️  ¡Que comience el combate en la arena!\n")
    
    if dificultad:
        print(f"🏛️  Dificultad: {dificultad['emoji']} {dificultad['nombre']}")
    
    # Seleccionar luchador
    gladiador = seleccionar_luchador(equipo)
    if not gladiador:
        return
    
    # Mostrar habilidades del gladiador
    mostrar_habilidades_gladiador(gladiador)
    
    # Generar enemigo con escalado de dificultad
    nivel_escalado = equipo.calcular_nivel_promedio()
    
    # Ajustar nivel según dificultad
    if dificultad:
        if "nivel +5" in dificultad["descripcion"]:  # LEGENDARIA
            nivel_escalado += 5
        elif "nivel +3" in dificultad["descripcion"]:  # EXPERTO
            nivel_escalado += 3
        elif "nivel -2" in dificultad["descripcion"]:  # NOVATO
            nivel_escalado = max(1, nivel_escalado - 2)
    
    enemigo = generar_enemigo(nivel=nivel_escalado)
    
    # Aplicar multiplicador de dificultad a stats del enemigo
    if multiplicador != 1.0:
        enemigo.hp = int(enemigo.hp * multiplicador)
        enemigo.attack = int(enemigo.attack * multiplicador)
        enemigo.defense = int(enemigo.defense * multiplicador)
    
    mostrar_info_enemigo(enemigo)
    
    input("\nPresiona ENTER para iniciar combate...")
    
    # Hacer combate (con integración de habilidades)
    victoria, salud_final_jugador, salud_final_enemigo = combate_arena(
        salud_jugador=gladiador.hp_actual,
        daño_jugador=gladiador.ataque_final(),
        velocidad_jugador=gladiador.agilidad_final(),
        defensa_jugador=gladiador.defensa_final(),
        salud_enemigo=enemigo.hp_final(),
        daño_enemigo=enemigo.ataque_final(),
        velocidad_enemigo=enemigo.agilidad_final(),
        defensa_enemigo=enemigo.defensa_final(),
        daño_base=10,
        gladiador=gladiador,
        enemigo=enemigo
    )
    
    # Actualizar HP del gladiador
    gladiador.hp_actual = max(0, salud_final_jugador)
    
    # Procesar resultado
    if victoria:
        print("\n✓ ¡VICTORIA!")
        recompensa_base = random.randint(150, 350)
        
        # Aplicar multiplicador de dificultad a recompensas
        if multiplicador != 1.0:
            recompensa = int(recompensa_base * multiplicador)
            print(f"  Recompensa base: {recompensa_base}g")
            print(f"  Multiplicador: x{multiplicador}")
        else:
            recompensa = recompensa_base
        
        equipo.dinero += recompensa
        print(f"  💰 Ganaste {recompensa}g")
        
        # XP por victoria
        xp_ganada = int(calcular_xp_recompensa(gladiador.nivel) * multiplicador)
        subio = gladiador.ganar_xp(xp_ganada)
        print(f"  📈 {gladiador.nombre} ganó {xp_ganada} XP")
        
        # AUTO-TRACKING: Evento de victoria en combate
        misiones_completadas_combate = gestor_misiones.evento_combate_ganado()
        notif_combate = gestor_misiones.generar_notificacion_misiones(misiones_completadas_combate)
        if notif_combate:
            print(notif_combate)
        
        # AUTO-TRACKING: Evento de dinero acumulado
        misiones_completadas_dinero = gestor_misiones.evento_dinero_acumulado(recompensa)
        notif_dinero = gestor_misiones.generar_notificacion_misiones(misiones_completadas_dinero)
        if notif_dinero and notif_dinero != notif_combate:
            print(notif_dinero)
        
        if subio:
            print(gladiador.animacion_nivel_up())
            gladiador.hp_actual = min(gladiador.hp_actual, gladiador.hp)
            
            misiones_completadas_nivel = gestor_misiones.evento_gladiador_sube_nivel()
            notif_nivel = gestor_misiones.generar_notificacion_misiones(misiones_completadas_nivel)
            if notif_nivel:
                print(notif_nivel)
        
        gladiador.combates_ganados += 1
        gladiador.dinero_generado += recompensa
    else:
        print("\n✗ DERROTA...")
        print(f"  {gladiador.nombre} fue derrotado")
        gladiador.combates_perdidos += 1
        
        # Aplicar estado según daño
        if gladiador.hp_actual == 0:
            print(f"  ⚠️  {gladiador.nombre} está MUERTO - necesita revivir en hospital")
        elif gladiador.hp_actual < gladiador.hp * 0.25:
            print(f"  ⚠️  {gladiador.nombre} está en ESTADO CRÍTICO")
        else:
            print(f"  ⚠️  {gladiador.nombre} está HERIDO")
    
    print(f"  Record: {gladiador.combates_ganados}W-{gladiador.combates_perdidos}L")
    
    # NUEVA: Registrar en sistema de ligas (Fase 2.4)
    if sistema_ligas:
        puntos_ganados, xp_bonus, dinero_bonus = sistema_ligas.registrar_combate(
            gladiador,
            nombre_enemigo=enemigo.__class__.__name__,
            dificultad=dificultad_label,
            victoria=victoria
        )
        print(f"\n🏆 Liga: +{puntos_ganados}pts | Liga: {sistema_ligas.obtener_liga(gladiador.nombre).value}")
    
    # IDEA 7: Mostrar histórico de últimos combates por dificultad
    if dificultad:
        print("\n" + "="*70)
        print("📊 ESTADÍSTICAS DE ARENA:")
        print("="*70)
        print(f"Combates totales: {gladiador.combates_totales}")
        print(f"Historial: {obtener_historico_combates(gladiador)}")
        print("="*70)
    
    input("\nPresiona ENTER para continuar...")


# ============================================
# HOSPITAL
# ============================================

def hospital_menu(equipo):
    """Menú del hospital."""
    print("\n" + "="*70)
    print("🏥  HOSPITAL")
    print("="*70 + "\n")
    
    heridos = [g for g in equipo.gladiadores if g.hp_actual < g.hp or g.estado == "muerto"]
    
    if not heridos:
        print("✓ Todos tus gladiadores están sanos")
        return
    
    print("GLADIADORES NECESITANDO ATENCIÓN:\n")
    for i, g in enumerate(heridos, 1):
        costo = g.hp - g.hp_actual
        if g.estado == "muerto":
            print(f"  [{i}] {g.nombre} - MUERTO")
            print(f"       Revivir: 100g (restaura 75% HP)")
        else:
            print(f"  [{i}] {g.nombre} - {g.hp_actual}/{g.hp} ({g.estado.upper()})")
            print(f"       Curación: {costo}g (restaura al 100%)")
    
    print("  [0] Salir")
    
    opcion = input("\n¿A quién atiender? [0-{}]: ".format(len(heridos))).strip()
    
    try:
        idx = int(opcion)
        if idx == 0:
            return
        if 1 <= idx <= len(heridos):
            gladiador = heridos[idx - 1]
            
            if gladiador.estado == "muerto":
                costo = 100
                if equipo.dinero < costo:
                    print(f"❌ No tienes dinero para revivir (cuesta {costo}g)")
                    return
                equipo.dinero -= costo
                gladiador.revivir()
                print(f"✓ {gladiador.nombre} fue revivido por {costo}g")
            else:
                costo = gladiador.hp - gladiador.hp_actual
                if equipo.dinero < costo:
                    print(f"❌ No tienes dinero para curar (cuesta {costo}g)")
                    return
                equipo.dinero -= costo
                gladiador.curar(costo)
                print(f"✓ {gladiador.nombre} fue curado por {costo}g")
    except ValueError:
        print("❌ Opción inválida")


# ============================================
# BARRACAS
# ============================================

def barracas_menu(equipo):
    """🏠 Menú de Gestión de Equipo (Fase 2.3 - Sistema de Gladiadores)."""
    while True:
        print("\n" + "="*70)
        print("🏠 GESTIÓN DE EQUIPO")
        print("="*70)
        print(f"Gladiadores: {len(equipo.gladiadores)}/{equipo.barracas.espacios_totales}")
        print(f"Dinero: {equipo.dinero}g")
        
        # Mostrar resumen rápido
        disponibles = sum(1 for g in equipo.gladiadores if g.puede_luchar())
        ocupados = sum(1 for g in equipo.gladiadores if g.ocupacion == "ocupado")
        muertos = sum(1 for g in equipo.gladiadores if g.estado == "muerto")
        
        print(f"Estado: {disponibles} listos │ {ocupados} ocupados │ {muertos} muertos")
        
        print("\n[1] Ver equipo (detalles)")
        print("[2] Reclutar gladiador (200-500g)")
        print("[3] Entrenar gladiador (+stats, 1-3 días)")
        print("[4] Curar gladiador (restaura HP)")
        print("[5] Vender/Liberar gladiador")
        print("[6] Ampliar barracas (+2 espacios)")
        print("[0] Volver")
        
        opcion = input("\n➤ Elige opción [0-6]: ").strip()
        
        if opcion == "0":
            break
        elif opcion == "1":
            ver_equipo_detallado(equipo)
        elif opcion == "2":
            reclutar_gladiador_menu(equipo)
        elif opcion == "3":
            entrenar_gladiador_menu(equipo)
        elif opcion == "4":
            curar_gladiador_menu(equipo)
        elif opcion == "5":
            vender_gladiador_menu(equipo)
        elif opcion == "6":
            ampliar_barracas_menu(equipo)
        else:
            print("❌ Opción inválida")


def ver_equipo_detallado(equipo):
    """🎭 Ver detalles completos de todos los gladiadores - VERSIÓN MEJORADA."""
    if not equipo.gladiadores:
        print("\n❌ Tu equipo está vacío")
        return
    
    print("\n" + "="*70)
    print("🎭 EQUIPO DETALLADO")
    print("="*70)
    
    for i, g in enumerate(equipo.gladiadores, 1):
        # IDEA 2: Indicador visual de ocupación
        estado_emoji = "✓" if g.estado == "sano" else \
                      "⚠️" if g.estado == "herido" else \
                      "🔴" if g.estado == "critico" else "💀"
        
        # Indicador de ocupación con emoji
        ocupacion_indicator = ""
        if g.ocupacion == "ocupado":
            if g.razon_ocupacion == "entrenamiento":
                ocupacion_indicator = f"💪 En Entrenamiento"
            elif g.razon_ocupacion == "curacion":
                ocupacion_indicator = f"🏥 En Curación"
            else:
                ocupacion_indicator = f"⏳ Ocupado"
            
            # IDEA 1: Barra de progreso de ocupación
            barra = generar_barra_ocupacion(g.dias_ocupado, g.dias_ocupado + (3 - g.dias_ocupado))
            ocupacion_str = f"{ocupacion_indicator} {barra}"
        else:
            ocupacion_str = "✓ Disponible para combatir"
        
        print(f"\n{i}. {estado_emoji} {g.nombre} - {g.tipo} | Lvl {g.nivel}")
        print(f"   {ocupacion_str}")
        print(f"   ❤️  {g.hp_actual}/{g.hp} HP ({int(g.hp_actual/g.hp*100)}%)")
        print(f"   ⚔️  ATK: {g.ataque_final()} │ 🛡️  DEF: {g.defensa_final()} │ ⚡ AGI: {g.agilidad_final()}")
        print(f"   📊 Combates: {g.combates_ganados}W-{g.combates_perdidos}L | Ganancia: {g.dinero_generado}g")
    
    input("\nPresiona ENTER para continuar...")


def reclutar_gladiador_menu(equipo):
    """👨‍💼 Reclutar un nuevo gladiador."""
    if equipo.equipo_lleno:
        print("\n❌ Barracas llenas - Compra más literas")
        return
    
    print("\n" + "="*70)
    print("👨‍💼 RECLUTAR NUEVO GLADIADOR")
    print("="*70)
    print(f"Costo base: 300g | Dinero: {equipo.dinero}g")
    print(f"Espacio disponible: {equipo.espacios_disponibles}")
    
    if equipo.dinero < 200:
        print("\n❌ No tienes suficiente dinero (mínimo 200g)")
        return
    
    print("\nTipos disponibles:")
    tipos = ["Murmillo", "Retiarius", "Secutor", "Thraex", "Hoplomachus"]
    for i, tipo in enumerate(tipos, 1):
        print(f"[{i}] {tipo}")
    print("[0] Cancelar")
    
    opcion = input("\nElige tipo: ").strip()
    
    if opcion == "0":
        return
    
    try:
        idx = int(opcion) - 1
        if 0 <= idx < len(tipos):
            tipo = tipos[idx]
            costo = 300  # Coste base
            
            if equipo.dinero < costo:
                print(f"\n❌ Necesitas {costo}g (tienes {equipo.dinero}g)")
                return
            
            nombre = input(f"¿Nombre del {tipo}? ").strip()
            if not nombre:
                nombre = f"{tipo}_{len(equipo.gladiadores)+1}"
            
            nuevo = Gladiador(nombre, tipo, nivel=1)
            exito, msg = equipo.agregar_gladiador(nuevo)
            
            if exito:
                equipo.dinero -= costo
                print(f"\n✅ {msg}")
                print(f"Dinero restante: {equipo.dinero}g")
            else:
                print(f"\n❌ {msg}")
    except ValueError:
        print("❌ Entrada inválida")


def entrenar_gladiador_menu(equipo):
    """💪 Entrenar un gladiador (mejora stats) - VERSIÓN MEJORADA."""
    if not equipo.gladiadores:
        print("\n❌ Tu equipo está vacío")
        return
    
    print("\n" + "="*70)
    print("💪 ENTRENAR GLADIADOR")
    print("="*70)
    print("Costo: 100g por día | Beneficio: +1-3 stats por día\n")
    
    # IDEA 5: Estadísticas del gladiador al seleccionar
    for i, g in enumerate(equipo.gladiadores, 1):
        estado = "Disponible ✓" if g.ocupacion == "disponible" else f"Ocupado ({g.razon_ocupacion})"
        
        # Indicador visual de ocupación
        ocupacion_visual = ""
        if g.ocupacion == "ocupado":
            ocupacion_visual = f"  {generar_barra_ocupacion(g.dias_ocupado, 3)}"
        
        # Historial de combates
        historial = obtener_historico_combates(g)
        
        print(f"[{i}] {g.nombre} ({g.tipo}, Lvl {g.nivel}) {estado}")
        print(f"    Stats: ⚔️ {g.ataque_final()} | 🛡️ {g.defensa_final()} | ❤️ {g.hp_final()}")
        print(f"    Historial: {historial}")
        if ocupacion_visual:
            print(f"    Progreso:{ocupacion_visual}")
        print()
    
    print("[0] Cancelar")
    
    opcion = input("Elige gladiador: ").strip()
    
    if opcion == "0":
        return
    
    try:
        idx = int(opcion) - 1
        if 0 <= idx < len(equipo.gladiadores):
            gladiador = equipo.gladiadores[idx]
            
            if gladiador.ocupacion == "ocupado":
                print(f"\n❌ {gladiador.nombre} está ocupado ({gladiador.dias_ocupado} días restantes)")
                return
            
            # Guardar stats antes del entrenamiento
            stats_antes = {
                "Fuerza": gladiador.fuerza,
                "Ataque": gladiador.ataque_final(),
                "Defensa": gladiador.defensa_final()
            }
            
            print(f"\nEntrenamiento de {gladiador.nombre}:")
            print("="*70)
            print("[1] Entrenamiento corto (1 día)")
            print("    Costo: 100g | Mejora: +1 Fuerza/Ataque")
            print("[2] Entrenamiento medio (2 días)")
            print("    Costo: 200g | Mejora: +2 Fuerza/Ataque")
            print("[3] Entrenamiento intenso (3 días)")
            print("    Costo: 300g | Mejora: +3 Fuerza/Ataque")
            print("[0] Cancelar")
            
            plan = input("\nElige plan: ").strip()
            
            planes = {
                "1": (1, 100, 1),
                "2": (2, 200, 2),
                "3": (3, 300, 3)
            }
            
            if plan in planes:
                dias, costo, stats = planes[plan]
                
                if equipo.dinero < costo:
                    print(f"\n❌ Necesitas {costo}g (tienes {equipo.dinero}g)")
                    return
                
                equipo.dinero -= costo
                gladiador.ocupar("entrenamiento", dias)
                
                # Aplicar mejora de stats
                gladiador.fuerza += stats
                gladiador.attack += stats
                gladiador.calcular_stats_finales()
                
                # IDEA 3: Mostrar resumen de cambios
                print(f"\n" + "="*70)
                print(f"✅ {gladiador.nombre} comenzó entrenamiento ({dias} día(s))")
                print("="*70)
                print(f"\n📊 CAMBIOS DE STATS:")
                print(f"  ⚔️  Ataque:  {stats_antes['Ataque']} → {gladiador.ataque_final()} (+{gladiador.ataque_final() - stats_antes['Ataque']}) ⬆️")
                print(f"  💪 Fuerza:  {stats_antes['Fuerza']} → {gladiador.fuerza} (+{gladiador.fuerza - stats_antes['Fuerza']}) ⬆️")
                print(f"  🛡️  Defensa: {stats_antes['Defensa']} (sin cambios)")
                
                # IDEA 4: Animación ASCII
                mostrar_animacion_mejora({"ATK": stats_antes['Ataque'], "Fuerza": int(stats_antes['Fuerza'])}, 
                                        {"ATK": gladiador.ataque_final(), "Fuerza": int(gladiador.fuerza)})
                
                print(f"💰 Dinero restante: {equipo.dinero}g")
                print(f"⏰ Disponible en: {dias} día(s)")
                print("="*70)
    except ValueError:
        print("❌ Entrada inválida")


def curar_gladiador_menu(equipo):
    """🏥 Curar un gladiador (restaura HP)."""
    heridos = [g for g in equipo.gladiadores if g.estado != "sano"]
    
    if not heridos:
        print("\n✓ Todos tus gladiadores están sanos")
        return
    
    print("\n" + "="*70)
    print("🏥 HOSPITAL")
    print("="*70)
    print("Costo: 50g por 25 HP restaurados\n")
    
    for i, g in enumerate(heridos, 1):
        hp_perdido = g.hp - g.hp_actual
        costo_curacion = int((hp_perdido / 25) * 50)
        print(f"[{i}] {g.nombre} ({g.estado})")
        print(f"    HP: {g.hp_actual}/{g.hp} | Costo total: {costo_curacion}g")
    print("[0] Cancelar")
    
    opcion = input("\nElige gladiador: ").strip()
    
    if opcion == "0":
        return
    
    try:
        idx = int(opcion) - 1
        if 0 <= idx < len(heridos):
            gladiador = heridos[idx]
            hp_perdido = gladiador.hp - gladiador.hp_actual
            costo = int((hp_perdido / 25) * 50)
            
            if equipo.dinero < costo:
                print(f"\n❌ Necesitas {costo}g (tienes {equipo.dinero}g)")
                return
            
            equipo.dinero -= costo
            gladiador.curar(hp_perdido)
            
            print(f"\n✅ {gladiador.nombre} fue curado")
            print(f"   HP: {gladiador.hp_actual}/{gladiador.hp}")
            print(f"   Dinero: {equipo.dinero}g")
    except ValueError:
        print("❌ Entrada inválida")


def vender_gladiador_menu(equipo):
    """🔄 Vender/Liberar un gladiador."""
    if not equipo.gladiadores:
        print("\n❌ Tu equipo está vacío")
        return
    
    print("\n" + "="*70)
    print("🔄 VENDER GLADIADOR")
    print("="*70)
    print("Valor venta: 50% del costo de reclutamiento (150g base)\n")
    
    for i, g in enumerate(equipo.gladiadores, 1):
        valor_venta = 150 + (g.nivel * 10)
        print(f"[{i}] {g.nombre} ({g.tipo}, Lvl {g.nivel})")
        print(f"    Valor: {valor_venta}g")
    print("[0] Cancelar")
    
    opcion = input("\nElige gladiador: ").strip()
    
    if opcion == "0":
        return
    
    try:
        idx = int(opcion) - 1
        if 0 <= idx < len(equipo.gladiadores):
            gladiador = equipo.gladiadores[idx]
            valor_venta = 150 + (gladiador.nivel * 10)
            
            confirmar = input(f"¿Vender {gladiador.nombre} por {valor_venta}g? (s/n): ").strip().lower()
            
            if confirmar == "s":
                equipo.dinero += valor_venta
                exito, msg = equipo.remover_gladiador(idx)
                print(f"\n✅ {msg}")
                print(f"   +{valor_venta}g | Dinero total: {equipo.dinero}g")
    except ValueError:
        print("❌ Entrada inválida")


def ampliar_barracas_menu(equipo):
    """🏗️ Comprar literas (ampliar barracas)."""
    if not equipo.barracas.proxima_litera_disponible:
        print("\n✓ Barracas al máximo (10 espacios)")
        return
    
    costo = equipo.barracas.costo_proxima_litera
    
    print("\n" + "="*70)
    print("🏗️  AMPLIAR BARRACAS")
    print("="*70)
    print(f"Literas actuales: {equipo.barracas.literas}/5")
    print(f"Espacios: {equipo.barracas.espacios_totales}/10")
    print(f"\nComprar litera: {costo}g")
    print(f"Dinero: {equipo.dinero}g")
    
    if equipo.dinero >= costo:
        confirmar = input("\n¿Comprar litera? (s/n): ").strip().lower()
        if confirmar == "s":
            exito, equipo.dinero, msg = equipo.barracas.comprar_litera(equipo.dinero)
            print(f"\n{msg}")
            if exito:
                print(f"Nuevos espacios: {equipo.barracas.espacios_totales}")
    else:
        print(f"\n❌ Necesitas {costo}g (te faltan {costo - equipo.dinero}g)")


# ============================================
# LIGA (Fase 2.4 - Sistema de Ligas)
# ============================================

def liga_menu(equipo, sistema_ligas):
    """🏆 Menú de Liga - Ver ranking y estadísticas."""
    while True:
        print("\n" + "="*70)
        print("🏆 SISTEMA DE LIGAS")
        print("="*70)
        
        # Mostrar estatus del equipo
        gladiadores_en_ligas = len(sistema_ligas.ranking)
        print(f"Gladiadores en liga: {gladiadores_en_ligas}")
        if gladiadores_en_ligas > 0:
            top = sistema_ligas.obtener_ranking_top10()
            if top:
                print(f"Líder: {top[0][0]} ({top[0][1]['puntos']}pts - {top[0][1]['liga'].value})")
        
        print("\n[1] Ver Ranking (Top 10)")
        print("[2] Ver mi Estadística")
        print("[3] Ver Historial de Combates")
        print("[4] Ver Detalles de Gladiador")
        print("[0] Volver")
        
        opcion = input("\n➤ Elige opción [0-4]: ").strip()
        
        if opcion == "0":
            break
        elif opcion == "1":
            mostrar_ranking_top10(sistema_ligas)
        elif opcion == "2":
            mostrar_estadistica_equipo(equipo, sistema_ligas)
        elif opcion == "3":
            mostrar_historial_combates(sistema_ligas)
        elif opcion == "4":
            ver_detalles_gladiador_liga(equipo, sistema_ligas)
        else:
            print("❌ Opción inválida")


def mostrar_ranking_top10(sistema_ligas):
    """Mostrar top 10 gladiadores."""
    top10 = sistema_ligas.obtener_ranking_top10()
    
    if not top10:
        print("\n❌ No hay combates registrados aún")
        return
    
    print("\n" + "="*70)
    print("🏆 RANKING TOP 10")
    print("="*70)
    print(f"{'Posición':<10} {'Nombre':<20} {'Liga':<12} {'Puntos':<10} {'W-L':<10}")
    print("-" * 70)
    
    for i, (nombre, stats) in enumerate(top10, 1):
        liga_emoji = {
            "Bronce": "🟢",
            "Plata": "⚪",
            "Oro": "🟡",
            "Leyenda": "⭐"
        }.get(stats["liga"].value, "?")
        
        print(f"{i:<10} {nombre:<20} {liga_emoji} {stats['liga'].value:<10} "
              f"{stats['puntos']:<10} {stats['victorias']}-{stats['derrotas']:<8}")
    
    input("\nPresiona ENTER para continuar...")


def mostrar_estadistica_equipo(equipo, sistema_ligas):
    """Mostrar estadísticas agregadas del equipo."""
    if not equipo.gladiadores:
        print("\n❌ Tu equipo está vacío")
        return
    
    print("\n" + "="*70)
    print("📊 ESTADÍSTICAS DEL EQUIPO")
    print("="*70)
    
    stats_totales = {
        "victorias": 0,
        "derrotas": 0,
        "puntos": 0,
        "combates": 0
    }
    
    print(f"\n{'Gladiador':<20} {'Liga':<12} {'Puntos':<10} {'W-L':<15} {'Winrate':<10}")
    print("-" * 70)
    
    for g in equipo.gladiadores:
        if g.nombre in sistema_ligas.ranking:
            stats = sistema_ligas.ranking[g.nombre]
            liga_emoji = {
                "Bronce": "🟢",
                "Plata": "⚪",
                "Oro": "🟡",
                "Leyenda": "⭐"
            }.get(stats["liga"].value, "?")
            
            winrate = sistema_ligas.obtener_winrate(g.nombre)
            print(f"{g.nombre:<20} {liga_emoji} {stats['liga'].value:<10} "
                  f"{stats['puntos']:<10} {stats['victorias']}-{stats['derrotas']:<13} {winrate}%")
            
            stats_totales["victorias"] += stats["victorias"]
            stats_totales["derrotas"] += stats["derrotas"]
            stats_totales["puntos"] += stats["puntos"]
            stats_totales["combates"] += stats["combates_totales"]
    
    if stats_totales["combates"] > 0:
        winrate_equipo = int((stats_totales["victorias"] / stats_totales["combates"]) * 100)
    else:
        winrate_equipo = 0
    
    print("-" * 70)
    print(f"{'TOTAL':<20} {'-':<12} {stats_totales['puntos']:<10} "
          f"{stats_totales['victorias']}-{stats_totales['derrotas']:<13} {winrate_equipo}%")
    
    input("\nPresiona ENTER para continuar...")


def mostrar_historial_combates(sistema_ligas, limite=20):
    """Mostrar últimos combates."""
    historial = sistema_ligas.obtener_historial(limite=limite)
    
    if not historial:
        print("\n❌ No hay combates registrados")
        return
    
    print("\n" + "="*70)
    print(f"📜 HISTORIAL DE COMBATES (Últimos {len(historial)})")
    print("="*70)
    
    for i, combate in enumerate(historial, 1):
        resultado = "✓ VICTORIA" if combate.victoria else "✗ DERROTA"
        print(f"\n{i}. {resultado}")
        print(f"   {combate.nombre_gladiador} (Lvl {combate.nivel_gladiador}) vs {combate.nombre_enemigo}")
        print(f"   Dificultad: {combate.dificultad}")
        print(f"   +{combate.puntos_ganados}pts | +{combate.xp_ganados}xp | +{combate.dinero_ganado}g")
        print(f"   Fecha: {combate.fecha.strftime('%d/%m/%Y %H:%M')}")
    
    input("\nPresiona ENTER para continuar...")


def ver_detalles_gladiador_liga(equipo, sistema_ligas):
    """Ver detalles detallados de un gladiador en la liga."""
    if not equipo.gladiadores:
        print("\n❌ Tu equipo está vacío")
        return
    
    print("\n" + "="*70)
    print("👤 DETALLES DE GLADIADOR EN LIGA")
    print("="*70)
    print("Selecciona un gladiador:\n")
    
    for i, g in enumerate(equipo.gladiadores, 1):
        print(f"[{i}] {g.nombre} ({g.tipo}, Lvl {g.nivel})")
    print("[0] Cancelar")
    
    opcion = input("\n➤ Elige: ").strip()
    
    if opcion == "0":
        return
    
    try:
        idx = int(opcion) - 1
        if 0 <= idx < len(equipo.gladiadores):
            gladiador = equipo.gladiadores[idx]
            reporte = sistema_ligas.generar_reporte_estadisticas(gladiador.nombre)
            
            if reporte:
                print("\n" + "="*70)
                print(f"📊 {reporte['nombre'].upper()}")
                print("="*70)
                print(f"Tipo: {gladiador.tipo} | Nivel: {gladiador.nivel}")
                print(f"\nLiga: ⭐ {reporte['liga']}")
                print(f"Puntos: {reporte['puntos']}")
                print(f"\nEstadísticas de Combate:")
                print(f"   Victorias: {reporte['victorias']}")
                print(f"   Derrotas: {reporte['derrotas']}")
                print(f"   Total: {reporte['combates']}")
                print(f"   Winrate: {reporte['winrate']}%")
                
                # Mostrar últimos combates del gladiador
                historial = sistema_ligas.obtener_historial(gladiador.nombre, limite=5)
                if historial:
                    print(f"\nÚltimos Combates:")
                    for combate in historial:
                        resultado = "✓" if combate.victoria else "✗"
                        print(f"   {resultado} {combate.nombre_enemigo} ({combate.dificultad}) - +{combate.puntos_ganados}pts")
            else:
                print(f"\n⚠️  {gladiador.nombre} aún no tiene combates registrados")
    except ValueError:
        print("❌ Entrada inválida")
    
    input("\nPresiona ENTER para continuar...")


# ============================================
# FACILIDADES - MÉDICO Y HERRERO (FASE 2.5)
# ============================================

def menu_facilidades(equipo, facilities):
    """Menú principal de mejoras de facilidades."""
    while True:
        print("\n" + "="*80)
        print("⚒️  MEJORAS DE FACILIDADES")
        print("="*80)
        print(facilities.generar_resumen())
        
        print("""
╔════════════════════════════════════════════╗
║        SELECCIONA UNA FACILIDAD            ║
╠════════════════════════════════════════════╣
║  1. 🏥 Médico (Curación + Curación Rápida) ║
║  2. ⚒️  Herrero (Armas + Mejoras)           ║
║  3. 🚪 Volver                               ║
╚════════════════════════════════════════════╝
        """)
        
        opcion = input("Elige una opción: ").strip()
        
        if opcion == "1":
            menu_medico(equipo, facilities)
        elif opcion == "2":
            menu_herrero(equipo, facilities)
        elif opcion == "3":
            break
        else:
            print("❌ Opción inválida")


def menu_medico(equipo, facilities):
    """Menú del Médico con curaciones progresivas."""
    medico = facilities.medico
    
    while True:
        print("\n" + "="*80)
        print("🏥 MÉDICO - SISTEMA DE CURACIÓN PROGRESIVA")
        print("="*80)
        print(medico.generar_string())
        print(medico.generar_resumen_estadisticas())
        
        print("╔════════════════════════════════════════╗")
        print("║         TIPOS DE CURACIÓN              ║")
        print("╠════════════════════════════════════════╣")
        
        # Muestra info de Curación Básica
        basica_porcentaje, basica_dias, basica_costo = medico.curacion_basica[medico.nivel]
        print(f"║ 1. CURACIÓN BÁSICA (❤️  {basica_porcentaje*100:.0f}% HP)      ║")
        print(f"║    Ocupación: {basica_dias} día | Costo: {basica_costo}g (estable)")
        
        # Muestra info de Curación Profunda
        profunda_porcentaje, profunda_dias, profunda_costo = medico.curacion_profunda[medico.nivel]
        print(f"║ 2. CURACIÓN PROFUNDA (💪 {profunda_porcentaje*100:.0f}% HP)   ║")
        print(f"║    Ocupación: {profunda_dias} días | Costo base: {profunda_costo}g")
        
        # Muestra info de Curación Completa
        completa_porcentaje, completa_dias, completa_costo = medico.curacion_completa[medico.nivel]
        print(f"║ 3. CURACIÓN COMPLETA (✨ {completa_porcentaje*100:.0f}% HP)   ║")
        print(f"║    Ocupación: {completa_dias} días | Costo base: {completa_costo}g")
        
        # Muestra info de Curación Rápida
        if medico.curacion_rapida_desbloqueada:
            rapida_porcentaje, rapida_costo = medico.curacion_rapida[medico.nivel]
            print(f"║ 4. CURACIÓN RÁPIDA (⚡ {rapida_porcentaje*100:.0f}% HP)      ║")
            print(f"║    Ocupación: 0 días (INMEDIATA) | Costo: {rapida_costo}g")
            print(f"║    Usos hoy: {'✅ Disponible' if not medico.curacion_rapida_usado else '❌ Usado'}")
        
        print("║────────────────────────────────────────║")
        print(f"║ 5. Revivir Gladiador (Costo: {medico.costo_revive[medico.nivel]}g)  ║")
        print(f"║ 6. Mejorar Médico (Costo: {medico.costo_proximo_nivel() if medico.puede_mejorar() else '---'}g)")
        print("║ 0. Volver                              ║")
        print("╚════════════════════════════════════════╝")
        
        opcion = input("\nSelecciona opción: ").strip()
        
        if opcion == "1":
            # Curación Básica
            print("\n" + "="*80)
            print("❤️  CURACIÓN BÁSICA")
            print("="*80)
            
            heridos = [g for g in equipo.gladiadores if g.hp_actual < g.hp_maximo]
            if not heridos:
                print("✅ Todos tus gladiadores están en perfectas condiciones")
            else:
                print(f"\n(Restaura {basica_porcentaje*100:.0f}% HP | Ocupación: {basica_dias} día | Costo: {basica_costo}g)\n")
                for i, g in enumerate(heridos, 1):
                    hp_faltante = g.hp_maximo - g.hp_actual
                    print(f"  {i}. {g.nombre} ({g.hp_actual}/{g.hp_maximo} HP, falta {hp_faltante})")
                
                try:
                    idx = int(input("\n¿Cuál gladiador?: ")) - 1
                    if 0 <= idx < len(heridos):
                        g = heridos[idx]
                        exito, costo, dias, msg = medico.curar_basica(g, equipo.dinero)
                        if exito:
                            equipo.dinero -= costo
                            g.ocupar("Curación", dias)
                            print(f"✅ {msg}")
                        else:
                            print(f"❌ {msg}")
                except ValueError:
                    print("❌ Operación cancelada")
            
            input("\nPresiona ENTER para continuar...")
        
        elif opcion == "2":
            # Curación Profunda
            print("\n" + "="*80)
            print("💪 CURACIÓN PROFUNDA")
            print("="*80)
            
            heridos = [g for g in equipo.gladiadores if g.hp_actual < g.hp_maximo]
            if not heridos:
                print("✅ Todos tus gladiadores están en perfectas condiciones")
            else:
                print(f"\n(Restaura {profunda_porcentaje*100:.0f}% HP | Ocupación: {profunda_dias} días | Costo base: {profunda_costo}g)")
                print("(+50% si está en estado crítico)\n")
                for i, g in enumerate(heridos, 1):
                    hp_faltante = g.hp_maximo - g.hp_actual
                    estado = "🔴 CRÍTICO" if (g.hp_actual / g.hp_maximo) * 100 < 30 else "🟡 HERIDO"
                    print(f"  {i}. {g.nombre} ({g.hp_actual}/{g.hp_maximo} HP) {estado}")
                
                try:
                    idx = int(input("\n¿Cuál gladiador?: ")) - 1
                    if 0 <= idx < len(heridos):
                        g = heridos[idx]
                        exito, costo, dias, msg = medico.curar_profunda(g, equipo.dinero)
                        if exito:
                            equipo.dinero -= costo
                            g.ocupar("Curación", dias)
                            print(f"✅ {msg}")
                        else:
                            print(f"❌ {msg}")
                except ValueError:
                    print("❌ Operación cancelada")
            
            input("\nPresiona ENTER para continuar...")
        
        elif opcion == "3":
            # Curación Completa
            print("\n" + "="*80)
            print("✨ CURACIÓN COMPLETA")
            print("="*80)
            
            heridos = [g for g in equipo.gladiadores if g.hp_actual < g.hp_maximo]
            if not heridos:
                print("✅ Todos tus gladiadores están en perfectas condiciones")
            else:
                print(f"\n(Restaura 100% HP | Ocupación: {completa_dias} días | Costo base: {completa_costo}g)")
                print("(+50% si está en estado crítico)\n")
                for i, g in enumerate(heridos, 1):
                    hp_faltante = g.hp_maximo - g.hp_actual
                    estado = "🔴 CRÍTICO" if (g.hp_actual / g.hp_maximo) * 100 < 30 else "🟡 HERIDO"
                    print(f"  {i}. {g.nombre} ({g.hp_actual}/{g.hp_maximo} HP) {estado}")
                
                try:
                    idx = int(input("\n¿Cuál gladiador?: ")) - 1
                    if 0 <= idx < len(heridos):
                        g = heridos[idx]
                        exito, costo, dias, msg = medico.curar_completa(g, equipo.dinero)
                        if exito:
                            equipo.dinero -= costo
                            g.ocupar("Curación", dias)
                            print(f"✅ {msg}")
                        else:
                            print(f"❌ {msg}")
                except ValueError:
                    print("❌ Operación cancelada")
            
            input("\nPresiona ENTER para continuar...")
        
        elif medico.curacion_rapida_desbloqueada and opcion == "4":
            # Curación Rápida (INMEDIATA)
            print("\n" + "="*80)
            print("⚡ CURACIÓN RÁPIDA (INMEDIATA)")
            print("="*80)
            
            heridos = [g for g in equipo.gladiadores if g.hp_actual < g.hp_maximo]
            if not heridos:
                print("Todos están sanos")
            else:
                rapida_porcentaje, rapida_costo = medico.curacion_rapida[medico.nivel]
                print(f"\n(Restaura {rapida_porcentaje*100:.0f}% HP | INMEDIATA (0 días) | Costo base: {rapida_costo}g)")
                print("(+100% si está en estado crítico)\n")
                
                for i, g in enumerate(heridos, 1):
                    hp_faltante = g.hp_maximo - g.hp_actual
                    estado = "🔴 CRÍTICO" if (g.hp_actual / g.hp_maximo) * 100 < 30 else "🟡 HERIDO"
                    print(f"  {i}. {g.nombre} ({g.hp_actual}/{g.hp_maximo} HP) {estado}")
                
                try:
                    idx = int(input("\n¿Quién recibirá Curación Rápida?: ")) - 1
                    if 0 <= idx < len(heridos):
                        g = heridos[idx]
                        exito, costo, dias, msg = medico.curar_rapida(g, equipo.dinero)
                        if exito:
                            equipo.dinero -= costo
                            # Curación Rápida NO ocupa días
                            print(f"✅ {msg}")
                        else:
                            print(f"❌ {msg}")
                except ValueError:
                    print("❌ Cancelado")
            
            input("\nPresiona ENTER para continuar...")
        
        elif opcion == "5":
            # Revivir
            print("\n" + "="*80)
            print("✅ REVIVIR GLADIADOR")
            print("="*80)
            
            muertos = [g for g in equipo.gladiadores if g.hp_actual <= 0]
            if not muertos:
                print("Todos tus gladiadores están vivos")
            else:
                print(f"\n(Costo: {medico.costo_revive[medico.nivel]}g)\n")
                for i, g in enumerate(muertos, 1):
                    print(f"  {i}. {g.nombre}")
                
                try:
                    idx = int(input("\n¿Cuál revivir?: ")) - 1
                    if 0 <= idx < len(muertos):
                        g = muertos[idx]
                        exito, costo, msg = medico.revivir(g, equipo.dinero)
                        if exito:
                            equipo.dinero -= costo
                            print(f"✅ {msg}")
                        else:
                            print(f"❌ {msg}")
                except ValueError:
                    print("❌ Cancelado")
            
            input("\nPresiona ENTER para continuar...")
        
        elif opcion == "6":
            # Mejorar Médico
            if medico.puede_mejorar():
                costo = medico.costo_proximo_nivel()
                exito, mensaje = medico.mejorar(equipo.dinero)
                if exito:
                    equipo.dinero -= costo
                    print(f"\n✅ {mensaje}")
                    if medico.nivel == 2:
                        print("🔓 ⚡ ¡Curación Rápida desbloqueada!")
                else:
                    print(f"\n❌ {mensaje}")
            else:
                print("\n🏥 Médico ya está al máximo nivel (5)")
            
            input("\nPresiona ENTER para continuar...")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")



def menu_herrero(equipo, facilities):
    """Menú del Herrero - Sistema de Mejora de Armas v2.0"""
    herrero = facilities.herrero
    
    while True:
        print("\n" + "="*80)
        print(herrero.generar_string())
        print("="*80)
        print()
        
        # Mostrar armas en inventario con durabilidad y costo de próxima mejora
        if equipo.inventario_armas:
            print("⚔️  ARMAS EN INVENTARIO:")
            for idx, arma in enumerate(equipo.inventario_armas, 1):
                nivel_mejora = getattr(arma, 'nivel_mejora', 0)
                durabilidad = getattr(arma, 'durabilidad', 100)
                costo_proximo = herrero._calcular_costo_mejora(arma) if hasattr(arma, 'tier') else 0
                
                # Color de durabilidad
                if durabilidad < 30:
                    durabilidad_icon = "🔴"
                elif durabilidad < 70:
                    durabilidad_icon = "🟡"
                else:
                    durabilidad_icon = "🟢"
                
                print(f"  {idx}. {arma.nombre} [+{nivel_mejora}] | ATK:{arma.attack} | {durabilidad_icon} {durabilidad:.0f}% durabilidad | Próxima mejora: {costo_proximo}g")
            print()
        
        print("OPCIONES:")
        print(f"  1. Mejorar Arma")
        print(f"  2. Reparar Arma")
        print(f"  3. Ver Armas Disponibles (Comprar)")
        print(f"  4. Mejorar Herrero (Costo: {herrero.costo_proximo_nivel()}g)")
        print(f"  5. Estadísticas del Herrero")
        print(f"  0. Volver")
        
        opcion = input("\nSelecciona opción: ").strip()
        
        if opcion == "1":
            # Mejorar arma
            if not equipo.inventario_armas:
                print("❌ No tienes armas para mejorar")
                input("\nPresiona ENTER para continuar...")
                continue
            
            print("\nSelecciona arma a mejorar (0 para cancelar):")
            for idx, arma in enumerate(equipo.inventario_armas, 1):
                print(f"  {idx}. {arma.nombre}")
            
            try:
                seleccion = int(input("➤ Número: ").strip())
                if seleccion == 0:
                    continue
                if 1 <= seleccion <= len(equipo.inventario_armas):
                    arma = equipo.inventario_armas[seleccion - 1]
                    exito, costo, msg = herrero.mejorar_arma(arma, equipo.dinero)
                    if exito:
                        equipo.dinero -= costo
                        print(f"\n✅ {msg}")
                    else:
                        print(f"\n❌ {msg}")
                else:
                    print("❌ Opción inválida")
            except ValueError:
                print("❌ Entrada inválida")
            
            input("\nPresiona ENTER para continuar...")
        
        elif opcion == "2":
            # Reparar arma
            if not equipo.inventario_armas:
                print("❌ No tienes armas para reparar")
                input("\nPresiona ENTER para continuar...")
                continue
            
            print("\nSelecciona arma a reparar (0 para cancelar):")
            for idx, arma in enumerate(equipo.inventario_armas, 1):
                durabilidad = getattr(arma, 'durabilidad', 100)
                if durabilidad < 100:
                    print(f"  {idx}. {arma.nombre} ({durabilidad:.0f}% durabilidad)")
                else:
                    print(f"  {idx}. {arma.nombre} (✅ Perfecta - No necesita reparación)")
            
            try:
                seleccion = int(input("➤ Número: ").strip())
                if seleccion == 0:
                    continue
                if 1 <= seleccion <= len(equipo.inventario_armas):
                    arma = equipo.inventario_armas[seleccion - 1]
                    exito, costo, msg = herrero.reparar_arma(arma, equipo.dinero)
                    if exito:
                        equipo.dinero -= costo
                        print(f"\n✅ {msg}")
                    else:
                        print(f"\n❌ {msg}")
                else:
                    print("❌ Opción inválida")
            except ValueError:
                print("❌ Entrada inválida")
            
            input("\nPresiona ENTER para continuar...")
        
        elif opcion == "3":
            # Ver catálogo y comprar
            mostrar_catalogo_herrero(herrero.obtener_tier_desbloqueado())
            
            print("\nCOMPRAR ARMA:")
            try:
                opcion_arma = input("Ingresa el número del arma (0 para cancelar): ").strip()
                if opcion_arma != "0":
                    exito, precio, msg = comprar_item_herrero(opcion_arma, equipo.dinero, equipo.inventario_armas, herrero.obtener_tier_desbloqueado())
                    if exito:
                        equipo.dinero -= precio
                        print(f"✅ {msg}")
                    else:
                        print(f"❌ {msg}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            input("\nPresiona ENTER para continuar...")
        
        elif opcion == "4":
            # Mejorar Herrero
            if herrero.puede_mejorar():
                costo = herrero.costo_proximo_nivel()
                if equipo.dinero >= costo:
                    exito, msg = herrero.mejorar(equipo.dinero)
                    if exito:
                        equipo.dinero -= costo
                        print(f"\n✅ {msg}")
                        print(f"🔓 Ahora puedes comprar armas Tier {herrero.obtener_tier_desbloqueado()}!")
                    else:
                        print(f"\n❌ {msg}")
                else:
                    print(f"\n❌ No tienes suficiente dinero. Necesitas {costo}g (tienes {equipo.dinero}g)")
            else:
                print("⚒️  Herrero ya está al máximo nivel (Nivel 5)")
            
            input("\nPresiona ENTER para continuar...")
        
        elif opcion == "5":
            # Estadísticas
            print(herrero.generar_resumen_estadisticas())
            input("\nPresiona ENTER para continuar...")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")



# ============================================
# TORNEOS (FASE 4)
# ============================================

def torneo_menu(equipo):
    """Menú de torneos."""
    while True:
        print("\n" + "="*70)
        print("🏆 SISTEMA DE TORNEOS")
        print("="*70)
        print("""
  [1] Crear nuevo torneo
  [2] Ver torneo activo
  [3] Completar siguiente enfrentamiento
  [4] Ver resultado del torneo
  [5] Volver
""")
        
        opcion = input("➤ Elige: ").strip()
        
        if opcion == "1":
            # Crear torneo
            if not equipo.gladiadores:
                print("\n❌ No tienes gladiadores para un torneo")
                input("Presiona ENTER...")
                continue
            
            print(f"\n📝 Creando nuevo torneo...")
            print(f"Participantes disponibles: {len(equipo.gladiadores)}")
            
            nombre_torneo = input("\n📛 Nombre del torneo: ").strip() or "Torneo Épico"
            
            # Usar todos los gladiadores del equipo como participantes
            participantes = [g for g in equipo.gladiadores if g.estado != "muerto"]
            
            if len(participantes) < 2:
                print("\n❌ Necesitas al menos 2 gladiadores vivos")
                input("Presiona ENTER...")
                continue
            
            from src.models import Torneo
            equipo.torneo_actual = Torneo(nombre_torneo, participantes)
            print(f"\n✓ Torneo '{nombre_torneo}' creado con {len(participantes)} participantes")
            print(f"✓ Total de emparejamientos: {sum(len(r) for r in equipo.torneo_actual.rondas)}")
            input("Presiona ENTER...")
        
        elif opcion == "2":
            # Ver torneo activo
            if not hasattr(equipo, 'torneo_actual') or equipo.torneo_actual is None:
                print("\n❌ No hay torneo activo")
                input("Presiona ENTER...")
                continue
            
            torneo = equipo.torneo_actual
            estado = torneo.obtener_estado_torneo()
            
            print("\n" + "="*70)
            print(f"🏆 {estado['nombre']}")
            print("="*70)
            print(f"Estado: {estado['estado'].upper()}")
            print(f"Participantes: {estado['total_participantes']}")
            print(f"Emparejamientos: {estado['emparejamientos_completados']}/{estado['emparejamientos_totales']}")
            
            if estado['ganador']:
                print(f"\n🏆 ¡GANADOR: {estado['ganador']}!")
                # Entregar recompensa
                for g in equipo.gladiadores:
                    if g.nombre == estado['ganador']:
                        recompensa = 500
                        equipo.dinero += recompensa
                        print(f"✓ Recompensa: {recompensa}g")
            else:
                # Mostrar bracket actual
                print(f"\n📊 BRACKET ACTUAL:")
                for num_ronda, ronda in enumerate(torneo.rondas, 1):
                    print(f"\n  Ronda {num_ronda}:")
                    for emp in ronda:
                        if emp.completado:
                            print(f"    ✓ {emp.participante1} vs {emp.participante2} → {emp.ganador}")
                        else:
                            print(f"    ⏳ {emp.participante1} vs {emp.participante2}")
            
            input("\nPresiona ENTER...")
        
        elif opcion == "3":
            # Completar emparejamiento
            if not hasattr(equipo, 'torneo_actual') or equipo.torneo_actual is None:
                print("\n❌ No hay torneo activo")
                input("Presiona ENTER...")
                continue
            
            torneo = equipo.torneo_actual
            emp = torneo.obtener_siguiente_emparejamiento_pendiente()
            
            if not emp:
                print("\n✓ Torneo finalizado")
                input("Presiona ENTER...")
                continue
            
            print(f"\n⚔️  {emp.participante1} vs {emp.participante2}")
            print("\n¿Quién ganó?")
            print(f"[1] {emp.participante1}")
            print(f"[2] {emp.participante2}")
            
            opcion_ganador = input("\n➤ Elige: ").strip()
            
            if opcion_ganador == "1":
                ganador = emp.participante1
            elif opcion_ganador == "2":
                ganador = emp.participante2
            else:
                print("❌ Opción inválida")
                continue
            
            torneo.completar_emparejamiento(ganador)
            print(f"\n✓ {ganador} avanza al siguiente emparejamiento")
            input("Presiona ENTER...")
        
        elif opcion == "4":
            # Ver resultado
            if not hasattr(equipo, 'torneo_actual') or equipo.torneo_actual is None:
                print("\n❌ No hay torneo activo")
                input("Presiona ENTER...")
                continue
            
            torneo = equipo.torneo_actual
            
            if torneo.ganador:
                print("\n" + "="*70)
                print("🏆 RESULTADO FINAL")
                print("="*70)
                print(f"Torneo: {torneo.nombre}")
                print(f"\n🥇 GANADOR: {torneo.ganador}")
                print(f"Recompensa: 500g")
                equipo.torneo_actual = None
            else:
                print("\n⏳ El torneo aún está en progreso")
            
            input("Presiona ENTER...")
        
        elif opcion == "5":
            break
        else:
            print("❌ Opción inválida")


# ============================================
# LIGAS AUTOMÁTICAS (FASE 4)
# ============================================

def ligas_automaticas_menu(equipo, ligas_automaticas):
    """Menú de ligas automáticas con temporadas."""
    while True:
        print("\n" + "="*70)
        print("🏅 LIGAS AUTOMÁTICAS - SISTEMA DE TEMPORADAS")
        print("="*70)
        
        ranking = ligas_automaticas.obtener_ranking_temporada()
        print(f"\n📅 Temporada Actual: {ligas_automaticas.temporada_actual}")
        print(f"📊 Gladiadores activos: {len(ranking)}")
        
        print("""
  [1] Ver ranking de temporada
  [2] Ver mis puntos
  [3] Ver recompensas por liga
  [4] Reclamar recompensas
  [5] Ver historial de temporadas
  [6] Finalizar temporada (reset)
  [7] Volver
""")
        
        opcion = input("➤ Elige: ").strip()
        
        if opcion == "1":
            # Ver ranking
            print("\n" + "="*70)
            print("📊 RANKING DE TEMPORADA")
            print("="*70)
            
            ranking = ligas_automaticas.obtener_ranking_temporada()
            if not ranking:
                print("\n⏳ Sin datos aún")
            else:
                for pos, (nombre, puntos) in enumerate(ranking[:20], 1):
                    liga = ligas_automaticas.obtener_liga_temporada(nombre)
                    liga_icon = {
                        "Bronce": "🟢",
                        "Plata": "⚪",
                        "Oro": "🟡",
                        "Leyenda": "⭐"
                    }.get(liga.value, "?")
                    
                    print(f"  {pos:2}. {liga_icon} {nombre:<20} {puntos:>4}pts")
            
            input("\nPresiona ENTER...")
        
        elif opcion == "2":
            # Ver mis puntos
            print("\nTus gladiadores en la temporada actual:\n")
            
            for g in equipo.gladiadores:
                puntos = ligas_automaticas.obtener_puntos_temporada(g.nombre)
                liga = ligas_automaticas.obtener_liga_temporada(g.nombre)
                
                liga_icon = {
                    "Bronce": "🟢",
                    "Plata": "⚪",
                    "Oro": "🟡",
                    "Leyenda": "⭐"
                }.get(liga.value, "?")
                
                print(f"  {liga_icon} {g.nombre:<20} {puntos:>4}pts ({liga.value})")
            
            input("\nPresiona ENTER...")
        
        elif opcion == "3":
            # Ver recompensas
            print("\n" + "="*70)
            print("🎁 RECOMPENSAS POR LIGA")
            print("="*70)
            print("""
  🟢 Bronce (0-99 pts):
     • 100g
  
  ⚪ Plata (100-249 pts):
     • 250g
     • Poción de Vida x2
  
  🟡 Oro (250-499 pts):
     • 500g
     • Poción de Vida x5
     • Mineral Raro x1
  
  ⭐ Leyenda (500+ pts):
     • 1000g
     • Poción de Vida x10
     • Mineral Raro x3
     • Equipo Legendario
""")
            input("Presiona ENTER...")
        
        elif opcion == "4":
            # Reclamar recompensas
            print("\nReclamando recompensas...\n")
            
            for g in equipo.gladiadores:
                puntos = ligas_automaticas.obtener_puntos_temporada(g.nombre)
                if puntos > 0:  # Solo si tiene puntos
                    recompensas = ligas_automaticas.calcular_recompensas_liga(g.nombre, None)
                    equipo.dinero += recompensas["dinero"]
                    print(f"✓ {g.nombre}: +{recompensas['dinero']}g")
            
            print(f"\n✓ Total: +{sum(ligas_automaticas.calcular_recompensas_liga(g.nombre, None)['dinero'] for g in equipo.gladiadores if ligas_automaticas.obtener_puntos_temporada(g.nombre) > 0)}g")
            input("Presiona ENTER...")
        
        elif opcion == "5":
            # Ver historial
            historial = ligas_automaticas.obtener_historial_temporadas()
            
            if not historial:
                print("\n⏳ Sin temporadas finalizadas aún")
            else:
                print("\n" + "="*70)
                print("📜 HISTORIAL DE TEMPORADAS")
                print("="*70)
                
                for num, temp in sorted(historial.items(), reverse=True)[:10]:
                    print(f"\n  Temporada {num}:")
                    if temp.ranking_final:
                        top3 = sorted(temp.ranking_final.items(), key=lambda x: x[1], reverse=True)[:3]
                        for pos, (nombre, puntos) in enumerate(top3, 1):
                            print(f"    {pos}. {nombre} - {puntos}pts")
            
            input("\nPresiona ENTER...")
        
        elif opcion == "6":
            # Finalizar temporada
            confirmacion = input("\n⚠️  ¿Finalizar temporada y resetear puntos? (s/n): ").strip().lower()
            
            if confirmacion == 's':
                temp_finalizada = ligas_automaticas.finalizar_temporada()
                print(f"\n✓ Temporada {temp_finalizada.numero} finalizada")
                print(f"✓ Nueva temporada iniciada: {ligas_automaticas.temporada_actual}")
                print("✓ Todos los puntos reseteados a 0")
            
            input("Presiona ENTER...")
        
        elif opcion == "7":
            break
        else:
            print("❌ Opción inválida")


# ============================================
# MERCADO
# ============================================

def mercado_menu(equipo):
    """Menú del mercado de gladiadores."""
    print("\n" + "="*70)
    print("🛍️  MERCADO DE GLADIADORES")
    print("="*70)
    print(f"Dinero: {equipo.dinero}g | Espacios: {equipo.espacios_disponibles}\n")
    
    while True:
        print("[1] Comprar Gladiador")
        print("[2] Vender Gladiador")
        print("[0] Salir")
        
        opcion = input("\n¿Qué haces? [0-2]: ").strip()
        
        if opcion == "0":
            break
        elif opcion == "1":
            # Mostrar mercado
            gladiadores = mostrar_mercado_gladiadores(equipo.calcular_nivel_promedio())
            opcion_gladiador = input("¿Cuál compras? [0-6]: ").strip()
            
            if opcion_gladiador != "0":
                exito, equipo.dinero, msg, _ = comprar_gladiador(gladiadores, opcion_gladiador, equipo.dinero, equipo)
                print(f"\n{msg}")
                if exito:
                    print(f"Dinero restante: {equipo.dinero}g")
        
        elif opcion == "2":
            dinero_ganado, exito = vender_gladiador(equipo)
            if exito:
                equipo.dinero += dinero_ganado
                print(f"Dinero actual: {equipo.dinero}g")
        
        else:
            print("❌ Opción inválida")


# ============================================
# BUCLE PRINCIPAL
# ============================================

def juego_principal():
    """Bucle principal del juego."""
    
    mostrar_titulo()
    
    # Autenticación
    usuario = mostrar_menu_autenticacion()
    if not usuario:
        print("\n👋 Gracias por jugar. ¡Hasta pronto!")
        return
    
    print(f"\n✓ ACCESO CONCEDIDO: {usuario}")
    
    # Cargar o crear equipo
    datos_guardados = cargar_partida(usuario)
    
    if datos_guardados:
        print("\n💾 Partida guardada encontrada")
        try:
            equipo = deserializar_equipo(datos_guardados)
            print(f"✓ Equipo restaurado: {len(equipo.gladiadores)} gladiadores")
            print(f"✓ Dinero: {equipo.dinero}💰")
            crear_nuevo = False
        except Exception as e:
            print(f"⚠️  Error al restaurar partida: {e}")
            print("   Creando nuevo equipo...")
            crear_nuevo = True
    else:
        crear_nuevo = True
    
    if crear_nuevo:
        # Crear equipo nuevo
        equipo = Equipo()
        equipo.dinero = 5000
        
        # Crear 2 gladiadores iniciales
        g1 = Gladiador("Ferox", "Murmillo", nivel=1)
        g2 = Gladiador("Velox", "Retiarius", nivel=1)
        equipo.agregar_gladiador(g1)
        equipo.agregar_gladiador(g2)
        print(f"\n✓ Nuevo equipo creado para {usuario}")
    
    # Inicializar gestor de misiones
    gestor_misiones = GestorMisiones()
    print("\n📋 Sistema de misiones activado")
    print(f"✓ {len(gestor_misiones.misiones)} misiones cargadas")
    
    # Cargar estado de misiones si existe partida anterior
    if datos_guardados and not crear_nuevo:
        if gestor_misiones.cargar_estado(f"data/misiones_{usuario}.json"):
            print("✓ Misiones restauradas desde partida anterior")
        else:
            print("⚠️  No se encontraron misiones guardadas (comenzando nuevas)")
    else:
        print("✓ Nuevas misiones iniciadas")
    
    # NUEVA: Inicializar sistema de ligas (Fase 2.4)
    from src.models import SistemaLigas, LigasAutomaticas
    sistema_ligas = SistemaLigas()
    ligas_automaticas = LigasAutomaticas()
    print("🏆 Sistema de ligas activado")
    print("🏅 Sistema de ligas automáticas activado")
    
    # NUEVA: Inicializar sistema de facilidades (Médico + Herrero)
    facilities = FacilitiesManager()
    if datos_guardados and not crear_nuevo:
        facilities = cargar_facilities(datos_guardados)
        print("⚒️  Sistema de facilidades restaurado")
    else:
        facilities = FacilitiesManager()
        print("⚒️  Sistema de facilidades inicializado")
    
    # LOOP PRINCIPAL DEL JUEGO
    juego_activo = True
    while juego_activo:
        mostrar_pantalla_equipo(equipo, usuario)
        mostrar_menu_principal()
        
        opcion = input("➤ Elige una opción: ").strip()
        
        if opcion == "1":
            # Arena - NUEVA: Menú con dificultades (Fase 2.3)
            if equipo.todos_muertos():
                print("\n💀 ¡Todos tus gladiadores están muertos! GAME OVER")
                juego_activo = False
            else:
                arena_menu(equipo, sistema_ligas)
        
        elif opcion == "2":
            # Barracas
            barracas_menu(equipo)
        
        elif opcion == "3":
            # Hospital
            hospital_menu(equipo)
        
        elif opcion == "4":
            # Mercado
            mercado_menu(equipo)
        
        elif opcion == "5":
        # Armería
            dinero_actualizado, _ = menu_armeria(equipo.dinero, [], gestor_misiones)
            equipo.dinero = dinero_actualizado
        
        elif opcion == "6":
            # Ver equipo detallado
            ver_equipo_detallado(equipo)
        
        elif opcion == "7":
            # Misiones
            mostrar_menu_misiones(gestor_misiones, equipo)
        
        elif opcion == "8":
            # Guardar
            print("\n💾 Guardando partida...")
            
            # Guardar datos del equipo
            datos_equipo = serializar_equipo(equipo)
            guardar_partida(usuario, datos_equipo)
            
            # Guardar misiones
            if gestor_misiones.guardar_estado(f"data/misiones_{usuario}.json"):
                print("✓ Misiones guardadas")
            
            # Guardar facilities
            guardar_facilities(usuario, facilities)
            print("✓ Facilities guardadas")
            print("✓ Partida completamente guardada")
        
        elif opcion == "9":
            # Salir - Guardar partida automáticamente
            print(f"\n💾 Guardando partida de {usuario}...")
            
            # Guardar estado del equipo
            datos_equipo = serializar_equipo(equipo)
            guardar_partida(usuario, datos_equipo)
            
            # Guardar misiones
            if gestor_misiones.guardar_estado(f"data/misiones_{usuario}.json"):
                print("✓ Misiones guardadas")
            
            print(f"✓ Partida completamente guardada")
            print(f"👋 Gracias por jugar, {usuario}!")
            juego_activo = False
        
        else:
            print("❌ Opción inválida")


# ============================================
# SISTEMA DE MISIONES
# ============================================

def mostrar_menu_misiones(gestor_misiones, equipo):
    """Menú principal de misiones."""
    while True:
        print("\n" + "="*70)
        print("📋 SISTEMA DE MISIONES")
        print("="*70)
        
        # Contar misiones por estado
        activas = len(gestor_misiones.obtener_misiones_activas())
        completadas = len([m for m in gestor_misiones.misiones.values() 
                          if m.estado == EstadoMision.COMPLETADA])
        reclamadas = len([m for m in gestor_misiones.misiones.values() 
                         if m.estado == EstadoMision.RECLAMADA])
        
        print(f"\n📊 Estado General:")
        print(f"   ⭐ Activas: {activas}")
        print(f"   ✓ Completadas (sin reclamar): {completadas}")
        print(f"   ✓✓ Reclamadas: {reclamadas}")
        
        print(f"\n🔹 OPCIONES:")
        print(f"   1. Ver todas las misiones")
        print(f"   2. Ver misiones activas")
        print(f"   3. Ver misiones completadas")
        print(f"   4. Ver detalles de una misión")
        print(f"   5. Reclamar recompensas")
        print(f"   0. Volver al menú principal")
        
        opcion = input("\nSelecciona opción [0-5]: ").strip()
        
        if opcion == "1":
            mostrar_todas_misiones_detalle(gestor_misiones)
        
        elif opcion == "2":
            mostrar_misiones_por_estado(gestor_misiones, "activa")
        
        elif opcion == "3":
            mostrar_misiones_por_estado(gestor_misiones, "completada")
        
        elif opcion == "4":
            ver_detalles_mision(gestor_misiones)
        
        elif opcion == "5":
            reclamar_recompensas_menu(gestor_misiones, equipo)
        
        elif opcion == "0":
            break
        
        else:
            print("❌ Opción inválida")


def mostrar_todas_misiones_detalle(gestor_misiones):
    """Muestra todas las misiones categorizadas."""
    from src.misiones import CapaMision
    
    print("\n" + "="*70)
    print("📋 TODAS LAS MISIONES")
    print("="*70)
    
    for capa in CapaMision:
        misiones = gestor_misiones.obtener_misiones_por_capa(capa)
        if misiones:
            icon = {
                "core": "🎯",
                "encadenada": "🔗",
                "secundaria": "⭐",
                "automatica": "🔄"
            }.get(capa.value, "📍")
            
            print(f"\n{icon} {capa.value.upper()} ({len(misiones)} misiones):")
            print("-" * 70)
            
            for m in misiones:
                estado_icon = {
                    "bloqueada": "🔒",
                    "activa": "⭐",
                    "completada": "✓",
                    "reclamada": "✓✓"
                }.get(m.estado.value, "?")
                
                barra = m.generar_string_progreso()
                print(f"  {estado_icon} [{m.id}] {m.nombre}")
                print(f"     {barra}")
                print(f"     💰 {m.recompensas['dinero']}g | 📈 {m.recompensas['xp']} XP")


def mostrar_misiones_por_estado(gestor_misiones, estado: str):
    """Muestra misiones filtradas por estado."""
    print("\n" + "="*70)
    print(f"📋 MISIONES {estado.upper()}")
    print("="*70)
    
    if estado == "activa":
        misiones = gestor_misiones.obtener_misiones_activas()
    elif estado == "completada":
        misiones = [m for m in gestor_misiones.misiones.values() 
                   if m.estado == EstadoMision.COMPLETADA]
    else:
        misiones = []
    
    if not misiones:
        print(f"\n❌ No hay misiones {estado}s")
        return
    
    print(f"\n✓ Total: {len(misiones)} misiones\n")
    
    for i, m in enumerate(misiones, 1):
        print(f"{i}. {m.nombre}")
        print(f"   {m.descripcion}")
        print(f"   Progreso: {m.generar_string_progreso()}")
        print(f"   Recompensas: {m.recompensas['dinero']}g + {m.recompensas['xp']} XP")
        if m.tiene_bonus:
            print(f"   ✨ BONUS: {m.descripcion_bonus} (+{m.bonus_extra_recompensa}g)")
        print()
    
    input("Presiona ENTER para continuar...")


def ver_detalles_mision(gestor_misiones):
    """Ver detalles completos de una misión específica."""
    print("\n" + "="*70)
    print("📋 DETALLES DE MISIÓN")
    print("="*70)
    
    id_mision = input("\nIngresa ID de misión (ej: combate_1, cadena_gloria_1): ").strip()
    mision = gestor_misiones.obtener_mision(id_mision)
    
    if not mision:
        print(f"❌ Misión '{id_mision}' no encontrada")
        return
    
    print("\n" + "="*70)
    print(mision.generar_string_completo())
    print("="*70)
    
    print(f"\n📊 INFORMACIÓN ADICIONAL:")
    print(f"   Tipo: {mision.tipo.value}")
    print(f"   Capa: {mision.capa.value}")
    print(f"   Dificultad: {mision.dificultad.value}")
    print(f"   Estado: {mision.estado.value}")
    
    if mision.mision_padre_id:
        padre = gestor_misiones.obtener_mision(mision.mision_padre_id)
        print(f"   Requiere: {padre.nombre if padre else 'Desconocida'}")
    
    if mision.misiones_hijo_ids:
        print(f"   Desbloquea: {len(mision.misiones_hijo_ids)} misión(es)")
    
    input("\nPresiona ENTER para volver...")


def reclamar_recompensas_menu(gestor_misiones, equipo):
    """Menú para reclamar recompensas de misiones completadas."""
    completadas = [m for m in gestor_misiones.misiones.values() 
                  if m.estado == EstadoMision.COMPLETADA]
    
    if not completadas:
        print("\n❌ No hay misiones completadas para reclamar")
        return
    
    print("\n" + "="*70)
    print("🎁 RECLAMAR RECOMPENSAS")
    print("="*70)
    print(f"\nTienes {len(completadas)} misión(es) completada(s):\n")
    
    for i, m in enumerate(completadas, 1):
        print(f"{i}. {m.nombre}")
        print(f"   💰 {m.recompensas['dinero']}g | 📈 {m.recompensas['xp']} XP")
    
    print(f"\n0. Volver")
    
    try:
        opcion = int(input("\nSelecciona misión a reclamar [0-{}]: ".format(len(completadas))).strip())
        
        if opcion == 0:
            return
        
        if 1 <= opcion <= len(completadas):
            mision = completadas[opcion - 1]
            recompensas = gestor_misiones.reclamar_recompensas_mision(mision.id)
            
            if recompensas:
                print(f"\n✅ ¡Recompensas reclamadas!")
                print(f"   💰 +{recompensas['dinero']}g")
                print(f"   📈 +{recompensas['xp']} XP")
                
                # Actualizar equipo
                equipo.dinero += recompensas['dinero']
                
                input("\nPresiona ENTER para continuar...")
    
    except ValueError:
        print("❌ Entrada inválida")




if __name__ == "__main__":
    try:
        juego_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Juego interrumpido. ¡Hasta pronto!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        raise