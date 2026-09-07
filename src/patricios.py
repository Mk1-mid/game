"""
Sistema de Patricios (Fase 3.2)
================================

Los patricios son los otros dueños de gladiadores de Roma: rivales y
aliados del jugador. Se generan UNA VEZ al crear la partida (5-7) y
evolucionan junto al jugador con simulación diaria ligera.

Cada patricio tiene:
- Su propio equipo de gladiadores (2-4, instancias reales de Gladiador)
- Honra propia (afecta qué eventos comparte contigo)
- Afinidad hacia ti (-100 enemigo jurado ... +100 aliado cercano)

La persistencia vive dentro del save del usuario (los patricios son
"tu mundo"), no en leaderboards globales.
"""

import random

from .models import Gladiador


NOMBRES_PATRICIOS = [
    "Quinto Fabio", "Cayo Julio", "Marco Licinio", "Aulo Cornelio",
    "Sexto Pompeyo", "Lucio Valerio", "Tito Flavio", "Numerio Claudio",
    "Servio Sulpicio", "Publio Emilio",
]

CIUDADES_ORIGEN = [
    "de Roma", "de Capua", "de Pompeya", "de Nápoles", "de Benevento",
    "de Tarento", "de Ostia", "de Brindisi",
]

PERSONALIDADES = [
    # (nombre, honra_inicial_min, honra_inicial_max, tono)
    ("honorable", 55, 75, "un hombre de palabra"),
    ("ambicioso", 35, 60, "siempre busca ventaja"),
    ("turbio", 10, 35, "se rumorea que amaña combates"),
]

NOMBRES_GLADIADORES_NPC = [
    "Brutus", "Crixus", "Spartacus", "Atticus", "Priscus", "Verus",
    "Flamma", "Tetraites", "Ursus", "Commodus", "Nero", "Draco",
]

TIPOS_GLADIADORES = ["Murmillo", "Retiarius", "Secutor", "Thraex", "Hoplomachus"]


class Patricio:
    """Un dueño de gladiadores rival: equipo, honra, afinidad y récords."""

    def __init__(self, nombre, honra, gladiadores=None, afinidad=0):
        """
        Args:
            nombre: Nombre completo (ej: "Cayo Julio de Capua")
            honra: 0-100, define su personalidad social
            gladiadores: Lista de Gladiador de su equipo
            afinidad: -100 (enemigo jurado) a +100 (aliado cercano)
        """
        self.nombre = nombre
        self.honra = honra
        self.afinidad = afinidad
        self.gladiadores = gladiadores or []
        self.victorias = 0
        self.derrotas = 0
        self.dinero_acumulado = 0

    def poder_equipo(self):
        """Poder bruto del equipo: suma de niveles + victorias. Base para simulación."""
        if not self.gladiadores:
            return 1
        return sum(g.nivel for g in self.gladiadores) + self.victorias // 3

    def mejor_gladiador(self):
        """Su gladiador estrella (mayor nivel y victorias). None si no tiene."""
        if not self.gladiadores:
            return None
        return max(self.gladiadores, key=lambda g: g.nivel + g.combates_ganados)

    def modificar_afinidad(self, delta):
        """Ajusta afinidad en rango -100..100. Retorna valor final."""
        self.afinidad = max(-100, min(100, self.afinidad + delta))
        return self.afinidad

    def __repr__(self):
        return f"Patricio({self.nombre}, honra={self.honra}, afinidad={self.afinidad}, {len(self.gladiadores)} gladiadores)"


# ============================================
# GESTOR
# ============================================

class GestorPatricios:
    """Genera y simula el mundo de patricios de una partida."""

    def __init__(self):
        self.patricios = []
        self.historial_npc = []  # Log de combates NPC (últimos 30)

    def generar_patricios(self, nivel_referencia=1, cantidad=None):
        """
        Genera 5-7 patricios con equipos iniciales cercanos al nivel del jugador.

        Args:
            nivel_referencia: Nivel del equipo del jugador al crear la partida
            cantidad: Fija el número (por defecto aleatorio 5-7)
        """
        if cantidad is None:
            cantidad = random.randint(5, 7)

        nombres = random.sample(NOMBRES_PATRICIOS, cantidad)
        for nombre_base in nombres:
            personalidad = random.choice(PERSONALIDADES)
            honra = random.randint(personalidad[1], personalidad[2])
            nombre = f"{nombre_base} {random.choice(CIUDADES_ORIGEN)}"

            # Equipo inicial: 2-4 gladiadores cerca del nivel del jugador
            n_glads = random.randint(2, 4)
            gladiadores = []
            nombres_usados = random.sample(NOMBRES_GLADIADORES_NPC, n_glads)
            for gname in nombres_usados:
                nivel = max(1, nivel_referencia + random.randint(-1, 1))
                gladiadores.append(
                    Gladiador(gname, random.choice(TIPOS_GLADIADORES), nivel=nivel)
                )

            p = Patricio(nombre, honra, gladiadores)
            # Afinidad inicial: ligeramente positiva con honorables, neutra con otros
            p.afinidad = random.randint(0, 20) if honra >= 55 else random.randint(-10, 15)
            self.patricios.append(p)

    def simular_dia(self):
        """
        Avanza la simulación del mundo patricio un día.

        - Cada patricio tiene probabilidad de ganar oro y XP según su poder.
        - Hay 1 combate NPC-vs-NPC al día (~35% de chance): afecta victorias.
        - Las afinidades hacia el jugador derivan suavemente (el mundo reacciona).

        Returns:
            list[str]: Mensajes de log del día (para mostrar al jugador).
        """
        log = []

        for p in self.patricios:
            # Progreso pasivo: su equipo entrena/gana fama
            if random.random() < 0.5:
                ganancia = random.randint(50, 150) + p.poder_equipo() * 5
                p.dinero_acumulado += ganancia

            # Su estrella gana experiencia
            estrella = p.mejor_gladiador()
            if estrella and random.random() < 0.4:
                estrella.ganar_xp(random.randint(20, 60))

        # Combate NPC vs NPC (resultado simplificado por poder + azar)
        if len(self.patricios) >= 2 and random.random() < 0.35:
            a, b = random.sample(self.patricios, 2)
            poder_a = a.poder_equipo() + random.uniform(0.5, 1.5)
            poder_b = b.poder_equipo() + random.uniform(0.5, 1.5)
            ganador, perdedor = (a, b) if poder_a >= poder_b else (b, a)

            ganador.victorias += 1
            perdedor.derrotas += 1
            bolsa = random.randint(100, 300)
            ganador.dinero_acumulado += bolsa

            entrada = (f"⚔️ {ganador.nombre} derrotó a {perdedor.nombre} "
                       f"en la arena de los patricios (+{bolsa}g)")
            self.historial_npc.append(entrada)
            self.historial_npc = self.historial_npc[-30:]
            log.append(entrada)

        return log

    def obtener_ranking(self):
        """Patricios ordenados por victorias (para mostrar en leaderboard local)."""
        return sorted(self.patricios, key=lambda p: p.victorias, reverse=True)

    def obtener_por_nombre(self, nombre):
        """Busca un patricio por su nombre exacto. None si no existe."""
        for p in self.patricios:
            if p.nombre == nombre:
                return p
        return None

    def rival_mas_fuerte(self, umbral_rivalidad=60):
        """
        El patricio con más rivalidad (afinidad <= -umbral_rivalidad... nota:
        afinidad negativa = rivalidad). None si nadie te odia tanto.
        """
        rivales = [p for p in self.patricios if p.afinidad <= -60]
        if not rivales:
            return None
        return min(rivales, key=lambda p: p.afinidad)

    # --- Persistencia ---

    def serializar(self):
        """Convierte el mundo de patricios a diccionario para JSON."""
        from .persistence import serializar_gladiador
        return {
            "patricios": [
                {
                    "nombre": p.nombre,
                    "honra": p.honra,
                    "afinidad": p.afinidad,
                    "victorias": p.victorias,
                    "derrotas": p.derrotas,
                    "dinero_acumulado": p.dinero_acumulado,
                    "gladiadores": [serializar_gladiador(g) for g in p.gladiadores],
                }
                for p in self.patricios
            ],
            "historial_npc": self.historial_npc,
        }

    def deserializar(self, data):
        """Restaura el mundo de patricios desde diccionario JSON."""
        from .persistence import deserializar_gladiador
        if not data:
            return
        self.patricios = []
        for pdata in data.get("patricios", []):
            gladiadores = [deserializar_gladiador(g) for g in pdata.get("gladiadores", [])]
            p = Patricio(
                nombre=pdata["nombre"],
                honra=pdata["honra"],
                gladiadores=gladiadores,
                afinidad=pdata.get("afinidad", 0),
            )
            p.victorias = pdata.get("victorias", 0)
            p.derrotas = pdata.get("derrotas", 0)
            p.dinero_acumulado = pdata.get("dinero_acumulado", 0)
            self.patricios.append(p)
        self.historial_npc = data.get("historial_npc", [])

    def __repr__(self):
        return f"GestorPatricios({len(self.patricios)} patricios)"
