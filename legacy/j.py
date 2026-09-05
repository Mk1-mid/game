import json
import os

# ============================================
# GESTIÓN DE ARCHIVOS JSON
# ============================================
USERS_FILE = "users.json"

def cargar_usuarios():
    """Carga usuarios desde el archivo JSON"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Archivo de usuarios corrupto. Creando nuevo")
            return {"admin": "123"}
    else:
        # Si no existe, crear archivo con usuario de prueba
        usuarios_default = {"admin": "123"}
        guardar_usuarios(usuarios_default)
        print("Archivo users.json creado.")
        return usuarios_default

def guardar_usuarios(users_db):
    """Guarda usuarios en el archivo JSON"""
    with open(USERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(users_db, file, indent=4, ensure_ascii=False)

# FUNCIONES ORIGINALES DE TU COMPAÑERO

def _hacer_registro(db):
    """
    Registra un nuevo usuario.
    MODIFICADO: Ahora guarda en JSON
    """
    print("\n--- Registro de Nuevo Gladiador ---")
    user = input("Nuevo nombre de usuario: ").strip()
    
    if not user:
        print("El nombre no puede estar vacio.")
        return
    
    # Validamos si el usuario ya existe
    if user in db:
        print("Error! Ese nombre de usuario ya existe.")
    else:
        passw = input("Nueva contraseña: ").strip()
        
        if not passw:
            print("La contrasena no puede estar vacia.")
            return
        
        db[user] = passw
        guardar_usuarios(db)  #  NUEVO: Guardar en JSON
        print(f"Usuario {user} registrado con éxito!")

def _hacer_login(db):
    """
    Inicia sesión de un usuario.
    Retorna el nombre de usuario si es exitoso, o None si falla.
    """
    print("\n--- Iniciar Sesión ---")
    
    # 3.1: "Manejar intentos fallidos con advertencias"
    intentos_maximos = 3
    intentos = 0
    
    # Este bucle controla los intentos
    while intentos < intentos_maximos:
        user = input("Usuario: ").strip()
        passw = input("Contraseña: ").strip()
        
        # 1. Revisamos si el usuario existe
        if user in db:
            # 2. Si existe, revisamos si la contraseña es correcta
            if db[user] == passw:
                print(f"\nBienvenido de vuelta, {user}!")
                return user  # Éxito
            else:
                print("Contraseña incorrecta.")
        else:
            print("Ese usuario no existe.")
            
        intentos = intentos + 1
        print(f"Te quedan {intentos_maximos - intentos} intentos.")
        
    print("Has fallado muchos intentos. Vuelve al menú.")
    return None  # Fallo

def mostrar_menu_autenticacion():
    """
    Muestra el menú de autenticación.
    MODIFICADO: Ahora carga usuarios desde JSON
    """
    users_db = cargar_usuarios()  # ⭐ NUEVO: Cargar desde JSON
    opcion = ""
    
    # Este bucle controla el menú de acceso
    while opcion != "3":
        print("\n" + "="*30)
        print("     MENU DE ACCESO")
        print("="*30)
        print("     1. Iniciar Sesión")
        print("     2. Registrarse")
        print("     3. Salir del Juego")
        print("="*30)
        opcion = input("    Elige una opción: ").strip()

        if opcion == "1":
            usuario_logueado = _hacer_login(users_db)
            if usuario_logueado:
                return usuario_logueado  # Sale del bucle si el login es bueno
        elif opcion == "2":
            _hacer_registro(users_db)
        elif opcion == "3":
            print("Saliendo...")
        else:
            # Manejo de opción inválida
            print("Opción no válida, intenta de nuevo.")
            
    return None  # Si el usuario elige "Salir" (3)


# FUNCIONES PARA GUARDAR PROGRESO DEL JUEGO
def cargar_partida(username):
    """Carga la partida guardada de un usuario"""
    filename = f"save_{username}.json"
    
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                print(f"Partida guardada encontrada para {username}")
                return json.load(file)
        except json.JSONDecodeError:
            print("Archivo de guardado corrupto. Iniciando nueva partida...")
            return None
    return None

def guardar_partida(username, datos_partida):
    """Guarda el progreso del jugador"""
    filename = f"save_{username}.json"
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(datos_partida, file, indent=4, ensure_ascii=False)
    
    print(f"Partida guardada exitosamente.")

def crear_nueva_partida():
    """Crea datos iniciales de una nueva partida"""
    return {
        "dinero": 1000,
        "salud_jugador": 100,
        "vida_maxima": 100,
        "victorias": 0,
        "derrotas": 0,
        "inventario_armas": [],
        "arma_equipada": None,
        "armadura_equipada": None
    }
