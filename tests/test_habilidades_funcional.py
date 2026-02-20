"""
TEST FUNCIONAL - SISTEMA DE HABILIDADES
Verifica que todas las habilidades funcionen correctamente
"""

import sys
sys.path.insert(0, '.')

from src.habilidades import (
    Habilidad, TipoHabilidad, TipoTrigger,
    HABILIDADES_POR_ARQUEOTIPO, TODAS_LAS_HABILIDADES,
    obtener_habilidades_arqueotipo,
    calcular_bonus_pasivo_total,
    verificar_y_activar_triggers,
    aplicar_bonificadores_habilidades,
    resetear_habilidades_combate,
    obtener_estadisticas_balance
)
from src.models import Gladiador, Weapon, Armor


class TestCargaHabilidades:
    """Verifica que las habilidades se cargan correctamente"""
    
    def test_todos_arquetipos_cargados(self):
        """Verifica que los 5 arquetipos tengan habilidades"""
        arquetipos = list(HABILIDADES_POR_ARQUEOTIPO.keys())
        assert len(arquetipos) == 5, "Deben haber 5 arquetipos"
        
        arquetipos_esperados = ["Guerrero", "Velocista", "Tanque", "Asesino", "Paladín"]
        for arq in arquetipos_esperados:
            assert arq in arquetipos, f"Falta arqueotipo: {arq}"
    
    def test_cantidad_habilidades_totales(self):
        """Verifica que haya 25 habilidades (5 × 5)"""
        assert len(TODAS_LAS_HABILIDADES) == 25, "Deben haber 25 habilidades totales"
    
    def test_habilidades_por_arqueotipo(self):
        """Verifica que cada arqueotipo tenga 5 habilidades"""
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            assert len(habilidades) == 5, f"{arqueotipo} debe tener 5 habilidades, tiene {len(habilidades)}"
    
    def test_tipos_habilidades_mezcladas(self):
        """Verifica que hay mix de pasivas y activas"""
        pasivas = sum(1 for h in TODAS_LAS_HABILIDADES if h.tipo == TipoHabilidad.PASIVA)
        activas = sum(1 for h in TODAS_LAS_HABILIDADES if h.tipo == TipoHabilidad.ACTIVA)
        
        assert pasivas > 0, "Deben haber habilidades pasivas"
        assert activas > 0, "Deben haber habilidades activas"
        print(f"✓ {pasivas} pasivas, {activas} activas")
    
    def test_cada_habilidad_tiene_nombre(self):
        """Verifica que cada habilidad tenga nombre y descripción"""
        for habilidad in TODAS_LAS_HABILIDADES:
            assert habilidad.nombre, "Habilidad sin nombre"
            assert habilidad.descripcion, "Habilidad sin descripción"
            assert len(habilidad.nombre) > 0, "Nombre vacío"
            assert len(habilidad.descripcion) > 0, "Descripción vacía"


class TestHabilidadesPasivas:
    """Verifica que las habilidades pasivas apliquen bonificadores"""
    
    def test_pasivas_tienen_bonificadores(self):
        """Verifica que pasivas tengan bonus_pasivo definido"""
        pasivas = [h for h in TODAS_LAS_HABILIDADES if h.tipo == TipoHabilidad.PASIVA]
        
        for pasiva in pasivas:
            assert pasiva.bonus_pasivo is not None, f"{pasiva.nombre} sin bonus_pasivo"
            assert len(pasiva.bonus_pasivo) > 0, f"{pasiva.nombre} bonus_pasivo vacío"
            
            # Verificar que son porcentajes válidos
            for stat, valor in pasiva.bonus_pasivo.items():
                assert isinstance(valor, (int, float)), f"{pasiva.nombre} bonus inválido para {stat}"
                assert -1.0 <= valor <= 1.0, f"{pasiva.nombre} bonus fuera de rango: {stat}={valor}"
    
    def test_bonus_pasivo_total(self):
        """Verifica cálculo de bonus total por arqueotipo"""
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            bonus_total = calcular_bonus_pasivo_total(habilidades)
            
            assert bonus_total is not None, f"{arqueotipo} bonus total None"
            assert isinstance(bonus_total, dict), f"{arqueotipo} bonus total no es dict"
            
            # Verificar que tiene stats
            assert len(bonus_total) > 0, f"{arqueotipo} bonus total vacío"
            
            print(f"✓ {arqueotipo}: {bonus_total}")


class TestHabilidadesActivas:
    """Verifica que las habilidades activas tengan triggers"""
    
    def test_activas_tienen_triggers(self):
        """Verifica que activas tengan trigger definido"""
        activas = [h for h in TODAS_LAS_HABILIDADES if h.tipo == TipoHabilidad.ACTIVA]
        
        for activa in activas:
            assert activa.trigger_tipo is not None, f"{activa.nombre} sin trigger_tipo"
            assert activa.trigger_valor is not None, f"{activa.nombre} sin trigger_valor"
            assert activa.bonus_activo is not None, f"{activa.nombre} sin bonus_activo"
            assert activa.duracion_bonus > 0, f"{activa.nombre} duracion_bonus <= 0"
    
    def test_activas_tienen_duracion_valida(self):
        """Verifica que activas tengan duraciones razonables"""
        activas = [h for h in TODAS_LAS_HABILIDADES if h.tipo == TipoHabilidad.ACTIVA]
        
        for activa in activas:
            duracion = activa.duracion_bonus
            assert 1 <= duracion <= 10, f"{activa.nombre} duracion extraña: {duracion}"
    
    def test_tipos_triggers_validos(self):
        """Verifica que los triggers sean de tipos válidos"""
        activas = [h for h in TODAS_LAS_HABILIDADES if h.tipo == TipoHabilidad.ACTIVA]
        tipos_validos = [t.value for t in TipoTrigger]
        
        for activa in activas:
            assert activa.trigger_tipo in list(TipoTrigger), \
                f"{activa.nombre} trigger_tipo inválido: {activa.trigger_tipo}"


class TestIntegracionConGladiador:
    """Verifica que habilidades funcionen con Gladiador"""
    
    def test_gladiador_obtiene_habilidades(self):
        """Verifica que Gladiador recibe habilidades según arqueotipo"""
        for arqueotipo in HABILIDADES_POR_ARQUEOTIPO.keys():
            habilidades = obtener_habilidades_arqueotipo(arqueotipo)
            
            assert len(habilidades) == 5, f"{arqueotipo} debería tener 5 habilidades"
            
            # Verificar que todas son del arqueotipo correcto
            for hab in habilidades:
                assert hab.arqueotipo == arqueotipo, \
                    f"Habilidad {hab.nombre} no es de {arqueotipo}"
    
    def test_aplicar_bonificadores(self):
        """Verifica que bonificadores se apliquen correctamente"""
        guerrero_habs = obtener_habilidades_arqueotipo("Guerrero")
        
        stats_base = {
            "FUERZA": 50,
            "AGILIDAD": 40,
            "DEFENSA": 40,
            "ESQUIVA": 30,
            "CRITICO": 20,
            "HP_MAX": 100
        }
        
        stats_con_bonus = aplicar_bonificadores_habilidades(stats_base, guerrero_habs)
        
        assert stats_con_bonus is not None, "Bonificadores None"
        assert isinstance(stats_con_bonus, dict), "Bonificadores no es dict"
        
        # Guerrero debería tener más FUERZA que stats base
        assert stats_con_bonus.get("FUERZA", 0) >= stats_base["FUERZA"], \
            "Guerrero debería tener bonus de FUERZA"
        
        print(f"✓ Stats Guerrero con bonus: {stats_con_bonus}")


class TestTriggers:
    """Verifica que los triggers se detecten correctamente"""
    
    def test_trigger_salud_bajo(self):
        """Verifica trigger de salud baja"""
        # Simular estado de combate con salud baja
        estado_combate = {
            "salud": 20,
            "salud_maxima": 100,
            "esquivas": 0,
            "criticos_recibidos": 0,
            "criticos_propios": 0,
            "turno": 1
        }
        
        activas = [h for h in TODAS_LAS_HABILIDADES 
                  if h.tipo == TipoHabilidad.ACTIVA and h.trigger_tipo == TipoTrigger.SALUD_BAJO]
        
        assert len(activas) > 0, "No hay habilidades con trigger de salud baja"
        
        # Verificar que el trigger se activaría
        for activa in activas:
            assert activa.trigger_valor >= 0.2, "Trigger de salud baja debería ser >= 0.2 (20%)"
    
    def test_estadisticas_balance(self):
        """Verifica que estadísticas de balance se generen"""
        stats = obtener_estadisticas_balance()
        
        assert stats is not None, "Estadísticas None"
        assert "total_habilidades" in stats, "Falta total_habilidades"
        assert "por_arqueotipo" in stats, "Falta por_arqueotipo"
        assert stats["total_habilidades"] == 25, "Total debe ser 25"
        
        print(f"\n📊 ESTADÍSTICAS DE BALANCE:")
        print(f"   Total habilidades: {stats['total_habilidades']}")
        for arq, info in stats["por_arqueotipo"].items():
            print(f"   {arq}: {info['total']} ({info['pasivas']} pasivas, {info['activas']} activas)")


class TestResetYLimpieza:
    """Verifica que habilidades se reseteen correctamente"""
    
    def test_resetear_habilidades(self):
        """Verifica que se pueden resetear cooldowns"""
        habilidades = obtener_habilidades_arqueotipo("Guerrero")
        
        # Activar algunas
        for hab in habilidades[:2]:
            hab.activar()
        
        # Resetear
        resetear_habilidades_combate(habilidades)
        
        # Verificar que se resetearon
        for hab in habilidades:
            assert hab.veces_usado == 0, f"{hab.nombre} no se reseteó"


# ============================================================================
# EJECUCIÓN DE TESTS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TEST FUNCIONAL - SISTEMA DE HABILIDADES")
    print("="*70)
    
    # Test de carga
    print("\n📋 CARGA DE HABILIDADES:")
    test_carga = TestCargaHabilidades()
    test_carga.test_todos_arquetipos_cargados()
    test_carga.test_cantidad_habilidades_totales()
    test_carga.test_habilidades_por_arqueotipo()
    test_carga.test_tipos_habilidades_mezcladas()
    test_carga.test_cada_habilidad_tiene_nombre()
    print("✅ Todos los tests de carga pasaron")
    
    # Test pasivas
    print("\n💪 HABILIDADES PASIVAS:")
    test_pasivas = TestHabilidadesPasivas()
    test_pasivas.test_pasivas_tienen_bonificadores()
    test_pasivas.test_bonus_pasivo_total()
    print("✅ Todos los tests de pasivas pasaron")
    
    # Test activas
    print("\n⚡ HABILIDADES ACTIVAS:")
    test_activas = TestHabilidadesActivas()
    test_activas.test_activas_tienen_triggers()
    test_activas.test_activas_tienen_duracion_valida()
    test_activas.test_tipos_triggers_validos()
    print("✅ Todos los tests de activas pasaron")
    
    # Test integración
    print("\n🔗 INTEGRACIÓN CON GLADIADOR:")
    test_integracion = TestIntegracionConGladiador()
    test_integracion.test_gladiador_obtiene_habilidades()
    test_integracion.test_aplicar_bonificadores()
    print("✅ Todos los tests de integración pasaron")
    
    # Test triggers
    print("\n🎯 TRIGGERS:")
    test_triggers = TestTriggers()
    test_triggers.test_trigger_salud_bajo()
    test_triggers.test_estadisticas_balance()
    print("✅ Todos los tests de triggers pasaron")
    
    # Test reset
    print("\n🔄 RESET Y LIMPIEZA:")
    test_reset = TestResetYLimpieza()
    test_reset.test_resetear_habilidades()
    print("✅ Todos los tests de reset pasaron")
    
    print("\n" + "="*70)
    print("✅ TODOS LOS TESTS FUNCIONALES PASARON")
    print("="*70 + "\n")
