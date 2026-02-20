"""
TEST DE INTEGRACIÓN - HABILIDADES EN MODELS Y COMBAT
Verifica que las habilidades estén correctamente integradas
"""

import sys
sys.path.insert(0, '.')

from src.models import Gladiador
from src.combat import aplicar_bonificadores_combate, verificar_triggers_combate


class TestIntegracionHabilidades:
    """Verifica integración de habilidades en models.py y combat.py"""
    
    def test_gladiador_carga_habilidades(self):
        """Verifica que Gladiador carga habilidades según tipo"""
        print("\n📋 CARGA DE HABILIDADES EN GLADIADOR:")
        
        tipos_y_arquetipos = {
            "Murmillo": "Guerrero",
            "Retiarius": "Velocista",
            "Secutor": "Paladín",
            "Thraex": "Asesino",
            "Hoplomachus": "Tanque",
        }
        
        for tipo, arqueotipo_esperado in tipos_y_arquetipos.items():
            gladiador = Gladiador("Test", tipo)
            
            # Verificar que tiene habilidades
            assert hasattr(gladiador, 'habilidades'), f"{tipo} no tiene habilidades"
            assert len(gladiador.habilidades) == 5, f"{tipo} debería tener 5 habilidades"
            
            # Verificar arqueotipo
            arqueotipo_real = gladiador.habilidades[0].arqueotipo
            assert arqueotipo_real == arqueotipo_esperado, \
                f"{tipo} debería tener arqueotipo {arqueotipo_esperado}, tiene {arqueotipo_real}"
            
            print(f"  ✓ {tipo:15} → {arqueotipo_esperado}")
        
        print("  ✅ Todos los tipos cargan habilidades correctas")
    
    def test_contadores_triggers(self):
        """Verifica que los contadores de triggers existen"""
        print("\n🎯 CONTADORES DE TRIGGERS:")
        
        gladiador = Gladiador("Test", "Murmillo")
        
        # Verificar estructura
        assert hasattr(gladiador, 'contadores_triggers'), "No tiene contadores_triggers"
        contadores = gladiador.contadores_triggers
        
        contadores_esperados = ["esquivas", "criticos_recibidos", "criticos_propios", "daño_recibido", "turnos"]
        for contador in contadores_esperados:
            assert contador in contadores, f"Falta contador: {contador}"
            assert contadores[contador] == 0, f"Contador {contador} no está en 0"
            print(f"  ✓ {contador}: {contadores[contador]}")
        
        print("  ✅ Todos los contadores inicializados")
    
    def test_aplicar_bonificadores(self):
        """Verifica que se aplican bonificadores de habilidades"""
        print("\n💪 APLICACIÓN DE BONIFICADORES:")
        
        arquetipos_test = ["Murmillo", "Retiarius", "Thraex", "Hoplomachus"]
        
        for tipo in arquetipos_test:
            gladiador = Gladiador("Test", tipo)
            
            # Stats base
            stats_base = {
                "FUERZA": 50,
                "AGILIDAD": 40,
                "DEFENSA": 40,
                "ESQUIVA": 30,
                "CRITICO": 20,
                "HP_MAX": 100
            }
            
            # Aplicar bonificadores
            stats_bonificados = aplicar_bonificadores_combate(stats_base, gladiador)
            
            # Verificar que hay cambios
            hay_cambios = any(
                stats_bonificados.get(k, 0) != stats_base.get(k, 0)
                for k in stats_base.keys()
            )
            
            assert hay_cambios, f"{tipo} no aplica bonificadores"
            
            # Mostrar cambios principales
            for stat in ["FUERZA", "AGILIDAD", "DEFENSA", "CRITICO"]:
                base = stats_base.get(stat, 0)
                bonus = stats_bonificados.get(stat, 0)
                if bonus != base:
                    cambio = ((bonus - base) / base * 100) if base > 0 else 0
                    print(f"  {tipo}: {stat} {base} → {bonus} (+{cambio:.1f}%)")
        
        print("  ✅ Bonificadores aplicados correctamente")
    
    def test_verificar_triggers(self):
        """Verifica que los triggers se registran"""
        print("\n🔄 VERIFICACIÓN DE TRIGGERS:")
        
        gladiador = Gladiador("Test", "Murmillo")
        enemigo = Gladiador("Enemigo", "Retiarius")
        
        # Simulación: ataque crítico
        estado_inicial = gladiador.contadores_triggers["criticos_propios"]
        
        verificar_triggers_combate(
            gladiador, enemigo, turno=1,
            resultado_ataque="crítico",
            resultado_defensa="golpe"
        )
        
        # Verificar que se incrementó
        assert gladiador.contadores_triggers["criticos_propios"] > estado_inicial, \
            "No se incrementó el contador de críticos propios"
        
        print(f"  ✓ Críticos propios: {gladiador.contadores_triggers['criticos_propios']}")
        
        # Simulación: esquiva
        verificar_triggers_combate(
            gladiador, enemigo, turno=2,
            resultado_ataque="golpe",
            resultado_defensa="esquiva"
        )
        
        # Verificar que se incrementó esquivas
        assert gladiador.contadores_triggers["esquivas"] > 0, \
            "No se incrementó el contador de esquivas"
        
        print(f"  ✓ Esquivas: {gladiador.contadores_triggers['esquivas']}")
        print("  ✅ Triggers registrados correctamente")
    
    def test_flujo_completo(self):
        """Prueba flujo completo: crear gladiador → aplicar bonificadores → verificar triggers"""
        print("\n🚀 FLUJO COMPLETO:")
        
        # 1. Crear gladiador
        gladiador = Gladiador("Ferox", "Murmillo")
        print(f"  1. ✓ Gladiador creado: {gladiador.nombre}")
        print(f"     Habilidades: {len(gladiador.habilidades)}")
        print(f"     Arqueotipo: {gladiador.habilidades[0].arqueotipo}")
        
        # 2. Stats base
        stats_base = {
            "FUERZA": 50,
            "AGILIDAD": 40,
            "DEFENSA": 40,
            "ESQUIVA": 30,
            "CRITICO": 20,
            "HP_MAX": 100
        }
        print(f"\n  2. ✓ Stats base: FUERZA={stats_base['FUERZA']}")
        
        # 3. Aplicar bonificadores
        stats_combat = aplicar_bonificadores_combate(stats_base, gladiador)
        bonus_fuerza = stats_combat["FUERZA"] - stats_base["FUERZA"]
        print(f"\n  3. ✓ Bonificadores aplicados:")
        print(f"     FUERZA: {stats_base['FUERZA']} → {stats_combat['FUERZA']} (+{bonus_fuerza})")
        
        # 4. Simular triggers
        print(f"\n  4. ✓ Simulando triggers en combate:")
        
        enemigo = Gladiador("Rivalis", "Retiarius")
        
        # Turno 1: Crítico
        verificar_triggers_combate(
            gladiador, enemigo, turno=1,
            resultado_ataque="crítico"
        )
        print(f"     Turno 1: Crítico → Contador: {gladiador.contadores_triggers['criticos_propios']}")
        
        # Turno 2: Golpe
        verificar_triggers_combate(
            gladiador, enemigo, turno=2,
            resultado_defensa="esquiva"
        )
        print(f"     Turno 2: Esquiva → Contador: {gladiador.contadores_triggers['esquivas']}")
        
        print(f"\n  ✅ FLUJO COMPLETO EXITOSO")


# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TEST DE INTEGRACIÓN - HABILIDADES EN MODELS Y COMBAT")
    print("="*70)
    
    test = TestIntegracionHabilidades()
    
    test.test_gladiador_carga_habilidades()
    test.test_contadores_triggers()
    test.test_aplicar_bonificadores()
    test.test_verificar_triggers()
    test.test_flujo_completo()
    
    print("\n" + "="*70)
    print("✅ TODOS LOS TESTS DE INTEGRACIÓN PASARON")
    print("="*70 + "\n")
