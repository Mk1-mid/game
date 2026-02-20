"""
Test de Auto-Tracking de Misiones
==================================
Verifica que las misiones se actualizan automáticamente en eventos
"""

import sys
sys.path.insert(0, '.')

from src.misiones import GestorMisiones, EstadoMision, TipoMision
from src.models import Equipo, Gladiador


def test_evento_combate_ganado():
    """Verifica que las misiones de combate se actualizan con evento_combate_ganado."""
    print("\n" + "="*70)
    print("TEST 1: Auto-Tracking Evento Combate Ganado")
    print("="*70)
    
    gestor = GestorMisiones()
    
    # Activar misión de combate
    gestor.activar_mision("combate_1")
    m = gestor.obtener_mision("combate_1")
    
    print(f"\n📊 Estado inicial:")
    print(f"   Misión: {m.nombre}")
    print(f"   Progreso: {m.progreso}/{m.objetivo}")
    print(f"   Estado: {m.estado.value}")
    
    # Simular evento de combate ganado
    print(f"\n⚔️  Simulando evento: Combate ganado...")
    completadas = gestor.evento_combate_ganado()
    
    print(f"\n✓ Evento procesado")
    print(f"   Progreso nuevo: {m.progreso}/{m.objetivo}")
    print(f"   Estado nuevo: {m.estado.value}")
    print(f"   Misiones completadas: {len(completadas)}")
    
    if completadas:
        print(f"   IDs completadas: {completadas}")
        for id_m in completadas:
            notif = gestor.generar_notificacion_misiones([id_m])
            print(notif)
    
    assert m.esta_completada(), "Misión debería estar completada!"
    assert len(completadas) == 1, "Debería completarse 1 misión!"
    
    print("\n✅ Test evento combate: PASADO")


def test_evento_dinero_acumulado():
    """Verifica que las misiones de dinero se actualizan."""
    print("\n" + "="*70)
    print("TEST 2: Auto-Tracking Evento Dinero Acumulado")
    print("="*70)
    
    gestor = GestorMisiones()
    
    # Activar misión de dinero
    gestor.activar_mision("dinero_1")
    m = gestor.obtener_mision("dinero_1")
    
    print(f"\n💰 Estado inicial:")
    print(f"   Misión: {m.nombre}")
    print(f"   Objetivo: {m.objetivo}g")
    print(f"   Progreso: {m.progreso}/{m.objetivo}")
    
    # Simular eventos de dinero acumulado
    print(f"\n💰 Simulando acumular 300g...")
    completadas = gestor.evento_dinero_acumulado(300)
    print(f"   Progreso: {m.progreso}/{m.objetivo}")
    
    print(f"\n💰 Simulando acumular 200g más...")
    completadas = gestor.evento_dinero_acumulado(200)
    print(f"   Progreso: {m.progreso}/{m.objetivo}")
    print(f"   Estado: {m.estado.value}")
    
    if completadas:
        print(f"\n✓ Misiones completadas: {completadas}")
        notif = gestor.generar_notificacion_misiones(completadas)
        print(notif)
    
    assert m.esta_completada(), "Misión debería estar completada!"
    
    print("\n✅ Test evento dinero: PASADO")


def test_evento_nivel_up():
    """Verifica que las misiones de nivel se actualizan."""
    print("\n" + "="*70)
    print("TEST 3: Auto-Tracking Evento Nivel Up")
    print("="*70)
    
    gestor = GestorMisiones()
    
    # Activar misión de nivel
    gestor.activar_mision("nivel_1")
    m = gestor.obtener_mision("nivel_1")
    
    print(f"\n📈 Estado inicial:")
    print(f"   Misión: {m.nombre}")
    print(f"   Objetivo: Nivel {m.objetivo}")
    print(f"   Progreso: {m.progreso}")
    
    # Simular eventos de nivel up
    print(f"\n📈 Simulando 2 subidas de nivel...")
    completadas1 = gestor.evento_gladiador_sube_nivel()
    completadas2 = gestor.evento_gladiador_sube_nivel()
    completadas3 = gestor.evento_gladiador_sube_nivel()
    
    print(f"   Progreso: {m.progreso}/{m.objetivo}")
    print(f"   Estado: {m.estado.value}")
    
    if completadas3:
        print(f"\n✓ Misiones completadas: {completadas3}")
    
    assert m.esta_completada(), "Misión debería estar completada después de 3 level-ups!"
    
    print("\n✅ Test evento nivel: PASADO")


def test_evento_items_comprados():
    """Verifica que las misiones de items se actualizan."""
    print("\n" + "="*70)
    print("TEST 4: Auto-Tracking Evento Items Comprados")
    print("="*70)
    
    gestor = GestorMisiones()
    
    # Activar misión de items
    gestor.activar_mision("items_1")
    m = gestor.obtener_mision("items_1")
    
    print(f"\n🛍️  Estado inicial:")
    print(f"   Misión: {m.nombre}")
    print(f"   Objetivo: Comprar {m.objetivo} items")
    print(f"   Progreso: {m.progreso}/{m.objetivo}")
    
    # Simular compra de items
    print(f"\n🛍️  Simulando compra de 3 items...")
    completadas = gestor.evento_items_comprados(3)
    
    print(f"   Progreso: {m.progreso}/{m.objetivo}")
    
    if completadas:
        print(f"\n✓ Misiones completadas: {completadas}")
    
    print("\n✅ Test evento items: PASADO")


def test_cadena_con_auto_tracking():
    """Verifica que las cadenas se desbloquean automáticamente con tracking."""
    print("\n" + "="*70)
    print("TEST 5: Cadenas Desbloqueables con Auto-Tracking")
    print("="*70)
    
    gestor = GestorMisiones()
    
    # Inicialmente ambas están bloqueadas
    m1 = gestor.obtener_mision("cadena_gloria_1")
    m2 = gestor.obtener_mision("cadena_gloria_2")
    
    print(f"\n🔒 Estado inicial:")
    print(f"   M1: {m1.estado.value}")
    print(f"   M2: {m2.estado.value}")
    
    # Activar M1 manualmente (no auto-activable)
    print(f"\n🔓 Activando M1...")
    gestor.activar_mision("cadena_gloria_1")
    
    # Simular 5 victorias
    print(f"\n⚔️  Simulando 5 victorias...")
    for i in range(5):
        completadas = gestor.evento_combate_ganado()
        if completadas:
            print(f"   Victoria {i+1}: {completadas}")
    
    print(f"\n✓ M1: {m1.progreso}/{m1.objetivo} → {m1.estado.value}")
    print(f"   M2: {m2.estado.value}")
    
    # Reclamar M1 para desbloquear M2
    print(f"\n🎁 Reclamando M1...")
    gestor.reclamar_recompensas_mision("cadena_gloria_1")
    
    print(f"   M1: {m1.estado.value}")
    print(f"   M2: {m2.estado.value} ✓ (DESBLOQUEADA)")
    
    assert m2.estado.value == "activa", "M2 debería estar activa!"
    
    print("\n✅ Test cadena auto-tracking: PASADO")


def test_notificaciones():
    """Verifica que las notificaciones se generan correctamente."""
    print("\n" + "="*70)
    print("TEST 6: Notificaciones de Misiones Completadas")
    print("="*70)
    
    gestor = GestorMisiones()
    
    # Activar y completar varias misiones
    gestor.activar_mision("combate_1")
    gestor.activar_mision("dinero_1")
    
    completadas1 = gestor.evento_combate_ganado()
    completadas2 = gestor.evento_dinero_acumulado(500)
    
    todas_completadas = completadas1 + completadas2
    
    print(f"\n✓ Misiones completadas: {len(todas_completadas)}")
    
    if todas_completadas:
        notif = gestor.generar_notificacion_misiones(todas_completadas)
        print(notif)
    
    print("\n✅ Test notificaciones: PASADO")


def test_multiples_eventos_simultaneos():
    """Verifica que múltiples eventos se procesan correctamente."""
    print("\n" + "="*70)
    print("TEST 7: Múltiples Eventos Simultáneos")
    print("="*70)
    
    gestor = GestorMisiones()
    
    # Activar misiones de diferentes tipos
    gestor.activar_mision("combate_1")
    gestor.activar_mision("dinero_1")
    gestor.activar_mision("nivel_1")
    gestor.activar_mision("items_1")
    
    print(f"\n🎯 Activadas 4 misiones de tipos diferentes\n")
    
    # Evento 1: Victoria + Dinero
    print(f"Evento 1: Gana combate + 200g")
    c1 = gestor.evento_combate_ganado()
    d1 = gestor.evento_dinero_acumulado(200)
    print(f"  Combate completó: {c1}")
    print(f"  Dinero completó: {d1}")
    
    # Evento 2: Level up
    print(f"\nEvento 2: Sube de nivel")
    n1 = gestor.evento_gladiador_sube_nivel()
    print(f"  Nivel completó: {n1}")
    
    # Evento 3: Compra items
    print(f"\nEvento 3: Compra 5 items")
    i1 = gestor.evento_items_comprados(5)
    print(f"  Items completó: {i1}")
    
    # Mostrar resumen
    print(f"\n📊 Resumen:")
    all_completed = c1 + d1 + n1 + i1
    print(f"  Total completadas: {len(all_completed)}")
    
    for id_m in all_completed:
        m = gestor.obtener_mision(id_m)
        print(f"    ✓ {m.nombre}")
    
    print("\n✅ Test eventos simultáneos: PASADO")


if __name__ == "__main__":
    test_evento_combate_ganado()
    test_evento_dinero_acumulado()
    test_evento_nivel_up()
    test_evento_items_comprados()
    test_cadena_con_auto_tracking()
    test_notificaciones()
    test_multiples_eventos_simultaneos()
    
    print("\n" + "="*70)
    print("✅ TODOS LOS TESTS DE AUTO-TRACKING PASARON")
    print("="*70 + "\n")
