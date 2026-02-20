"""
Test de Integración: Notificaciones + Persistencia en Main.py
==============================================================
Simula un flujo completo:
1. Usuario juega y completa misiones
2. Guarda la partida
3. Carga la partida
4. Verifica que misiones se restauren
5. Continúa jugando
"""

import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.misiones import GestorMisiones, EstadoMision, TipoMision
from src.models import Equipo, Gladiador


def simular_sesion_completa():
    """Simula una sesión completa de juego con guardado y carga."""
    
    print("\n" + "="*70)
    print("INTEGRACIÓN: Sesión Completa con Guardado y Carga")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        archivo_misiones = os.path.join(tmpdir, "misiones_usuario1.json")
        
        # ============================================
        # SESIÓN 1: Jugar y guardar
        # ============================================
        
        print("\n" + "-"*70)
        print("SESIÓN 1: Jugar y Guardar Partida")
        print("-"*70)
        
        print("\n🎮 Iniciando sesión 1...")
        usuario = "usuario1"
        equipo1 = Equipo()
        equipo1.dinero = 5000
        
        g1 = Gladiador("Ferox", "Murmillo", nivel=1)
        g2 = Gladiador("Velox", "Retiarius", nivel=1)
        equipo1.agregar_gladiador(g1)
        equipo1.agregar_gladiador(g2)
        
        print(f"✓ Equipo creado: {len(equipo1.gladiadores)} gladiadores")
        
        # Crear misiones
        gestor1 = GestorMisiones()
        print(f"✓ {len(gestor1.misiones)} misiones cargadas")
        
        # Simular progreso
        print("\n⚔️  Simulando jugabilidad (combates, dinero, etc)...")
        
        # Activar combate_1 y progresar
        gestor1.activar_mision("combate_1")
        for i in range(1):
            misiones_completadas = gestor1.evento_combate_ganado()
            if misiones_completadas:
                notif = gestor1.generar_notificacion_misiones(misiones_completadas)
                print(f"  Victory {i+1}:")
                print(f"    {notif.strip()}")
        
        # Dinero acumulado
        for i in range(3):
            misiones_completadas = gestor1.evento_dinero_acumulado(200)
            if misiones_completadas:
                notif = gestor1.generar_notificacion_misiones(misiones_completadas)
                print(f"  Money event {i+1}:")
                print(f"    {notif.strip()}")
        
        # Nivel up
        misiones_completadas = gestor1.evento_gladiador_sube_nivel()
        if misiones_completadas:
            notif = gestor1.generar_notificacion_misiones(misiones_completadas)
            print(f"  Level up event:")
            print(f"    {notif.strip()}")
        
        # Mostrar estado de misiones importantes
        print("\n📊 Estado de misiones al final de Sesión 1:")
        combate_1 = gestor1.obtener_mision("combate_1")
        dinero_1 = gestor1.obtener_mision("dinero_1")
        nivel_1 = gestor1.obtener_mision("nivel_1")
        
        print(f"  Combate_1: {combate_1.estado.value} ({combate_1.progreso}/{combate_1.objetivo})")
        print(f"  Dinero_1: {dinero_1.estado.value} ({dinero_1.progreso}/{dinero_1.objetivo})")
        print(f"  Nivel_1: {nivel_1.estado.value} ({nivel_1.progreso}/{nivel_1.objetivo})")
        
        # Guardar
        print("\n💾 Guardando partida...")
        if gestor1.guardar_estado(archivo_misiones):
            print(f"✓ Misiones guardadas en: {archivo_misiones}")
        else:
            print("❌ Error al guardar")
            return False
        
        # Verificar archivo JSON
        with open(archivo_misiones, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        print(f"✓ Archivo JSON válido ({len(datos['misiones'])} misiones, {len(datos['activas'])} activas)")
        
        # ============================================
        # SESIÓN 2: Cargar y continuar
        # ============================================
        
        print("\n" + "-"*70)
        print("SESIÓN 2: Cargar Partida y Continuar")
        print("-"*70)
        
        print("\n🎮 Iniciando sesión 2 (reapertura de juego)...")
        
        # Simular cierre y apertura
        print("  [Juego cerrado]")
        print("  [Usuario reinicia sesión]")
        
        # Cargar nuevo gestor
        gestor2 = GestorMisiones()
        print("✓ Nuevo gestor de misiones creado (estado inicial)")
        
        # Cargar estado guardado
        print("\n📂 Cargando partida guardada...")
        if gestor2.cargar_estado(archivo_misiones):
            print("✓ Misiones restauradas exitosamente")
        else:
            print("❌ Error al cargar")
            return False
        
        # Verificar que el estado se restauró
        print("\n✓ Verificando integridad de datos restaurados:")
        combate_1_loaded = gestor2.obtener_mision("combate_1")
        dinero_1_loaded = gestor2.obtener_mision("dinero_1")
        nivel_1_loaded = gestor2.obtener_mision("nivel_1")
        
        print(f"  Combate_1: {combate_1_loaded.estado.value} ({combate_1_loaded.progreso}/{combate_1_loaded.objetivo})")
        print(f"  Dinero_1: {dinero_1_loaded.estado.value} ({dinero_1_loaded.progreso}/{dinero_1_loaded.objetivo})")
        print(f"  Nivel_1: {nivel_1_loaded.estado.value} ({nivel_1_loaded.progreso}/{nivel_1_loaded.objetivo})")
        
        # Validar que coincida
        assert combate_1_loaded.estado == combate_1.estado, "Combate_1 estado no coincide"
        assert combate_1_loaded.progreso == combate_1.progreso, "Combate_1 progreso no coincide"
        assert dinero_1_loaded.progreso == dinero_1.progreso, "Dinero_1 progreso no coincide"
        assert nivel_1_loaded.progreso == nivel_1.progreso, "Nivel_1 progreso no coincide"
        
        print("  ✓ Todos los estados coinciden con sesión anterior")
        
        # Continuar jugando
        print("\n⚔️  Continuando sesión 2...")
        
        # Más combates
        for i in range(1):
            misiones_completadas = gestor2.evento_combate_ganado()
            if misiones_completadas:
                notif = gestor2.generar_notificacion_misiones(misiones_completadas)
                print(f"  Victory {i+1}:")
                for line in notif.strip().split('\n')[:5]:  # Mostrar solo primeras líneas
                    print(f"    {line}")
        
        # Dinero
        for i in range(2):
            misiones_completadas = gestor2.evento_dinero_acumulado(200)
            if misiones_completadas:
                print(f"  Money event {i+1}: Misiones completadas")
        
        print("\n📊 Estado final de Sesión 2:")
        combate_final = gestor2.obtener_mision("combate_1")
        dinero_final = gestor2.obtener_mision("dinero_1")
        
        print(f"  Combate_1: {combate_final.estado.value} ({combate_final.progreso}/{combate_final.objetivo})")
        print(f"  Dinero_1: {dinero_final.estado.value} ({dinero_final.progreso}/{dinero_final.objetivo})")
        
        # Guardar de nuevo
        print("\n💾 Guardando partida actualizada...")
        if gestor2.guardar_estado(archivo_misiones):
            print(f"✓ Partida actualizada y guardada")
        else:
            print("❌ Error al guardar")
            return False
        
        print("\n" + "="*70)
        print("✅ INTEGRACIÓN COMPLETA: SESIÓN EXITOSA")
        print("="*70)
        print("\n📋 Resumen:")
        print("  ✓ Sesión 1: Crear, jugar, guardar")
        print("  ✓ Sesión 2: Cargar, continuar, guardar")
        print("  ✓ Integridad de datos: OK")
        print("  ✓ Notificaciones: Funcionales")
        print("  ✓ Persistencia: Funcional")
        
        return True


def test_carga_partida_no_existente():
    """Test que manejar correctamente cuando no existe archivo."""
    print("\n" + "="*70)
    print("TEST: Carga de Partida No Existente")
    print("="*70)
    
    gestor = GestorMisiones()
    resultado = gestor.cargar_estado("datos/partida_inexistente.json")
    
    if not resultado:
        print("✓ Manejo correcto: No existe archivo (retorna False)")
        print("✓ Gestor continúa con estado inicial")
        assert len(gestor.misiones) == 23, "Misiones no cargadas correctamente"
        print("✅ Test manejo de no existencia: PASADO")
    else:
        print("❌ Debería retornar False para archivo inexistente")
        return False
    
    return True


# ============================================
# EJECUTAR
# ============================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SUITE DE INTEGRACIÓN: NOTIFICACIONES + PERSISTENCIA")
    print("="*70)
    
    try:
        if not simular_sesion_completa():
            sys.exit(1)
        
        if not test_carga_partida_no_existente():
            sys.exit(1)
        
        print("\n" + "="*70)
        print("✅ TODOS LOS TESTS DE INTEGRACIÓN PASARON")
        print("="*70)
        
    except AssertionError as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
