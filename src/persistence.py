"""
Funciones de persistencia para Equipo y Gladiador
===============================================
"""

import json
import os
from .models import Equipo, Gladiador, Barracas, Weapon, Armor


def serializar_arma(arma):
    """Serializa un arma a diccionario para JSON."""
    if not arma:
        return None
    return {
        "nombre": arma.nombre,
        "attack": arma.attack,
        "agilidad": arma.agilidad,
        "peso": arma.peso,
        "critico_bonus": arma.critico_bonus,
        "tier": arma.tier,
        "str_requirement": arma.str_requirement,
        "nivel_mejora": arma.nivel_mejora,
        # Fase 3.4
        "arquetipo": getattr(arma, 'arquetipo', "desconocido"),
        "rareza": getattr(arma, 'rareza', "comun"),
        "max_nivel_mejora": getattr(arma, 'max_nivel_mejora', 3),
        "es_historica": getattr(arma, 'es_historica', False),
        "efecto_especial": getattr(arma, 'efecto_especial', None),
    }


def serializar_armadura(armadura):
    """Serializa una armadura a diccionario para JSON."""
    if not armadura:
        return None
    return {
        "nombre": armadura.nombre,
        "defense": armadura.defense,
        "hp": armadura.hp,
        "peso": armadura.peso,
    }


def serializar_gladiador(gladiador):
    """Convierte un Gladiador a diccionario para JSON."""
    # Serializar habilidades si existen
    habilidades_data = None
    if hasattr(gladiador, 'habilidades') and gladiador.habilidades:
        habilidades_data = {
            "habilidades_activas": gladiador.habilidades_activas if hasattr(gladiador, 'habilidades_activas') else {},
            "contadores_triggers": gladiador.contadores_triggers if hasattr(gladiador, 'contadores_triggers') else {}
        }
    
    # Serializar arma y armadura
    weapon_data = serializar_arma(gladiador.weapon) if gladiador.weapon else None
    armor_data = serializar_armadura(gladiador.armor) if gladiador.armor else None
    
    return {
        "nombre": gladiador.nombre,
        "tipo": gladiador.tipo,
        "nivel": gladiador.nivel,
        "xp": gladiador.xp,
        "hp": gladiador.hp,
        "hp_actual": gladiador.hp_actual,
        "attack": gladiador.attack,
        "defense": gladiador.defense,
        "agilidad": gladiador.agilidad,
        "fuerza": gladiador.fuerza,
        "critico": gladiador.critico,
        "esquiva": gladiador.esquiva,
        "estado": gladiador.estado,
        "ocupacion": gladiador.ocupacion,
        "dias_ocupado": gladiador.dias_ocupado,
        "razon_ocupacion": gladiador.razon_ocupacion,
        "combates_ganados": gladiador.combates_ganados,
        "combates_perdidos": gladiador.combates_perdidos,
        "combates_totales": gladiador.combates_totales,
        "dinero_generado": gladiador.dinero_generado,
        # Fase 4: Árbol de Talentos
        "puntos_talento": gladiador.puntos_talento,
        "arbol_talentos": gladiador.arbol_talentos if hasattr(gladiador, 'arbol_talentos') else {"fuerza": 0, "resistencia": 0, "agilidad": 0, "tecnica": 0},
        "weapon": weapon_data,
        "armor": serializar_armadura(gladiador.armor) if gladiador.armor else None,
        "habilidades": None,  # Estado de habilidades
    }


def deserializar_arma(data):
    """Deserializa un arma desde diccionario JSON."""
    if not data:
        return None
    arma = Weapon(
        nombre=data["nombre"],
        attack=data.get("attack", 0),
        agilidad=data.get("agilidad", 0),
        peso=data.get("peso", 0),
        critico_bonus=data.get("critico_bonus", 0),
        tier=data.get("tier", 1),
        str_requirement=data.get("str_requirement", 10)
    )
    arma.nivel_mejora = data.get("nivel_mejora", 0)
    # Fase 3.4: nuevos campos con defaults para compatibilidad
    arma.arquetipo = data.get("arquetipo", "desconocido")
    arma.rareza = data.get("rareza", "comun")
    arma.max_nivel_mejora = data.get("max_nivel_mejora", 3)
    arma.es_historica = data.get("es_historica", False)
    arma.efecto_especial = data.get("efecto_especial", None)
    return arma


def deserializar_armadura(data):
    """Deserializa una armadura desde diccionario JSON."""
    if not data:
        return None
    return Armor(
        nombre=data["nombre"],
        defense=data.get("defense", 0),
        hp=data.get("hp", 0),
        peso=data.get("peso", 0)
    )


def deserializar_gladiador(data):
    """Crea un Gladiador desde diccionario JSON."""
    # Crear con nivel 1 primero para obtener la estructura base
    g = Gladiador(data["nombre"], data["tipo"], nivel=1)
    
    # Ahora sobreescribir TODOS los valores del JSON
    g.nivel = data["nivel"]
    g.xp = data["xp"]
    g.hp = data["hp"]
    g.hp_actual = data["hp_actual"]
    g.attack = data["attack"]
    g.defense = data["defense"]
    g.agilidad = data.get("agilidad", 10)  # Compatibilidad con datos antiguos
    g.fuerza = data.get("fuerza", 15)
    g.critico = data.get("critico", 12)
    g.esquiva = data.get("esquiva", 8)
    
    # Restaurar estado
    g.estado = data["estado"]
    g.ocupacion = data["ocupacion"]
    g.dias_ocupado = data["dias_ocupado"]
    g.razon_ocupacion = data["razon_ocupacion"]
    
    # Restaurar historico
    g.combates_ganados = data["combates_ganados"]
    g.combates_perdidos = data["combates_perdidos"]
    g.combates_totales = data["combates_totales"]
    g.dinero_generado = data["dinero_generado"]
    
    # Fase 4: Árbol de Talentos
    g.puntos_talento = data.get("puntos_talento", 0)
    g.arbol_talentos = data.get("arbol_talentos", {"fuerza": 0, "resistencia": 0, "agilidad": 0, "tecnica": 0})
    
    # Restaurar arma y armadura
    if "weapon" in data and data["weapon"]:
        g.weapon = deserializar_arma(data["weapon"])
    if "armor" in data and data["armor"]:
        g.armor = deserializar_armadura(data["armor"])
    
    # Restaurar estado de habilidades si existe
    if "habilidades" in data and data["habilidades"]:
        hab_data = data["habilidades"]
        if hasattr(g, 'habilidades_activas'):
            g.habilidades_activas = hab_data.get("habilidades_activas", {})
        if hasattr(g, 'contadores_triggers'):
            g.contadores_triggers = hab_data.get("contadores_triggers", {})
    
    # Recalcular stats derivados
    g.calcular_stats_finales()
    
    return g


def serializar_equipo(equipo):
    """Convierte un Equipo a diccionario para JSON."""
    return {
        "dinero": equipo.dinero,
        "literas": equipo.barracas.literas,
        "espacios_totales": equipo.barracas.espacios_totales,
        "gladiadores": [serializar_gladiador(g) for g in equipo.gladiadores],
        # Fase 3.2: honra, materiales y estado social
        "honra": equipo.honra,
        "racha_victorias_limpias": equipo.racha_victorias_limpias,
        "materiales": equipo.materiales,
        "habilitado_clandestino": equipo.habilitado_clandestino,
        "rumor_ofrecido": equipo.rumor_ofrecido,
        "fama": equipo.fama,
        "prestamos_pendientes": equipo.prestamos_pendientes,
        "penitencia_fama_dias": equipo.penitencia_fama_dias,
        # Fase 3.3: instalaciones y trabajadores
        "instalaciones": equipo.instalaciones.serializar() if equipo.instalaciones else None,
        "trabajadores_activos": equipo.trabajadores_activos,
    }


def deserializar_equipo(data):
    """Crea un Equipo desde diccionario JSON."""
    equipo = Equipo()
    
    # Restaurar dinero
    equipo.dinero = data["dinero"]
    
    # Restaurar barracas
    equipo.barracas.literas = data["literas"]
    equipo.barracas.espacios_totales = data["espacios_totales"]
    
    # Restaurar gladiadores
    for gdata in data["gladiadores"]:
        g = deserializar_gladiador(gdata)
        equipo.gladiadores.append(g)

    # Fase 3.2: campos nuevos con defaults para compatibilidad con saves antiguos
    equipo.honra = data.get("honra", 50)
    equipo.racha_victorias_limpias = data.get("racha_victorias_limpias", 0)
    equipo.materiales = data.get("materiales", {})
    equipo.habilitado_clandestino = data.get("habilitado_clandestino", False)
    equipo.rumor_ofrecido = data.get("rumor_ofrecido", False)
    equipo.fama = data.get("fama", 0)
    equipo.prestamos_pendientes = data.get("prestamos_pendientes", [])
    equipo.penitencia_fama_dias = data.get("penitencia_fama_dias", 0)

    # Fase 3.3: instalaciones y trabajadores
    if data.get("instalaciones"):
        from .instalaciones import cargar_instalaciones
        equipo.instalaciones = cargar_instalaciones({"instalaciones": data["instalaciones"]})
    else:
        from .instalaciones import GestorInstalaciones
        equipo.instalaciones = GestorInstalaciones()

    equipo.trabajadores_activos = data.get("trabajadores_activos", [])

    return equipo


def guardar_equipo_partida(usuario, equipo):
    """Guarda el equipo en JSON."""
    os.makedirs("data/saves", exist_ok=True)
    
    archivo = os.path.join("data/saves", f"save_{usuario}.json")
    datos = serializar_equipo(equipo)
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    
    print(f"[OK] Partida guardada para {usuario}")


def guardar_facilities(usuario, facilities_manager):
    """Guarda el estado de facilities (Medico y Herrero)."""
    archivo = os.path.join("data/saves", f"save_{usuario}.json")
    
    try:
        # Lee datos existentes
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        else:
            datos = {}
        
        # Agrega datos de facilities
        datos["facilities"] = {
            "medico_nivel": facilities_manager.medico.nivel,
            "herrero_nivel": facilities_manager.herrero.nivel,
            "medico_curacion_rapida_usado": facilities_manager.medico.curacion_rapida_usado,
        }
        
        # Guarda todo
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Facilities guardadas para {usuario}")
    except Exception as e:
        print(f"[FAIL] Error guardando facilities: {e}")


def cargar_facilities(datos):
    """Carga facilities desde datos JSON."""
    from .facilities import FacilitiesManager
    
    fm = FacilitiesManager()
    
    if datos and "facilities" in datos:
        fm.cargar_estado(datos["facilities"])
    
    return fm


def guardar_patricios(usuario, gestor_patricios):
    """
    Guarda el mundo de patricios dentro del save del usuario (Fase 3.2).
    Sigue el patron de guardar_facilities: fusiona con datos existentes.
    """
    archivo = os.path.join("data/saves", f"save_{usuario}.json")

    try:
        datos = {}
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)

        datos["patricios"] = gestor_patricios.serializar()

        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[FAIL] Error guardando patricios: {e}")
        return False


def cargar_patricios(datos):
    """
    Restaura el gestor de patricios desde el dict del save (Fase 3.2).

    Args:
        datos: Diccionario completo del save (o None)

    Returns:
        GestorPatricios: con patricios restaurados, o vacio si no hay datos
    """
    from .patricios import GestorPatricios

    gestor = GestorPatricios()
    if datos and "patricios" in datos:
        gestor.deserializar(datos["patricios"])
    return gestor


def cargar_equipo_partida(usuario):
    """Carga el equipo desde JSON."""
    archivo = os.path.join("data/saves", f"save_{usuario}.json")
    
    if not os.path.exists(archivo):
        return None
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        return deserializar_equipo(datos)
    except json.JSONDecodeError:
        print(f"⚠️  Partida de {usuario} corrupta")
        return None
