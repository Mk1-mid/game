"""
Sistema de autenticación y guardado de partidas
==============================================
"""

import json
import os


USERS_FILE = "data/users.json"
SAVE_DIR = "data/saves"


# ============================================
# GESTIÓN DE ARCHIVOS
# ============================================

def asegurar_archivos():
    """Crea los directorios necesarios si no existen."""
    os.makedirs(SAVE_DIR, exist_ok=True)


def cargar_usuarios():
    """
    Carga la base de datos de usuarios desde JSON.
    
    Returns:
        dict: Diccionario {usuario: contraseña}
    """
    asegurar_archivos()
    
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("⚠️  Archivo de usuarios corrupto. Creando nuevo.")
            return {"admin": "123"}
    else:
        usuarios_default = {"admin": "123"}
        guardar_usuarios(usuarios_default)
        print("✓ Archivo users.json creado.")
        return usuarios_default


def guardar_usuarios(usuarios):
    """Guarda la base de datos de usuarios en JSON."""
    asegurar_archivos()
    with open(USERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(usuarios, file, indent=4, ensure_ascii=False)


# ============================================
# AUTENTICACIÓN
# ============================================

def registrar_usuario():
    """Registra un nuevo usuario con validación."""
    print("\n--- Registro de Nuevo Gladiador ---")
    usuario = input("Nuevo nombre de usuario: ").strip()
    
    if not usuario:
        print("❌ El nombre no puede estar vacío.")
        return False
    
    db = cargar_usuarios()
    
    if usuario in db:
        print("❌ Ese nombre de usuario ya existe.")
        return False
    
    contraseña = input("Nueva contraseña: ").strip()
    
    if not contraseña:
        print("❌ La contraseña no puede estar vacía.")
        return False
    
    db[usuario] = contraseña
    guardar_usuarios(db)
    print(f"✓ ¡Bienvenido, {usuario}! Tu cuenta ha sido creada.")
    return True


def iniciar_sesion():
    """Inicia sesión con validación (máx 3 intentos)."""
    print("\n--- Inicio de Sesión ---")
    usuario = input("Usuario: ").strip()
    
    db = cargar_usuarios()
    
    if usuario not in db:
        print(f"❌ Usuario '{usuario}' no encontrado.")
        return None
    
    for intento in range(1, 4):
        contraseña = input(f"Contraseña (intento {intento}/3): ").strip()
        
        if db[usuario] == contraseña:
            print(f"✓ Bienvenido, {usuario}!")
            return usuario
        else:
            print("❌ Contraseña incorrecta.")
    
    print("❌ Máximo de intentos alcanzado.")
    return None


def mostrar_menu_autenticacion():
    """Menú de autenticación (registro/login)."""
    while True:
        print("""
╔════════════════════════════════════════╗
║        BIENVENIDO AL COLISEO           ║
╠════════════════════════════════════════╣
║  1. Iniciar Sesión                     ║
║  2. Registrarse                        ║
║  3. Salir                              ║
╚════════════════════════════════════════╝
        """)
        
        opcion = input("Elige una opción: ").strip()
        
        if opcion == "1":
            usuario = iniciar_sesion()
            if usuario:
                return usuario
        elif opcion == "2":
            if registrar_usuario():
                usuario = iniciar_sesion()
                if usuario:
                    return usuario
        elif opcion == "3":
            return None
        else:
            print("❌ Opción inválida.")


# ============================================
# GUARDADO DE PARTIDAS
# ============================================

def crear_nueva_partida():
    """Crea una estructura de partida nueva."""
    return {
        "dinero": 1000,
        "salud_jugador": 100,
        "vida_maxima": 100,
        "victorias": 0,
        "derrotas": 0,
        "inventario_armas": [],
        "inventario_armaduras": [],
        "experiencia": 0,
        "nivel": 1
    }


def cargar_partida(usuario):
    """
    Carga la partida guardada de un usuario.
    
    Args:
        usuario: Nombre de usuario
    
    Returns:
        dict: Datos de partida o None si no existe
    """
    archivo_partida = os.path.join(SAVE_DIR, f"save_{usuario}.json")
    
    if os.path.exists(archivo_partida):
        try:
            with open(archivo_partida, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"⚠️  Partida de {usuario} corrupta.")
            return None
    
    return None


def guardar_partida(usuario, datos_partida):
    """
    Guarda la partida de un usuario.
    
    Args:
        usuario: Nombre de usuario
        datos_partida: Diccionario con datos de partida
    """
    asegurar_archivos()
    archivo_partida = os.path.join(SAVE_DIR, f"save_{usuario}.json")
    
    with open(archivo_partida, 'w', encoding='utf-8') as file:
        json.dump(datos_partida, file, indent=4, ensure_ascii=False)
    
    print(f"✓ Partida guardada para {usuario}")
