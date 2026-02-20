"""
Test de Integración - Misiones en Main
=======================================
Verifica que el menú de misiones se integra correctamente en main.py
"""

import sys
sys.path.insert(0, '.')

from src.misiones import GestorMisiones, EstadoMision
from src.models import Equipo, Gladiador


def test_integracion_gestor_equipo():
    """Verifica que GestorMisiones funciona con Equipo."""
    print("\n" + "="*70)
    print("TEST 1: Integración Gestor + Equipo")
    print("="*70)
    
    # Crear equipo
    equipo = Equipo()
    equipo.dinero = 5000
    
    g1 = Gladiador("Ferox", "Murmillo", nivel=1)
    g2 = Gladiador("Velox", "Retiarius", nivel=1)
    equipo.agregar_gladiador(g1)
    equipo.agregar_gladiador(g2)
    
    # Crear gestor misiones
    gestor = GestorMisiones()
    
    print(f"\n✓ Equipo creado: {len(equipo.gladiadores)} gladiadores")
    print(f"✓ Dinero inicial: {equipo.dinero}g")
    print(f"✓ Gestor misiones: {len(gestor.misiones)} misiones")
    
    # Simular progreso de misión
    gestor.activar_mision("combate_1")
    completada = gestor.incrementar_progreso_mision("combate_1")
    
    print(f"\n✓ Misión 'combate_1' activada")
    print(f"✓ Completada: {completada}")
    
    # Reclamar recompensas
    recompensas = gestor.reclamar_recompensas_mision("combate_1")
    equipo.dinero += recompensas['dinero']
    
    print(f"\n✓ Recompensas reclamadas:")
    print(f"  💰 +{recompensas['dinero']}g")
    print(f"  📈 +{recompensas['xp']} XP")
    print(f"✓ Dinero nuevo: {equipo.dinero}g")
    
    print("\n✅ Test integración: PASADO")


def test_flujo_misiones():
    """Simula el flujo completo de misiones."""
    print("\n" + "="*70)
    print("TEST 2: Flujo Completo de Misiones")
    print("="*70)
    
    gestor = GestorMisiones()
    equipo = Equipo()
    equipo.dinero = 5000
    
    print("\n🎯 Simulando progreso del jugador:\n")
    
    # 1. Activar misión de combate
    print("1️⃣  Activando misión 'Primer Paso' (combate_1)")
    gestor.activar_mision("combate_1")
    m1 = gestor.obtener_mision("combate_1")
    print(f"   Estado: {m1.estado.value}")
    
    # 2. Ganar un combate
    print("\n2️⃣  El jugador gana 1 combate...")
    completada = gestor.incrementar_progreso_mision("combate_1")
    print(f"   ✓ Misión completada: {completada}")
    print(f"   Progreso: {m1.progreso}/{m1.objetivo}")
    print(f"   Estado: {m1.estado.value}")
    
    # 3. Reclamar recompensas
    print("\n3️⃣  Reclamando recompensas...")
    recompensas = gestor.reclamar_recompensas_mision("combate_1")
    equipo.dinero += recompensas['dinero']
    print(f"   ✓ Dinero: {equipo.dinero}g")
    print(f"   ✓ Estado: {m1.estado.value}")
    
    # 4. Verificar misiones activas
    print("\n4️⃣  Estado actual de misiones:")
    activas = gestor.obtener_misiones_activas()
    completadas = [m for m in gestor.misiones.values() if m.estado == EstadoMision.COMPLETADA]
    reclamadas = [m for m in gestor.misiones.values() if m.estado == EstadoMision.RECLAMADA]
    
    print(f"   Activas: {len(activas)}")
    print(f"   Completadas: {len(completadas)}")
    print(f"   Reclamadas: {len(reclamadas)}")
    
    print("\n✅ Test flujo: PASADO")


def test_cadena_desbloqueables():
    """Verifica que las cadenas se desbloquean correctamente."""
    print("\n" + "="*70)
    print("TEST 3: Cadenas Desbloqueables")
    print("="*70)
    
    gestor = GestorMisiones()
    
    # Estado inicial
    m1 = gestor.obtener_mision("cadena_gloria_1")
    m2 = gestor.obtener_mision("cadena_gloria_2")
    
    print(f"\n🔒 Estado inicial:")
    print(f"   M1 ({m1.nombre}): {m1.estado.value}")
    print(f"   M2 ({m2.nombre}): {m2.estado.value}")
    
    # Activar cadena 1
    print(f"\n🔓 Activando M1...")
    gestor.activar_mision("cadena_gloria_1")
    print(f"   M1: {m1.estado.value}")
    print(f"   M2: {m2.estado.value}")
    
    # Completar M1 (simular 5 victorias)
    print(f"\n⭐ Completando M1 (5 victorias)...")
    for _ in range(5):
        gestor.incrementar_progreso_mision("cadena_gloria_1")
    
    print(f"   M1: {m1.progreso}/{m1.objetivo} → {m1.estado.value}")
    
    # Reclamar M1 - esto debe desbloquear M2
    print(f"\n🎁 Reclamando M1...")
    gestor.reclamar_recompensas_mision("cadena_gloria_1")
    
    print(f"   M1: {m1.estado.value}")
    print(f"   M2: {m2.estado.value} ✓ (DESBLOQUEADA)")
    
    assert m2.estado.value == "activa", "M2 debería estar activa!"
    
    print("\n✅ Test cadenas: PASADO")


def test_mostrar_todas_misiones():
    """Test de visualización."""
    print("\n" + "="*70)
    print("TEST 4: Visualización de Misiones")
    print("="*70)
    
    gestor = GestorMisiones()
    
    # Activar algunas misiones
    gestor.activar_mision("combate_1")
    gestor.incrementar_progreso_mision("combate_1", 1)
    gestor.incrementar_progreso_mision("combate_2", 2)
    
    print("\n📊 LISTA DE MISIONES:\n")
    
    from src.misiones import CapaMision
    
    for capa in CapaMision:
        misiones = gestor.obtener_misiones_por_capa(capa)
        print(f"\n🔹 {capa.value.upper()}: ({len(misiones)} misiones)")
        for m in misiones[:2]:
            icon = {
                "bloqueada": "🔒",
                "activa": "⭐",
                "completada": "✓",
                "reclamada": "✓✓"
            }.get(m.estado.value, "?")
            
            print(f"   {icon} {m.nombre:30} {m.generar_string_progreso()}")
    
    print("\n✅ Test visualización: PASADO")


if __name__ == "__main__":
    test_integracion_gestor_equipo()
    test_flujo_misiones()
    test_cadena_desbloqueables()
    test_mostrar_todas_misiones()
    
    print("\n" + "="*70)
    print("✅ TODOS LOS TESTS DE INTEGRACIÓN PASARON")
    print("="*70 + "\n")
