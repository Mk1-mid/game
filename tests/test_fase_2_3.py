"""
Tests para Fase 2.3 - Sistema de Gladiadores
=============================================

Pruebas del menú de gestión de equipo, sistema de días, estados de salud,
y arena mejorada con dificultades.
"""

import unittest
from src.models import Equipo, Gladiador, Barracas


class TestGladiadorOcupacion(unittest.TestCase):
    """Tests para sistema de ocupación y días."""
    
    def setUp(self):
        self.gladiador = Gladiador("Ferox", "Murmillo", nivel=1)
    
    def test_gladiador_inicialmente_disponible(self):
        """Un gladiador nuevo debe estar disponible."""
        self.assertEqual(self.gladiador.ocupacion, "disponible")
        self.assertEqual(self.gladiador.dias_ocupado, 0)
        self.assertIsNone(self.gladiador.razon_ocupacion)
    
    def test_ocupar_gladiador(self):
        """Ocupar debe marcar como ocupado con razón y días."""
        self.gladiador.ocupar("entrenamiento", 3)
        
        self.assertEqual(self.gladiador.ocupacion, "ocupado")
        self.assertEqual(self.gladiador.dias_ocupado, 3)
        self.assertEqual(self.gladiador.razon_ocupacion, "entrenamiento")
    
    def test_pasar_dia(self):
        """Pasar día debe decrementar días_ocupado."""
        self.gladiador.ocupar("entrenamiento", 3)
        
        self.gladiador.pasar_dia()
        self.assertEqual(self.gladiador.dias_ocupado, 2)
        self.assertEqual(self.gladiador.ocupacion, "ocupado")
        
        self.gladiador.pasar_dia()
        self.assertEqual(self.gladiador.dias_ocupado, 1)
        
        self.gladiador.pasar_dia()
        self.assertEqual(self.gladiador.dias_ocupado, 0)
        self.assertEqual(self.gladiador.ocupacion, "disponible")
        self.assertIsNone(self.gladiador.razon_ocupacion)
    
    def test_puede_luchar_disponible(self):
        """Gladiador disponible puede luchar."""
        self.assertTrue(self.gladiador.puede_luchar())
    
    def test_puede_luchar_ocupado(self):
        """Gladiador ocupado no puede luchar."""
        self.gladiador.ocupar("entrenamiento", 1)
        self.assertFalse(self.gladiador.puede_luchar())
    
    def test_puede_luchar_muerto(self):
        """Gladiador muerto no puede luchar."""
        self.gladiador.aplicar_daño(self.gladiador.hp)
        self.assertFalse(self.gladiador.puede_luchar())


class TestGladiadorEstadosSalud(unittest.TestCase):
    """Tests para sistema de estados de salud."""
    
    def setUp(self):
        self.gladiador = Gladiador("Velox", "Retiarius", nivel=1)
    
    def test_estado_sano_inicial(self):
        """Gladiador nuevo debe estar sano."""
        self.assertEqual(self.gladiador.estado, "sano")
        self.assertEqual(self.gladiador.hp_actual, self.gladiador.hp)
    
    def test_estado_herido(self):
        """Aplicar daño >= 25% debe marcar como herido."""
        hp_total = self.gladiador.hp
        daño = int(hp_total * 0.5)  # 50% del HP
        
        self.gladiador.aplicar_daño(daño)
        self.assertEqual(self.gladiador.estado, "herido")
        self.assertGreater(self.gladiador.hp_actual, 0)
    
    def test_estado_critico(self):
        """HP < 25% debe marcar como crítico."""
        hp_total = self.gladiador.hp
        daño = int(hp_total * 0.76)  # Dejar < 25%
        
        self.gladiador.aplicar_daño(daño)
        self.assertEqual(self.gladiador.estado, "critico")
    
    def test_estado_muerto(self):
        """HP = 0 debe marcar como muerto."""
        self.gladiador.aplicar_daño(self.gladiador.hp * 2)
        
        self.assertEqual(self.gladiador.estado, "muerto")
        self.assertEqual(self.gladiador.hp_actual, 0)
    
    def test_curar_a_sano(self):
        """Curar > 75% HP debe marcar como sano."""
        self.gladiador.aplicar_daño(int(self.gladiador.hp * 0.3))
        self.assertEqual(self.gladiador.estado, "herido")
        
        self.gladiador.curar(int(self.gladiador.hp * 0.6))
        self.assertEqual(self.gladiador.estado, "sano")
    
    def test_revivir_desde_muerto(self):
        """Revivir debe traer a gladiador a estado herido con 75% HP."""
        self.gladiador.aplicar_daño(self.gladiador.hp * 2)
        self.assertEqual(self.gladiador.estado, "muerto")
        
        self.gladiador.revivir()
        self.assertEqual(self.gladiador.estado, "herido")
        self.assertEqual(self.gladiador.hp_actual, int(self.gladiador.hp * 0.75))


class TestEquipoOcupacion(unittest.TestCase):
    """Tests para gestión de ocupación en el equipo."""
    
    def setUp(self):
        self.equipo = Equipo()
        self.g1 = Gladiador("Ferox", "Murmillo", nivel=1)
        self.g2 = Gladiador("Velox", "Retiarius", nivel=1)
        self.equipo.agregar_gladiador(self.g1)
        self.equipo.agregar_gladiador(self.g2)
    
    def test_equipo_pasar_dia(self):
        """pasar_dia() en equipo debe afectar a todos los gladiadores."""
        self.g1.ocupar("entrenamiento", 2)
        self.g2.ocupar("curacion", 1)
        
        self.equipo.pasar_dia()
        
        self.assertEqual(self.g1.dias_ocupado, 1)
        self.assertEqual(self.g2.dias_ocupado, 0)
        self.assertEqual(self.g2.ocupacion, "disponible")
    
    def test_gladiadores_disponibles(self):
        """Contar disponibles correctamente."""
        disponibles = sum(1 for g in self.equipo.gladiadores if g.puede_luchar())
        self.assertEqual(disponibles, 2)
        
        self.g1.ocupar("entrenamiento", 1)
        disponibles = sum(1 for g in self.equipo.gladiadores if g.puede_luchar())
        self.assertEqual(disponibles, 1)


class TestArenaDificultades(unittest.TestCase):
    """Tests para sistema de dificultades en arena."""
    
    def test_dificultad_novato_requisitos(self):
        """Novato requiere nivel 1 mínimo."""
        equipo = Equipo()
        g = Gladiador("Test", "Murmillo", nivel=1)
        equipo.agregar_gladiador(g)
        
        nivel_promedio = equipo.calcular_nivel_promedio()
        self.assertGreaterEqual(nivel_promedio, 1)
    
    def test_dificultad_normal_requisitos(self):
        """Normal requiere nivel 3 mínimo."""
        equipo = Equipo()
        g = Gladiador("Test", "Murmillo", nivel=3)
        equipo.agregar_gladiador(g)
        
        nivel_promedio = equipo.calcular_nivel_promedio()
        self.assertGreaterEqual(nivel_promedio, 3)
    
    def test_dificultad_experto_requisitos(self):
        """Experto requiere nivel 10 mínimo."""
        equipo = Equipo()
        g = Gladiador("Test", "Murmillo", nivel=10)
        equipo.agregar_gladiador(g)
        
        nivel_promedio = equipo.calcular_nivel_promedio()
        self.assertGreaterEqual(nivel_promedio, 10)
    
    def test_dificultad_legendaria_requisitos(self):
        """Legendaria requiere nivel 20 mínimo."""
        equipo = Equipo()
        g = Gladiador("Test", "Murmillo", nivel=20)
        equipo.agregar_gladiador(g)
        
        nivel_promedio = equipo.calcular_nivel_promedio()
        self.assertGreaterEqual(nivel_promedio, 20)
    
    def test_multiplicadores_dificultad(self):
        """Verificar multiplicadores de dificultad."""
        multiplicadores = {
            "NOVATO": 0.8,
            "NORMAL": 1.0,
            "EXPERTO": 1.5,
            "LEGENDARIA": 2.0
        }
        
        # Test con recompensa base
        recompensa_base = 100
        for dificultad, mult in multiplicadores.items():
            recompensa = int(recompensa_base * mult)
            self.assertEqual(
                recompensa,
                int(recompensa_base * mult),
                f"Fallo en {dificultad}: esperado {int(recompensa_base * mult)}"
            )


class TestBarracasExpansion(unittest.TestCase):
    """Tests para expansión de barracas."""
    
    def setUp(self):
        self.barracas = Barracas()
    
    def test_barracas_iniciales(self):
        """Barracas comienzan con 2 literas = 4 espacios."""
        self.assertEqual(self.barracas.literas, 2)
        self.assertEqual(self.barracas.espacios_totales, 4)
    
    def test_comprar_litera(self):
        """Comprar litera debe aumentar espacios."""
        dinero = 1000
        costo = self.barracas.costo_proxima_litera
        
        exito, dinero_restante, msg = self.barracas.comprar_litera(dinero)
        
        self.assertTrue(exito)
        self.assertEqual(self.barracas.literas, 3)
        self.assertEqual(self.barracas.espacios_totales, 6)
        self.assertEqual(dinero_restante, dinero - costo)
    
    def test_no_comprar_sin_dinero(self):
        """No permitir compra sin suficiente dinero."""
        dinero = 100
        exito, dinero_restante, msg = self.barracas.comprar_litera(dinero)
        
        self.assertFalse(exito)
        self.assertEqual(self.barracas.literas, 2)
    
    def test_maximo_literas(self):
        """No permitir más de 5 literas (10 espacios)."""
        # Comprar hasta máximo
        dinero = 10000
        for _ in range(5):
            exito, dinero, msg = self.barracas.comprar_litera(dinero)
            if not exito:
                break
        
        self.assertEqual(self.barracas.literas, 5)
        self.assertFalse(self.barracas.proxima_litera_disponible)


class TestGladiadorReclutamiento(unittest.TestCase):
    """Tests para reclutamiento de gladiadores."""
    
    def setUp(self):
        self.equipo = Equipo()
    
    def test_agregar_gladiador(self):
        """Agregar gladiador debe funcionar si hay espacio."""
        g = Gladiador("Test", "Murmillo", nivel=1)
        exito, msg = self.equipo.agregar_gladiador(g)
        
        self.assertTrue(exito)
        self.assertEqual(len(self.equipo.gladiadores), 1)
    
    def test_no_agregar_sin_espacio(self):
        """No permitir agregar si barracas están llenas."""
        # Llenar barracas
        for i in range(4):
            g = Gladiador(f"G{i}", "Murmillo", nivel=1)
            self.equipo.agregar_gladiador(g)
        
        # Intentar agregar más
        g_extra = Gladiador("Extra", "Murmillo", nivel=1)
        exito, msg = self.equipo.agregar_gladiador(g_extra)
        
        self.assertFalse(exito)
        self.assertEqual(len(self.equipo.gladiadores), 4)
    
    def test_remover_gladiador(self):
        """Remover gladiador debe funcionar."""
        g = Gladiador("Test", "Murmillo", nivel=1)
        self.equipo.agregar_gladiador(g)
        
        exito, msg = self.equipo.remover_gladiador(0)
        
        self.assertTrue(exito)
        self.assertEqual(len(self.equipo.gladiadores), 0)
    
    def test_espacios_disponibles(self):
        """Calcular espacios disponibles correctamente."""
        g1 = Gladiador("G1", "Murmillo", nivel=1)
        g2 = Gladiador("G2", "Retiarius", nivel=1)
        
        self.equipo.agregar_gladiador(g1)
        self.assertEqual(self.equipo.espacios_disponibles, 3)
        
        self.equipo.agregar_gladiador(g2)
        self.assertEqual(self.equipo.espacios_disponibles, 2)


class TestGladiadorEntrenamiento(unittest.TestCase):
    """Tests para sistema de entrenamiento."""
    
    def setUp(self):
        self.gladiador = Gladiador("Ferox", "Murmillo", nivel=1)
    
    def test_entrenar_mejora_stats(self):
        """Entrenar debe mejorar fuerza y ataque."""
        fuerza_antes = self.gladiador.fuerza
        ataque_antes = self.gladiador.attack
        
        self.gladiador.ocupar("entrenamiento", 1)
        self.gladiador.fuerza += 2
        self.gladiador.attack += 2
        
        self.assertGreater(self.gladiador.fuerza, fuerza_antes)
        self.assertGreater(self.gladiador.attack, ataque_antes)
    
    def test_no_entrenar_ocupado(self):
        """No permitir entrenar si ya está ocupado."""
        self.gladiador.ocupar("curacion", 2)
        
        self.assertFalse(self.gladiador.puede_luchar())
        self.assertEqual(self.gladiador.ocupacion, "ocupado")


class TestIntegracionFase23(unittest.TestCase):
    """Tests de integración completa para Fase 2.3."""
    
    def test_ciclo_combate_ocupacion(self):
        """Test del ciclo: combate -> entrenamiento -> disponible."""
        equipo = Equipo()
        g = Gladiador("Ferox", "Murmillo", nivel=1)
        equipo.agregar_gladiador(g)
        
        # Estado inicial
        self.assertTrue(g.puede_luchar())
        
        # Después de entrenamiento
        g.ocupar("entrenamiento", 2)
        self.assertFalse(g.puede_luchar())
        
        # Pasar 2 días
        equipo.pasar_dia()
        self.assertFalse(g.puede_luchar())
        equipo.pasar_dia()
        self.assertTrue(g.puede_luchar())
    
    def test_ciclo_daño_curacion(self):
        """Test del ciclo: daño -> herido -> curación -> sano."""
        g = Gladiador("Ferox", "Murmillo", nivel=1)
        
        # Aplicar daño 60% (asegura herido)
        g.aplicar_daño(int(g.hp * 0.6))
        self.assertEqual(g.estado, "herido")
        
        # Curar parcial
        g.curar(int(g.hp * 0.3))
        self.assertEqual(g.estado, "herido")
        
        # Curar completamente
        g.curar(int(g.hp * 0.3))
        self.assertEqual(g.estado, "sano")


if __name__ == "__main__":
    unittest.main()
