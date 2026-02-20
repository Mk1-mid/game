"""
Tests para Fase 2.4 - Sistema de Ligas y Ranking
=================================================

Pruebas del sistema de ligas, ranking, historial de combates
y estadísticas de gladiadores.
"""

import unittest
from datetime import datetime
from src.models import Equipo, Gladiador, SistemaLigas, Liga, CombateHistorial


class TestCombateHistorial(unittest.TestCase):
    """Tests para historial de combates."""
    
    def test_crear_combate_historial(self):
        """Crear registro de combate."""
        combate = CombateHistorial(
            nombre_gladiador="Ferox",
            nombre_enemigo="Enemigo Básico",
            dificultad="🟡 NORMAL",
            victoria=True,
            puntos_ganados=20,
            xp_ganados=50,
            dinero_ganado=100,
            nivel_gladiador=1
        )
        
        self.assertEqual(combate.nombre_gladiador, "Ferox")
        self.assertEqual(combate.nombre_enemigo, "Enemigo Básico")
        self.assertTrue(combate.victoria)
        self.assertEqual(combate.puntos_ganados, 20)
    
    def test_combate_derrota(self):
        """Registrar derrota."""
        combate = CombateHistorial(
            nombre_gladiador="Velox",
            nombre_enemigo="Enemigo Fuerte",
            dificultad="🔴 EXPERTO",
            victoria=False,
            puntos_ganados=10,
            xp_ganados=25,
            dinero_ganado=0,
            nivel_gladiador=5
        )
        
        self.assertFalse(combate.victoria)
        self.assertEqual(combate.dinero_ganado, 0)


class TestSistemaLigas(unittest.TestCase):
    """Tests para sistema de ligas."""
    
    def setUp(self):
        self.sistema = SistemaLigas()
        self.gladiador = Gladiador("Ferox", "Murmillo", nivel=1)
    
    def test_registrar_combate_victoria(self):
        """Registrar victoria aumenta puntos."""
        puntos, xp, dinero = self.sistema.registrar_combate(
            self.gladiador,
            "Enemigo Básico",
            "🟡 NORMAL",
            victoria=True
        )
        
        self.assertEqual(puntos, 20)
        self.assertEqual(xp, 50)
        self.assertEqual(dinero, 100)
        self.assertEqual(self.sistema.obtener_puntos("Ferox"), 20)
    
    def test_registrar_combate_derrota(self):
        """Registrar derrota da menos puntos."""
        puntos, xp, dinero = self.sistema.registrar_combate(
            self.gladiador,
            "Enemigo Fuerte",
            "🟡 NORMAL",
            victoria=False
        )
        
        self.assertEqual(puntos, 10)  # 20 / 2
        self.assertEqual(xp, 25)
        self.assertEqual(dinero, 0)
    
    def test_multiplier_dificultad_novato(self):
        """Novato multiplica correctamente."""
        puntos, _, _ = self.sistema.registrar_combate(
            self.gladiador,
            "Enemigo",
            "🟢 NOVATO",
            victoria=True
        )
        
        self.assertEqual(puntos, 10)  # 10 base
    
    def test_multiplier_dificultad_normal(self):
        """Normal multiplica correctamente."""
        puntos, _, _ = self.sistema.registrar_combate(
            self.gladiador,
            "Enemigo",
            "🟡 NORMAL",
            victoria=True
        )
        
        self.assertEqual(puntos, 20)
    
    def test_multiplier_dificultad_experto(self):
        """Experto multiplica correctamente."""
        puntos, _, _ = self.sistema.registrar_combate(
            self.gladiador,
            "Enemigo",
            "🔴 EXPERTO",
            victoria=True
        )
        
        self.assertEqual(puntos, 40)
    
    def test_multiplier_dificultad_legendaria(self):
        """Legendaria multiplica correctamente."""
        puntos, _, _ = self.sistema.registrar_combate(
            self.gladiador,
            "Enemigo",
            "⭐ LEGENDARIA",
            victoria=True
        )
        
        self.assertEqual(puntos, 80)


class TestLigas(unittest.TestCase):
    """Tests para sistema de ligas."""
    
    def test_liga_bronce(self):
        """0-99 puntos = Bronce."""
        sistema = SistemaLigas()
        g = Gladiador("Test", "Murmillo", nivel=1)
        
        sistema.registrar_combate(g, "Enemigo", "🟢 NOVATO", True)  # 10pts
        self.assertEqual(sistema.obtener_liga("Test"), Liga.BRONCE)
    
    def test_liga_plata(self):
        """100-249 puntos = Plata."""
        sistema = SistemaLigas()
        g = Gladiador("Test", "Murmillo", nivel=1)
        
        for _ in range(6):
            sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", True)  # 20pts c/u
        
        puntos = sistema.obtener_puntos("Test")
        self.assertGreaterEqual(puntos, 100)
        self.assertEqual(sistema.obtener_liga("Test"), Liga.PLATA)
    
    def test_liga_oro(self):
        """250-499 puntos = Oro."""
        sistema = SistemaLigas()
        g = Gladiador("Test", "Murmillo", nivel=1)
        
        for _ in range(7):
            sistema.registrar_combate(g, "Enemigo", "🔴 EXPERTO", True)  # 40pts c/u
        
        puntos = sistema.obtener_puntos("Test")
        self.assertGreaterEqual(puntos, 250)
        self.assertEqual(sistema.obtener_liga("Test"), Liga.ORO)
    
    def test_liga_leyenda(self):
        """500+ puntos = Leyenda."""
        sistema = SistemaLigas()
        g = Gladiador("Test", "Murmillo", nivel=1)
        
        for _ in range(7):
            sistema.registrar_combate(g, "Enemigo", "⭐ LEGENDARIA", True)  # 80pts c/u
        
        puntos = sistema.obtener_puntos("Test")
        self.assertGreaterEqual(puntos, 500)
        self.assertEqual(sistema.obtener_liga("Test"), Liga.LEYENDA)


class TestWinrate(unittest.TestCase):
    """Tests para cálculo de winrate."""
    
    def test_winrate_100_porciento(self):
        """5 victorias = 100% winrate."""
        sistema = SistemaLigas()
        g = Gladiador("Test", "Murmillo", nivel=1)
        
        for _ in range(5):
            sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", True)
        
        winrate = sistema.obtener_winrate("Test")
        self.assertEqual(winrate, 100)
    
    def test_winrate_50_porciento(self):
        """2 victorias, 2 derrotas = 50% winrate."""
        sistema = SistemaLigas()
        g = Gladiador("Test", "Murmillo", nivel=1)
        
        sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", True)
        sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", False)
        sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", True)
        sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", False)
        
        winrate = sistema.obtener_winrate("Test")
        self.assertEqual(winrate, 50)
    
    def test_winrate_0_porciento(self):
        """5 derrotas = 0% winrate."""
        sistema = SistemaLigas()
        g = Gladiador("Test", "Murmillo", nivel=1)
        
        for _ in range(5):
            sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", False)
        
        winrate = sistema.obtener_winrate("Test")
        self.assertEqual(winrate, 0)


class TestRanking(unittest.TestCase):
    """Tests para ranking de gladiadores."""
    
    def test_ranking_top_10(self):
        """Obtener top 10 gladiadores."""
        sistema = SistemaLigas()
        
        # Crear 15 gladiadores
        for i in range(15):
            g = Gladiador(f"Glad{i}", "Murmillo", nivel=i+1)
            for j in range(i):
                sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", True)
        
        top10 = sistema.obtener_ranking_top10()
        self.assertEqual(len(top10), 10)
        
        # Verificar orden descendente
        for i in range(len(top10) - 1):
            self.assertGreater(top10[i][1]["puntos"], top10[i+1][1]["puntos"])
    
    def test_ranking_orden_correcto(self):
        """Ranking ordenado por puntos descendente."""
        sistema = SistemaLigas()
        
        g1 = Gladiador("Débil", "Murmillo", nivel=1)
        g2 = Gladiador("Fuerte", "Murmillo", nivel=1)
        
        # Débil: 20 puntos
        sistema.registrar_combate(g1, "Enemigo", "🟡 NORMAL", True)
        
        # Fuerte: 80 puntos
        sistema.registrar_combate(g2, "Enemigo", "⭐ LEGENDARIA", True)
        
        top = sistema.obtener_ranking_top10()
        self.assertEqual(top[0][0], "Fuerte")
        self.assertEqual(top[1][0], "Débil")


class TestHistorial(unittest.TestCase):
    """Tests para historial de combates."""
    
    def test_historial_global(self):
        """Obtener historial completo."""
        sistema = SistemaLigas()
        g = Gladiador("Test", "Murmillo", nivel=1)
        
        for i in range(5):
            victoria = i % 2 == 0
            sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", victoria)
        
        historial = sistema.obtener_historial(limite=10)
        self.assertEqual(len(historial), 5)
    
    def test_historial_filtrado(self):
        """Obtener historial filtrado por gladiador."""
        sistema = SistemaLigas()
        g1 = Gladiador("Glad1", "Murmillo", nivel=1)
        g2 = Gladiador("Glad2", "Retiarius", nivel=1)
        
        sistema.registrar_combate(g1, "Enemigo", "🟡 NORMAL", True)
        sistema.registrar_combate(g2, "Enemigo", "🟡 NORMAL", True)
        sistema.registrar_combate(g1, "Enemigo", "🟡 NORMAL", False)
        
        historial_g1 = sistema.obtener_historial("Glad1", limite=10)
        self.assertEqual(len(historial_g1), 2)
        self.assertTrue(all(c.nombre_gladiador == "Glad1" for c in historial_g1))
    
    def test_historial_limite(self):
        """Respetar límite de combates."""
        sistema = SistemaLigas()
        g = Gladiador("Test", "Murmillo", nivel=1)
        
        for i in range(20):
            sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", True)
        
        historial_5 = sistema.obtener_historial(limite=5)
        self.assertEqual(len(historial_5), 5)


class TestReporteEstadisticas(unittest.TestCase):
    """Tests para reporte de estadísticas."""
    
    def test_reporte_completo(self):
        """Generar reporte completo."""
        sistema = SistemaLigas()
        g = Gladiador("Ferox", "Murmillo", nivel=5)
        
        sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", True)
        sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", True)
        sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", False)
        
        reporte = sistema.generar_reporte_estadisticas("Ferox")
        
        self.assertEqual(reporte["nombre"], "Ferox")
        self.assertEqual(reporte["victorias"], 2)
        self.assertEqual(reporte["derrotas"], 1)
        self.assertEqual(reporte["combates"], 3)
        self.assertEqual(reporte["winrate"], 66)  # 2/3 = 66%
    
    def test_reporte_inexistente(self):
        """Reporte de gladiador sin combates."""
        sistema = SistemaLigas()
        
        reporte = sistema.generar_reporte_estadisticas("NoExiste")
        self.assertIsNone(reporte)


class TestIntegracionFase24(unittest.TestCase):
    """Tests de integración para Fase 2.4."""
    
    def test_flujo_completo(self):
        """Test del flujo completo: múltiples combates y cambios de liga."""
        sistema = SistemaLigas()
        equipo = Equipo()
        
        g1 = Gladiador("Campeón", "Murmillo", nivel=1)
        g2 = Gladiador("Novato", "Retiarius", nivel=1)
        
        equipo.agregar_gladiador(g1)
        equipo.agregar_gladiador(g2)
        
        # Campeón gana varios combates (15 x 20 = 300 = ORO)
        for _ in range(15):
            sistema.registrar_combate(g1, "Enemigo", "🟡 NORMAL", True)
        
        # Novato gana pocos
        for _ in range(2):
            sistema.registrar_combate(g2, "Enemigo", "🟢 NOVATO", True)
        
        # Verificar ranking
        ranking = sistema.obtener_ranking_top10()
        self.assertEqual(ranking[0][0], "Campeón")
        self.assertEqual(ranking[1][0], "Novato")
        
        # Verificar ligas
        self.assertEqual(sistema.obtener_liga("Campeón"), Liga.ORO)  # 300 pts = ORO
        self.assertEqual(sistema.obtener_liga("Novato"), Liga.BRONCE)
    
    def test_progresion_liga(self):
        """Test de progresión: Bronce -> Plata -> Oro -> Leyenda."""
        sistema = SistemaLigas()
        g = Gladiador("Progresivo", "Murmillo", nivel=1)
        
        # Bronce (0-99)
        sistema.registrar_combate(g, "Enemigo", "🟢 NOVATO", True)
        self.assertEqual(sistema.obtener_liga("Progresivo"), Liga.BRONCE)
        
        # Plata (100-249)
        for _ in range(5):
            sistema.registrar_combate(g, "Enemigo", "🟡 NORMAL", True)
        self.assertEqual(sistema.obtener_liga("Progresivo"), Liga.PLATA)
        
        # Oro (250-499)
        for _ in range(7):
            sistema.registrar_combate(g, "Enemigo", "🔴 EXPERTO", True)
        self.assertEqual(sistema.obtener_liga("Progresivo"), Liga.ORO)
        
        # Leyenda (500+)
        for _ in range(7):
            sistema.registrar_combate(g, "Enemigo", "⭐ LEGENDARIA", True)
        self.assertEqual(sistema.obtener_liga("Progresivo"), Liga.LEYENDA)


if __name__ == "__main__":
    unittest.main()
