from Character import Weapon, Armor

# Catálogo de armas disponibles
catalogo_armas = {
    "1": Weapon("Espada Ridius", attack=20, speed=0),
    "2": Weapon("Espada Gladius", attack=15, speed=0),
    "3": Weapon("Hacha de Pompeya", attack=5, speed=5),
}

# Catálogo de armaduras disponibles
catalogo_armaduras = {
    "4": Armor("Escudo Imperial", deffense=10, hp=0),
    "5": Armor("Armadura Espartana", deffense=20, hp=0),
    "6": Armor("Armadura Acorazada", deffense=25, hp=0),
}

# Precios de los items
precios = {
    "1": 300,
    "2": 200,
    "3": 150,
    "4": 200,
    "5": 300,
    "6": 350
}

def mostrar_catalogo():
    """Muestra el catálogo de items disponibles"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                  ⚔️  ARMERÍA DISPONIBLE  ⚔️                    ║
╠══════════════════════════════════════════════════════════════╣
║                         ⚔️  ARMAS  ⚔️                          ║
╠══════════════════════════════════════════════════════════════╣
║  1. ESPADA RIDIUS       │ 300g │ ATK: 20 │ VEL: 0            ║
║  2. ESPADA GLADIUS      │ 200g │ ATK: 15 │ VEL: 0            ║
║  3. HACHA DE POMPEYA    │ 150g │ ATK:  5 │ VEL: 5            ║
╠══════════════════════════════════════════════════════════════╣
║                       🛡️  ARMADURAS  🛡️                        ║
╠══════════════════════════════════════════════════════════════╣
║  4. ESCUDO IMPERIAL     │ 200g │ DEF: 10 │ HP:  0            ║
║  5. ARMADURA ESPARTANA  │ 300g │ DEF: 20 │ HP:  0            ║
║  6. ARMADURA ACORAZADA  │ 350g │ DEF: 25 │ HP:  0            ║
╚══════════════════════════════════════════════════════════════╝
    """)

def comprar_item(opcion, dinero, inventario):
    """
    Compra un item y lo añade al inventario.
    Retorna: (dinero_actualizado, inventario_actualizado, item_comprado o None)
    """
    if opcion not in precios:
        print("\n  ❌ Opción inválida!")
        return dinero, inventario, None
    
    precio = precios[opcion]
    
    # Verificar si tiene dinero
    if dinero < precio:
        print(f"\n  ⚠️  ━━━ NO TIENES SUFICIENTE DINERO ━━━")
        print(f"      Te faltan {precio - dinero}g")
        return dinero, inventario, None
    
    # Obtener el item
    if opcion in catalogo_armas:
        item = catalogo_armas[opcion]
        tipo = "arma"
    else:
        item = catalogo_armaduras[opcion]
        tipo = "armadura"
    
    print(f"\n  ┌────────────────────────────────────┐")
    print(f"  │  Has elegido: {item.nombre:<20} │")
    print(f"  │  Precio: {precio}g{' ' * (25 - len(str(precio)))}│")
    print(f"  └────────────────────────────────────┘")
    
    confirmacion = input("\n  ¿Confirmar compra? (s/n): ").strip().lower()
    
    if confirmacion != "s":
        print("\n  🚫 Compra cancelada!")
        return dinero, inventario, None
    
    # Realizar compra
    dinero -= precio
    
    if tipo == "arma":
        inventario.append({
            "tipo": "arma",
            "nombre": item.nombre,
            "attack": item.attack,
            "speed": item.speed,
            "precio": precio
        })
    else:
        inventario.append({
            "tipo": "armadura",
            "nombre": item.nombre,
            "deffense": item.deffense,
            "hp": item.hp,
            "precio": precio
        })
    
    print(f"\n  ✓ {item.nombre} añadido al inventario!")
    print(f"  💰 Dinero restante: {dinero}g")
    
    return dinero, inventario, item

def mostrar_inventario(inventario):
    """Muestra el inventario del jugador"""
    print("\n  ╔════════════════════════════════════╗")
    print("  ║       📦 INVENTARIO 📦             ║")
    print("  ╚════════════════════════════════════╝")
    
    if len(inventario) == 0:
        print("\n  ⚠️  Tu inventario está vacío")
        return
    
    for i, elemento in enumerate(inventario, 1):
        tipo = elemento["tipo"]
        nombre = elemento["nombre"]
        
        if tipo == "arma":
            print(f"  {i}. ⚔️  {nombre}")
            print(f"      └─ ATK: +{elemento['attack']} | VEL: +{elemento['speed']}")
        else:
            print(f"  {i}. 🛡️  {nombre}")
            print(f"      └─ DEF: +{elemento['deffense']} | HP: +{elemento['hp']}")

def equipar_item(inventario, gladiador):
    """Permite equipar un item del inventario al gladiador"""
    if len(inventario) == 0:
        print("\n  ⚠️  No tienes items para equipar.")
        return
    
    mostrar_inventario(inventario)
    
    try:
        opcion = int(input("\n  ➤ ¿Qué item deseas equipar? (número): "))
        if opcion < 1 or opcion > len(inventario):
            print("\n  ❌ Opción inválida.")
            return
        
        elemento = inventario[opcion - 1]
        tipo = elemento["tipo"]
        
        # Recrear el objeto desde los datos guardados
        if tipo == "arma":
            item = Weapon(elemento["nombre"], elemento["attack"], elemento["speed"])
            
            if gladiador.weapon:
                print(f"\n  ⚠️  Ya tienes equipada: {gladiador.weapon.nombre}")
                confirmar = input("  ¿Deseas reemplazarla? (s/n): ").strip().lower()
                if confirmar != "s":
                    print("\n  🚫 Equipo cancelado")
                    return
            gladiador.weapon = item
            print(f"\n  ✓ ¡{item.nombre} equipada como arma!")
        else:
            item = Armor(elemento["nombre"], elemento["deffense"], elemento["hp"])
            
            if gladiador.armor:
                print(f"\n  ⚠️  Ya tienes equipada: {gladiador.armor.nombre}")
                confirmar = input("  ¿Deseas reemplazarla? (s/n): ").strip().lower()
                if confirmar != "s":
                    print("\n  🚫 Equipo cancelado")
                    return
            gladiador.armor = item
            print(f"\n  ✓ ¡{item.nombre} equipada como armadura!")
            
    except ValueError:
        print("\n  ❌ Ingresa un número válido.")

def menu_armeria(dinero, inventario, gladiador):
    """
    Menu principal de la armeria.
    Retorna: (dinero_actualizado, inventario_actualizado)
    """
    while True:
        print("\n╔════════════════════════════════════════╗")
        print("║          🗡️  ARMERÍA  🗡️                 ║")
        print("╚════════════════════════════════════════╝")
        print(f"  💰 Dinero disponible: {dinero}g")
        print("\n  ┌────────────────────┐")
        print("  │  1. 💳 COMPRAR     │")
        print("  │  2. 📦 INVENTARIO  │")
        print("  │  3. ⚔️  EQUIPAR     │")
        print("  │  4. 🚪 SALIR       │")
        print("  └────────────────────┘")
        
        opcion = input("\n  ➤ ¿Qué deseas hacer? (1-4): ").strip()
        
        if opcion == "1":
            mostrar_catalogo()
            item_opcion = input("\n  ➤ Escoge un item (1-6) o '0' para cancelar: ").strip()
            
            if item_opcion == "0":
                continue
            
            dinero, inventario, _ = comprar_item(item_opcion, dinero, inventario)
            
        elif opcion == "2":
            mostrar_inventario(inventario)
            
        elif opcion == "3":
            equipar_item(inventario, gladiador)
            
        elif opcion == "4":
            print("\n  👋 ¡Hasta pronto, gladiador!")
            break
        else:
            print("\n  ❌ Opción inválida. Intenta de nuevo.")
    
    return dinero, inventario