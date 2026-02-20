"""
SISTEMA DE HABILIDADES - SANGRE Y FORTUNA v2.2
Habilidades Pasivas y Activas para los 5 arquetipos
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class TipoHabilidad(Enum):
    """Tipos de habilidades disponibles"""
    PASIVA = "pasiva"
    ACTIVA = "activa"


class TipoTrigger(Enum):
    """Tipos de triggers para habilidades activas"""
    SALUD_BAJO = "salud_bajo"
    ESQUIVAS_CONSECUTIVAS = "esquivas_consecutivas"
    CRITICOS_RECIBIDOS = "criticos_recibidos"
    CRITICOS_PROPIOS = "criticos_propios"
    DAÑO_RECIBIDO = "daño_recibido"
    TURNOS_COMBATE = "turnos_combate"


@dataclass
class Habilidad:
    """Clase que representa una habilidad"""
    nombre: str
    descripcion: str
    tipo: TipoHabilidad
    arqueotipo: str  # "Guerrero", "Velocista", etc.
    
    # Para pasivas: bonificadores permanentes
    bonus_pasivo: Optional[Dict[str, float]] = None  # {"FUERZA": 0.10, "CRITICO": 0.05}
    
    # Para activas: trigger y efectos temporales
    trigger_tipo: Optional[TipoTrigger] = None
    trigger_valor: Optional[float] = None
    bonus_activo: Optional[Dict[str, float]] = None
    duracion_bonus: int = 0  # turnos que dura el efecto
    cooldown: int = 1  # veces por combate (1 = una sola vez)
    
    # Estado interno
    veces_usado: int = field(default=0, init=False)
    turnos_restantes: int = field(default=0, init=False)
    
    def obtener_bonus_pasivo(self) -> Dict[str, float]:
        """Retorna el bonus de habilidad pasiva"""
        if self.tipo == TipoHabilidad.PASIVA and self.bonus_pasivo:
            return self.bonus_pasivo.copy()
        return {}
    
    def obtener_bonus_activo(self) -> Dict[str, float]:
        """Retorna el bonus de habilidad activa si está activa"""
        if self.tipo == TipoHabilidad.ACTIVA and self.turnos_restantes > 0 and self.bonus_activo:
            return self.bonus_activo.copy()
        return {}
    
    def verificar_trigger(self, salud_actual: float, salud_max: float, 
                         estadisticas: Dict[str, any]) -> bool:
        """
        Verifica si se activa esta habilidad.
        Retorna True si se cumple el trigger.
        """
        if self.tipo == TipoHabilidad.PASIVA:
            return False
        
        if self.veces_usado >= self.cooldown:
            return False
        
        # Trigger: Salud baja
        if self.trigger_tipo == TipoTrigger.SALUD_BAJO:
            porcentaje_salud = salud_actual / salud_max if salud_max > 0 else 1.0
            return porcentaje_salud <= self.trigger_valor
        
        # Trigger: Esquivas consecutivas
        if self.trigger_tipo == TipoTrigger.ESQUIVAS_CONSECUTIVAS:
            esquivas = estadisticas.get("esquivas_consecutivas", 0)
            return esquivas >= int(self.trigger_valor)
        
        # Trigger: Críticos recibidos
        if self.trigger_tipo == TipoTrigger.CRITICOS_RECIBIDOS:
            criticos = estadisticas.get("criticos_recibidos_turno", 0)
            return criticos >= int(self.trigger_valor)
        
        # Trigger: Críticos propios
        if self.trigger_tipo == TipoTrigger.CRITICOS_PROPIOS:
            criticos = estadisticas.get("criticos_propios", 0)
            return criticos >= int(self.trigger_valor)
        
        # Trigger: Daño recibido en turno
        if self.trigger_tipo == TipoTrigger.DAÑO_RECIBIDO:
            daño_turno = estadisticas.get("daño_recibido_turno", 0)
            return daño_turno >= int(self.trigger_valor)
        
        return False
    
    def activar(self):
        """Activa la habilidad"""
        if self.tipo == TipoHabilidad.ACTIVA:
            self.turnos_restantes = self.duracion_bonus
            self.veces_usado += 1
    
    def decrementar_turno(self):
        """Decrementa los turnos restantes"""
        if self.turnos_restantes > 0:
            self.turnos_restantes -= 1
    
    def resetear_cooldown(self):
        """Resetea el cooldown al terminar combate"""
        self.veces_usado = 0
        self.turnos_restantes = 0
    
    def __str__(self) -> str:
        tipo_str = f"[{self.tipo.value.upper()}]"
        estado = "✓ Activa" if self.turnos_restantes > 0 else ""
        return f"{tipo_str} {self.nombre} ({self.arqueotipo}) {estado}"


# ============================================================================
# HABILIDADES DEFINIDAS - 25 HABILIDADES (5 ARQUETIPOS × 5 HABILIDADES)
# ============================================================================

# GUERRERO (Ataque + Defensa Balanceado)
HABILIDADES_GUERRERO = [
    # Pasivas
    Habilidad(
        nombre="Entrenamiento de Fuerza",
        descripcion="Años de práctica mejoran tu fuerza base",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Guerrero",
        bonus_pasivo={"FUERZA": 0.14}
    ),
    Habilidad(
        nombre="Golpe Certero",
        descripcion="Tu experiencia mejora la precisión de tus ataques",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Guerrero",
        bonus_pasivo={"CRITICO": 0.10}
    ),
    Habilidad(
        nombre="Defensa Entrenada",
        descripcion="Sabes cómo bloquear mejor",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Guerrero",
        bonus_pasivo={"DEFENSA": 0.08, "ESQUIVA": 0.05, "AGILIDAD": 0.03}
    ),
    # Activas
    Habilidad(
        nombre="Furia Desatada",
        descripcion="Cuando la salud es baja, desatas toda tu furia",
        tipo=TipoHabilidad.ACTIVA,
        arqueotipo="Guerrero",
        trigger_tipo=TipoTrigger.SALUD_BAJO,
        trigger_valor=0.25,
        bonus_activo={"FUERZA": 0.25, "AGILIDAD": 0.15},
        duracion_bonus=4,
        cooldown=1
    ),
    Habilidad(
        nombre="Último Aliento",
        descripcion="Recibir golpes críticos te prepara para contraatacar",
        tipo=TipoHabilidad.ACTIVA,
        arqueotipo="Guerrero",
        trigger_tipo=TipoTrigger.CRITICOS_RECIBIDOS,
        trigger_valor=2,
        bonus_activo={"DEFENSA": 0.18, "CRITICO": 0.10},
        duracion_bonus=5,
        cooldown=1
    ),
]

# VELOCISTA (Crítico + Esquiva)
HABILIDADES_VELOCISTA = [
    # Pasivas
    Habilidad(
        nombre="Agilidad Natural",
        descripcion="Tu cuerpo es naturalmente rápido",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Velocista",
        bonus_pasivo={"AGILIDAD": 0.15}
    ),
    Habilidad(
        nombre="Reflejos Felinos",
        descripcion="Esquivas con elegancia innata",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Velocista",
        bonus_pasivo={"ESQUIVA": 0.12}
    ),
    Habilidad(
        nombre="Ataque Ligero",
        descripcion="Golpeas rápido y con precisión",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Velocista",
        bonus_pasivo={"CRITICO": 0.12, "FUERZA": 0.05}
    ),
    # Activas
    Habilidad(
        nombre="Confianza de Campeón",
        descripcion="Después de 3 esquivas, confías en ti mismo",
        tipo=TipoHabilidad.ACTIVA,
        arqueotipo="Velocista",
        trigger_tipo=TipoTrigger.ESQUIVAS_CONSECUTIVAS,
        trigger_valor=3,
        bonus_activo={"ESQUIVA": 0.25, "CRITICO": 0.20},
        duracion_bonus=5,
        cooldown=1
    ),
    Habilidad(
        nombre="Ráfaga de Velocidad",
        descripcion="Dos críticos te ponen en trance de velocidad",
        tipo=TipoHabilidad.ACTIVA,
        arqueotipo="Velocista",
        trigger_tipo=TipoTrigger.CRITICOS_PROPIOS,
        trigger_valor=2,
        bonus_activo={"AGILIDAD": 0.30, "CRITICO": 0.15},
        duracion_bonus=4,
        cooldown=1
    ),
]

# TANQUE (Defensa + HP)
HABILIDADES_TANQUE = [
    # Pasivas
    Habilidad(
        nombre="Armadura Mejorada",
        descripcion="Entrenamientos en blindaje mejoran tu defensa",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Tanque",
        bonus_pasivo={"DEFENSA": 0.15}
    ),
    Habilidad(
        nombre="Constitución",
        descripcion="Tu cuerpo es robusto y resistente",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Tanque",
        bonus_pasivo={"HP_MAX": 0.18}
    ),
    Habilidad(
        nombre="Escudo Mental",
        descripcion="Reduces el daño de críticos enemigos",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Tanque",
        bonus_pasivo={"DEFENSA": 0.08, "ESQUIVA": 0.03}
    ),
    # Activas
    Habilidad(
        nombre="Barrera Inquebrantable",
        descripcion="3 críticos enemigos te endurecen",
        tipo=TipoHabilidad.ACTIVA,
        arqueotipo="Tanque",
        trigger_tipo=TipoTrigger.CRITICOS_RECIBIDOS,
        trigger_valor=3,
        bonus_activo={"DEFENSA": 0.35},
        duracion_bonus=6,
        cooldown=1
    ),
    Habilidad(
        nombre="Último Bastión",
        descripcion="Cuando la muerte acecha, te vuelves inquebrantable",
        tipo=TipoHabilidad.ACTIVA,
        arqueotipo="Tanque",
        trigger_tipo=TipoTrigger.SALUD_BAJO,
        trigger_valor=0.20,
        bonus_activo={"DEFENSA": 0.40, "CRITICO": -0.30},
        duracion_bonus=5,
        cooldown=1
    ),
]

# ASESINO (Crítico + Daño)
HABILIDADES_ASESINO = [
    # Pasivas
    Habilidad(
        nombre="Golpe Letal",
        descripcion="Tus golpes son precisos y mortales",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Asesino",
        bonus_pasivo={"CRITICO": 0.12}
    ),
    Habilidad(
        nombre="Sombra Silenciosa",
        descripcion="Tus movimientos pasan desapercibidos",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Asesino",
        bonus_pasivo={"ESQUIVA": 0.12, "CRITICO": 0.08}
    ),
    Habilidad(
        nombre="Filo Envenenado",
        descripcion="Tus armas cargan veneno",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Asesino",
        bonus_pasivo={"CRITICO": 0.06, "FUERZA": 0.05}
    ),
    # Activas
    Habilidad(
        nombre="Momento Mortal",
        descripcion="2 críticos con salud alta = ataque devastador",
        tipo=TipoHabilidad.ACTIVA,
        arqueotipo="Asesino",
        trigger_tipo=TipoTrigger.CRITICOS_PROPIOS,
        trigger_valor=2,
        bonus_activo={"CRITICO": 0.40, "FUERZA": 0.20},
        duracion_bonus=3,
        cooldown=1
    ),
    Habilidad(
        nombre="Desaparición",
        descripcion="Cuando huyes, te vuelves invisible",
        tipo=TipoHabilidad.ACTIVA,
        arqueotipo="Asesino",
        trigger_tipo=TipoTrigger.SALUD_BAJO,
        trigger_valor=0.30,
        bonus_activo={"ESQUIVA": 0.50, "AGILIDAD": 0.20},
        duracion_bonus=3,
        cooldown=1
    ),
]

# PALADÍN (Balance + Regen)
HABILIDADES_PALADIN = [
    # Pasivas
    Habilidad(
        nombre="Protección Divina",
        descripcion="Los dioses te protegen con balance",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Paladín",
        bonus_pasivo={"DEFENSA": 0.10, "ESQUIVA": 0.05}
    ),
    Habilidad(
        nombre="Bendición",
        descripcion="Tu cuerpo está bendecido",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Paladín",
        bonus_pasivo={"HP_MAX": 0.10, "DEFENSA": 0.05, "AGILIDAD": 0.03}
    ),
    Habilidad(
        nombre="Justicia Divina",
        descripcion="Tu ataque es justo y poderoso",
        tipo=TipoHabilidad.PASIVA,
        arqueotipo="Paladín",
        bonus_pasivo={"CRITICO": 0.08, "FUERZA": 0.05}
    ),
    # Activas
    Habilidad(
        nombre="Salvación Sagrada",
        descripcion="Cuando necesitas ayuda, los dioses responden",
        tipo=TipoHabilidad.ACTIVA,
        arqueotipo="Paladín",
        trigger_tipo=TipoTrigger.SALUD_BAJO,
        trigger_valor=0.40,
        bonus_activo={"DEFENSA": 0.20, "CRITICO": 0.15},
        duracion_bonus=5,
        cooldown=1
    ),
    Habilidad(
        nombre="Escudo Sagrado",
        descripcion="Después de esquivar críticos, tu defensa es mayor",
        tipo=TipoHabilidad.ACTIVA,
        arqueotipo="Paladín",
        trigger_tipo=TipoTrigger.ESQUIVAS_CONSECUTIVAS,
        trigger_valor=2,
        bonus_activo={"DEFENSA": 0.25, "ESQUIVA": 0.12},
        duracion_bonus=4,
        cooldown=1
    ),
]

# ============================================================================
# DICCIONARIO DE HABILIDADES POR ARQUEOTIPO
# ============================================================================

HABILIDADES_POR_ARQUEOTIPO = {
    "Guerrero": HABILIDADES_GUERRERO,
    "Velocista": HABILIDADES_VELOCISTA,
    "Tanque": HABILIDADES_TANQUE,
    "Asesino": HABILIDADES_ASESINO,
    "Paladín": HABILIDADES_PALADIN,
}

TODAS_LAS_HABILIDADES = (
    HABILIDADES_GUERRERO +
    HABILIDADES_VELOCISTA +
    HABILIDADES_TANQUE +
    HABILIDADES_ASESINO +
    HABILIDADES_PALADIN
)


# ============================================================================
# FUNCIONES HELPER
# ============================================================================

def obtener_habilidades_arqueotipo(arqueotipo: str) -> List[Habilidad]:
    """Obtiene todas las habilidades de un arqueotipo"""
    return HABILIDADES_POR_ARQUEOTIPO.get(arqueotipo, [])


def calcular_bonus_pasivo_total(habilidades: List[Habilidad]) -> Dict[str, float]:
    """
    Calcula el bonus pasivo total de todas las habilidades.
    
    Args:
        habilidades: Lista de habilidades del gladiador
        
    Returns:
        Dict con bonificadores multiplicativos acumulados
    """
    bonus_acumulado = {
        "FUERZA": 0.0,
        "AGILIDAD": 0.0,
        "DEFENSA": 0.0,
        "ESQUIVA": 0.0,
        "CRITICO": 0.0,
        "HP_MAX": 0.0,
    }
    
    for habilidad in habilidades:
        if habilidad.tipo == TipoHabilidad.PASIVA:
            bonus = habilidad.obtener_bonus_pasivo()
            for stat, valor in bonus.items():
                bonus_acumulado[stat] += valor
    
    return bonus_acumulado


def calcular_bonus_activo_total(habilidades: List[Habilidad]) -> Dict[str, float]:
    """
    Calcula el bonus activo total (habilidades temporales activadas).
    
    Args:
        habilidades: Lista de habilidades del gladiador
        
    Returns:
        Dict con bonificadores multiplicativos acumulados
    """
    bonus_acumulado = {
        "FUERZA": 0.0,
        "AGILIDAD": 0.0,
        "DEFENSA": 0.0,
        "ESQUIVA": 0.0,
        "CRITICO": 0.0,
        "HP_MAX": 0.0,
    }
    
    for habilidad in habilidades:
        if habilidad.tipo == TipoHabilidad.ACTIVA and habilidad.turnos_restantes > 0:
            bonus = habilidad.obtener_bonus_activo()
            for stat, valor in bonus.items():
                bonus_acumulado[stat] += valor
    
    return bonus_acumulado


def aplicar_bonificadores_habilidades(stats_base: Dict[str, float], 
                                      habilidades: List[Habilidad]) -> Dict[str, float]:
    """
    Aplica todos los bonificadores de habilidades a los stats base.
    
    Args:
        stats_base: Stats originales del gladiador
        habilidades: Lista de habilidades del gladiador
        
    Returns:
        Stats finales con bonificadores aplicados
    """
    stats_finales = stats_base.copy()
    
    # Bonificadores pasivos
    bonus_pasivo = calcular_bonus_pasivo_total(habilidades)
    
    # Bonificadores activos
    bonus_activo = calcular_bonus_activo_total(habilidades)
    
    # Aplicar bonificadores
    for stat in stats_finales:
        multiplicador = 1.0 + bonus_pasivo.get(stat, 0.0) + bonus_activo.get(stat, 0.0)
        stats_finales[stat] = stats_finales[stat] * multiplicador
    
    return stats_finales


def verificar_y_activar_triggers(gladiador, estado_combate: Dict) -> List[str]:
    """
    Verifica todos los triggers y activa habilidades si corresponde.
    
    Args:
        gladiador: Objeto Gladiador
        estado_combate: Dict con estadísticas actuales del combate
        
    Returns:
        Lista con nombres de habilidades activadas
    """
    habilidades_activadas = []
    
    for habilidad in gladiador.habilidades:
        if habilidad.verificar_trigger(
            gladiador.salud,
            gladiador.salud_maxima,
            estado_combate
        ):
            habilidad.activar()
            habilidades_activadas.append(habilidad.nombre)
    
    return habilidades_activadas


def resetear_habilidades_combate(habilidades: List[Habilidad]):
    """Resetea el estado de habilidades al terminar combate"""
    for habilidad in habilidades:
        habilidad.resetear_cooldown()


def decrementar_duraciones(habilidades: List[Habilidad]):
    """Decrementa las duraciones de habilidades activas"""
    for habilidad in habilidades:
        habilidad.decrementar_turno()


# ============================================================================
# INFORMACIÓN ESTADÍSTICA PARA BALANCE
# ============================================================================

def obtener_estadisticas_balance() -> Dict:
    """Retorna estadísticas de balance para debugging"""
    stats = {
        "total_habilidades": len(TODAS_LAS_HABILIDADES),
        "por_arqueotipo": {},
        "pasivas_vs_activas": {"pasivas": 0, "activas": 0},
        "bonus_promedio_por_stat": {
            "FUERZA": [],
            "AGILIDAD": [],
            "DEFENSA": [],
            "ESQUIVA": [],
            "CRITICO": [],
            "HP_MAX": [],
        }
    }
    
    for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
        stats["por_arqueotipo"][arqueotipo] = {
            "total": len(habilidades),
            "pasivas": sum(1 for h in habilidades if h.tipo == TipoHabilidad.PASIVA),
            "activas": sum(1 for h in habilidades if h.tipo == TipoHabilidad.ACTIVA),
            "bonus_total_pasivo": calcular_bonus_pasivo_total(habilidades),
        }
    
    for habilidad in TODAS_LAS_HABILIDADES:
        if habilidad.tipo == TipoHabilidad.PASIVA:
            stats["pasivas_vs_activas"]["pasivas"] += 1
            bonus = habilidad.obtener_bonus_pasivo()
            for stat, valor in bonus.items():
                stats["bonus_promedio_por_stat"][stat].append(valor)
        else:
            stats["pasivas_vs_activas"]["activas"] += 1
    
    return stats


if __name__ == "__main__":
    # Debug: Mostrar todas las habilidades
    print("=" * 80)
    print("SISTEMA DE HABILIDADES - SANGRE Y FORTUNA")
    print("=" * 80)
    
    for arqueotipo, habilidades in HABILIDADES_POR_ARQUEOTIPO.items():
        print(f"\n{arqueotipo.upper()}")
        print("-" * 80)
        for hab in habilidades:
            print(f"  {hab}")
    
    # Mostrar estadísticas
    print("\n" + "=" * 80)
    print("ESTADÍSTICAS DE BALANCE")
    print("=" * 80)
    stats = obtener_estadisticas_balance()
    print(f"\nTotal de habilidades: {stats['total_habilidades']}")
    print(f"Pasivas: {stats['pasivas_vs_activas']['pasivas']}")
    print(f"Activas: {stats['pasivas_vs_activas']['activas']}")
    
    print("\nBONUS TOTAL POR ARQUEOTIPO (Pasivas):")
    for arqueotipo, info in stats['por_arqueotipo'].items():
        print(f"  {arqueotipo}:")
        print(f"    - Total habilidades: {info['total']} ({info['pasivas']} pasivas, {info['activas']} activas)")
        bonus = info['bonus_total_pasivo']
        for stat, valor in sorted(bonus.items()):
            if valor > 0:
                print(f"      • {stat}: +{valor*100:.0f}%")
