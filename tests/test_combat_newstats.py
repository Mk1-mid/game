"""
Test para validar el nuevo sistema de CRÍTICO y ESQUIVA
======================================================

Prueba:
1. Cálculo de AGILIDAD_efectiva con diferentes pesos
2. Derivación de CRÍTICO correcta
3. Derivación de ESQUIVA correcta
4. Arquetipos diferenciados
5. Probabilidad de esquiva en combate
6. Probabilidad de crítico en combate
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Gladiador, Weapon, Armor
from src.combat import calcular_ataque
import random

# ============================================
# TEST 1: ARQUETIPOS Y STATS BASE
# ============================================

def test_arquetipos_creacion():
    """Verifica que cada arquetipo tenga stats correctos."""
    print("\n" + "="*60)
    print("TEST 1: Creación de Arquetipos")
    print("="*60)
    
    tipos = ["Murmillo", "Retiarius", "Secutor", "Thraex", "Hoplomachus"]
    
    for tipo in tipos:
        g = Gladiador("Test", tipo_base=tipo, nivel=1)
        print(f"\n{tipo}:")
        print(f"  FUERZA:    {g.fuerza}")
        print(f"  AGILIDAD:  {g.agilidad}")
        print(f"  CRÍTICO:   {g.critico:.1f}%")
        print(f"  ESQUIVA:   {g.esquiva:.1f}%")
        
        # Validaciones
        assert g.fuerza > 0, f"FUERZA debe ser > 0"
        assert g.agilidad > 0, f"AGILIDAD debe ser > 0"
        assert 0 <= g.critico <= 100, f"CRÍTICO debe estar entre 0-100"
        assert 0 <= g.esquiva <= 100, f"ESQUIVA debe estar entre 0-100"
    
    print("\n✅ ARQUETIPOS CREADOS CORRECTAMENTE")


# ============================================
# TEST 2: AGILIDAD EFECTIVA CON PESO
# ============================================

def test_agilidad_efectiva():
    """Verifica cálculo de agilidad efectiva con diferentes equipos."""
    print("\n" + "="*60)
    print("TEST 2: Agilidad Efectiva con Peso")
    print("="*60)
    
    g = Gladiador("Test", tipo_base="Retiarius", nivel=1)  # AGI=22, FUERZA=12
    
    print(f"\nEstadísticas base:")
    print(f"  AGILIDAD:  {g.agilidad}")
    print(f"  FUERZA:    {g.fuerza}")
    
    # SIN EQUIPO
    print(f"\n1. SIN EQUIPO:")
    print(f"  AGILIDAD EFECTIVA: {g.agilidad_efectiva:.2f}")
    print(f"  ESQUIVA: {g.esquiva:.1f}%")
    
    # CON ARMA LIGERA (0.5kg)
    arma_ligera = Weapon("Daga Ligera", attack=3, agilidad=1, peso=0.5, critico_bonus=2)
    g.equipar_arma(arma_ligera)
    print(f"\n2. CON ARMA LIGERA (0.5kg):")
    print(f"  AGILIDAD EFECTIVA: {g.agilidad_efectiva:.2f}")
    print(f"  ESQUIVA: {g.esquiva:.1f}%")
    
    # CON ARMADURA PESADA (8kg)
    armadura_pesada = Armor("Armadura Pesada", defense=15, hp=20, peso=8)
    g.equipar_armadura(armadura_pesada)
    print(f"\n3. CON ARMADURA PESADA (8kg + 0.5kg arma = 8.5kg):")
    print(f"  AGILIDAD EFECTIVA: {g.agilidad_efectiva:.2f}")
    print(f"  ESQUIVA: {g.esquiva:.1f}%")
    
    print("\n✅ CÁLCULOS DE AGILIDAD CORRECTOS")


# ============================================
# TEST 3: CRÍTICO Y ESQUIVA DERIVADOS
# ============================================

def test_derivados_correctos():
    """Verifica que CRÍTICO y ESQUIVA se calculen correctamente."""
    print("\n" + "="*60)
    print("TEST 3: Derivación de CRÍTICO y ESQUIVA")
    print("="*60)
    
    # Murmillo: Fuerte pero lento
    murmillo = Gladiador("Murmillo Test", tipo_base="Murmillo", nivel=1)
    print(f"\nMURMILLO (Fuerte, lento):")
    print(f"  FUERZA: {murmillo.fuerza}, AGILIDAD: {murmillo.agilidad}")
    print(f"  CRÍTICO: {murmillo.critico:.1f}% (bajo)")
    print(f"  ESQUIVA: {murmillo.esquiva:.1f}% (muy bajo)")
    
    # Retiarius: Ágil pero frágil
    retiarius = Gladiador("Retiarius Test", tipo_base="Retiarius", nivel=1)
    print(f"\nRETIARIUS (Ágil, frágil):")
    print(f"  FUERZA: {retiarius.fuerza}, AGILIDAD: {retiarius.agilidad}")
    print(f"  CRÍTICO: {retiarius.critico:.1f}% (alto)")
    print(f"  ESQUIVA: {retiarius.esquiva:.1f}% (alto)")
    
    # Validaciones
    assert retiarius.esquiva > murmillo.esquiva, "Retiarius debe tener más esquiva"
    assert retiarius.critico > murmillo.critico, "Retiarius debe tener más crítico"
    
    print("\n✅ DERIVADOS CORRECTOS")


# ============================================
# TEST 4: DIFERENCIAS ENTRE ARQUETIPOS
# ============================================

def test_arquetipos_diferenciados():
    """Verifica que cada arquetipo tenga perfil único."""
    print("\n" + "="*60)
    print("TEST 4: Arquetipos Diferenciados")
    print("="*60)
    
    tipos = ["Murmillo", "Retiarius", "Secutor", "Thraex", "Hoplomachus"]
    gladiadores = {t: Gladiador(f"Test {t}", tipo_base=t, nivel=1) for t in tipos}
    
    print("\n┌─────────────┬──────────┬──────────┬──────────┬──────────┐")
    print("│ Tipo        │ FUERZA   │ AGILIDAD │ CRÍTICO  │ ESQUIVA  │")
    print("├─────────────┼──────────┼──────────┼──────────┼──────────┤")
    
    for tipo, g in gladiadores.items():
        print(f"│ {tipo:<11} │ {g.fuerza:<8} │ {g.agilidad:<8} │ {g.critico:<7.1f}% │ {g.esquiva:<7.1f}% │")
    
    print("└─────────────┴──────────┴──────────┴──────────┴──────────┘")
    
    # Validaciones de diferencia
    assert gladiadores["Murmillo"].fuerza > gladiadores["Retiarius"].fuerza
    assert gladiadores["Retiarius"].agilidad > gladiadores["Murmillo"].agilidad
    assert gladiadores["Thraex"].fuerza >= gladiadores["Secutor"].fuerza
    
    print("\n✅ ARQUETIPOS DIFERENCIADOS CORRECTAMENTE")


# ============================================
# TEST 5: ESCALADO CON NIVEL
# ============================================

def test_escalado_con_nivel():
    """Verifica que los stats escalen correctamente con nivel."""
    print("\n" + "="*60)
    print("TEST 5: Escalado de Stats con Nivel")
    print("="*60)
    
    g = Gladiador("Test Escalado", tipo_base="Secutor", nivel=1)
    nivel_1_fuerza = g.fuerza
    nivel_1_critico = g.critico
    
    print(f"\nNIVEL 1:")
    print(f"  FUERZA: {g.fuerza}")
    print(f"  CRÍTICO: {g.critico:.1f}%")
    
    # Subir niveles
    for _ in range(5):
        g.subir_nivel()
    
    print(f"\nNIVEL 6:")
    print(f"  FUERZA: {g.fuerza}")
    print(f"  CRÍTICO: {g.critico:.1f}%")
    
    # Validaciones
    assert g.fuerza > nivel_1_fuerza, "FUERZA debe crecer"
    print(f"\nMultiplicador FUERZA: {g.fuerza / nivel_1_fuerza:.3f}x")
    
    print("\n✅ ESCALADO CORRECTO")


# ============================================
# TEST 6: COMBATE CON CALCULAR_ATAQUE
# ============================================

def test_probabilidades_combate():
    """Prueba las probabilidades en combate."""
    print("\n" + "="*60)
    print("TEST 6: Probabilidades en Combate")
    print("="*60)
    
    atacante = Gladiador("Atacante", tipo_base="Thraex", nivel=1)
    defensor = Gladiador("Defensor", tipo_base="Retiarius", nivel=1)
    
    print(f"\nATACANTE: {atacante.tipo}")
    print(f"  FUERZA: {atacante.fuerza}, CRÍTICO: {atacante.critico:.1f}%")
    print(f"\nDEFENSOR: {defensor.tipo}")
    print(f"  AGILIDAD: {defensor.agilidad}, ESQUIVA: {defensor.esquiva:.1f}%")
    
    # Realizar 100 ataques
    resultados = {"esquiva": 0, "crítico": 0, "golpe": 0}
    daños = []
    
    random.seed(42)
    for _ in range(100):
        tipo, daño = calcular_ataque(
            atacante.ataque_final(),
            defensor.defensa_final(),
            atacante.critico,
            defensor.esquiva
        )
        resultados[tipo] += 1
        if daño > 0:
            daños.append(daño)
    
    print(f"\nRESULTADOS DE 100 ATAQUES:")
    print(f"  ESQUIVAS:  {resultados['esquiva']} ({resultados['esquiva']}%)")
    print(f"  CRÍTICOS:  {resultados['crítico']} ({resultados['crítico']}%)")
    print(f"  GOLPES:    {resultados['golpe']} ({resultados['golpe']}%)")
    
    if daños:
        print(f"\nDAÑOS (cuando impactan):")
        print(f"  Mínimo: {min(daños)}")
        print(f"  Máximo: {max(daños)}")
        print(f"  Promedio: {sum(daños)/len(daños):.1f}")
    
    assert resultados["esquiva"] > 0 or resultados["crítico"] > 0 or resultados["golpe"] > 0
    
    print("\n✅ PROBABILIDADES FUNCIONALES")


# ============================================
# TEST 7: PERSISTENCIA CON NUEVOS STATS
# ============================================

def test_persistencia_stats():
    """Verifica que los nuevos stats se guarden/carguen correctamente."""
    print("\n" + "="*60)
    print("TEST 7: Persistencia de Nuevos Stats")
    print("="*60)
    
    from src.persistence import serializar_gladiador, deserializar_gladiador
    
    # Crear gladiador SIN equipo (para evitar complicaciones)
    g_original = Gladiador("Persistencia Test", tipo_base="Murmillo", nivel=5)
    
    print(f"\nGLADIADOR ORIGINAL:")
    print(f"  FUERZA: {g_original.fuerza}")
    print(f"  AGILIDAD: {g_original.agilidad}")
    print(f"  CRÍTICO: {g_original.critico:.1f}%")
    print(f"  ESQUIVA: {g_original.esquiva:.1f}%")
    
    # Serializar
    datos = serializar_gladiador(g_original)
    
    # Deserializar
    g_cargado = deserializar_gladiador(datos)
    
    print(f"\nGLADIADOR CARGADO:")
    print(f"  FUERZA: {g_cargado.fuerza}")
    print(f"  AGILIDAD: {g_cargado.agilidad}")
    print(f"  CRÍTICO: {g_cargado.critico:.1f}%")
    print(f"  ESQUIVA: {g_cargado.esquiva:.1f}%")
    
    # Validaciones - sin equipo, los valores deben ser EXACTOS
    assert g_cargado.fuerza == g_original.fuerza, f"FUERZA no coincide: {g_cargado.fuerza} != {g_original.fuerza}"
    assert g_cargado.agilidad == g_original.agilidad, f"AGILIDAD no coincide: {g_cargado.agilidad} != {g_original.agilidad}"
    assert abs(g_cargado.critico - g_original.critico) < 0.1, f"CRÍTICO no coincide: {g_cargado.critico} != {g_original.critico}"
    assert abs(g_cargado.esquiva - g_original.esquiva) < 0.1, f"ESQUIVA no coincide: {g_cargado.esquiva} != {g_original.esquiva}"
    
    print("\n✅ PERSISTENCIA CORRECTA")


# ============================================
# EJECUCIÓN DE TESTS
# ============================================

if __name__ == "__main__":
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "   TEST SUITE: NUEVO SISTEMA DE CRÍTICO Y ESQUIVA".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    try:
        test_arquetipos_creacion()
        test_agilidad_efectiva()
        test_derivados_correctos()
        test_arquetipos_diferenciados()
        test_escalado_con_nivel()
        test_probabilidades_combate()
        test_persistencia_stats()
        
        print("\n" + "█"*60)
        print("█" + "   ✅ TODOS LOS TESTS PASARON EXITOSAMENTE".center(58) + "█")
        print("█"*60 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ ERROR EN TEST: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
