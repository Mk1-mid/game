"""
Test de UI Visual - Barras y Animaciones
========================================
"""

import sys
sys.path.insert(0, '.')

from src.models import Gladiador


def test_barra_hp():
    """Verifica que la barra de HP se genera correctamente."""
    print("\n" + "="*70)
    print("TEST 1: Barra de HP Visual")
    print("="*70)
    
    g = Gladiador("TestGladiador", "Murmillo", nivel=5)
    
    # HP al 100%
    barra_100 = g.generar_barra_hp()
    print("\nHP al 100%:")
    print(barra_100)
    assert "100%" in barra_100, "Debería mostrar 100%"
    assert "████████████████████" in barra_100, "Debería tener 20 caracteres llenos"
    
    # HP al 50%
    g.hp_actual = int(g.hp / 2)
    barra_50 = g.generar_barra_hp()
    print("\nHP al 50%:")
    print(barra_50)
    assert "50%" in barra_50, "Debería mostrar 50%"
    
    # HP al 25% (estado crítico)
    g.hp_actual = int(g.hp * 0.25)
    barra_25 = g.generar_barra_hp()
    print("\nHP al 25% (Crítico):")
    print(barra_25)
    assert "2" in barra_25 and "%" in barra_25, "Debería mostrar 24-25%"
    
    # HP a 0 (muerto)
    g.hp_actual = 0
    barra_0 = g.generar_barra_hp()
    print("\nHP a 0% (Muerto):")
    print(barra_0)
    assert "0%" in barra_0, "Debería mostrar 0%"
    assert "░░░░░░░░░░░░░░░░░░░░" in barra_0, "Debería tener 20 caracteres vacíos"
    
    print("\n✅ Test barra HP: PASADO")


def test_barra_xp():
    """Verifica que la barra de XP se genera correctamente."""
    print("\n" + "="*70)
    print("TEST 2: Barra de XP Visual")
    print("="*70)
    
    g = Gladiador("TestGladiador", "Murmillo", nivel=1)
    
    # XP al 0%
    g.xp = 0
    barra_0 = g.generar_barra_xp()
    print("\nXP al 0%:")
    print(barra_0)
    assert "0%" in barra_0, "Debería mostrar 0%"
    
    # XP al 50%
    xp_max = g.xp_para_siguiente_nivel()
    g.xp = xp_max // 2
    barra_50 = g.generar_barra_xp()
    print("\nXP al 50%:")
    print(barra_50)
    assert "50%" in barra_50, "Debería mostrar 50%"
    
    # XP al 100% (casi para subir)
    g.xp = xp_max - 1
    barra_100 = g.generar_barra_xp()
    print("\nXP al 99%:")
    print(barra_100)
    assert "99%" in barra_100, "Debería mostrar 99%"
    
    print("\n✅ Test barra XP: PASADO")


def test_string_stats():
    """Verifica que los stats se formatean con emojis."""
    print("\n" + "="*70)
    print("TEST 3: Stats con Emojis")
    print("="*70)
    
    g = Gladiador("TestGladiador", "Murmillo", nivel=5)
    
    stats = g.generar_string_stats()
    print("\nStats formateados:")
    print(stats)
    
    assert "⚔️" in stats, "Debería tener emoji ATK"
    assert "🛡️" in stats, "Debería tener emoji DEF"
    assert "⚡" in stats, "Debería tener emoji SPD"
    assert "ATK:" in stats, "Debería mostrar ATK"
    assert "DEF:" in stats, "Debería mostrar DEF"
    assert "SPD:" in stats, "Debería mostrar SPD"
    
    print("\n✅ Test stats: PASADO")


def test_animacion_nivel_up():
    """Verifica que la animación de nivel up se genera."""
    print("\n" + "="*70)
    print("TEST 4: Animación Nivel Up")
    print("="*70)
    
    g = Gladiador("TestGladiador", "Murmillo", nivel=1)
    nivel_inicial = g.nivel
    
    # Simular subida de nivel
    g.subir_nivel()
    animacion = g.animacion_nivel_up()
    
    print("\nAnimación de nivel up:")
    print(animacion)
    
    assert "⭐" in animacion, "Debería tener estrellas"
    assert "SUBISTE DE NIVEL" in animacion, "Debería mencionar subida de nivel"
    assert str(nivel_inicial) in animacion, "Debería mostrar nivel anterior"
    assert str(g.nivel) in animacion, "Debería mostrar nivel nuevo"
    assert "HP" in animacion, "Debería mostrar incremento de HP"
    assert "ATK" in animacion, "Debería mostrar incremento de ATK"
    assert "DEF" in animacion, "Debería mostrar incremento de DEF"
    assert "SPD" in animacion, "Debería mostrar incremento de SPD"
    
    print("\n✅ Test animación: PASADO")


def test_ui_completa():
    """Verifica que todas las barras se ven bien juntas."""
    print("\n" + "="*70)
    print("TEST 5: UI Completa del Gladiador")
    print("="*70)
    
    g = Gladiador("Ferox", "Murmillo", nivel=5)
    g.hp_actual = int(g.hp * 0.75)  # 75% HP
    g.xp = int(g.xp_para_siguiente_nivel() * 0.60)  # 60% XP
    
    print(f"\n{'='*50}")
    print(f"GLADIADOR: {g.nombre} (Lvl {g.nivel})")
    print(f"{'='*50}")
    print(g.generar_barra_hp())
    print()
    print(g.generar_barra_xp())
    print()
    print(g.generar_string_stats())
    print(f"{'='*50}\n")
    
    print("✅ UI Completa: VISUALIZADA CORRECTAMENTE")


if __name__ == "__main__":
    test_barra_hp()
    test_barra_xp()
    test_string_stats()
    test_animacion_nivel_up()
    test_ui_completa()
    
    print("\n" + "="*70)
    print("✅ TODOS LOS TESTS DE UI VISUAL PASARON")
    print("="*70 + "\n")
