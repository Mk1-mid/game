#!/usr/bin/env python3
"""
🎮 GUÍA RÁPIDA - SANGRE POR FORTUNA
====================================

Script para mostrar información útil sobre el proyecto.
Ejecuta: python guia.py
"""

def mostrar_menu():
    """Menú de ayuda rápida."""
    print("""
╔═════════════════════════════════════════════════════════════╗
║                                                             ║
║           🎮 SANGRE POR FORTUNA - GUÍA RÁPIDA 🎮          ║
║                                                             ║
╚═════════════════════════════════════════════════════════════╝

¿QUÉ NECESITAS?

  1. Ejecutar el juego
  2. Ver la estructura del proyecto
  3. Cómo agregar un nuevo enemigo
  4. Cómo agregar un nuevo item
  5. Cómo contribuir
  6. Solucionar problemas
  7. Salir
    """)

def ejecutar_juego():
    print("""
╔═════════════════════════════════════════════════════════════╗
║                   EJECUTAR EL JUEGO
╚═════════════════════════════════════════════════════════════╝

1️⃣  Abre una terminal en: c:\\Users\\USUARIO\\Desktop\\juego

2️⃣  Escribe:
    python main.py

3️⃣  Usa credenciales:
    Usuario: admin
    Contraseña: 123

✅ ¡El juego debería iniciar!
    """)

def estructura():
    print("""
╔═════════════════════════════════════════════════════════════╗
║              ESTRUCTURA DEL PROYECTO
╚═════════════════════════════════════════════════════════════╝

📁 juego/
├── src/                       Código fuente
│   ├── models.py             Clases de personajes
│   ├── combat.py             Sistema de combate
│   ├── store.py              Tienda/armería
│   ├── enemies.py            Enemigos aleatorios
│   └── auth.py               Autenticación
│
├── data/                     Datos persistentes
│   ├── users.json            Usuarios registrados
│   └── saves/                Archivos de partidas
│
├── docs/                     Documentación
│   ├── TECNICA.md            Referencia técnica
│   ├── ROADMAP.md            Estado y planes
│   └── HISTORIAL.md          Historial del desarrollo
│
├── main.py                   Punto de entrada
└── README.md                 Información principal

📖 DOCUMENTACIÓN:
  → README.md                 Información general
  → docs/TECNICA.md           Detalles técnicos y guía de desarrollo
  → docs/ROADMAP.md           Estado actual y planes
    """)

def nuevo_enemigo():
    print("""
╔═════════════════════════════════════════════════════════════╗
║           AGREGAR UN NUEVO TIPO DE ENEMIGO
╚═════════════════════════════════════════════════════════════╝

1️⃣  Abre: src/enemies.py

2️⃣  Copia este código ANTES de generar_enemigo():

class MiEnemigo(EnemyVariant):
    \"\"\"Descripción breve del enemigo.\"\"\"
    
    def __init__(self):
        super().__init__(
            nombre=generar_nombre_gladiador(),
            hp=100,        # Puntos de vida
            attack=20,     # Daño base
            defense=10,    # Defensa base
            speed=12       # Velocidad
        )
        self.tipo = "Mi Enemigo"

3️⃣  Agrega a la lista TIPOS_ENEMIGOS:

TIPOS_ENEMIGOS = [Murmillo, Retiarius, Secutor, 
                  Thraex, Hoplomachus, MiEnemigo]

4️⃣  Guarda y ¡listo!

💡 TIPS:
  - HP alto = tanque
  - ATK alto = agresivo
  - SPD alto = rápido
  - DEF alto = defensivo
    """)

def nuevo_item():
    print("""
╔═════════════════════════════════════════════════════════════╗
║            AGREGAR UN NUEVO ITEM A LA TIENDA
╚═════════════════════════════════════════════════════════════╝

1️⃣  Abre: src/store.py

2️⃣  Agregar ARMA:

CATALOGO_ARMAS["7"] = Weapon("Mi Arma", attack=25, speed=1)
PRECIOS["7"] = 400

3️⃣  Agregar ARMADURA:

CATALOGO_ARMADURAS["8"] = Armor("Mi Armadura", defense=15, hp=20)
PRECIOS["8"] = 350

4️⃣  Actualizar mostrar_catalogo() para mostrar en el menú

5️⃣  Guarda y ¡listo!

💡 TIPS:
  - attack: daño adicional (0-30)
  - speed: velocidad adicional (0-10)
  - defense: defensa adicional (0-30)
  - hp: HP adicional (0-50)
    """)

def contribuir():
    print("""
╔═════════════════════════════════════════════════════════════╗
║                    CÓMO CONTRIBUIR
╚═════════════════════════════════════════════════════════════╝

✅ LO FÁCIL (sin experiencia):
  □ Agregar nuevos enemigos
  □ Agregar nuevos items
  □ Mejorar descriptions/textos
  □ Crear nuevos nombres romanos

✅ INTERMEDIO:
  □ Crear sistema de quests
  □ Agregar habilidades especiales
  □ Mejorar IA de enemigos
  □ Nuevas opciones de menú

✅ AVANZADO:
  □ Base de datos SQL
  □ Sistema de multiplayer
  □ Cliente gráfico (pygame/tkinter)
  □ API REST

📝 PROCESO:
  1. Crea una rama: git checkout -b feature/mifeature
  2. Haz cambios
  3. Prueba con: python test_proyecto.py
  4. Commit: git commit -m "Agrego mifeature"
  5. Push y crea Pull Request

🎯 CONVENCIONES:
  - Funciones: snake_case
  - Clases: PascalCase
  - Constantes: UPPER_SNAKE_CASE
  - Docstrings en todo
    """)

def problemas():
    print("""
╔═════════════════════════════════════════════════════════════╗
║                  SOLUCIONAR PROBLEMAS
╚═════════════════════════════════════════════════════════════╝

❌ ERROR: "ModuleNotFoundError: No module named 'src'"
✅ SOLUCIÓN:
   - Asegúrate de estar en c:\\Users\\USUARIO\\Desktop\\juego
   - Verifica que exista la carpeta src/
   - Intenta de nuevo

❌ ERROR: "Archivo de usuarios corrupto"
✅ SOLUCIÓN:
   - Borra data/users.json
   - El juego lo recreará automáticamente
   - Usa admin/123 para iniciar sesión

❌ ERROR: "No se reproduce música"
✅ SOLUCIÓN:
   - Instala pygame: pip install pygame
   - O coloca musica.mp3 en la raíz del proyecto
   - Si no quieres música, ignora el error

❌ ERROR: "El juego se cierra"
✅ SOLUCIÓN:
   - Verifica la salud del gladiador (debe ser > 0)
   - Descansa en la base para curarte
   - Crea una nueva partida

❌ ERROR: "No puedo comprar items"
✅ SOLUCIÓN:
   - Verifica que tengas suficiente dinero (usa opción 4)
   - Gana combates para obtener dinero
   - Asegúrate de escribir la opción correcta

📞 MÁS AYUDA:
   - Lee docs/TECNICA.md
   - Consulta docs/ROADMAP.md
    """)

def main():
    """Menú principal."""
    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-7): ").strip()
        
        print("\n")
        
        if opcion == "1":
            ejecutar_juego()
        elif opcion == "2":
            estructura()
        elif opcion == "3":
            nuevo_enemigo()
        elif opcion == "4":
            nuevo_item()
        elif opcion == "5":
            contribuir()
        elif opcion == "6":
            problemas()
        elif opcion == "7":
            print("¡Hasta pronto! 👋\n")
            break
        else:
            print("❌ Opción inválida\n")
        
        input("Presiona ENTER para continuar...")
        print("\n" * 2)

if __name__ == "__main__":
    main()
