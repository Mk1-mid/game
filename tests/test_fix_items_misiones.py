#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para verificar que el auto-tracking de items en misiones funciona correctamente.
Fase 2.1 - Fix final
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.misiones import GestorMisiones, TipoMision, EstadoMision
from src.store import menu_armeria, comprar_item

def test_evento_items_comprados():
    """Test que evento_items_comprados() trackea correctamente."""
    gestor = GestorMisiones()
    
    # Verificar que la misión de items existe
    m = gestor.obtener_mision("items_1")
    assert m is not None, "Misión items_1 no existe"
    assert m.tipo == TipoMision.ITEMS, "Misión items_1 no es de tipo ITEMS"
    
    # Activar misión
    success = gestor.activar_mision("items_1")
    assert success, "No se pudo activar misión items_1"
    assert m.estado == EstadoMision.ACTIVA, "Misión items_1 no está activa"
    
    print("✓ Misión items_1 activada correctamente")
    

def test_trackeo_items_en_gesto():
    """Test que evento_items_comprados incrementa progreso."""
    gestor = GestorMisiones()
    
    # Activar misión de items
    gestor.activar_mision("items_1")  # Objetivo: Compra 5 items
    m = gestor.obtener_mision("items_1")
    
    # Simular 2 compras
    completadas = gestor.evento_items_comprados(2)
    
    assert m.progreso == 2, f"Progreso esperado 2, obtuvo {m.progreso}"
    assert m.estado == EstadoMision.ACTIVA, "Misión debería seguir activa"
    
    print(f"✓ Progreso actualizado: {m.progreso}/{m.objetivo}")
    
    # Simular 3 compras más (del mismo evento)
    completadas = gestor.evento_items_comprados(3)
    
    assert m.progreso == 5, f"Progreso esperado 5, obtuvo {m.progreso}"
    assert m.estado == EstadoMision.COMPLETADA, "Misión debería estar completada"
    assert "items_1" in completadas, "Misión items_1 debería estar en lista de completadas"
    
    print(f"✓ Misión completada: {m.progreso}/{m.objetivo}")


def test_notificacion_items():
    """Test que la notificación se genera correctamente."""
    gestor = GestorMisiones()
    
    # Activar y completar misión
    gestor.activar_mision("items_1")
    m = gestor.obtener_mision("items_1")
    
    # Completar misión
    for _ in range(5):
        completadas = gestor.evento_items_comprados(1)
    
    # Generar notificación
    notif = gestor.generar_notificacion_misiones(["items_1"])
    
    assert notif != "", "Notificación vacía"
    assert "items_1" in notif or "Equipero" in notif, "Notificación no contiene info de misión"
    assert "dinero" in notif.lower() or "xp" in notif.lower(), "Notificación no muestra recompensas"
    
    print("✓ Notificación generada correctamente")
    print("\nEjemplo de notificación:")
    print(notif)


def test_multiple_misiones_items():
    """Test que múltiples misiones de items se completan."""
    gestor = GestorMisiones()
    
    # Activar ambas misiones de items
    gestor.activar_mision("items_1")  # Compra 5 items
    gestor.activar_mision("items_2")  # Compra 10 items diferentes
    
    m1 = gestor.obtener_mision("items_1")
    m2 = gestor.obtener_mision("items_2")
    
    # Simular 5 compras
    completadas = gestor.evento_items_comprados(5)
    
    assert m1.estado == EstadoMision.COMPLETADA, "Misión items_1 debería estar completada"
    assert m2.progreso == 5, "Misión items_2 debería tener 5 de progreso"
    assert "items_1" in completadas, "items_1 debería estar en completadas"
    
    print("✓ Primera misión completada después de 5 compras")
    print(f"✓ Segunda misión en progreso: {m2.progreso}/{m2.objetivo}")
    
    # Simular 5 compras más
    completadas = gestor.evento_items_comprados(5)
    
    assert m2.estado == EstadoMision.COMPLETADA, "Misión items_2 debería estar completada"
    assert "items_2" in completadas, "items_2 debería estar en completadas"
    
    print(f"✓ Segunda misión completada: {m2.progreso}/{m2.objetivo}")


if __name__ == "__main__":
    print("=" * 70)
    print("🧪 TESTS - SISTEMA DE MISIONES DE ITEMS (FIX FINAL FASE 2.1)")
    print("=" * 70 + "\n")
    
    try:
        print("1. Test: evento_items_comprados existe y es accesible...")
        test_evento_items_comprados()
        
        print("\n2. Test: evento_items_comprados incrementa progreso...")
        test_trackeo_items_en_gesto()
        
        print("\n3. Test: Notificación se genera correctamente...")
        test_notificacion_items()
        
        print("\n4. Test: Múltiples misiones de items funcionan...")
        test_multiple_misiones_items()
        
        print("\n" + "=" * 70)
        print("✅ TODOS LOS TESTS PASARON - FASE 2.1 COMPLETADA AL 100%")
        print("=" * 70)
        
    except AssertionError as e:
        print(f"\n❌ TEST FALLÓ: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
