"""
Sistema de tienda/armería y mercado de gladiadores
===================================================
"""

import random
from .models import Weapon, Armor, Potion, Gladiador


# ============================================
# CATÁLOGOS
# ============================================

CATALOGO_ARMAS = {
    # TIER 1 (50-100g) - Básicas - STR: 10
    "1": Weapon("Daga Oxidada", attack=3, agilidad=1, peso=0.5, critico_bonus=2, tier=1, str_requirement=10),
    "2": Weapon("Lanza Corta", attack=6, agilidad=0, peso=1.5, critico_bonus=0, tier=1, str_requirement=10),
    
    # TIER 2 (150-300g) - Intermedias - STR: 15
    "3": Weapon("Espada Corta", attack=10, agilidad=1, peso=1.2, critico_bonus=3, tier=2, str_requirement=15),
    "4": Weapon("Tridente Romano", attack=8, agilidad=2, peso=1.0, critico_bonus=2, tier=2, str_requirement=15),
    "5": Weapon("Martillo de Guerra", attack=12, agilidad=-1, peso=3.0, critico_bonus=1, tier=2, str_requirement=15),
    
    # TIER 3 (400-600g) - Avanzadas - STR: 20
    "6": Weapon("Espada Gladius", attack=15, agilidad=0, peso=2.0, critico_bonus=5, tier=3, str_requirement=20),
    "7": Weapon("Gladius Imperial", attack=18, agilidad=1, peso=2.2, critico_bonus=6, tier=3, str_requirement=20),
    "8": Weapon("Hacha Doble", attack=16, agilidad=-1, peso=3.5, critico_bonus=3, tier=3, str_requirement=20),
    
    # TIER 4 (800-1500g) - Legendarias - STR: 25
    "9": Weapon("Espada Ridius", attack=20, agilidad=0, peso=2.5, critico_bonus=7, tier=4, str_requirement=25),
    "10": Weapon("Espada de Marte", attack=25, agilidad=2, peso=2.8, critico_bonus=10, tier=4, str_requirement=25),
    "11": Weapon("Tridente Neptuno", attack=22, agilidad=1, peso=2.2, critico_bonus=8, tier=4, str_requirement=25),
    "12": Weapon("Lanza del Destino", attack=24, agilidad=0, peso=2.0, critico_bonus=6, tier=4, str_requirement=25),
    "13": Weapon("Hacha de Pompeya", attack=20, agilidad=3, peso=2.0, critico_bonus=9, tier=4, str_requirement=25),
}

CATALOGO_ARMADURAS = {
    # TIER 1 (50-100g) - Básicas
    "14": Armor("Ropa Harapienta", defense=2, hp=10, peso=0.5),
    "15": Armor("Cuero Endurecido", defense=5, hp=15, peso=1.5),
    
    # TIER 2 (150-300g) - Intermedias
    "16": Armor("Cota Malla", defense=10, hp=20, peso=4.0),
    "17": Armor("Armadura Bronce", defense=12, hp=25, peso=5.0),
    "18": Armor("Peto Hierro", defense=14, hp=20, peso=4.5),
    
    # TIER 3 (400-600g) - Avanzadas
    "19": Armor("Escudo Imperial", defense=10, hp=0, peso=2.0),
    "20": Armor("Armadura Centurión", defense=18, hp=30, peso=6.5),
    "21": Armor("Coraza Reforzada", defense=20, hp=35, peso=7.0),
    
    # TIER 4 (800-1500g) - Legendarias
    "22": Armor("Armadura Espartana", defense=20, hp=0, peso=5.5),
    "23": Armor("Armadura Acorazada", defense=25, hp=0, peso=8.0),
    "24": Armor("Armadura Júpiter", defense=28, hp=40, peso=8.5),
    "25": Armor("Peto Divino", defense=30, hp=50, peso=9.0),
    "26": Armor("Armadura Inmortal", defense=32, hp=60, peso=9.5),
}

CATALOGO_POCIONES = {
    "27": Potion("Curación Menor", "heal", 50),
    "28": Potion("Curación Mayor", "heal", 100),
    "29": Potion("Fuerza Temporal", "attack", 10),
    "30": Potion("Defensa Temporal", "defense", 5),
    "31": Potion("Velocidad Temporal", "speed", 5),
}

PRECIOS = {
    # ARMAS
    "1": 50,    # Daga Oxidada
    "2": 75,    # Lanza Corta
    "3": 150,   # Espada Corta
    "4": 180,   # Tridente Romano
    "5": 200,   # Martillo de Guerra
    "6": 350,   # Espada Gladius
    "7": 450,   # Gladius Imperial
    "8": 420,   # Hacha Doble
    "9": 300,   # Espada Ridius (original, reubicada)
    "10": 900,  # Espada de Marte
    "11": 850,  # Tridente Neptuno
    "12": 800,  # Lanza del Destino
    "13": 150,  # Hacha de Pompeya
    
    # ARMADURAS
    "14": 50,   # Ropa Harapienta
    "15": 80,   # Cuero Endurecido
    "16": 150,  # Cota Malla
    "17": 200,  # Armadura Bronce
    "18": 220,  # Peto Hierro
    "19": 200,  # Escudo Imperial
    "20": 400,  # Armadura Centurión
    "21": 500,  # Coraza Reforzada
    "22": 300,  # Armadura Espartana
    "23": 350,  # Armadura Acorazada
    "24": 900,  # Armadura Júpiter
    "25": 1000, # Peto Divino
    "26": 1200, # Armadura Inmortal
    
    # POCIONES
    "27": 30,   # Curación Menor
    "28": 60,   # Curación Mayor
    "29": 50,   # Fuerza Temporal
    "30": 50,   # Defensa Temporal
    "31": 50,   # Velocidad Temporal
}


# ============================================
# FUNCIONES DE TIENDA
# ============================================

def mostrar_catalogo():
    """Muestra el catálogo de items disponibles."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       ⚔️  ARMERÍA DISPONIBLE  ⚔️                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                         ⚔️  ARMAS (Tier 1-2)  ⚔️                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  1. DAGA OXIDADA        │  50g │ ATK:  3 │ VEL:  2            ║
║  2. LANZA CORTA         │  75g │ ATK:  6 │ VEL:  0            ║
║  3. ESPADA CORTA        │ 150g │ ATK: 10 │ VEL:  1            ║
║  4. TRIDENTE ROMANO     │ 180g │ ATK:  8 │ VEL:  2            ║
║  5. MARTILLO DE GUERRA  │ 200g │ ATK: 12 │ VEL: -1            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                         ⚔️  ARMAS (Tier 3-4)  ⚔️                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  6. ESPADA GLADIUS      │ 350g │ ATK: 15 │ VEL:  0            ║
║  7. GLADIUS IMPERIAL    │ 450g │ ATK: 18 │ VEL:  1            ║
║  8. HACHA DOBLE         │ 420g │ ATK: 16 │ VEL: -1            ║
║  9. ESPADA RIDIUS       │ 300g │ ATK: 20 │ VEL:  0            ║
║ 10. ESPADA DE MARTE     │ 900g │ ATK: 25 │ VEL:  2 ⭐         ║
║ 11. TRIDENTE NEPTUNO    │ 850g │ ATK: 22 │ VEL:  1 ⭐         ║
║ 12. LANZA DEL DESTINO   │ 800g │ ATK: 24 │ VEL:  0 ⭐         ║
║ 13. HACHA DE POMPEYA    │ 150g │ ATK:  5 │ VEL:  5            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                       🛡️  ARMADURAS (Tier 1-2)  🛡️                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 14. ROPA HARAPIENTA     │  50g │ DEF:  2 │ HP: 10             ║
║ 15. CUERO ENDURECIDO    │  80g │ DEF:  5 │ HP: 15             ║
║ 16. COTA MALLA          │ 150g │ DEF: 10 │ HP: 20             ║
║ 17. ARMADURA BRONCE     │ 200g │ DEF: 12 │ HP: 25             ║
║ 18. PETO HIERRO         │ 220g │ DEF: 14 │ HP: 20             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                       🛡️  ARMADURAS (Tier 3-4)  🛡️                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 19. ESCUDO IMPERIAL     │ 200g │ DEF: 10 │ HP:  0             ║
║ 20. ARMADURA CENTURIÓN  │ 400g │ DEF: 18 │ HP: 30             ║
║ 21. CORAZA REFORZADA    │ 500g │ DEF: 20 │ HP: 35             ║
║ 22. ARMADURA ESPARTANA  │ 300g │ DEF: 20 │ HP:  0             ║
║ 23. ARMADURA ACORAZADA  │ 350g │ DEF: 25 │ HP:  0             ║
║ 24. ARMADURA JÚPITER    │ 900g │ DEF: 28 │ HP: 40 ⭐          ║
║ 25. PETO DIVINO         │1000g │ DEF: 30 │ HP: 50 ⭐          ║
║ 26. ARMADURA INMORTAL   │1200g │ DEF: 32 │ HP: 60 ⭐ ⭐        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                         🧪  POCIONES  🧪                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 27. CURACIÓN MENOR      │  30g │ Restaura 50 HP             ║
║ 28. CURACIÓN MAYOR      │  60g │ Restaura 100 HP            ║
║ 29. FUERZA TEMPORAL     │  50g │ +10 ATK (temporal)          ║
║ 30. DEFENSA TEMPORAL    │  50g │ +5 DEF (temporal)           ║
║ 31. VELOCIDAD TEMPORAL  │  50g │ +5 SPD (temporal)           ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)


def comprar_item(opcion, dinero, inventario, modificador_precio=1.0):
    """
    Compra un item y lo añade al inventario.

    Args:
        opcion: ID del item a comprar
        dinero: Dinero disponible del jugador
        inventario: Inventario actual del jugador
        modificador_precio: Multiplicador (1.0 = normal, 0.9 = -10%, 1.15 = +15%)

    Returns:
        tuple: (dinero_actualizado, inventario_actualizado, item_comprado o None)
    """

    if opcion not in PRECIOS:
        print("❌ Opción inválida")
        return dinero, inventario, None

    precio_base = PRECIOS[opcion]
    precio = int(precio_base * modificador_precio)

    if dinero < precio:
        print(f"❌ No tienes suficiente dinero. Necesitas {precio}g, tienes {dinero}g")
        return dinero, inventario, None

    # Obtener el item
    if opcion in CATALOGO_ARMAS:
        item = CATALOGO_ARMAS[opcion]
    else:
        item = CATALOGO_ARMADURAS[opcion]

    dinero -= precio
    inventario.append(item)

    if modificador_precio != 1.0:
        signo = "-" if modificador_precio < 1.0 else "+"
        print(f"✓ ¡Compraste {item.nombre} por {precio}g! ({signo}{int((modificador_precio-1)*100)}% por tu fama)")
    else:
        print(f"✓ ¡Compraste {item.nombre} por {precio}g!")
    print(f"  Dinero restante: {dinero}g")

    return dinero, inventario, item


def menu_armeria(dinero, inventario, gestor_misiones=None, modificador_precio=1.0):
    """Recibe gestor_misiones como parámetro."""
    
    while True:
        print(f"\n💰 Dinero disponible: {dinero}g")
        mostrar_catalogo()
        print("\n0. Volver")
        
        opcion = input("Elige un item: ").strip()
        
        if opcion == "0":
            break
        
        dinero, inventario, item = comprar_item(opcion, dinero, inventario)
        
        # NUEVO: Trackear compra si se realizó
        if item and gestor_misiones:
            misiones_completadas = gestor_misiones.evento_items_comprados(1)
            if misiones_completadas:
                notif = gestor_misiones.generar_notificacion_misiones(misiones_completadas)
                print(notif)
    
    return dinero, inventario


def equipar_item(jugador, inventario):
    """
    Menú para equipar items del inventario.
    
    Args:
        jugador: Objeto Player
        inventario: Lista de items disponibles
    """
    
    if not inventario:
        print("❌ Inventario vacío")
        return
    
    print("\n📦 INVENTARIO:")
    for i, item in enumerate(inventario, 1):
        print(f"  {i}. {item.nombre}")
    print("  0. Cancelar")
    
    opcion = input("Elige un item: ").strip()
    
    if opcion == "0":
        return
    
    try:
        idx = int(opcion) - 1
        if 0 <= idx < len(inventario):
            item = inventario[idx]
            
            if isinstance(item, Weapon):
                jugador.equipar_arma(item)
                print(f"✓ Equipaste: {item.nombre}")
            elif isinstance(item, Armor):
                jugador.equipar_armadura(item)
                print(f"✓ Equipaste: {item.nombre}")
    except (ValueError, IndexError):
        print("❌ Opción inválida")


# ============================================
# MERCADO DE GLADIADORES
# ============================================

NOMBRES_GLADIADORES = [
    "Marcus", "Lucius", "Gaius", "Publius", "Quintus", "Titus", "Maximus",
    "Decimus", "Servius", "Appius", "Tiberius", "Gnaeus", "Spurius", "Manius"
]

TIPOS_GLADIADORES = ["Murmillo", "Retiarius", "Secutor", "Thraex", "Hoplomachus"]

APODOS = [
    "el Feroz", "el Invencible", "el Veloz", "el Implacable", "la Bestia",
    "el Carnicero", "el Demoledor", "el Furioso", "Mano de Hierro"
]


def generar_nombre_gladiador():
    """Genera un nombre romano aleatorio para gladiador."""
    nombre = random.choice(NOMBRES_GLADIADORES)
    if random.random() < 0.5:
        apodo = random.choice(APODOS)
        return f"{nombre} '{apodo}'"
    return nombre


def calcular_costo_gladiador(nivel):
    """
    Calcula el costo de un gladiador por su nivel.
    Fórmula: 150 * (1.15 ^ nivel)
    """
    return int(150 * (1.15 ** nivel))


def generar_gladiador_disponible(nivel_minimo=1, nivel_maximo=5):
    """
    Genera un gladiador disponible en el mercado.
    
    Args:
        nivel_minimo: Nivel mínimo
        nivel_maximo: Nivel máximo
    
    Returns:
        Gladiador: Nuevo gladiador
    """
    nivel = random.randint(nivel_minimo, nivel_maximo)
    nombre = generar_nombre_gladiador()
    tipo = random.choice(TIPOS_GLADIADORES)
    return Gladiador(nombre, tipo, nivel=nivel)


def mostrar_mercado_gladiadores(nivel_promedio_equipo=1):
    """
    Muestra gladiadores disponibles en el mercado.
    
    Args:
        nivel_promedio_equipo: Para escalar ofertas
    """
    # Generar 6 gladiadores disponibles
    nivel_min = max(1, nivel_promedio_equipo - 2)
    nivel_max = nivel_promedio_equipo + 3
    
    gladiadores = []
    for i in range(6):
        g = generar_gladiador_disponible(nivel_min, nivel_max)
        gladiadores.append(g)
    
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                  🏛️  MERCADO DE GLADIADORES  🏛️                       ║
╠═══════════════════════════════════════════════════════════════════════╣
    """)
    
    for i, g in enumerate(gladiadores, 1):
        costo = calcular_costo_gladiador(g.nivel)
        print(f"║ [{i}] {g.nombre:<20} │ Lvl {g.nivel:>2} │ {g.tipo:<12} │ {costo:>5}g    ║")
    
    print("""╠═══════════════════════════════════════════════════════════════════════╣
║  0. Salir del mercado                                                 ║
╚═══════════════════════════════════════════════════════════════════════╝
    """)
    
    return gladiadores


def comprar_gladiador(gladiadores, opcion, dinero, equipo):
    """
    Intenta comprar un gladiador.
    
    Returns:
        (éxito, dinero_restante, mensaje, gladiador_comprado)
    """
    try:
        idx = int(opcion) - 1
        if not (0 <= idx < len(gladiadores)):
            return False, dinero, "❌ Opción inválida", None
        
        if equipo.equipo_lleno:
            return False, dinero, "❌ Barracas llenas (compra espacio)", None
        
        gladiador = gladiadores[idx]
        costo = calcular_costo_gladiador(gladiador.nivel)
        
        if dinero < costo:
            return False, dinero, f"❌ No tienes suficiente dinero ({costo}g)", None
        
        dinero -= costo
        exito, msg = equipo.agregar_gladiador(gladiador)
        if exito:
            return True, dinero, f"✓ {gladiador.nombre} (Lvl {gladiador.nivel}) se unió por {costo}g", gladiador
        else:
            return False, dinero + costo, msg, None
    
    except (ValueError, IndexError):
        return False, dinero, "❌ Opción inválida", None


def vender_gladiador(equipo):
    """
    Menú para vender un gladiador del equipo.
    
    Returns:
        (dinero_ganado, éxito)
    """
    if not equipo.gladiadores:
        print("❌ No tienes gladiadores para vender")
        return 0, False
    
    print("\n🏛️  VENDER GLADIADOR")
    for i, g in enumerate(equipo.gladiadores, 1):
        costo = calcular_costo_gladiador(g.nivel)
        precio_venta = int(costo * 0.5)  # 50% del precio original
        print(f"  [{i}] {g.nombre} (Lvl {g.nivel}) → Vende por {precio_venta}g")
    print("  [0] Cancelar")
    
    opcion = input("\n¿A quién vendes? [0-{}]: ".format(len(equipo.gladiadores))).strip()
    
    try:
        idx = int(opcion) - 1
        if idx == -1:
            return 0, False
        
        if 0 <= idx < len(equipo.gladiadores):
            gladiador = equipo.gladiadores[idx]
            costo = calcular_costo_gladiador(gladiador.nivel)
            precio_venta = int(costo * 0.5)
            
            equipo.remover_gladiador(idx)
            print(f"✓ Vendiste {gladiador.nombre} por {precio_venta}g")
            return precio_venta, True
    except (ValueError, IndexError):
        pass
    
    return 0, False


# ============================================
# POCIONES Y VENTA DE ITEMS
# ============================================

def comprar_pocion(opcion, dinero, inventario):
    """
    Compra una poción y la añade al inventario.
    
    Returns:
        tuple: (dinero_actualizado, inventario_actualizado, pocion o None)
    """
    if opcion not in PRECIOS:
        print("❌ Opción inválida")
        return dinero, inventario, None
    
    if opcion not in CATALOGO_POCIONES:
        print("❌ Esto no es una poción")
        return dinero, inventario, None
    
    precio = PRECIOS[opcion]
    
    if dinero < precio:
        print(f"❌ No tienes suficiente dinero (cuesta {precio}g, tienes {dinero}g)")
        return dinero, inventario, None
    
    pocion = CATALOGO_POCIONES[opcion]
    dinero -= precio
    
    if opcion not in inventario:
        inventario[opcion] = 0
    inventario[opcion] += 1
    
    print(f"✓ Compraste {pocion.nombre} por {precio}g")
    return dinero, inventario, pocion


def vender_item(opcion, dinero, inventario):
    """
    Vende un item del inventario (devuelve 50% del precio).
    
    Returns:
        tuple: (dinero_actualizado, inventario_actualizado, True/False)
    """
    if opcion not in PRECIOS:
        print("❌ Opción inválida")
        return dinero, inventario, False
    
    if opcion not in inventario or inventario[opcion] <= 0:
        print("❌ No tienes este item")
        return dinero, inventario, False
    
    precio_original = PRECIOS[opcion]
    precio_venta = int(precio_original * 0.5)
    
    inventario[opcion] -= 1
    dinero += precio_venta
    
    # Obtener nombre del item
    item_nombre = "Item"
    if opcion in CATALOGO_ARMAS:
        item_nombre = CATALOGO_ARMAS[opcion].nombre
    elif opcion in CATALOGO_ARMADURAS:
        item_nombre = CATALOGO_ARMADURAS[opcion].nombre
    elif opcion in CATALOGO_POCIONES:
        item_nombre = CATALOGO_POCIONES[opcion].nombre
    
    print(f"✓ Vendiste {item_nombre} por {precio_venta}g")
    return dinero, inventario, True


def mostrar_inventario(inventario):
    """Muestra el inventario con precios de venta."""
    print("\n" + "=" * 80)
    print("INVENTARIO - PRECIOS DE VENTA (50% del precio original)")
    print("=" * 80)
    
    if not inventario or all(v <= 0 for v in inventario.values()):
        print("❌ Inventario vacío")
        return
    
    print("\n⚔️  ARMAS:")
    for key in sorted(CATALOGO_ARMAS.keys()):
        if key in inventario and inventario[key] > 0:
            arma = CATALOGO_ARMAS[key]
            precio_venta = int(PRECIOS[key] * 0.5)
            print(f"  [{key}] {arma.nombre:<25} (original: {PRECIOS[key]}g → vende: {precio_venta}g) x{inventario[key]}")
    
    print("\n🛡️  ARMADURAS:")
    for key in sorted(CATALOGO_ARMADURAS.keys()):
        if key in inventario and inventario[key] > 0:
            arm = CATALOGO_ARMADURAS[key]
            precio_venta = int(PRECIOS[key] * 0.5)
            print(f"  [{key}] {arm.nombre:<25} (original: {PRECIOS[key]}g → vende: {precio_venta}g) x{inventario[key]}")
    
    print("\n🧪 POCIONES:")
    for key in sorted(CATALOGO_POCIONES.keys()):
        if key in inventario and inventario[key] > 0:
            pocion = CATALOGO_POCIONES[key]
            precio_venta = int(PRECIOS[key] * 0.5)
            print(f"  [{key}] {pocion.nombre:<25} (original: {PRECIOS[key]}g → vende: {precio_venta}g) x{inventario[key]}")
    
    print("=" * 80)


def mostrar_catalogo_herrero(herrero_nivel=1):
    """Muestra catálogo de armas con estado de desbloqueo según nivel Herrero."""
    tier_desbloqueado = herrero_nivel
    
    print("\n" + "=" * 90)
    print("⚒️  ARMERÍA - ARMAS DISPONIBLES")
    print("=" * 90)
    
    for tier in range(1, 5):
        if tier == 1:
            print("\n🗡️  TIER 1 - BÁSICAS (STR: 10)")
        elif tier == 2:
            print("\n🗡️  TIER 2 - INTERMEDIAS (STR: 15)")
        elif tier == 3:
            print("\n🗡️  TIER 3 - AVANZADAS (STR: 20)")
        else:
            print("\n⭐ TIER 4 - LEGENDARIAS (STR: 25)")
        
        print("-" * 90)
        
        for key, arma in CATALOGO_ARMAS.items():
            if arma.tier == tier:
                precio = PRECIOS[key]
                desbloqueada = tier <= tier_desbloqueado
                
                # Construye línea de arma
                if desbloqueada:
                    linea = f"  [{key:>2}] {arma.nombre:<25} │ {precio:>5}g │ "
                    linea += f"ATK: {arma.attack:>2} │ VEL: {arma.agilidad:>2} │ PESO: {arma.peso:>3.1f}kg"
                else:
                    linea = f"  🔒 [{key:>2}] {arma.nombre:<25} │ ??? │ "
                    linea += f"(Se desbloquea a nivel {tier} de Herrero)"
                
                print(linea)
    
    print("\n" + "=" * 90)
    print(f"⚒️  Herrero Nivel: {herrero_nivel}/5 │ Tier Desbloqueado: {tier_desbloqueado}")
    print("=" * 90 + "\n")


def comprar_item_herrero(opcion, dinero, inventario, herrero_nivel=1, modificador_precio=1.0):
    """
    Compra un item verificando requisitos de Herrero.
    Si es un arma bloqueada, muestra mensaje de desbloqueo.
    """
    if opcion not in PRECIOS:
        return False, 0, "❌ Opción inválida"

    precio_base = PRECIOS[opcion]
    precio = int(precio_base * modificador_precio)

    # Si es una arma, verifica si está desbloqueada
    if opcion in CATALOGO_ARMAS:
        arma = CATALOGO_ARMAS[opcion]
        if arma.tier > herrero_nivel:
            return False, 0, f"🔒 Esta arma está bloqueada. Se desbloquea a nivel {arma.tier} de Herrero"

    # Verifica dinero
    if dinero < precio:
        return False, 0, f"💰 No tienes suficiente dinero. Necesitas {precio}g"

    # Compra normalmente
    if opcion not in inventario:
        inventario[opcion] = 0
    inventario[opcion] += 1

    if modificador_precio != 1.0:
        signo = "-" if modificador_precio < 1.0 else "+"
        return True, precio, (f"✅ Compraste {CATALOGO_ARMAS.get(opcion, CATALOGO_ARMADURAS.get(opcion, CATALOGO_POCIONES.get(opcion, 'Item'))).nombre} "
                f"({signo}{int((modificador_precio-1)*100)}% por tu fama)")

    return True, precio, f"✅ Compraste {CATALOGO_ARMAS.get(opcion, CATALOGO_ARMADURAS.get(opcion, CATALOGO_POCIONES.get(opcion, 'Item'))).nombre}"