
# 3.1: "Mantener los usuarios creados en memoria durante la ejecucion."
# Usamos un diccionario para guardar usuarios.
users_db = {
    "admin": "123"  # Un usuario de prueba
}
def _hacer_registro(db):

    print("\n--- Registro de Nuevo Gladiador ---")
    user = input("Nuevo nombre de usuario: ")
    
    # Validamos si el usuario ya existe
    if user in db:
        print("Error! Ese nombre de usuario ya existe.")
    else:
        passw = input("Nueva contrasena: ")
        db[user] = passw
        print(f"Usuario {user} registrado con exito!")

def _hacer_login(db):
    
    #Retorna el nombre de usuario si es exitoso, o None si falla.
    
    print("\n--- Iniciar Sesion ---")
    
    # 3.1: "Manejar intentos fallidos con advertencias"
    intentos_maximos = 3
    intentos = 0
    
    # Este bucle controla los intentos
    while intentos < intentos_maximos:
        user = input("Usuario: ")
        passw = input("Contrasena: ")
        
        # 1. Revisamos si el usuario existe
        if user in db:
            # 2. Si existe, revisamos si la contrasena es correcta
            if db[user] == passw:
                print(f"\n¡Bienvenido de vuelta, {user}!")
                return user # Exito
            else:
                print("Contrasena incorrecta.")
        else:
            print("Ese usuario no existe.")
            
        intentos = intentos + 1
        print(f"Te quedan {intentos_maximos - intentos} intentos.")
        
    print("Has fallado muchos intentos. Vuelve al menu.")
    return None # Fallo

def mostrar_menu_autenticacion(users_db):
  
    opcion = ""
    
    # Este bucle controla el menu de acceso
    while opcion != "3":
        print("\n" + "="*25)
        print("   MENU DE ACCESO   ")
        print("="*25)
        print("1. Iniciar Sesion")
        print("2. Registrarse")
        print("3. Salir del Juego")
        opcion = input("Elige una opcion: ")

        if opcion == "1":
            usuario_logueado = _hacer_login(users_db)
            if usuario_logueado:
                return usuario_logueado # Sale del bucle si el login es bueno
        elif opcion == "2":
            _hacer_registro(users_db)
        elif opcion == "3":
            print("Saliendo...")
        else:
            # Manejo de opcion invalida
            print("Opcion no valida, intenta de nuevo.")
            
    return None # Si el usuario elige "Salir" (3)

print("--- BIENVENIDO A CRUDZASO GAMES ---")

# Llamamos a la funcion principal de autenticacion
username_logueado = mostrar_menu_autenticacion(users_db)

# Este 'if' es la puerta de entrada al juego.
if username_logueado:
    print(f"\n--- ACCESO CONCEDIDO, {username_logueado} ---")
        
    # nombre temporal del juego
    print("\n\n" + "="*40)
    print("||" + " " * 36 + "||")
    print("||" + " EL DESPERTAR DEL GLADIADOR".center(36) + "||")
    print("||" + "(por Crudzaso Games)".center(36) + "||")
    print("||" + " " * 36 + "||")
    print("="*40)
    
    # boton de start y salir
    print("\n" + "-"*20)
    print("  [ 1. STAR GAME ]")
    print("  [ 2. SALIR     ]")
    print("-"*20)
    
    opcion_star = input("... Pulsa 1 para empezar: ")
    
    if opcion_star == "1":
        print("\n¡Comienza el juego!")
    else:
        print("Decides no jugar hoy. Saliendo...")

else:
    # Finaliza el programa de manera ordenada
    print("\nGracias por jugar. ¡Vuelve pronto!")