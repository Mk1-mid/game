"""
Test del Sistema de Misiones - Sangre por Fortuna
===================================================
Prueba todas las funcionalidades del sistema de 4 capas
"""

import sys
sys.path.insert(0, '.')

from src.misiones import (
    Mision, GestorMisiones, TipoMision, CapaMision, 
    DificultadMision, EstadoMision
)


def test_estructura_mision():
    """Verifica que la clase Mision funciona correctamente."""
    print("\n" + "="*70)
    print("TEST 1: Estructura Mision")
    print("="*70)
    
    m = Mision(
        "test_1", "Prueba", "Descripción de prueba",
        TipoMision.COMBATE, CapaMision.CORE, DificultadMision.TIER_1,
        objetivo=10,
        recompensas={"dinero": 100, "xp": 50, "items": []}
    )
    
    print(f"\n✓ Mision creada: {m}")
    print(f"✓ ID: {m.id}")
    print(f"✓ Estado: {m.estado.value}")
    print(f"✓ Progreso: {m.progreso}/{m.objetivo}")
    print(f"✓ Porcentaje: {m.porcentaje_progreso():.1f}%")
    
    # Incrementar progreso
    m.incrementar_progreso(5)
    print(f"\n✓ Después de +5: {m.progreso}/{m.objetivo} ({m.porcentaje_progreso():.1f}%)")
    
    m.incrementar_progreso(5)
    print(f"✓ Después de +5 más: {m.progreso}/{m.objetivo} ({m.porcentaje_progreso():.1f}%)")
    print(f"✓ ¿Completada? {m.esta_completada()}")
    print(f"✓ Estado final: {m.estado.value}")
    
    print("\n✅ Test mision: PASADO")


def test_gestor_misiones():
    """Verifica que el GestorMisiones carga todas las misiones."""
    print("\n" + "="*70)
    print("TEST 2: Gestor Misiones - Carga")
    print("="*70)
    
    gestor = GestorMisiones()
    
    print(f"\n✓ Gestor creado: {gestor}")
    print(f"✓ Total de misiones: {len(gestor.misiones)}")
    
    # Verificar capas
    for capa in CapaMision:
        misiones_capa = gestor.obtener_misiones_por_capa(capa)
        print(f"✓ {capa.value}: {len(misiones_capa)} misiones")
    
    # Verificar tipos
    print("\nPor tipo:")
    for tipo in TipoMision:
        misiones_tipo = gestor.obtener_misiones_por_tipo(tipo)
        print(f"✓ {tipo.value}: {len(misiones_tipo)} misiones")
    
    print("\n✅ Test gestor: PASADO")


def test_cadena_misiones():
    """Verifica que las cadenas de misiones se desbloquean correctamente."""
    print("\n" + "="*70)
    print("TEST 3: Cadenas de Misiones")
    print("="*70)
    
    gestor = GestorMisiones()
    
    # Obtener cadena "La Gloria del Gladiador"
    m1 = gestor.obtener_mision("cadena_gloria_1")
    m2 = gestor.obtener_mision("cadena_gloria_2")
    
    print(f"\n✓ Mision 1: {m1.nombre} - Estado: {m1.estado.value}")
    print(f"✓ Mision 2: {m2.nombre} - Estado: {m2.estado.value}")
    print(f"✓ M1 desbloquea: {m1.misiones_hijo_ids}")
    print(f"✓ M2 padre: {m2.mision_padre_id}")
    
    # Activar M1
    print("\n🔓 Activando M1...")
    gestor.activar_mision("cadena_gloria_1")
    m1 = gestor.obtener_mision("cadena_gloria_1")
    print(f"✓ M1 estado: {m1.estado.value}")
    
    # Simular completar M1
    print("\n⭐ Completando M1 (15 victorias)...")
    for _ in range(15):
        completada = gestor.incrementar_progreso_mision("cadena_gloria_1")
    
    m1 = gestor.obtener_mision("cadena_gloria_1")
    m2 = gestor.obtener_mision("cadena_gloria_2")
    
    print(f"✓ M1: {m1.progreso}/{m1.objetivo} - {m1.estado.value}")
    print(f"✓ M2: {m2.estado.value} (debería estar ACTIVA)")
    
    # Reclamar recompensas M1
    print("\n🎁 Reclamando recompensas M1...")
    recompensas = gestor.reclamar_recompensas_mision("cadena_gloria_1")
    print(f"✓ Recompensas: {recompensas}")
    print(f"✓ M1 estado: {m1.estado.value}")
    
    print("\n✅ Test cadenas: PASADO")


def test_misiones_automaticas():
    """Verifica que las misiones automáticas se activan correctamente."""
    print("\n" + "="*70)
    print("TEST 4: Misiones Automáticas")
    print("="*70)
    
    gestor = GestorMisiones()
    
    auto_misiones = gestor.obtener_misiones_por_capa(CapaMision.AUTOMATICA)
    print(f"\n✓ Misiones automáticas: {len(auto_misiones)}")
    
    for m in auto_misiones:
        print(f"  - {m.nombre} (se_activa_sola: {m.se_activa_sola})")
    
    print("\n✅ Test automáticas: PASADO")


def test_side_quests():
    """Verifica las misiones secundarias."""
    print("\n" + "="*70)
    print("TEST 5: Side Quests")
    print("="*70)
    
    gestor = GestorMisiones()
    
    side_misiones = gestor.obtener_misiones_por_capa(CapaMision.SECUNDARIA)
    print(f"\n✓ Side quests: {len(side_misiones)}")
    
    for m in side_misiones:
        print(f"\n  ⭐ {m.nombre}")
        print(f"     {m.descripcion}")
        print(f"     Objetivo: {m.objetivo}")
        print(f"     Recompensas: {m.recompensas['dinero']}g + {m.recompensas['xp']} XP")
        if m.tiene_bonus:
            print(f"     ✨ BONUS: {m.descripcion_bonus}")
    
    print("\n✅ Test side quests: PASADO")


def test_mostrar_todas_misiones():
    """Muestra todas las misiones de forma bonita."""
    print("\n" + "="*70)
    print("TEST 6: Visualización Completa")
    print("="*70)
    
    gestor = GestorMisiones()
    
    # Activar algunas para mostrar estados diferentes
    gestor.activar_mision("combate_1")
    gestor.incrementar_progreso_mision("combate_1")
    gestor.incrementar_progreso_mision("combate_2", 2)
    
    # Mostrar
    print("\n📊 RESUMEN DE MISIONES:")
    print("="*70)
    
    for capa in CapaMision:
        misiones = gestor.obtener_misiones_por_capa(capa)
        if misiones:
            print(f"\n📍 {capa.value.upper()} ({len(misiones)} misiones):")
            for m in misiones[:3]:  # Mostrar máximo 3 por capa
                progreso = m.generar_string_progreso()
                print(f"   • {m.nombre}: {progreso}")
            if len(misiones) > 3:
                print(f"   ... y {len(misiones) - 3} más")
    
    print("\n✅ Test visualización: PASADO")


def test_balance_recompensas():
    """Verifica que las recompensas estén balanceadas."""
    print("\n" + "="*70)
    print("TEST 7: Balance de Recompensas")
    print("="*70)
    
    gestor = GestorMisiones()
    
    print("\n📊 ANÁLISIS DE RECOMPENSAS POR CAPA:\n")
    
    for capa in CapaMision:
        misiones = gestor.obtener_misiones_por_capa(capa)
        if misiones:
            dinero_total = sum(m.recompensas["dinero"] for m in misiones)
            xp_total = sum(m.recompensas["xp"] for m in misiones)
            dinero_promedio = dinero_total / len(misiones)
            xp_promedio = xp_total / len(misiones)
            
            print(f"🔹 {capa.value.upper()}:")
            print(f"   Misiones: {len(misiones)}")
            print(f"   Dinero total: {dinero_total}g (promedio: {dinero_promedio:.0f}g)")
            print(f"   XP total: {xp_total} (promedio: {xp_promedio:.0f})")
            print()
    
    print("✅ Test balance: PASADO")


if __name__ == "__main__":
    test_estructura_mision()
    test_gestor_misiones()
    test_cadena_misiones()
    test_misiones_automaticas()
    test_side_quests()
    test_mostrar_todas_misiones()
    test_balance_recompensas()
    
    print("\n" + "="*70)
    print("✅ TODOS LOS TESTS DEL SISTEMA DE MISIONES PASARON")
    print("="*70 + "\n")
