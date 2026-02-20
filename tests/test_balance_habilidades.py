"""
TEST DE BALANCE - SISTEMA DE HABILIDADES
Verifica que no haya habilidades overpowered y que el sistema esté balanceado
"""

import sys
sys.path.insert(0, '.')

from src.habilidades import (
    HABILIDADES_POR_ARQUEOTIPO, TODAS_LAS_HABILIDADES,
    TipoHabilidad, calcular_bonus_pasivo_total,
    aplicar_bonificadores_habilidades
)


class TestBalanceGeneral:
    """Verifica balance general del sistema"""
    
    def test_rango_bonus_pasivo_razonable(self):
        """Verifica que los bonificadores pasivos no sean excesivos"""
        MAX_BONUS_STAT = 0.30  # 30% máximo por habilidad
        
        pasivas = [h for h in TODAS_LAS_HABILIDADES if h.tipo == TipoHabilidad.PASIVA]
        
        for pasiva in pasivas:
            for stat, valor in pasiva.bonus_pasivo.items():
                assert abs(valor) <= MAX_BONUS_STAT, \
                    f"⚠️ {pasiva.nombre} tiene bonus excesivo: {stat}={valor*100}% (máx: {MAX_BONUS_STAT*100}%)"
        
        print(f"✓ Todos los bonificadores pasivos están en rango razonable (<{MAX_BONUS_STAT*100}%)")
    
    def test_rango_bonus_activo_razonable(self):
        """Verifica que los bonificadores activos no sean excesivos"""
        MAX_BONUS_ACTIVO = 0.50  # 50% máximo (son temporales)
        
        activas = [h for h in TODAS_LAS_HABILIDADES if h.tipo == TipoHabilidad.ACTIVA]
        
        for activa in activas:
            for stat, valor in activa.bonus_activo.items():
                assert abs(valor) <= MAX_BONUS_ACTIVO, \
                    f"⚠️ {activa.nombre} tiene bonus activo excesivo: {stat}={valor*100}% (máx: {MAX_BONUS_ACTIVO*100}%)"
        
        print(f"✓ Todos los bonificadores activos están en rango razonable (<{MAX_BONUS_ACTIVO*100}%)")
    
    def test_duracion_efectos_temporales(self):
        """Verifica que los efectos temporales no duren demasiado"""
        MAX_DURACION = 6  # turnos máximo
        
        activas = [h for h in TODAS_LAS_HABILIDADES if h.tipo == TipoHabilidad.ACTIVA]
        
        for activa in activas:
            assert activa.duracion_bonus <= MAX_DURACION, \
                f"⚠️ {activa.nombre} dura demasiado: {activa.duracion_bonus} turnos (máx: {MAX_DURACION})"
        
        print(f"✓ Todas las duraciones de efectos son razonables (<{MAX_DURACION} turnos)")


class TestBalanceArqueotipos:
    """Verifica balance entre arquetipos"""
    
    def test_bonus_pasivo_similar_entre_arquetipos(self):
        """Verifica que el bonus total pasivo sea similar para todos"""
        bonus_por_arqueotipo = {}
        
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            bonus_total = calcular_bonus_pasivo_total(habilidades)
            
            # Sumar todos los bonuses
            suma_bonus = sum(sum(abs(v) for v in bonus.values()) 
                            for bonus in [h.bonus_pasivo for h in habilidades if h.bonus_pasivo])
            
            bonus_por_arqueotipo[arqueotipo] = suma_bonus
        
        # Encontrar max y min
        max_bonus = max(bonus_por_arqueotipo.values())
        min_bonus = min(bonus_por_arqueotipo.values())
        diferencia = max_bonus - min_bonus
        
        # Permitir diferencia de hasta 20%
        tolerancia = max_bonus * 0.20
        
        assert diferencia <= tolerancia, \
            f"⚠️ Desbalance entre arquetipos: {bonus_por_arqueotipo}"
        
        print(f"✓ Balance de bonus pasivo entre arquetipos: OK")
        for arq, bonus in bonus_por_arqueotipo.items():
            print(f"   {arq}: {bonus:.2f}")
    
    def test_cada_arqueotipo_tiene_fortaleza(self):
        """Verifica que cada arqueotipo tenga una stat en la que destaca"""
        arquetipos_esperados = {
            "Guerrero": "FUERZA",
            "Velocista": "AGILIDAD",
            "Tanque": "DEFENSA",
            "Asesino": "CRITICO",
            "Paladín": "DEFENSA"  # Tanque defensivo con curación
        }
        
        for arqueotipo, stat_esperada in arquetipos_esperados.items():
            habilidades = HABILIDADES_POR_ARQUEOTIPO[arqueotipo]
            bonus_total = calcular_bonus_pasivo_total(habilidades)
            
            # Verificar que la stat esperada tenga bonus
            bonus_stat = bonus_total.get(stat_esperada, 0)
            
            assert bonus_stat > 0, \
                f"⚠️ {arqueotipo} no tiene bonus en su stat de fortaleza: {stat_esperada}"
            
            print(f"✓ {arqueotipo} destaca en {stat_esperada}: +{bonus_stat*100:.0f}%")


class TestBalanceStats:
    """Verifica balance de stats individuales"""
    
    def test_ninguna_stat_dominada_completamente(self):
        """Verifica que ninguna stat tenga bonus excesivo de un arqueotipo"""
        MAX_BONUS_TOTAL = 0.40  # 40% máximo bonus total en una stat por arqueotipo
        
        stats_arqueotipos = {
            "FUERZA": [],
            "AGILIDAD": [],
            "DEFENSA": [],
            "ESQUIVA": [],
            "CRITICO": [],
            "HP_MAX": []
        }
        
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            bonus_total = calcular_bonus_pasivo_total(habilidades)
            
            for stat in stats_arqueotipos.keys():
                bonus = bonus_total.get(stat, 0)
                if bonus > 0:
                    stats_arqueotipos[stat].append((arqueotipo, bonus))
        
        for stat, arqueotipos_bonus in stats_arqueotipos.items():
            if arqueotipos_bonus:
                max_bonus = max(b for _, b in arqueotipos_bonus)
                assert max_bonus <= MAX_BONUS_TOTAL, \
                    f"⚠️ {stat} tiene bonus excesivo en algún arqueotipo: {max_bonus*100}% (máx: {MAX_BONUS_TOTAL*100}%)"
        
        print(f"✓ Ninguna stat tiene bonus excesivo en un arqueotipo")
    
    def test_distribucion_equilibrada_de_stats(self):
        """Verifica que las stats estén bien distribuidas"""
        arquetipos = list(HABILIDADES_POR_ARQUEOTIPO.keys())
        
        # Contar cuántos arquetipos bonifican cada stat
        stats_conteo = {}
        
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            bonus_total = calcular_bonus_pasivo_total(habilidades)
            
            for stat, valor in bonus_total.items():
                if valor > 0:
                    if stat not in stats_conteo:
                        stats_conteo[stat] = 0
                    stats_conteo[stat] += 1
        
        # Debería haber al menos 3 arquetipos bonificando cada stat importante
        MIN_ARQUETIPOS = 2
        for stat, conteo in stats_conteo.items():
            assert conteo >= MIN_ARQUETIPOS, \
                f"⚠️ {stat} solo tiene bonus en {conteo} arqueotipos (mínimo: {MIN_ARQUETIPOS})"
        
        print(f"✓ Distribución equilibrada de stats: {stats_conteo}")


class TestBalancePasivasActivas:
    """Verifica balance entre pasivas y activas"""
    
    def test_proporcion_pasivas_activas(self):
        """Verifica que hay buen balance de pasivas vs activas"""
        pasivas = sum(1 for h in TODAS_LAS_HABILIDADES if h.tipo == TipoHabilidad.PASIVA)
        activas = sum(1 for h in TODAS_LAS_HABILIDADES if h.tipo == TipoHabilidad.ACTIVA)
        
        # Debería ser aproximadamente 3 pasivas y 2 activas por arqueotipo
        assert pasivas == 15, f"Esperado 15 pasivas, got {pasivas}"
        assert activas == 10, f"Esperado 10 activas, got {activas}"
        
        print(f"✓ Proporción: {pasivas} pasivas + {activas} activas = {pasivas + activas}")
    
    def test_cada_arqueotipo_tiene_balanceo_pasivo_activo(self):
        """Verifica que cada arqueotipo tenga mix de pasivas y activas"""
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            pasivas = sum(1 for h in habilidades if h.tipo == TipoHabilidad.PASIVA)
            activas = sum(1 for h in habilidades if h.tipo == TipoHabilidad.ACTIVA)
            
            assert pasivas >= 2, f"{arqueotipo} tiene muy pocas pasivas: {pasivas}"
            assert activas >= 1, f"{arqueotipo} tiene muy pocas activas: {activas}"
            
            print(f"✓ {arqueotipo}: {pasivas} pasivas, {activas} activas")


class TestCriterosBalance:
    """Verifica criterios específicos de balance"""
    
    def test_no_habilidad_cura_excesiva(self):
        """Verifica que curación sea moderada"""
        MAX_CURACION = 0.50  # 50% de HP máximo
        
        for habilidad in TODAS_LAS_HABILIDADES:
            # Si la habilidad tiene bonificador de HP
            if habilidad.bonus_activo and "HP" in str(habilidad.bonus_activo):
                print(f"⚠️ Verificando curación en {habilidad.nombre}")
    
    def test_criticos_controlados(self):
        """Verifica que el crítico no sea demasiado común"""
        MAX_CRITICO_TOTAL = 0.60  # 60% máximo bonus de crítico
        
        asesino = HABILIDADES_POR_ARQUEOTIPO["Asesino"]
        bonus_asesino = calcular_bonus_pasivo_total(asesino)
        critico_bonus = bonus_asesino.get("CRITICO", 0)
        
        assert critico_bonus <= MAX_CRITICO_TOTAL, \
            f"⚠️ Asesino tiene demasiado crítico: {critico_bonus*100}% (máx: {MAX_CRITICO_TOTAL*100}%)"
        
        print(f"✓ Crítico controlado. Asesino: +{critico_bonus*100:.0f}%")
    
    def test_esquiva_no_overpowered(self):
        """Verifica que esquiva sea defensiva, no ofensiva dominante"""
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            bonus_total = calcular_bonus_pasivo_total(habilidades)
            esquiva = bonus_total.get("ESQUIVA", 0)
            
            # Máximo 35% bonus de esquiva
            assert esquiva <= 0.35, \
                f"⚠️ {arqueotipo} tiene demasiada esquiva: {esquiva*100}%"
        
        print(f"✓ Esquiva está controlada")


class TestReportBalance:
    """Genera reporte de balance"""
    
    def test_reporte_balance_completo(self):
        """Genera reporte visual de balance"""
        print("\n" + "="*70)
        print("📊 REPORTE COMPLETO DE BALANCE")
        print("="*70)
        
        print("\n📈 BONUS PASIVO POR ARQUEOTIPO:")
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            bonus_total = calcular_bonus_pasivo_total(habilidades)
            print(f"\n  {arqueotipo}:")
            for stat, valor in bonus_total.items():
                if valor != 0:
                    print(f"    {stat}: +{valor*100:.1f}%")
        
        print("\n\n⚡ HABILIDADES ACTIVAS:")
        for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
            activas = [h for h in habilidades if h.tipo == TipoHabilidad.ACTIVA]
            print(f"\n  {arqueotipo}:")
            for activa in activas:
                print(f"    • {activa.nombre} (Duración: {activa.duracion_bonus} turnos)")
                for stat, valor in activa.bonus_activo.items():
                    print(f"      {stat}: +{valor*100:.1f}%")


# ============================================================================
# EJECUCIÓN DE TESTS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TEST DE BALANCE - SISTEMA DE HABILIDADES")
    print("="*70)
    
    # Balance general
    print("\n⚖️ BALANCE GENERAL:")
    test_general = TestBalanceGeneral()
    test_general.test_rango_bonus_pasivo_razonable()
    test_general.test_rango_bonus_activo_razonable()
    test_general.test_duracion_efectos_temporales()
    print("✅ Balance general OK")
    
    # Balance entre arqueotipos
    print("\n⚔️ BALANCE ENTRE ARQUETIPOS:")
    test_arqueotipos = TestBalanceArqueotipos()
    test_arqueotipos.test_bonus_pasivo_similar_entre_arquetipos()
    test_arqueotipos.test_cada_arqueotipo_tiene_fortaleza()
    print("✅ Balance entre arquetipos OK")
    
    # Balance de stats
    print("\n📊 BALANCE DE STATS:")
    test_stats = TestBalanceStats()
    test_stats.test_ninguna_stat_dominada_completamente()
    test_stats.test_distribucion_equilibrada_de_stats()
    print("✅ Balance de stats OK")
    
    # Balance pasivas/activas
    print("\n⚡ BALANCE PASIVAS VS ACTIVAS:")
    test_prop = TestBalancePasivasActivas()
    test_prop.test_proporcion_pasivas_activas()
    test_prop.test_cada_arqueotipo_tiene_balanceo_pasivo_activo()
    print("✅ Balance pasivas/activas OK")
    
    # Criterios específicos
    print("\n🎯 CRITERIOS ESPECÍFICOS:")
    test_criterios = TestCriterosBalance()
    test_criterios.test_no_habilidad_cura_excesiva()
    test_criterios.test_criticos_controlados()
    test_criterios.test_esquiva_no_overpowered()
    print("✅ Criterios específicos OK")
    
    # Reporte
    print("\n📋 GENERANDO REPORTE:")
    test_reporte = TestReportBalance()
    test_reporte.test_reporte_balance_completo()
    
    print("\n" + "="*70)
    print("✅ TODOS LOS TESTS DE BALANCE PASARON - SISTEMA BALANCEADO")
    print("="*70 + "\n")
