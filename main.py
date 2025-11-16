from combate import combate_arena, curar_en_base
from Character import Player, Enemy_1, Enemy_Champ
from armeria import menu_armeria
import j  # Módulo de autenticación de tu compañero
import random

# INICIO DEL JUEGO - AUTENTICACIÓN
print("   BIENVENIDO A Titulo del juego")

# Usamos la función de tu compañero
username_logueado = j.mostrar_menu_autenticacion()

if not username_logueado:
    print("\nGracias por jugar")
    exit()

# PANTALLA DE TÍTULO
print(f"\n--- ACCESO CONCEDIDO, {username_logueado} ---")

print(  " Titulo del juego".center(36) )

print("  [ 1. START GAME ]")
print("  [ 2. SALIR     ]")

opcion_start = input("Pulsa 1 para empezar: ").strip()

if opcion_start != "1":
    print("Decides no jugar hoy. Saliendo...")
    exit()

print("\n¡Comienza el juego!")

# CARGAR O CREAR PARTIDA
datos_guardados = j.cargar_partida(username_logueado)

if datos_guardados:
    print("\n¿Deseas continuar tu partida guardada? (s/n)")
    continuar = input("> ").strip().lower()
    if continuar == "s":
        partida = datos_guardados
        print("Partida cargada!")
    else:
        partida = j.crear_nueva_partida()
        print("Nueva partida iniciada!")
else:
    partida = j.crear_nueva_partida()
    print("\n Nueva partida creada!")

# VARIABLES DEL JUEGO (desde partida guardada)
dinero = partida["dinero"]
salud_jugador = partida["salud_jugador"]
vida_maxima = partida["vida_maxima"]
victorias = partida["victorias"]
derrotas = partida["derrotas"]

# CREACIÓN DEL GLADIADOR
mi_gladiador = Player()
print(f"\n¡Gladiador '{username_logueado}' listo para el combate!")

# Restaurar equipo guardado si existe
# if partida["arma_equipada"]:
#     mi_gladiador.weapon = partida["arma_equipada"]
# if partida["armadura_equipada"]:
#     mi_gladiador.armor = partida["armadura_equipada"]

# CONSTANTES DEL JUEGO
valor_entrada = 50
cantidad_cura = 40
costo_curacion = 20
daño_base = 15

# BUCLE PRINCIPAL DEL JUEGO
juego_activo = True

while juego_activo:
    print("           COLISEO ROMANO")
    print(f"Jugador: {username_logueado}")
    print(f"Dinero: {dinero} |   Salud: {salud_jugador}/{vida_maxima}")
    print(f"Victorias: {victorias} |  Derrotas: {derrotas}") 
    print("1. Ir a la arena")
    print("2. Ir a la base (curarte)")
    print("3. Ir a la armería")
    print("4. Ver stats del gladiador")
    print("5. Guardar partida")
    print("6.  Salir del juego")

    opcion = input("Elige una opción: ").strip()
    # OPCIÓN 1: ARENA
    if opcion == "1":
        if dinero < valor_entrada:
            print("\n No tienes suficiente dinero para entrar a la arena!")
            print(f"   Necesitas {valor_entrada} monedas, tienes {dinero}.")
            continue
        
        if salud_jugador < vida_maxima * 0.5:
            print("\n Tu gladiador está muy herido (menos del 50% de vida)")
            print("   Ve a la base a curarte primero.")
            continue
        
        dinero -= valor_entrada
        print(f"\nPagaste {valor_entrada} monedas. Dinero restante: {dinero}")
        
        # Generar enemigo (75% normal, 25% campeón)
        tipo_enemigo = random.choice([Enemy_1, Enemy_1, Enemy_1, Enemy_Champ])
        enemigo = tipo_enemigo()
        
        print("\nTu oponente entra a la arena...")
        if isinstance(enemigo, Enemy_Champ):
            print(" ES EL CAMPEÓN ")
        # Obtener stats finales (con equipamiento)
        daño_jugador = mi_gladiador.ataque_final()
        velocidad_jugador = mi_gladiador.velocidad_final()
        salud_enemigo = enemigo.hp_final()
        daño_enemigo = enemigo.ataque_final()
        velocidad_enemigo = enemigo.velocidad_final()
        
        # Combate
        salud_jugador, gano = combate_arena(
            salud_jugador, daño_jugador, velocidad_jugador,
            salud_enemigo, daño_enemigo, velocidad_enemigo, 
            daño_base
        )
        # Actualizar estadísticas
        if gano:
            victorias += 1
            if isinstance(enemigo, Enemy_Champ):
                recompensa = 300
                print("🎉 ¡Derrotaste a un CAMPEÓN!")
            else:
                recompensa = 100
            dinero += recompensa
            print(f"Ganaste {recompensa} monedas! Total: {dinero}")
        else:
            derrotas += 1
            print("No ganaste recompensa por perder.")
        
        # Verificar game over
        if dinero < valor_entrada and salud_jugador < vida_maxima * 0.5:
            print("                GAME OVER ")
            print(f"Victorias: {victorias} | Derrotas: {derrotas}")
            print(f"Tu legado terminó en el coliseo, {username_logueado}.")
            juego_activo = False

    # OPCIÓN 2: BASE (CURARSE)
    elif opcion == "2":
        print("\n Casa ")
        print(f"Salud actual: {salud_jugador}/{vida_maxima}")
        print(f"Costo de curación: {costo_curacion} monedas")
        print(f"Recuperación: {cantidad_cura} HP")
        
        if salud_jugador >= vida_maxima:
            print("\n✓ Ya tienes la salud al máximo!")
        elif dinero < costo_curacion:
            print(f"\nNo tienes suficiente dinero. Necesitas {costo_curacion} monedas.")
        else:
            confirmar = input("\n¿Deseas curarte? (s/n): ").strip().lower()
            if confirmar == "s":
                dinero -= costo_curacion
                salud_jugador = curar_en_base(salud_jugador, vida_maxima, cantidad_cura)
                print(f"Pagaste {costo_curacion} monedas. Dinero restante: {dinero}")
            else:
                print("Curación cancelada.")

    # OPCIÓN 3: ARMERÍA
    elif opcion == "3":
        # Obtener inventario actual de la partida
        inventario_actual = partida.get("inventario_armas", [])
        # Llamar al menú de armería (retorna dinero e inventario actualizados)
        dinero, inventario_actualizado = menu_armeria(dinero, inventario_actual, mi_gladiador)
        # Guardar el inventario actualizado en la partida
        partida["inventario_armas"] = inventario_actualizado
        partida["dinero"] = dinero  # También actualizar el dinero en la partida

# OPCIÓN 4: VER STATS
    elif opcion == "4":
        print("\n STATS DEL GLADIADOR ")
        print(f"Nombre: {username_logueado}")
        print("\n Stats Base ")
        print(f"HP Base: {mi_gladiador.hp}")
        print(f"Ataque Base: {mi_gladiador.attack}")
        print(f"Defensa Base: {mi_gladiador.deffense}")
        print(f"Velocidad Base: {mi_gladiador.speed}")
        
        print("\n Stats Finales (con equipo) ")
        print(f"HP Total: {mi_gladiador.hp_final()}")
        print(f"Ataque Total: {mi_gladiador.ataque_final()}")
        print(f"Defensa Total: {mi_gladiador.defensa_final()}")
        print(f"Velocidad Total: {mi_gladiador.velocidad_final()}")
        
        print("\n Récord")
        print(f"Victorias: {victorias}")
        print(f"Derrotas: {derrotas}")
        if victorias + derrotas > 0:
            winrate = (victorias / (victorias + derrotas)) * 100
            print(f"📈 Winrate: {winrate:.1f}%")

    # OPCIÓN 5: GUARDAR PARTIDA
    elif opcion == "5":
        partida_actual = {
            "dinero": dinero,
            "salud_jugador": salud_jugador,
            "vida_maxima": vida_maxima,
            "victorias": victorias,
            "derrotas": derrotas,
            "inventario_armas": [],  # Actualizar cuando tengan armería
            "arma_equipada": None,
            "armadura_equipada": None
        }
        j.guardar_partida(username_logueado, partida_actual)

    # OPCIÓN 6: SALIR
    elif opcion == "6":
        print("\n¿Deseas guardar antes de salir? (s/n)")
        guardar = input("> ").strip().lower()
        if guardar == "s":
            partida_actual = {
                "dinero": dinero,
                "salud_jugador": salud_jugador,
                "vida_maxima": vida_maxima,
                "victorias": victorias,
                "derrotas": derrotas,
                "inventario_armas": [],
                "arma_equipada": None,
                "armadura_equipada": None
            }
            j.guardar_partida(username_logueado, partida_actual)
        
        print(f"\n Gracias por jugar, {username_logueado}")
        juego_activo = False

    else:
        print("\n Opción inválida. Intenta de nuevo.")

print("\n Fin del juego.")