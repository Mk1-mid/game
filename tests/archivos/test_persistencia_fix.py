#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DE PERSISTENCIA - Verifica que el guardado/carga funciona correctamente
"""

import os
import sys
sys.path.insert(0, os.path.abspath('.'))

from src.models import Equipo, Gladiador
from src.persistence import serializar_equipo, deserializar_equipo
from src.auth import guardar_partida, cargar_partida

def test_persistencia_completa():
    """Test completo de serialización/deserialización"""
    
    print("="*70)
    print("🧪 TEST DE PERSISTENCIA - GUARDADO Y CARGA")
    print("="*70)
    
    # 1. Crear equipo con datos
    print("\n1️⃣ Creando equipo de prueba...")
    equipo_original = Equipo()
    equipo_original.dinero = 15000
    
    g1 = Gladiador("Testius", "Murmillo", nivel=5)
    g1.xp = 500
    g1.hp_actual = 75
    
    g2 = Gladiador("Velocis", "Retiarius", nivel=3)
    g2.xp = 200
    
    equipo_original.agregar_gladiador(g1)
    equipo_original.agregar_gladiador(g2)
    
    print(f"   ✓ Equipo creado: {len(equipo_original.gladiadores)} gladiadores")
    print(f"   ✓ Dinero: {equipo_original.dinero}💰")
    
    # 2. Serializar
    print("\n2️⃣ Serializando equipo...")
    datos_serializado = serializar_equipo(equipo_original)
    print(f"   ✓ Equipo serializado a diccionario")
    print(f"   ✓ Dinero: {datos_serializado['dinero']}")
    print(f"   ✓ Gladiadores: {len(datos_serializado['gladiadores'])}")
    
    # 3. Guardar en archivo
    print("\n3️⃣ Guardando en archivo...")
    usuario_prueba = "test_usuario_persistencia"
    guardar_partida(usuario_prueba, datos_serializado)
    
    # Verificar archivo existe
    archivo = f"data/saves/save_{usuario_prueba}.json"
    if os.path.exists(archivo):
        print(f"   ✓ Archivo creado: {archivo}")
    else:
        print(f"   ❌ Archivo NO creado")
        return False
    
    # 4. Cargar desde archivo
    print("\n4️⃣ Cargando desde archivo...")
    datos_cargados = cargar_partida(usuario_prueba)
    if datos_cargados:
        print(f"   ✓ Datos cargados del archivo")
        print(f"   ✓ Dinero: {datos_cargados['dinero']}")
    else:
        print(f"   ❌ No se cargaron datos")
        return False
    
    # 5. Deserializar
    print("\n5️⃣ Deserializando equipo...")
    try:
        equipo_restaurado = deserializar_equipo(datos_cargados)
        print(f"   ✓ Equipo deserializado")
        print(f"   ✓ Dinero: {equipo_restaurado.dinero}💰")
        print(f"   ✓ Gladiadores: {len(equipo_restaurado.gladiadores)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 6. Verificar integridad
    print("\n6️⃣ Verificando integridad de datos...")
    
    verificaciones = [
        ("Dinero", equipo_original.dinero == equipo_restaurado.dinero),
        ("Cantidad de gladiadores", len(equipo_original.gladiadores) == len(equipo_restaurado.gladiadores)),
        ("Primer gladiador nombre", equipo_original.gladiadores[0].nombre == equipo_restaurado.gladiadores[0].nombre),
        ("Primer gladiador nivel", equipo_original.gladiadores[0].nivel == equipo_restaurado.gladiadores[0].nivel),
        ("Primer gladiador XP", equipo_original.gladiadores[0].xp == equipo_restaurado.gladiadores[0].xp),
        ("Segundo gladiador nombre", equipo_original.gladiadores[1].nombre == equipo_restaurado.gladiadores[1].nombre),
    ]
    
    todos_ok = True
    for verificacion, resultado in verificaciones:
        icon = "✓" if resultado else "❌"
        print(f"   {icon} {verificacion}: {resultado}")
        if not resultado:
            todos_ok = False
    
    # 7. Limpiar
    print("\n7️⃣ Limpiando archivo de prueba...")
    try:
        os.remove(archivo)
        print(f"   ✓ Archivo eliminado")
    except:
        print(f"   ⚠️ No se pudo eliminar {archivo}")
    
    # Resultado final
    print("\n" + "="*70)
    if todos_ok:
        print("✅ TEST EXITOSO: Persistencia funcionando correctamente")
        print("="*70)
        return True
    else:
        print("❌ TEST FALLIDO: Hay problemas con la persistencia")
        print("="*70)
        return False


if __name__ == "__main__":
    success = test_persistencia_completa()
    sys.exit(0 if success else 1)
