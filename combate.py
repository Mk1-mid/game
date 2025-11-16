import random

# --- FUNCIONES ---
def combate_arena(salud_jugador, daño_jugador, velocidad_jugador, salud_enemigo, daño_enemigo, velocidad_enemigo, daño_base):
    
    salud_simulada_jugador = salud_jugador
    salud_simulada_enemigo = salud_enemigo
    victoria = None
    print("     COMBATE INICIADO")
    print(f"Tu gladiador: {salud_simulada_jugador} HP")
    print(f"Enemigo:      {salud_simulada_enemigo} HP")
    input("\nPresiona ENTER para comenzar el combate")

    jugador_primero = velocidad_jugador >= velocidad_enemigo
    
    turno = 1
    while victoria is None:
        print(f"\n Turno {turno} ")
        
        if jugador_primero:
            # Jugador ataca
            daño_infligido = calcular_daño(daño_jugador)
            salud_simulada_enemigo -= daño_infligido
            print(f"  Tu gladiador ataca con {daño_infligido} de daño")
            print(f"   Salud enemiga: {salud_simulada_enemigo} HP")
            
            if salud_simulada_enemigo <= 0:
                print("   Enemigo derrotado ")
                victoria = True
                break

            input("   Presiona ENTER para continuar")

            # Enemigo ataca
            daño_recibido = calcular_daño(daño_enemigo)
            salud_simulada_jugador -= daño_recibido
            print(f"  El enemigo ataca con {daño_recibido} de daño")
            print(f"   Tu salud: {salud_simulada_jugador} HP")
            
            if salud_simulada_jugador <= 0:
                print("   Has sido derrotado")
                victoria = False
                break
        else:
            # Enemigo ataca
            daño_recibido = calcular_daño(daño_enemigo)
            salud_simulada_jugador -= daño_recibido
            print(f"  El enemigo ataca con {daño_recibido} de daño")
            print(f"   Tu salud: {salud_simulada_jugador} HP")
            
            if salud_simulada_jugador <= 0:
                print("   Has sido derrotado")
                victoria = False
                break

            input("   Presiona ENTER para continuar")

            # Jugador ataca
            daño_infligido = calcular_daño(daño_jugador)
            salud_simulada_enemigo -= daño_infligido
            print(f"⚔️  Tu gladiador ataca con {daño_infligido} de daño")
            print(f"   Salud enemiga: {salud_simulada_enemigo} HP")
            
            if salud_simulada_enemigo <= 0:
                print("   Enemigo derrotado")
                victoria = True
                break
        
        turno += 1
        input("   [Presiona ENTER para el siguiente turno...]")
    
    # Aplicar daño real
    
    if victoria:
        daño_real = daño_base
        salud_jugador -= daño_real
        print(" VICTORIA")
        print(f"Tu gladiador recibió {daño_real} de daño por el esfuerzo del combate.")
    else:
        daño_real = daño_base * 2
        salud_jugador -= daño_real
        print(" DERROTA")
        print(f"Tu gladiador recibió {daño_real} de daño por las heridas graves.")
    
    if salud_jugador < 1:
        salud_jugador = 1
    
    print(f"Salud actual: {salud_jugador} HP")

    
    input("Presiona ENTER para continuar")
    
    return salud_jugador, victoria


def calcular_daño(daño_base):
    """Calcula daño con variación random ±20%"""
    variacion = int(daño_base * 0.2)  # 20% de variación
    daño_min = daño_base - variacion
    daño_max = daño_base + variacion
    return random.randint(daño_min, daño_max)


def curar_en_base(salud_jugador, vida_maxima, cantidad_cura):
    salud_jugador += cantidad_cura
    if salud_jugador > vida_maxima:
        salud_jugador = vida_maxima
    print(f"  Te has curado {cantidad_cura} puntos. Salud actual: {salud_jugador}/{vida_maxima}")
    return salud_jugador