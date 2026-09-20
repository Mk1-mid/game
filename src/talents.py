"""
SISTEMA DE TALENTOS - SANGRE Y FORTUNA v4.0
Árbol de talentos con 4 ramas × 5 niveles
=============================================

Cada punto de talento se gana al subir de nivel.
Se asigna permanentemente a una de las 4 ramas.
Nivel 5 de cada rama desbloquea una habilidad única.
"""

from typing import Dict, List, Tuple


RAMAS = ("fuerza", "resistencia", "agilidad", "tecnica")
NIVEL_MAXIMO = 5
BONUS_POR_NIVEL = {
    "fuerza": {
        1: {"ATK": 0.08},
        2: {"ATK": 0.08},
        3: {"ATK": 0.08},
        4: {"CRITICO": 0.10},
        5: {"ATK": 0.25},
    },
    "resistencia": {
        1: {"DEFENSA": 0.08},
        2: {"DEFENSA": 0.08},
        3: {"DEFENSA": 0.08},
        4: {"HP_MAX": 0.10},
        5: {"DEFENSA": 0.30},
    },
    "agilidad": {
        1: {"SPD": 0.10},
        2: {"SPD": 0.10},
        3: {"SPD": 0.10},
        4: {"ESQUIVA": 0.08},
        5: {"ESQUIVA": 0.40},
    },
    "tecnica": {
        1: {"CRITICO": 0.05},
        2: {"CRITICO": 0.05},
        3: {"CRITICO": 0.05},
        4: {"ATK": 0.05},
        5: {"XP_BONUS": 0.20},
    },
}

NOMBRE_HABILIDAD_UNICA = {
    "fuerza": "Furia Gladiatoria",
    "resistencia": "Escudo Ancestral",
    "agilidad": "Reflejo Táctico",
    "tecnica": "Maestría del Guerrero",
}

DESCRIPCION_HABILIDAD_UNICA = {
    "fuerza": "+25% ATK cuando HP > 50%",
    "resistencia": "+30% DEF cuando HP < 30%",
    "agilidad": "+40% ESQ por 1 turno (trigger: 3 esquivas)",
    "tecnica": "+20% XP ganada en combates",
}

NOMBRE_RAMA = {
    "fuerza": "Fuerza",
    "resistencia": "Resistencia",
    "agilidad": "Agilidad",
    "tecnica": "Técnica",
}

ESTADISTICA_POR_RAMA = {
    "fuerza": "ATK",
    "resistencia": "DEF",
    "agilidad": "SPD",
    "tecnica": "CRITICO",
}

EMOJI_RAMA = {
    "fuerza": "⚔️",
    "resistencia": "🛡️",
    "agilidad": "⚡",
    "tecnica": "⭐",
}


def crear_arbol_vacio() -> dict:
    """Crea un árbol de talentos vacío."""
    return {rama: 0 for rama in RAMAS}


def obtener_bonus_talentos(arbol: dict) -> dict:
    """
    Calcula el bonus total de todos los talentos invertidos.

    Args:
        arbol: dict {"fuerza": int, "resistencia": int, "agilidad": int, "tecnica": int}

    Returns:
        dict con bonificadores acumulados por stat.
        Ej: {"FUERZA": 0.24, "ATK": 0.13, ...}
    """
    bonus = {
        "FUERZA": 0.0,
        "AGILIDAD": 0.0,
        "DEFENSA": 0.0,
        "CRITICO": 0.0,
        "ESQUIVA": 0.0,
        "HP_MAX": 0.0,
        "SPD": 0.0,
        "ATK": 0.0,
        "XP_BONUS": 0.0,
    }

    for rama in RAMAS:
        nivel = arbol.get(rama, 0)
        if nivel <= 0:
            continue
        for lvl in range(1, nivel + 1):
            stat_bonuses = BONUS_POR_NIVEL[rama].get(lvl, {})
            for stat, valor in stat_bonuses.items():
                bonus[stat] = bonus.get(stat, 0.0) + valor

    return bonus


def puede_asignar(puntos_disponibles: int, rama: str, nivel_actual: int) -> Tuple[bool, str]:
    """
    Verifica si se puede asignar un punto de talento a una rama.

    Args:
        puntos_disponibles: Puntos de talento sin gastar
        rama: Nombre de la rama ("fuerza", "resistencia", "agilidad", "tecnica")
        nivel_actual: Nivel actual de la rama (0-5)

    Returns:
        (exito, mensaje)
    """
    if rama not in RAMAS:
        return False, "[FAIL] Rama de talento invalida"

    if puntos_disponibles <= 0:
        return False, "[FAIL] No tienes puntos de talento disponibles"

    if nivel_actual >= NIVEL_MAXIMO:
        return False, "[FAIL] Esta rama ya esta al nivel maximo (5)"

    return True, ""


def asignar_talento(gladiador, rama: str) -> Tuple[bool, int, str]:
    """
    Asigna 1 punto de talento a la rama indicada.

    Args:
        gladiador: Instancia de Gladiador (debe tener puntos_talento y arbol_talentos)
        rama: Nombre de la rama

    Returns:
        (exito: bool, costo: int, mensaje: str)
        costo siempre es 0 (puntos de talento, no oro).
    """
    if rama not in RAMAS:
        return False, 0, "[FAIL] Rama de talento invalida"

    puntos = getattr(gladiador, "puntos_talento", 0)
    arbol = getattr(gladiador, "arbol_talentos", None)

    if arbol is None:
        return False, 0, "[FAIL] Arbol de talentos no inicializado"

    nivel_actual = arbol.get(rama, 0)
    exito, msg = puede_asignar(puntos, rama, nivel_actual)

    if not exito:
        return False, 0, msg

    arbol[rama] = nivel_actual + 1
    gladiador.puntos_talento = puntos - 1

    nombre = NOMBRE_RAMA[rama]
    emoji = EMOJI_RAMA[rama]
    nuevo_nivel = arbol[rama]

    if nuevo_nivel == NIVEL_MAXIMO:
        hab = NOMBRE_HABILIDAD_UNICA[rama]
        return True, 0, f"{emoji} {nombre} -> Nivel {nuevo_nivel} OK ! ¡Habilidad desbloqueada: {hab}!"

    return True, 0, f"{emoji} {nombre} -> Nivel {nuevo_nivel}"


def verificar_habilidad_unica(gladiador) -> List[str]:
    """
    Verifica qué habilidades únicas están desbloqueadas.

    Args:
        gladiador: Instancia de Gladiador

    Returns:
        Lista de nombres de habilidades únicas desbloqueadas (nivel 5 alcanzado)
    """
    arbol = getattr(gladiador, "arbol_talentos", None)
    if arbol is None:
        return []

    habilidades = []
    for rama in RAMAS:
        if arbol.get(rama, 0) >= NIVEL_MAXIMO:
            habilidades.append(NOMBRE_HABILIDAD_UNICA[rama])

    return habilidades


def obtener_nivel_rama(gladiador, rama: str) -> int:
    """Retorna el nivel actual de una rama de talentos."""
    arbol = getattr(gladiador, "arbol_talentos", None)
    if arbol is None:
        return 0
    return arbol.get(rama, 0)


def obtener_resumen_talentos(gladiador) -> dict:
    """
    Retorna resumen completo del árbol de talentos de un gladiador.

    Args:
        gladiador: Instancia de Gladiador

    Returns:
        dict con: puntos_disponibles, arbol, bonus_total, habilidades_unicas
    """
    arbol = getattr(gladiador, "arbol_talentos", crear_arbol_vacio())
    return {
        "puntos_disponibles": getattr(gladiador, "puntos_talento", 0),
        "arbol": dict(arbol),
        "bonus_total": obtener_bonus_talentos(arbol),
        "habilidades_unicas": verificar_habilidad_unica(gladiador),
    }
