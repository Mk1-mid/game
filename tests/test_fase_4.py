#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para Fase 4: Sistema de Torneos y Ligas Automáticas
"""

import unittest
from datetime import datetime, timedelta
from src.models import (
    Gladiador, Torneo, Emparejamiento, Temporada, 
    LigasAutomaticas, Liga
)


# ============================================
# TESTS - EMPAREJAMIENTOS
# ============================================

class TestEmparejamiento(unittest.TestCase):
    """Tests para emparejamientos individuales."""
    
    def test_crear_emparejamiento(self):
        """Crear emparejamiento entre dos participantes."""
        emp = Emparejamiento("Ferox", "Brutus", numero_ronda=1)
        self.assertEqual(emp.participante1, "Ferox")
        self.assertEqual(emp.participante2, "Brutus")
        self.assertEqual(emp.numero_ronda, 1)
        self.assertFalse(emp.completado)
        self.assertIsNone(emp.ganador)
    
    def test_completar_emparejamiento(self):
        """Marcar emparejamiento como completado."""
        emp = Emparejamiento("Ferox", "Brutus", numero_ronda=1)
        emp.completar("Ferox")
        
        self.assertTrue(emp.completado)
        self.assertEqual(emp.ganador, "Ferox")


# ============================================
# TESTS - TORNEOS
# ============================================

class TestTorneo(unittest.TestCase):
    """Tests para creación y gestión de torneos."""
    
    def setUp(self):
        """Preparar gladiadores para torneos."""
        self.g1 = Gladiador("Ferox", "Murmillo", nivel=5)
        self.g2 = Gladiador("Brutus", "Retiarius", nivel=5)
        self.g3 = Gladiador("Velox", "Murmillo", nivel=5)
        self.g4 = Gladiador("Rex", "Retiarius", nivel=5)
    
    def test_crear_torneo(self):
        """Crear torneo con 4 participantes."""
        participantes = [self.g1, self.g2, self.g3, self.g4]
        torneo = Torneo("Gran Torneo", participantes)
        
        self.assertEqual(torneo.nombre, "Gran Torneo")
        self.assertEqual(len(torneo.participantes), 4)
        self.assertEqual(torneo.estado, "creado")
        self.assertIsNone(torneo.ganador)
    
    def test_generar_brackets_4_participantes(self):
        """Generar brackets para 4 participantes (2 rondas)."""
        participantes = [self.g1, self.g2, self.g3, self.g4]
        torneo = Torneo("Torneo 4", participantes)
        
        # Debe haber 2 rondas: semifinales (2 emparejamientos) y final (1)
        self.assertEqual(len(torneo.rondas), 2)
        self.assertEqual(len(torneo.rondas[0]), 2)  # Semifinales
        self.assertEqual(len(torneo.rondas[1]), 1)  # Final
    
    def test_obtener_siguiente_emparejamiento(self):
        """Obtener siguiente emparejamiento sin completar."""
        participantes = [self.g1, self.g2, self.g3, self.g4]
        torneo = Torneo("Torneo", participantes)
        
        emp = torneo.obtener_siguiente_emparejamiento_pendiente()
        self.assertIsNotNone(emp)
        self.assertFalse(emp.completado)
    
    def test_completar_emparejamiento_torneo(self):
        """Completar un emparejamiento del torneo."""
        participantes = [self.g1, self.g2, self.g3, self.g4]
        torneo = Torneo("Torneo", participantes)
        
        # Completar primer emparejamiento
        emp_inicial = torneo.rondas[0][0]
        ganador_semifinal = emp_inicial.participante1
        
        torneo.completar_emparejamiento(ganador_semifinal)
        
        # Verificar que se marcó como completado
        self.assertTrue(torneo.rondas[0][0].completado)
        self.assertEqual(torneo.rondas[0][0].ganador, ganador_semifinal)
    
    def test_finalizar_torneo(self):
        """Completar un torneo hasta el ganador final."""
        participantes = [self.g1, self.g2, self.g3, self.g4]
        torneo = Torneo("Torneo Final", participantes)
        
        # Completar semifinales
        torneo.completar_emparejamiento(torneo.rondas[0][0].participante1)
        torneo.completar_emparejamiento(torneo.rondas[0][1].participante1)
        
        # Completar final
        emp_final = torneo.obtener_siguiente_emparejamiento_pendiente()
        if emp_final:
            ganador_final = emp_final.participante1
            torneo.completar_emparejamiento(ganador_final)
            
            self.assertEqual(torneo.ganador, ganador_final)
            self.assertEqual(torneo.estado, "finalizado")
    
    def test_obtener_estado_torneo(self):
        """Obtener estado actual del torneo."""
        participantes = [self.g1, self.g2, self.g3, self.g4]
        torneo = Torneo("Torneo Estado", participantes)
        
        estado = torneo.obtener_estado_torneo()
        
        self.assertEqual(estado["nombre"], "Torneo Estado")
        self.assertEqual(estado["total_participantes"], 4)
        self.assertEqual(estado["estado"], "creado")
        self.assertEqual(estado["emparejamientos_completados"], 0)
        self.assertGreater(estado["emparejamientos_totales"], 0)


# ============================================
# TESTS - TEMPORADAS
# ============================================

class TestTemporada(unittest.TestCase):
    """Tests para temporadas."""
    
    def test_crear_temporada(self):
        """Crear una temporada."""
        ahora = datetime.now()
        temp = Temporada(numero=1, fecha_inicio=ahora)
        
        self.assertEqual(temp.numero, 1)
        self.assertEqual(temp.fecha_inicio, ahora)
        self.assertIsNone(temp.fecha_fin)
        self.assertFalse(temp.finalizada)
    
    def test_finalizar_temporada(self):
        """Finalizar una temporada."""
        ahora = datetime.now()
        temp = Temporada(numero=1, fecha_inicio=ahora)
        
        temp.ranking_final = {"Ferox": 300, "Brutus": 200}
        temp.fecha_fin = datetime.now()
        temp.finalizada = True
        
        self.assertTrue(temp.finalizada)
        self.assertIsNotNone(temp.fecha_fin)
        self.assertGreater(len(temp.ranking_final), 0)


# ============================================
# TESTS - LIGAS AUTOMÁTICAS
# ============================================

class TestLigasAutomaticas(unittest.TestCase):
    """Tests para sistema de ligas automáticas."""
    
    def setUp(self):
        """Preparar sistema de ligas."""
        self.ligas = LigasAutomaticas()
    
    def test_inicializar_ligas(self):
        """Inicializar sistema de ligas automáticas."""
        self.assertEqual(self.ligas.temporada_actual, 1)
        self.assertEqual(len(self.ligas.temporadas), 1)
        self.assertEqual(len(self.ligas.ranking_temporal), 0)
    
    def test_actualizar_puntos(self):
        """Actualizar puntos de gladiador."""
        self.ligas.actualizar_puntos("Ferox", 50)
        self.ligas.actualizar_puntos("Ferox", 30)
        
        self.assertEqual(self.ligas.obtener_puntos_temporada("Ferox"), 80)
    
    def test_obtener_liga_por_puntos(self):
        """Obtener liga según puntos."""
        self.ligas.actualizar_puntos("Bronce", 50)
        self.ligas.actualizar_puntos("Plata", 150)
        self.ligas.actualizar_puntos("Oro", 300)
        self.ligas.actualizar_puntos("Leyenda", 600)
        
        self.assertEqual(self.ligas.obtener_liga_temporada("Bronce"), Liga.BRONCE)
        self.assertEqual(self.ligas.obtener_liga_temporada("Plata"), Liga.PLATA)
        self.assertEqual(self.ligas.obtener_liga_temporada("Oro"), Liga.ORO)
        self.assertEqual(self.ligas.obtener_liga_temporada("Leyenda"), Liga.LEYENDA)
    
    def test_obtener_ranking_temporada(self):
        """Obtener ranking ordenado de temporada."""
        self.ligas.actualizar_puntos("Ferox", 300)
        self.ligas.actualizar_puntos("Brutus", 200)
        self.ligas.actualizar_puntos("Velox", 400)
        
        ranking = self.ligas.obtener_ranking_temporada()
        
        self.assertEqual(ranking[0][0], "Velox")  # 400 pts
        self.assertEqual(ranking[1][0], "Ferox")  # 300 pts
        self.assertEqual(ranking[2][0], "Brutus") # 200 pts
    
    def test_calcular_recompensas_bronce(self):
        """Calcular recompensas para liga Bronce."""
        self.ligas.actualizar_puntos("Gladiador", 50)
        recompensas = self.ligas.calcular_recompensas_liga("Gladiador", None)
        
        self.assertEqual(recompensas["dinero"], 100)
    
    def test_calcular_recompensas_leyenda(self):
        """Calcular recompensas para liga Leyenda."""
        self.ligas.actualizar_puntos("Gladiador", 600)
        recompensas = self.ligas.calcular_recompensas_liga("Gladiador", None)
        
        self.assertEqual(recompensas["dinero"], 1000)
        self.assertIn("Equipo Legendario", recompensas["items"])
    
    def test_finalizar_temporada(self):
        """Finalizar temporada e iniciar nueva."""
        self.ligas.actualizar_puntos("Ferox", 200)
        self.ligas.actualizar_puntos("Brutus", 150)
        
        temporada_anterior = self.ligas.temporada_actual
        temp_finalizada = self.ligas.finalizar_temporada()
        
        # Verificar que temporada anterior se guardó
        self.assertTrue(temp_finalizada.finalizada)
        self.assertEqual(len(temp_finalizada.ranking_final), 2)
        
        # Verificar que nueva temporada empezó
        self.assertEqual(self.ligas.temporada_actual, temporada_anterior + 1)
        self.assertEqual(len(self.ligas.ranking_temporal), 0)  # Puntos reseteados
    
    def test_historial_temporadas(self):
        """Obtener historial de temporadas finalizadas."""
        self.ligas.actualizar_puntos("Ferox", 200)
        self.ligas.finalizar_temporada()
        
        self.ligas.actualizar_puntos("Brutus", 300)
        self.ligas.finalizar_temporada()
        
        historial = self.ligas.obtener_historial_temporadas()
        
        self.assertGreaterEqual(len(historial), 2)
        for num, temp in historial.items():
            self.assertTrue(temp.finalizada)


# ============================================
# TESTS - INTEGRACIÓN FASE 4
# ============================================

class TestIntegracionFase4(unittest.TestCase):
    """Tests de integración para Fase 4."""
    
    def test_flujo_completo_torneo(self):
        """Flujo completo: crear torneo, completar rondas, determinar ganador."""
        # Crear participantes
        g1 = Gladiador("Ferox", "Murmillo", nivel=5)
        g2 = Gladiador("Brutus", "Retiarius", nivel=5)
        g3 = Gladiador("Velox", "Murmillo", nivel=5)
        g4 = Gladiador("Rex", "Retiarius", nivel=5)
        
        # Crear torneo
        torneo = Torneo("Épico", [g1, g2, g3, g4])
        
        # Completar todas las rondas
        while torneo.ganador is None:
            emp = torneo.obtener_siguiente_emparejamiento_pendiente()
            if emp:
                torneo.completar_emparejamiento(emp.participante1)
        
        # Verificar resultado final
        self.assertIsNotNone(torneo.ganador)
        self.assertEqual(torneo.estado, "finalizado")
    
    def test_flujo_completo_ligas_automaticas(self):
        """Flujo: actualizar puntos, cambiar ligas, finalizar temporada."""
        ligas = LigasAutomaticas()
        
        # Simular combates
        for i in range(15):
            ligas.actualizar_puntos("Ferox", 20)  # 300 total = ORO
            ligas.actualizar_puntos("Brutus", 15)  # 225 total = PLATA
            ligas.actualizar_puntos("Velox", 8)   # 120 total = PLATA
        
        # Verificar ligas
        self.assertEqual(ligas.obtener_liga_temporada("Ferox"), Liga.ORO)
        self.assertEqual(ligas.obtener_liga_temporada("Brutus"), Liga.PLATA)
        self.assertEqual(ligas.obtener_liga_temporada("Velox"), Liga.PLATA)
        
        # Finalizar temporada
        temp = ligas.finalizar_temporada()
        
        # Verificar reset
        self.assertEqual(ligas.obtener_puntos_temporada("Ferox"), 0)
        self.assertEqual(ligas.temporada_actual, 2)


class TestTorneoEdgeCases(unittest.TestCase):
    """Tests edge cases para torneos."""
    
    def test_torneo_con_participantes_impares(self):
        """Torneo con número impar de participantes (3)."""
        g1 = Gladiador("Ferox", "Murmillo", nivel=5)
        g2 = Gladiador("Brutus", "Retiarius", nivel=5)
        g3 = Gladiador("Velox", "Murmillo", nivel=5)
        
        torneo = Torneo("Torneo 3", [g1, g2, g3])
        
        # Debe haber generado brackets válidos (próxima potencia de 2 es 4)
        self.assertGreater(len(torneo.rondas), 0)
        
        # Completar torneo
        while torneo.ganador is None:
            emp = torneo.obtener_siguiente_emparejamiento_pendiente()
            if emp:
                torneo.completar_emparejamiento(emp.participante1)
        
        self.assertIsNotNone(torneo.ganador)
    
    def test_torneo_8_participantes(self):
        """Torneo con 8 participantes."""
        participantes = []
        nombres = ["Ferox", "Brutus", "Velox", "Rex", "Agile", "Strong", "Swift", "Giant"]
        for nombre in nombres:
            participantes.append(Gladiador(nombre, "Murmillo", nivel=5))
        
        torneo = Torneo("Torneo 8", participantes)
        
        # Debe haber 3 rondas: 4 emparejamientos, 2 emparejamientos, 1 emparejamiento
        self.assertEqual(len(torneo.rondas), 3)


if __name__ == '__main__':
    unittest.main()
