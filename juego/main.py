from combate import combate_arena, curar_en_base

# ============================================
# AQUÍ SE IMPORTARÁN LOS MÓDULOS DE TU COMPAÑERO
# ============================================
# from gladiadores import crear_gladiador, obtener_stats_gladiador
# from enemigos import generar_enemigo_aleatorio
# from armeria import inventario_armas, equipar_arma, comprar_arma

# ============================================
# VARIABLES INICIALES DEL JUGADOR
# ============================================
dinero = 1000
valor_entrada = 50

# ============================================
# AQUÍ SE CREARÁ EL GLADIADOR DEL JUGADOR (objeto)
# ============================================
# mi_gladiador = crear_gladiador("Maximus", escuela="Murmillo")
# Por ahora usamos valores temporales:
vida_maxima = 100
salud_jugador = vida_maxima
daño_jugador = 20
velocidad_jugador = 10
daño_base = 15  # Daño real que se aplica al final del combate

# ============================================
# AQUÍ SE CARGARÁ EL INVENTARIO DE ARMAS (diccionario)
# ============================================
# inventario_jugador = []  # Lista de armas equipadas/compradas
# Por ahora no hay armas equipadas

# ============================================
# CONFIGURACIÓN DE CURACIÓN
# ============================================
cantidad_cura = 40
costo_curacion = 20

# ============================================
# BUCLE PRINCIPAL DEL JUEGO
# ============================================
juego_activo = True

while juego_activo:
    print("\n" + "="*50)
    print("           🏛️  COLISEO ROMANO 🏛️")
    print("="*50)
    print(f"💰 Dinero: {dinero} | ❤️  Salud: {salud_jugador}/{vida_maxima}")
    print("="*50)
    print("1. 🏟️  Ir a la arena")
    print("2. ⚕️  Ir a la base (curarte)")
    print("3. 🗡️  Ir a la armería")
    print("4. 🚪 Salir del juego")
    print("="*50)

    opcion = input("Elige una opción: ").strip()

    # ========================================
    # OPCIÓN 1: ARENA
    # ========================================
    if opcion == "1":
        # Verificar si tiene dinero
        if dinero < valor_entrada:
            print("\n  No tienes suficiente dinero para entrar a la arena!")
            print(f"   Necesitas {valor_entrada} monedas, tienes {dinero}.")
            continue
        
        # Verificar si tiene suficiente salud
        if salud_jugador < vida_maxima * 0.5:
            print("\n  Tu gladiador está muy herido (menos del 50% de vida)")
            print("   Ve a la base a curarte primero.")
            continue
        
        # Cobrar entrada
        dinero -= valor_entrada
        print(f"\n💸 Pagaste {valor_entrada} monedas. Dinero restante: {dinero}")
        
        # ========================================
        # AQUÍ SE GENERARÁ EL ENEMIGO (objeto)
        # ========================================
        # enemigo = generar_enemigo_aleatorio(nivel_dificultad)
        # salud_enemigo = enemigo.salud
        # daño_enemigo = enemigo.daño
        # velocidad_enemigo = enemigo.velocidad
        # Por ahora valores temporales:
        salud_enemigo = 80
        daño_enemigo = 18
        velocidad_enemigo = 8
        
        print("\n🎭 Tu oponente entra a la arena...")
        # print(f"   Nombre: {enemigo.nombre}")
        # print(f"   Escuela: {enemigo.escuela}")
        
        # ========================================
        # AQUÍ SE OBTENDRÁN LAS STATS DEL GLADIADOR
        # (incluyendo bonos de armas equipadas)
        # ========================================
        # daño_jugador = mi_gladiador.daño + bonus_arma_daño
        # velocidad_jugador = mi_gladiador.velocidad + bonus_arma_velocidad
        
        # Combate
        salud_jugador, gano = combate_arena(
            salud_jugador, daño_jugador, velocidad_jugador,
            salud_enemigo, daño_enemigo, velocidad_enemigo, 
            daño_base
        )
        
        # Recompensa si gana
        if gano:
            recompensa = 100
            dinero += recompensa
            print(f"💰 ¡Ganaste {recompensa} monedas! Total: {dinero}")
        else:
            print("💔 No ganaste recompensa por perder.")
        
        # Verificar game over
        if dinero < valor_entrada and salud_jugador < vida_maxima * 0.5:
            print("\n" + "="*50)
            print("              ⚰️  GAME OVER ⚰️")
            print("="*50)
            print("Sin dinero ni salud suficiente para continuar.")
            print(f"Combates ganados: ???")  # Agregar contador después
            juego_activo = False

    # ========================================
    # OPCIÓN 2: BASE (CURARSE)
    # ========================================
    elif opcion == "2":
        print("\n⚕️  --- BASE MÉDICA ---")
        print(f"Salud actual: {salud_jugador}/{vida_maxima}")
        print(f"Costo de curación: {costo_curacion} monedas")
        print(f"Recuperación: {cantidad_cura} HP")
        
        if salud_jugador >= vida_maxima:
            print("\n✓ Ya tienes la salud al máximo!")
        elif dinero < costo_curacion:
            print(f"\n⚠️  No tienes suficiente dinero. Necesitas {costo_curacion} monedas.")
        else:
            confirmar = input("\n¿Deseas curarte? (s/n): ").strip().lower()
            if confirmar == "s":
                dinero -= costo_curacion
                salud_jugador = curar_en_base(salud_jugador, vida_maxima, cantidad_cura)
                print(f"💸 Pagaste {costo_curacion} monedas. Dinero restante: {dinero}")
            else:
                print("Curación cancelada.")

    # ========================================
    # OPCIÓN 3: ARMERÍA
    # ========================================
    elif opcion == "3":
        print("\n🗡️  --- ARMERÍA ---")
        print("Bienvenido a la armería del coliseo.")
        
        # ========================================
        # AQUÍ SE MOSTRARÁ EL INVENTARIO DE ARMAS
        # ========================================
        # print("\n📦 Armas disponibles para comprar:")
        # for arma, datos in inventario_armas.items():
        #     print(f"  - {arma}: +{datos['daño']} daño, +{datos['velocidad']} vel | Precio: {datos['precio']}")
        
        # print("\n⚔️  Tus armas equipadas:")
        # if not inventario_jugador:
        #     print("  (Ninguna)")
        # else:
        #     for arma in inventario_jugador:
        #         print(f"  - {arma}")
        
        print("\n[Por implementar]")
        print("1. Comprar arma")
        print("2. Equipar arma")
        print("3. Volver al menú")
        
        # sub_opcion = input("\nElige una opción: ").strip()
        # if sub_opcion == "1":
        #     # Lógica de compra
        #     pass
        # elif sub_opcion == "2":
        #     # Lógica de equipar
        #     pass

    # ========================================
    # OPCIÓN 4: SALIR
    # ========================================
    elif opcion == "4":
        print("\n👋 Gracias por jugar. ¡Hasta pronto, gladiador!")
        juego_activo = False

    # ========================================
    # OPCIÓN INVÁLIDA
    # ========================================
    else:
        print("\n❌ Opción inválida. Intenta de nuevo.")

print("\n🏁 Fin del juego.")