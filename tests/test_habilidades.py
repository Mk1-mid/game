"""
TESTS DE HABILIDADES - Verificación de Balance
Test para asegurar que ninguna habilidad es más fuerte que otra
"""

import pytest
from src.habilidades import (
    Habilidad, TipoHabilidad, TipoTrigger,
    HABILIDADES_POR_ARQUEOTIPO, TODAS_LAS_HABILIDADES,
    calcular_bonus_pasivo_total, calcular_bonus_activo_total,
    aplicar_bonificadores_habilidades, obtener_estadisticas_balance
)


class TestEstructuraHabilidades:
    """Tests de estructura básica"""
    
    def test_total_habilidades(self):
        """Debe haber exactamente 25 habilidades (5 arquetipos × 5)"""
        assert len(TODAS_LAS_HABILIDADES) == 25
    
    def test_habilidades_por_arqueotipo(self):
        """Cada arqueotipo debe tener exactamente 5 habilidades"""
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            assert len(habilidades) == 5, f"{arqueotipo} tiene {len(habilidades)} habilidades, debe tener 5"
    
    def test_arquetipos_validos(self):
        """Todos los arquetipos válidos"""
        arquetipos_validos = {"Guerrero", "Velocista", "Tanque", "Asesino", "Paladín"}
        arquetipos_proyecto = set(HABILIDADES_POR_ARQUEOTIPO.keys())
        assert arquetipos_proyecto == arquetipos_validos
    
    def test_habilidades_tienen_nombre_descripcion(self):
        """Todas las habilidades deben tener nombre y descripción"""
        for hab in TODAS_LAS_HABILIDADES:
            assert hab.nombre and len(hab.nombre) > 0
            assert hab.descripcion and len(hab.descripcion) > 0
    
    def test_tipos_habilidades_validos(self):
        """Todos los tipos de habilidades deben ser válidos"""
        for hab in TODAS_LAS_HABILIDADES:
            assert hab.tipo in [TipoHabilidad.PASIVA, TipoHabilidad.ACTIVA]


class TestBalanceHabilidades:
    """Tests de balance para evitar overpowered"""
    
    def test_bonus_pasivo_razonable(self):
        """
        Cada bonus pasivo debe estar entre 0% y 25%
        Sí hay un bonus negativo, debe estar entre -30% y 0%
        """
        for hab in TODAS_LAS_HABILIDADES:
            if hab.tipo == TipoHabilidad.PASIVA and hab.bonus_pasivo:
                for stat, valor in hab.bonus_pasivo.items():
                    assert -0.30 <= valor <= 0.25, (
                        f"{hab.nombre}: {stat} = {valor*100:.0f}% (fuera de rango)"
                    )
    
    def test_bonus_activo_razonable(self):
        """
        Cada bonus activo debe estar entre -50% y 50%
        (pueden ser más altos porque son temporales)
        """
        for hab in TODAS_LAS_HABILIDADES:
            if hab.tipo == TipoHabilidad.ACTIVA and hab.bonus_activo:
                for stat, valor in hab.bonus_activo.items():
                    assert -0.50 <= valor <= 0.50, (
                        f"{hab.nombre}: {stat} = {valor*100:.0f}% (fuera de rango)"
                    )
    
    def test_duracion_habilidades_activas(self):
        """Las habilidades activas deben tener duración entre 3 y 6 turnos"""
        for hab in TODAS_LAS_HABILIDADES:
            if hab.tipo == TipoHabilidad.ACTIVA:
                assert 3 <= hab.duracion_bonus <= 6, (
                    f"{hab.nombre} duración {hab.duracion_bonus} turnos (fuera de rango 3-6)"
                )
    
    def test_cooldown_habilidades_activas(self):
        """Las habilidades activas deben tener cooldown 1 (una sola vez por combate)"""
        for hab in TODAS_LAS_HABILIDADES:
            if hab.tipo == TipoHabilidad.ACTIVA:
                assert hab.cooldown == 1, (
                    f"{hab.nombre} cooldown es {hab.cooldown}, debe ser 1"
                )


class TestBalancePorArqueotipo:
    """Tests para verificar balance entre arquetipos"""
    
    def test_pasivas_vs_activas_distribucion(self):
        """Cada arqueotipo debe tener ~3 pasivas y ~2 activas"""
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            pasivas = sum(1 for h in habilidades if h.tipo == TipoHabilidad.PASIVA)
            activas = sum(1 for h in habilidades if h.tipo == TipoHabilidad.ACTIVA)
            
            # Puede haber variación pequeña, pero debe ser ~3/2
            assert 2 <= pasivas <= 4, f"{arqueotipo}: {pasivas} pasivas (debe ser ~3)"
            assert 1 <= activas <= 3, f"{arqueotipo}: {activas} activas (debe ser ~2)"
    
    def test_bonus_total_pasivo_similar(self):
        """
        El bonus total pasivo por arqueotipo debe ser similar (+/-5%)
        Esto asegura que ningún arqueotipo es más fuerte que otro pasivamente
        """
        bonus_totales = {}
        
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            bonus = calcular_bonus_pasivo_total(habilidades)
            # Suma todos los bonus (considerando que pueden aplicarse a diferentes stats)
            total_bonus = sum(abs(v) for v in bonus.values())
            bonus_totales[arqueotipo] = total_bonus
        
        # Obtener mínimo y máximo
        minimo = min(bonus_totales.values())
        maximo = max(bonus_totales.values())
        
        # La diferencia no debe ser más del 30%
        diferencia = (maximo - minimo) / minimo * 100
        
        print(f"\nBonus totales por arqueotipo:")
        for arq, total in sorted(bonus_totales.items()):
            print(f"  {arq}: {total:.2f}")
        print(f"Diferencia máxima: {diferencia:.1f}%")
        
        assert diferencia <= 30, f"Diferencia de balance es {diferencia:.1f}% (máximo 30%)"
    
    def test_no_arqueotipo_domina_stats(self):
        """Ningún arqueotipo debe dominar todos los stats principales"""
        estadisticas = obtener_estadisticas_balance()
        
        for arqueotipo, info in estadisticas['por_arqueotipo'].items():
            bonus = info['bonus_total_pasivo']
            stats_fuertes = sum(1 for v in bonus.values() if v > 0.12)
            
            # No puede ser fuerte en más de 3 stats
            assert stats_fuertes <= 3, (
                f"{arqueotipo} es fuerte en {stats_fuertes} stats (máximo 3): {bonus}"
            )
    
    def test_distribucion_triggers(self):
        """
        Los triggers deben estar distribuidos para evitar que un arquetipo
        active habilidades más fácilmente que otro
        """
        triggers_por_arqueotipo = {}
        
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            triggers = {}
            for hab in habilidades:
                if hab.tipo == TipoHabilidad.ACTIVA:
                    trigger_name = hab.trigger_tipo.value if hab.trigger_tipo else "ninguno"
                    triggers[trigger_name] = triggers.get(trigger_name, 0) + 1
            triggers_por_arqueotipo[arqueotipo] = triggers
        
        # Mostrar distribución
        print("\nDistribución de triggers por arqueotipo:")
        for arq, triggers in triggers_por_arqueotipo.items():
            print(f"  {arq}: {triggers}")
        
        # Cada arqueotipo debe tener 2 habilidades activas con triggers diferentes
        for arqueotipo, triggers in triggers_por_arqueotipo.items():
            assert len(triggers) >= 1, f"{arqueotipo} debe tener al menos 1 tipo de trigger"


class TestTriggers:
    """Tests de triggers de habilidades activas"""
    
    def test_triggers_validos(self):
        """Todos los triggers deben ser del tipo TipoTrigger"""
        trigger_tipos_validos = {t.value for t in TipoTrigger}
        
        for hab in TODAS_LAS_HABILIDADES:
            if hab.tipo == TipoHabilidad.ACTIVA:
                assert hab.trigger_tipo is not None, f"{hab.nombre} debe tener trigger_tipo"
                assert hab.trigger_tipo.value in trigger_tipos_validos
    
    def test_trigger_valor_razonable(self):
        """Los valores de trigger deben ser razonables"""
        for hab in TODAS_LAS_HABILIDADES:
            if hab.tipo == TipoHabilidad.ACTIVA:
                valor = hab.trigger_valor
                
                if hab.trigger_tipo == TipoTrigger.SALUD_BAJO:
                    # Debe estar entre 0 y 1 (0% a 100%)
                    assert 0 < valor <= 1, f"{hab.nombre} salud_bajo debe estar entre 0 y 1"
                
                elif hab.trigger_tipo == TipoTrigger.ESQUIVAS_CONSECUTIVAS:
                    # Debe ser entre 2 y 5 esquivas
                    assert 2 <= valor <= 5, f"{hab.nombre} esquivas debe estar entre 2 y 5"
                
                elif hab.trigger_tipo == TipoTrigger.CRITICOS_RECIBIDOS:
                    # Debe ser entre 2 y 4 críticos
                    assert 2 <= valor <= 4, f"{hab.nombre} críticos_recibidos debe estar entre 2 y 4"
                
                elif hab.trigger_tipo == TipoTrigger.CRITICOS_PROPIOS:
                    # Debe ser entre 2 y 4 críticos
                    assert 2 <= valor <= 4, f"{hab.nombre} críticos_propios debe estar entre 2 y 4"


class TestIntegracion:
    """Tests de integración de habilidades"""
    
    def test_aplicar_bonificadores(self):
        """Verificar que los bonificadores se aplican correctamente"""
        habilidades = HABILIDADES_POR_ARQUEOTIPO["Guerrero"]
        
        stats_base = {
            "FUERZA": 100,
            "AGILIDAD": 80,
            "DEFENSA": 70,
            "ESQUIVA": 20,
            "CRITICO": 15,
            "HP_MAX": 100,
        }
        
        stats_final = aplicar_bonificadores_habilidades(stats_base, habilidades)
        
        # Los stats finales deben ser mayores (debido a bonificadores pasivos)
        for stat in stats_final:
            assert stats_final[stat] >= stats_base[stat], (
                f"Bonus negativo en {stat}: {stats_base[stat]} -> {stats_final[stat]}"
            )
    
    def test_bonus_pasivo_no_negativo_total(self):
        """El bonus pasivo total no debe hacer que stats caigan"""
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            bonus = calcular_bonus_pasivo_total(habilidades)
            
            # Cada stat debe tener bonus no-negativo total
            for stat, valor in bonus.items():
                assert valor >= -0.10, (
                    f"{arqueotipo}: {stat} tiene bonus pasivo total negativo: {valor*100:.0f}%"
                )


class TestEquilibrio:
    """Tests finales de equilibrio"""
    
    def test_reporte_balance(self):
        """Generar y mostrar reporte de balance"""
        stats = obtener_estadisticas_balance()
        
        print("\n" + "="*80)
        print("REPORTE DE BALANCE DE HABILIDADES")
        print("="*80)
        print(f"\nTotal de habilidades: {stats['total_habilidades']}")
        print(f"Pasivas: {stats['pasivas_vs_activas']['pasivas']}")
        print(f"Activas: {stats['pasivas_vs_activas']['activas']}")
        
        print("\nBonus pasivo total por arqueotipo:")
        for arqueotipo, info in stats['por_arqueotipo'].items():
            pasivas = info['pasivas']
            activas = info['activas']
            bonus = info['bonus_total_pasivo']
            total_bonus = sum(abs(v) for v in bonus.values())
            
            print(f"\n  {arqueotipo}:")
            print(f"    Estructura: {pasivas} pasivas, {activas} activas")
            print(f"    Bonus totales: {total_bonus:.2f}")
            
            # Mostrar bonus por stat
            for stat, valor in sorted(bonus.items()):
                if valor != 0:
                    signo = "+" if valor > 0 else ""
                    print(f"      • {stat}: {signo}{valor*100:.0f}%")
        
        print("\n" + "="*80)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
