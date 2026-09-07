"""
Sistema de Leaderboards Globales (Fase 3.1)
============================================

Rankings compartidos entre TODOS los usuarios del juego.
A diferencia del sistema de ligas (que es por gladiador, por partida),
los leaderboards comparan jugadores (usuarios) entre sí globalmente.

Por eso se guardan en un archivo global (data/leaderboards_global.json)
y no dentro del save de cada usuario: un jugador no debería poder
borrar los registros de otro al sobreescribir su partida.

Se registran máximos históricos (no valores actuales): si un jugador
tuvo 5000g y ahora tiene 100g, su récord en el ranking sigue siendo 5000g.
Así el ranking premia logros alcanzados, no el estado momentáneo.
"""

import json
import os


ARCHIVO_LEADERBOARDS = "data/leaderboards_global.json"

# Categorías disponibles. Mantenerlas centralizadas evita errores de tipeo
# al pedir un ranking inexistente desde el menú o los tests.
CATEGORIAS = ("victorias", "dinero", "nivel")


class LeaderboardsGlobales:
    """Gestiona los rankings Top 10 compartidos entre todos los usuarios."""

    def __init__(self, archivo=ARCHIVO_LEADERBOARDS):
        """
        Args:
            archivo: Ruta al JSON global (parametrizable para tests).
        """
        self.archivo = archivo
        # {usuario: {"victorias": int, "dinero": int, "nivel": int}}
        self.registros = {}
        self._cargar()

    def _cargar(self):
        """Lee el JSON global sin romper si está corrupto o no existe."""
        if not os.path.exists(self.archivo):
            return
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.registros = datos.get("registros", {})
        except json.JSONDecodeError:
            # Un archivo corrupto no debe tumbar el juego: empezamos vacío
            self.registros = {}

    def _guardar(self):
        """Escribe el JSON global, creando el directorio si hace falta."""
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump({"registros": self.registros}, f, indent=4, ensure_ascii=False)

    def actualizar_jugador(self, usuario, victorias, dinero, nivel_maximo, titulo=None):
        """
        Actualiza los récords de un usuario (guarda el máximo histórico).

        Args:
            usuario: Nombre de usuario
            victorias: Victorias totales actuales de su equipo
            dinero: Dinero actual del equipo
            nivel_maximo: Nivel del mejor gladiador del equipo
            titulo: Título de honra (ej: "El Honorable", "El Corrupto de Roma")

        Returns:
            (True, 0, mensaje) siguiendo el patrón (éxito, costo, mensaje).
        """
        if not usuario or not isinstance(usuario, str):
            return False, 0, "❌ Usuario inválido"

        actual = self.registros.get(usuario, {"victorias": 0, "dinero": 0, "nivel": 1, "titulo": None})

        self.registros[usuario] = {
            "victorias": max(actual["victorias"], max(0, int(victorias))),
            "dinero": max(actual["dinero"], max(0, int(dinero))),
            "nivel": max(actual["nivel"], max(1, int(nivel_maximo))),
            "titulo": titulo if titulo else actual.get("titulo"),
        }

        self._guardar()
        return True, 0, f"✓ Récords de {usuario} actualizados"

    def obtener_top(self, categoria, limite=10):
        """
        Retorna el Top N de una categoría ordenado de mayor a menor.

        Args:
            categoria: "victorias", "dinero" o "nivel"
            limite: Tamaño del ranking (por defecto Top 10)

        Returns:
            Lista de tuplas [(usuario, valor), ...]. Lista vacía si la
            categoría no existe (el menú decide cómo mostrarlo).
        """
        if categoria not in CATEGORIAS:
            return []

        ordenado = sorted(
            self.registros.items(),
            key=lambda item: item[1].get(categoria, 0),
            reverse=True
        )
        return [(usuario, datos[categoria]) for usuario, datos in ordenado[:limite]]

    def obtener_posicion(self, usuario, categoria):
        """
        Retorna la posición de un usuario en una categoría (1 = primero).

        Returns:
            int o None si el usuario no está registrado o la categoría es inválida.
        """
        if categoria not in CATEGORIAS or usuario not in self.registros:
            return None

        valor_usuario = self.registros[usuario][categoria]
        superiores = sum(
            1 for datos in self.registros.values()
            if datos.get(categoria, 0) > valor_usuario
        )
        return superiores + 1

    def generar_string_ranking(self, categoria, limite=10):
        """
        Genera el ranking formateado para mostrar en consola.

        Args:
            categoria: "victorias", "dinero" o "nivel"

        Returns:
            str con el ranking listo para imprimir.
        """
        titulos = {
            "victorias": "🏆 TOP VICTORIAS",
            "dinero": "💰 TOP FORTUNA",
            "nivel": "⭐ TOP NIVEL MÁXIMO",
        }

        if categoria not in CATEGORIAS:
            return "❌ Categoría inválida"

        unidad = {"victorias": "victorias", "dinero": "g", "nivel": "nivel"}[categoria]
        lineas = ["=" * 50, titulos[categoria].center(50), "=" * 50]

        top = self.obtener_top(categoria, limite)
        if not top:
            lineas.append("\n   Aún no hay registros. ¡Sé el primero en jugar!")
        else:
            for pos, (usuario, valor) in enumerate(top, 1):
                medalla = {1: "🥇", 2: "🥈", 3: "🥉"}.get(pos, f"{pos}.")
                datos = self.registros.get(usuario, {})
                titulo = datos.get("titulo")
                if titulo:
                    lineas.append(f"  {medalla} {usuario:<16} {titulo:<20} {valor:>8} {unidad}")
                else:
                    lineas.append(f"  {medalla} {usuario:<20} {valor:>8} {unidad}")

        lineas.append("=" * 50)
        return "\n".join(lineas)

    def __repr__(self):
        return f"LeaderboardsGlobales({len(self.registros)} jugadores registrados)"


# ============================================
# FUNCIONES DE NIVEL MÓDULO (patrón del proyecto)
# ============================================

def guardar_leaderboards(leaderboards, archivo=ARCHIVO_LEADERBOARDS):
    """
    Guarda los leaderboards en JSON global.

    Args:
        leaderboards: Instancia de LeaderboardsGlobales
        archivo: Ruta destino (parametrizable para tests)
    """
    leaderboards.archivo = archivo
    leaderboards._guardar()


def cargar_leaderboards(archivo=ARCHIVO_LEADERBOARDS):
    """
    Carga los leaderboards desde JSON global.

    Returns:
        LeaderboardsGlobales: instancia con los registros cargados.
    """
    return LeaderboardsGlobales(archivo)
