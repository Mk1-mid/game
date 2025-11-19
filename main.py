from combate import combate_arena, curar_en_base
from Character import Player
from armeria import menu_armeria
from enemigo import generar_enemigo, mostrar_info_enemigo
import j
import random
import pygame

pygame.mixer.init()
pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.play(-1)  # -1 = loop infinito

# ============================================
# INICIO DEL JUEGO - AUTENTICACIÓN
# ============================================
print("""
╔══════════════════════════════════════════╗
║                                          ║
║      🏛️  BIENVENIDO AL COLISEO  🏛️         ║
║                                          ║
╚══════════════════════════════════════════╝
""")

username_logueado = j.mostrar_menu_autenticacion()

if not username_logueado:
    print("\n👋 Gracias por jugar. ¡Hasta pronto!")
    exit()

# ============================================
# PANTALLA DE TÍTULO
# ============================================
print(f"\n╔════════════════════════════════════════════╗")
print(f"║   ✓ ACCESO CONCEDIDO: {username_logueado:<20} ║")
print(f"╚════════════════════════════════════════════╝\n")

print("""
╔════════════════════════════════════════╗
║          ⠀⠀⠀⠀⠀⢀⣀⢠⣴⣶⣶⣶⣆⣤⣄⣀⠀             ║
║          ⠀⠀⢀⣤⣾⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠆            ║
║          ⠀⢀⣺⣿⣿⣿⠿⣛⣭⣥⣴⣤⣬⣍⠛⠉⠀⠀            ║
║          ⢀⣿⣿⣿⡿⡡⣚⣭⣵⣶⣦⣭⣙⠃⠀⠀⠀⠀            ║
║          ⢸⣿⣿⣿⢁⣾⣿⠿⢛⣋⣉⣉⣉⣓⣠⠀⠀⠀            ║
║          ⢸⣿⣿⡏⢸⣿⢇⣾⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀            ║
║          ⢸⣿⡿⠁⣸⣿⡸⣿⣿⣿⡉⠀⠉⢻⣿⠀⠀⠀            ║
║          ⠚⠋⠀⠀⣿⣿⣿⣮⢻⣿⣿⣷⣆⠀⣿⠀⠀⠀            ║
║          ⠀⠀⠀⢀⣿⣿⣿⣿⡇⢿⣿⣿⣿⡄⠉⠀⠀⠀            ║
║          ⠀⠀⠀⠉⠛⠛⠛⠋⠁⢸⣿⣿⣿⣿⣄⠀⠀⠀            ║
║          ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠿⠿⠿⠛⠁⠀⠀            ║
║        ⚔️  SANGRE POR FORTUNA  ⚔️        ║
╚════════════════════════════════════════╝
""")

print("        ┌─────────────────────┐")
print("        │  1. ⚔️  START GAME   │")
print("        │  2. 🚪 SALIR        │")
print("        └─────────────────────┘")

opcion_start = input("\n        ➤ Elige una opción: ").strip()

if opcion_start != "1":
    print("\n        Decides no jugar hoy. ¡Hasta pronto!")
    exit()

print("\n        ⚔️  ¡Que comience la batalla! ⚔️\n")

# ============================================
# CARGAR O CREAR PARTIDA
# ============================================
datos_guardados = j.cargar_partida(username_logueado)

if datos_guardados:
    print("\n┌────────────────────────────────────────┐")
    print("│  💾 Partida guardada encontrada       │")
    print("└────────────────────────────────────────┘")
    continuar = input("\n¿Deseas continuar? (s/n): ").strip().lower()
    if continuar == "s":
        partida = datos_guardados
        print("✓ Partida cargada exitosamente!")
    else:
        partida = j.crear_nueva_partida()
        print("✓ Nueva partida iniciada!")
else:
    partida = j.crear_nueva_partida()
    print("\n✓ Nueva partida creada!")

# ============================================
# VARIABLES DEL JUEGO
# ============================================
dinero = partida["dinero"]
salud_jugador = partida["salud_jugador"]
vida_maxima = partida["vida_maxima"]
victorias = partida["victorias"]
derrotas = partida["derrotas"]

# ============================================
# CREACIÓN DEL GLADIADOR
# ============================================
mi_gladiador = Player()
print(f"\n⚔️  Gladiador '{username_logueado}' preparado para el combate!")

# ============================================
# CONSTANTES DEL JUEGO
# ============================================
valor_entrada = 50
cantidad_cura = 40
costo_curacion = 20
daño_base = 15

# ============================================
# BUCLE PRINCIPAL DEL JUEGO
# ============================================
juego_activo = True

while juego_activo:
    print("\n" + "="*50)
    print("           🏛️  COLISEO ROMANO  🏛️")
    print("="*50)
    print(f"  👤 Gladiador: {username_logueado}")
    print(f"  💰 Dinero: {dinero}g  |  ❤️  Salud: {salud_jugador}/{vida_maxima}")
    print(f"  🏆 Victorias: {victorias}  |  💀 Derrotas: {derrotas}")
    print("="*50)
    print("  1. 🏟️  Ir a la arena")
    print("  2. ⚕️  Ir a la base (curarte)")
    print("  3. 🗡️  Ir a la armería")
    print("  4. 📊 Ver stats del gladiador")
    print("  5. 💾 Guardar partida")
    print("  6. 🚪 Salir del juego")
    print("="*50)

    opcion = input("  ➤ Elige una opción: ").strip()
    
    # ========================================
    # OPCIÓN 1: ARENA
    # ========================================
    if opcion == "1":
        if dinero < valor_entrada:
            print("\n  ⚠️  ━━━ NO TIENES SUFICIENTE DINERO ━━━")
            print(f"      Necesitas {valor_entrada}g, tienes {dinero}g")
            continue
        
        if salud_jugador < vida_maxima * 0.5:
            print("\n  ⚠️  ━━━ GLADIADOR MUY HERIDO ━━━")
            print("      Ve a la base a curarte primero")
            continue
        
        dinero -= valor_entrada
        print(f"\n  💸 Pagaste {valor_entrada}g | Restante: {dinero}g")
        
        print("\n" + "="*50)
        print("      🎭 UN GLADIADOR ENTRA A LA ARENA...")
        print("="*50)
        
        enemigo, es_campeon = generar_enemigo(victorias)
        mostrar_info_enemigo(enemigo, es_campeon)
        
        # Obtener stats finales (con equipamiento y DEFENSA)
        daño_jugador = mi_gladiador.ataque_final()
        velocidad_jugador = mi_gladiador.velocidad_final()
        defensa_jugador = mi_gladiador.defensa_final()
        
        salud_enemigo = enemigo.hp_final()
        daño_enemigo = enemigo.ataque_final()
        velocidad_enemigo = enemigo.velocidad_final()
        defensa_enemigo = enemigo.defensa_final()
        
        # Combate (ahora con defensas)
        salud_jugador, gano = combate_arena(
            salud_jugador, daño_jugador, velocidad_jugador, defensa_jugador,
            salud_enemigo, daño_enemigo, velocidad_enemigo, defensa_enemigo,
            daño_base
        )
        
        # Resultado
        if gano:
            victorias += 1
            if es_campeon:
                recompensa = 500
                print("\n" + "  🎉"*15)
                print("      ¡¡¡DERROTASTE AL CAMPEÓN!!!")
                print("  " + "🎉"*15)
            elif victorias >= 5:
                recompensa = 150
            else:
                recompensa = 100
            
            dinero += recompensa
            print(f"\n  💰 ¡Ganaste {recompensa}g! | Total: {dinero}g")
        else:
            derrotas += 1
            print("\n  💔 Derrota. No ganaste recompensa.")
        
        # Game over
        if dinero < valor_entrada and salud_jugador < vida_maxima * 0.5:
            print("\n" + "="*50)
            print("              ⚰️  GAME OVER  ⚰️")
            print("="*50)
            print(f"      🏆 Victorias: {victorias}")
            print(f"      💀 Derrotas: {derrotas}")
            print(f"\n      Tu legado terminó, {username_logueado}")
            print("="*50)
            juego_activo = False

    # ========================================
    # OPCIÓN 2: BASE (CURARSE)
    # ========================================
    elif opcion == "2":
        print("\n  ╔══════════════════════════════════╗")
        print("  ║      ⚕️  BASE MÉDICA  ⚕️          ║")
        print("  ╚══════════════════════════════════╝")
        print(f"    ❤️  Salud actual: {salud_jugador}/{vida_maxima}")
        print(f"    💰 Costo: {costo_curacion}g")
        print(f"    ➕ Recuperación: +{cantidad_cura} HP")
        
        if salud_jugador >= vida_maxima:
            print("\n    ✓ Ya tienes la salud al máximo!")
        elif dinero < costo_curacion:
            print(f"\n    ⚠️  No tienes suficiente dinero ({costo_curacion}g)")
        else:
            confirmar = input("\n  ¿Deseas curarte? (s/n): ").strip().lower()
            if confirmar == "s":
                dinero -= costo_curacion
                salud_jugador = curar_en_base(salud_jugador, vida_maxima, cantidad_cura)
                print(f"    💸 Pagaste {costo_curacion}g | Restante: {dinero}g")
            else:
                print("    Curación cancelada.")

    # ========================================
    # OPCIÓN 3: ARMERÍA
    # ========================================
    elif opcion == "3":
        inventario_actual = partida.get("inventario_armas", [])
        dinero, inventario_actualizado = menu_armeria(dinero, inventario_actual, mi_gladiador)
        partida["inventario_armas"] = inventario_actualizado
        partida["dinero"] = dinero

    # ========================================
    # OPCIÓN 4: VER STATS
    # ========================================
    elif opcion == "4":
        print("\n  ╔══════════════════════════════════════╗")
        print("  ║     📊 STATS DEL GLADIADOR 📊        ║")
        print("  ╚══════════════════════════════════════╝")
        print(f"    👤 Nombre: {username_logueado}")
        
        print("\n    ┌─── 📈 Stats Base ───┐")
        print(f"    │ ❤️  HP:       {mi_gladiador.hp:>3}    │")
        print(f"    │ ⚔️  Ataque:   {mi_gladiador.attack:>3}    │")
        print(f"    │ 🛡️  Defensa:  {mi_gladiador.deffense:>3}    │")
        print(f"    │ ⚡ Velocidad: {mi_gladiador.speed:>3}   │")
        print("    └─────────────────────┘")
        
        print("\n    ┌─── 💪 Stats Finales (con equipo) ───┐")
        print(f"    │ ❤️  HP Total:       {mi_gladiador.hp_final():>3}              │")
        print(f"    │ ⚔️  Ataque Total:   {mi_gladiador.ataque_final():>3}              │")
        print(f"    │ 🛡️  Defensa Total:  {mi_gladiador.defensa_final():>3}              │")
        print(f"    │ ⚡ Velocidad Total: {mi_gladiador.velocidad_final():>3}             │")
        print("    └─────────────────────────────────────┘")
        
        print("\n    ┌───── 🎒 Equipo Equipado ─────┐")
        if mi_gladiador.weapon:
            print(f"     ⚔️  {mi_gladiador.weapon.nombre:<28} ")
            print(f"        └─ ATK: +{mi_gladiador.weapon.attack}  VEL: +{mi_gladiador.weapon.speed}                │")
        else:
            print("     ⚔️  Arma: Ninguna                        ")
        
        if mi_gladiador.armor:
            print(f"     🛡️  {mi_gladiador.armor.nombre:<28} ")
            print(f"        └─ DEF: +{mi_gladiador.armor.deffense}  HP: +{mi_gladiador.armor.hp}                │")
        else:
            print("     🛡️  Armadura: Ninguna                    ")
        print("    └──────────────────────────────┘")
        
        print("\n    ┌─── 🏆 Récord ───┐")
        print(f"    │ ✅ Victorias: {victorias:<2}│")
        print(f"    │ ❌ Derrotas:  {derrotas:<2}│")
        if victorias + derrotas > 0:
            winrate = (victorias / (victorias + derrotas)) * 100
            print(f"    │ 📈 Winrate: {winrate:>5.1f}% │")
        print("    └─────────────────┘")

    # ========================================
    # OPCIÓN 5: GUARDAR PARTIDA
    # ========================================
    elif opcion == "5":
        partida_actual = {
            "dinero": dinero,
            "salud_jugador": salud_jugador,
            "vida_maxima": vida_maxima,
            "victorias": victorias,
            "derrotas": derrotas,
            "inventario_armas": partida.get("inventario_armas", []),
            "arma_equipada": None,
            "armadura_equipada": None
        }
        j.guardar_partida(username_logueado, partida_actual)

    # ========================================
    # OPCIÓN 6: SALIR
    # ========================================
    elif opcion == "6":
        print("\n  ┌────────────────────────────────┐")
        print("  │  ¿Deseas guardar antes de      │")
        print("  │  salir? (s/n)                  │")
        print("  └────────────────────────────────┘")
        guardar = input("  ➤ ").strip().lower()
        if guardar == "s":
            partida_actual = {
                "dinero": dinero,
                "salud_jugador": salud_jugador,
                "vida_maxima": vida_maxima,
                "victorias": victorias,
                "derrotas": derrotas,
                "inventario_armas": partida.get("inventario_armas", []),
                "arma_equipada": None,
                "armadura_equipada": None
            }
            j.guardar_partida(username_logueado, partida_actual)
        
        print(f"\n      👋 Gracias por jugar, {username_logueado}")
        print("      ⚔️  Que los dioses te favorezcan  ⚔️")
        juego_activo = False

    else:
        print("\n  ❌ Opción inválida. Intenta de nuevo.")

# ============================================
# FIN DEL JUEGO
# ============================================
print("\n╔══════════════════════════════════════╗")
print("║         🏁 FIN DEL JUEGO 🏁          ║")
print("╚══════════════════════════════════════╝\n")