"""
Tests para Notificaciones Mejoradas y Persistencia de Misiones
==============================================================
Valida que:
1. Las notificaciones se generan correctamente con totales
2. La persistencia guarda y carga estado correctamente
3. Las misiones se restauran en sesión posterior
"""

import sys
import os
import json
import tempfile

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.misiones import GestorMisiones, EstadoMision, TipoMision
from src.models import Equipo, Gladiador


def test_notificaciones_mejoradas():
    """Test que las notificaciones muestren totales y detalles."""
    print("\n" + "="*70)
    print("TEST 1: Notificaciones Mejoradas con Totales")
    print("="*70)
    
    gestor = GestorMisiones()
    
    # Simular completar misiones
    gestor.activar_mision("combate_1")
    gestor.evento_combate_ganado()  # Completa combate_1
    
    misiones_completadas = gestor.evento_combate_ganado()  # Completa combate_1 nuevamente (ya está completada, no hace nada)
    
    # Completar manualmente para test
    m1 = gestor.obtener_mision("combate_1")
    m1.progreso = 1
    m1.estado = EstadoMision.COMPLETADA
    
    m2 = gestor.obtener_mision("dinero_1")
    m2.progreso = 500
    m2.estado = EstadoMision.COMPLETADA
    
    # Generar notificación
    notif = gestor.generar_notificacion_misiones(["combate_1", "dinero_1"])
    
    print(notif)
    
    # Validaciones
    assert "✨ ¡MISIONES COMPLETADAS! ✨" in notif, "Header de notificación no encontrado"
    assert "TOTAL:" in notif, "Total no mostrado"
    assert "+" in notif, "Formato de suma no encontrado"
    assert "reclamar recompensas" in notif, "Hint no mostrado"
    
    # Contar dinero total
    m1_dinero = gestor.obtener_mision("combate_1").recompensas['dinero']
    m2_dinero = gestor.obtener_mision("dinero_1").recompensas['dinero']
    dinero_total = m1_dinero + m2_dinero
    
    assert str(dinero_total) in notif, f"Dinero total ({dinero_total}) no está en notificación"
    
    print("✅ Test notificaciones mejoradas: PASADO")


def test_persistencia_guardar_cargar():
    """Test que el estado se guarde y cargue correctamente."""
    print("\n" + "="*70)
    print("TEST 2: Persistencia - Guardar y Cargar Misiones")
    print("="*70)
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as tmpdir:
        archivo_test = os.path.join(tmpdir, "misiones_test.json")
        
        # Crear gestor y modificar misiones
        print("\n📝 FASE 1: Creando y modificando misiones...")
        gestor1 = GestorMisiones()
        
        # Simular progreso
        gestor1.activar_mision("combate_1")
        m1 = gestor1.obtener_mision("combate_1")
        m1.progreso = 5
        m1.estado = EstadoMision.COMPLETADA
        
        gestor1.activar_mision("dinero_1")
        m2 = gestor1.obtener_mision("dinero_1")
        m2.progreso = 250
        
        print(f"  Combate_1: {m1.estado.value}, progreso {m1.progreso}/1")
        print(f"  Dinero_1: {m2.estado.value}, progreso {m2.progreso}/500")
        
        # Guardar
        print("\n💾 Guardando misiones...")
        exito = gestor1.guardar_estado(archivo_test)
        assert exito, "Error al guardar misiones"
        assert os.path.exists(archivo_test), "Archivo no fue creado"
        print(f"  ✓ Guardado en: {archivo_test}")
        
        # Verificar que JSON es válido
        with open(archivo_test, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        print(f"  ✓ JSON válido con {len(datos['misiones'])} misiones")
        
        # Crear nuevo gestor (estado original)
        print("\n🔄 FASE 2: Creando nuevo gestor (estado original)...")
        gestor2 = GestorMisiones()
        m1_antes = gestor2.obtener_mision("combate_1")
        m2_antes = gestor2.obtener_mision("dinero_1")
        
        print(f"  Combate_1: {m1_antes.estado.value}, progreso {m1_antes.progreso}/1")
        print(f"  Dinero_1: {m2_antes.estado.value}, progreso {m2_antes.progreso}/500")
        
        # Cargar estado guardado
        print("\n📂 Cargando misiones guardadas...")
        exito_carga = gestor2.cargar_estado(archivo_test)
        assert exito_carga, "Error al cargar misiones"
        
        # Verificar que se restauró correctamente
        print("\n✓ Estado restaurado:")
        m1_despues = gestor2.obtener_mision("combate_1")
        m2_despues = gestor2.obtener_mision("dinero_1")
        
        print(f"  Combate_1: {m1_despues.estado.value}, progreso {m1_despues.progreso}/1")
        print(f"  Dinero_1: {m2_despues.estado.value}, progreso {m2_despues.progreso}/500")
        
        assert m1_despues.estado == EstadoMision.COMPLETADA, "Estado no se restauró"
        assert m1_despues.progreso == 5, "Progreso no se restauró"
        assert m2_despues.progreso == 250, "Dinero_1 progreso no se restauró"
        
        print("\n✅ Test persistencia: PASADO")


def test_persistencia_multiples_usuarios():
    """Test que archivos de diferentes usuarios no se mezclen."""
    print("\n" + "="*70)
    print("TEST 3: Persistencia - Múltiples Usuarios (Aislamiento)")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Usuario 1
        print("\n👤 Usuario 1: Creando y guardando misiones...")
        gestor_u1 = GestorMisiones()
        m1_u1 = gestor_u1.obtener_mision("combate_1")
        m1_u1.progreso = 1
        m1_u1.estado = EstadoMision.COMPLETADA
        
        archivo_u1 = os.path.join(tmpdir, "misiones_usuario1.json")
        gestor_u1.guardar_estado(archivo_u1)
        print(f"  ✓ Guardado: {archivo_u1}")
        
        # Usuario 2
        print("\n👤 Usuario 2: Creando y guardando misiones diferentes...")
        gestor_u2 = GestorMisiones()
        m2_u2 = gestor_u2.obtener_mision("dinero_1")
        m2_u2.progreso = 500
        m2_u2.estado = EstadoMision.COMPLETADA
        
        archivo_u2 = os.path.join(tmpdir, "misiones_usuario2.json")
        gestor_u2.guardar_estado(archivo_u2)
        print(f"  ✓ Guardado: {archivo_u2}")
        
        # Cargar y verificar usuario 1
        print("\n🔄 Verificando Usuario 1...")
        gestor_check_u1 = GestorMisiones()
        gestor_check_u1.cargar_estado(archivo_u1)
        
        m1_check = gestor_check_u1.obtener_mision("combate_1")
        m2_check = gestor_check_u1.obtener_mision("dinero_1")
        
        assert m1_check.estado == EstadoMision.COMPLETADA, "Usuario 1: combate_1 debería estar completada"
        assert m2_check.estado != EstadoMision.COMPLETADA, "Usuario 1: dinero_1 debería estar bloqueada"
        print("  ✓ Usuario 1 tiene combate_1 completada (correcto)")
        print("  ✓ Usuario 1 tiene dinero_1 bloqueada (correcto)")
        
        # Cargar y verificar usuario 2
        print("\n🔄 Verificando Usuario 2...")
        gestor_check_u2 = GestorMisiones()
        gestor_check_u2.cargar_estado(archivo_u2)
        
        m1_check2 = gestor_check_u2.obtener_mision("combate_1")
        m2_check2 = gestor_check_u2.obtener_mision("dinero_1")
        
        assert m1_check2.estado != EstadoMision.COMPLETADA, "Usuario 2: combate_1 debería estar bloqueada"
        assert m2_check2.estado == EstadoMision.COMPLETADA, "Usuario 2: dinero_1 debería estar completada"
        print("  ✓ Usuario 2 tiene combate_1 bloqueada (correcto)")
        print("  ✓ Usuario 2 tiene dinero_1 completada (correcto)")
        
        print("\n✅ Test aislamiento de usuarios: PASADO")


def test_persistencia_con_bonus():
    """Test que los bonus se guarden correctamente."""
    print("\n" + "="*70)
    print("TEST 4: Persistencia - Estados con Bonus")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        archivo_test = os.path.join(tmpdir, "misiones_bonus.json")
        
        # Crear misiones con bonus
        print("\n🎁 Guardando misiones con bonus...")
        gestor1 = GestorMisiones()
        m_bonus = gestor1.obtener_mision("racha_10")
        
        if m_bonus:
            m_bonus.progreso = 10
            m_bonus.estado = EstadoMision.COMPLETADA
            m_bonus.tiene_bonus = True
            m_bonus.descripcion_bonus = "Racha de 10 victorias"
            m_bonus.bonus_extra_recompensa = 500
            
            print(f"  Misión: {m_bonus.nombre}")
            print(f"  Bonus: {m_bonus.descripcion_bonus} = +{m_bonus.bonus_extra_recompensa}g")
            
            # Guardar
            gestor1.guardar_estado(archivo_test)
            
            # Cargar
            print("\n📂 Cargando misiones con bonus...")
            gestor2 = GestorMisiones()
            gestor2.cargar_estado(archivo_test)
            
            m_check = gestor2.obtener_mision("racha_10")
            print(f"  Bonus restaurado: {m_check.descripcion_bonus} = +{m_check.bonus_extra_recompensa}g")
            
            assert m_check.tiene_bonus == True, "Bonus flag no se restauró"
            assert m_check.descripcion_bonus == "Racha de 10 victorias", "Descripción bonus no se restauró"
            assert m_check.bonus_extra_recompensa == 500, "Cantidad bonus no se restauró"
            
            print("  ✓ Todos los campos de bonus restaurados")
            print("\n✅ Test persistencia con bonus: PASADO")
        else:
            print("  ⚠️  Misión 'racha_10' no encontrada, skipping")


def test_resetear_misiones():
    """Test función de reset de misiones."""
    print("\n" + "="*70)
    print("TEST 5: Resetear Misiones")
    print("="*70)
    
    gestor = GestorMisiones()
    
    print("\n📝 Modificando misiones...")
    # Modificar varias misiones
    m1 = gestor.obtener_mision("combate_1")
    m1.progreso = 5
    m1.estado = EstadoMision.COMPLETADA
    
    m2 = gestor.obtener_mision("dinero_1")
    m2.progreso = 250
    m2.estado = EstadoMision.ACTIVA
    
    print(f"  Combate_1: {m1.estado.value}, progreso {m1.progreso}")
    print(f"  Dinero_1: {m2.estado.value}, progreso {m2.progreso}")
    
    # Resetear
    print("\n🔄 Reseteando misiones...")
    gestor.resetear_misiones()
    
    # Verificar
    print("\n✓ Estado después de reset:")
    m1_reset = gestor.obtener_mision("combate_1")
    m2_reset = gestor.obtener_mision("dinero_1")
    
    print(f"  Combate_1: {m1_reset.estado.value}, progreso {m1_reset.progreso}")
    print(f"  Dinero_1: {m2_reset.estado.value}, progreso {m2_reset.progreso}")
    
    assert m1_reset.progreso == 0, "Combate_1 progreso no se reseteó"
    assert m2_reset.progreso == 0, "Dinero_1 progreso no se reseteó"
    assert m1_reset.estado == EstadoMision.ACTIVA, "Combate_1 debería estar activa"
    
    print("\n✅ Test resetear misiones: PASADO")


# ============================================
# EJECUTAR TODOS LOS TESTS
# ============================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SUITE DE TESTS: NOTIFICACIONES Y PERSISTENCIA")
    print("="*70)
    
    try:
        test_notificaciones_mejoradas()
        test_persistencia_guardar_cargar()
        test_persistencia_multiples_usuarios()
        test_persistencia_con_bonus()
        test_resetear_misiones()
        
        print("\n" + "="*70)
        print("✅ TODOS LOS TESTS DE NOTIFICACIONES Y PERSISTENCIA PASARON")
        print("="*70)
        
    except AssertionError as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
