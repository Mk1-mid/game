"""
Test simple para verificar que el proyecto está bien organizado
Ejecuta: python test_proyecto.py
"""

import os
import sys

def verificar_estructura():
    """Verifica que todos los archivos necesarios existan."""
    
    archivos_necesarios = {
        "Código fuente": [
            "src/__init__.py",
            "src/models.py",
            "src/combat.py",
            "src/store.py",
            "src/enemies.py",
            "src/auth.py",
        ],
        "Documentación": [
            "README.md",
            "docs/ESTRUCTURA.md",
            "docs/GUIA_DESARROLLO.md",
        ],
        "Configuración": [
            "main.py",
            "requirements.txt",
            ".gitignore",
        ]
    }
    
    print("\n" + "="*60)
    print("  VERIFICACIÓN DE ESTRUCTURA DEL PROYECTO")
    print("="*60 + "\n")
    
    todos_ok = True
    
    for categoria, archivos in archivos_necesarios.items():
        print(f"📁 {categoria}:")
        
        for archivo in archivos:
            existe = os.path.exists(archivo)
            estado = "✅" if existe else "❌"
            print(f"   {estado} {archivo}")
            todos_ok = todos_ok and existe
        
        print()
    
    return todos_ok


def verificar_imports():
    """Verifica que los imports funcionen correctamente."""
    
    print("📚 VERIFICACIÓN DE IMPORTS:\n")
    
    try:
        print("   Cargando src.models...", end=" ")
        from src.models import Player, Weapon, Armor
        print("✅")
        
        print("   Cargando src.combat...", end=" ")
        from src.combat import combate_arena, calcular_daño
        print("✅")
        
        print("   Cargando src.store...", end=" ")
        from src.store import menu_armeria, CATALOGO_ARMAS
        print("✅")
        
        print("   Cargando src.enemies...", end=" ")
        from src.enemies import generar_enemigo, Murmillo
        print("✅")
        
        print("   Cargando src.auth...", end=" ")
        from src.auth import cargar_usuarios, mostrar_menu_autenticacion
        print("✅")
        
        print("\n✅ Todos los imports funcionan correctamente!\n")
        return True
    
    except ImportError as e:
        print(f"\n❌ Error de import: {e}\n")
        return False


def verificar_clases():
    """Verifica que las clases principales existan."""
    
    print("🎯 VERIFICACIÓN DE CLASES:\n")
    
    try:
        from src.models import (
            Character, Player, Weapon, Armor, Item,
            EnemyBasic, EnemyChampion
        )
        
        print("   ✅ Character (clase base)")
        print("   ✅ Player (jugador)")
        print("   ✅ Weapon (armas)")
        print("   ✅ Armor (armaduras)")
        print("   ✅ Item (items)")
        print("   ✅ EnemyBasic (enemigo básico)")
        print("   ✅ EnemyChampion (enemigo campeón)")
        
        from src.enemies import (
            Murmillo, Retiarius, Secutor, Thraex, Hoplomachus
        )
        
        print("   ✅ Murmillo (tanque)")
        print("   ✅ Retiarius (rápido)")
        print("   ✅ Secutor (equilibrado)")
        print("   ✅ Thraex (agresivo)")
        print("   ✅ Hoplomachus (defensivo)")
        
        print("\n✅ Todas las clases existen!\n")
        return True
    
    except (ImportError, AttributeError) as e:
        print(f"\n❌ Error: {e}\n")
        return False


def verificar_funcionales():
    """Prueba funciones básicas."""
    
    print("⚙️  VERIFICACIÓN DE FUNCIONALIDAD:\n")
    
    try:
        from src.models import Player, Weapon
        from src.enemies import generar_enemigo
        from src.combat import calcular_daño
        
        # Test 1: Crear jugador
        print("   1. Creando jugador...", end=" ")
        jugador = Player()
        assert jugador.hp == 100
        print("✅")
        
        # Test 2: Crear arma
        print("   2. Creando arma...", end=" ")
        arma = Weapon("Espada", attack=20, speed=2)
        jugador.equipar_arma(arma)
        assert jugador.ataque_final() == 40  # 20 base + 20 arma
        print("✅")
        
        # Test 3: Generar enemigo
        print("   3. Generando enemigo...", end=" ")
        enemigo = generar_enemigo(nivel=1)
        assert enemigo.hp > 0
        print("✅")
        
        # Test 4: Calcular daño
        print("   4. Calculando daño...", end=" ")
        daño = calcular_daño(20, 5)
        assert daño >= 1
        print("✅")
        
        print("\n✅ Todas las funciones básicas funcionan!\n")
        return True
    
    except AssertionError as e:
        print(f"\n❌ Assertion falló: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        return False


def main():
    """Ejecuta todas las verificaciones."""
    
    ok1 = verificar_estructura()
    ok2 = verificar_imports()
    ok3 = verificar_clases()
    ok4 = verificar_funcionales()
    
    print("="*60)
    if ok1 and ok2 and ok3 and ok4:
        print("  ✅ ¡TODO OK! El proyecto está correctamente organizado")
        print("\n  Puedes ejecutar: python main.py")
    else:
        print("  ❌ Hay problemas. Verifica los errores arriba.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
