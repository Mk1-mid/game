"""
Sistema de generación de enemigos
=================================
"""

from .models import Character, Weapon, Armor, EnemyBasic
import random


# ============================================
# NOMBRES ROMANOS
# ============================================

NOMBRES_ROMANOS = [
    "Marcus", "Lucius", "Gaius", "Publius", "Quintus", "Titus", "Maximus",
    "Decimus", "Servius", "Appius", "Tiberius", "Gnaeus", "Spurius", "Manius",
    "Caius", "Kaeso", "Numerius", "Sextus", "Aulus", "Vibius", "Vopiscus"
]

APELLIDOS_ROMANOS = [
    "Aurelius", "Flavius", "Cornelius", "Julius", "Claudius", "Valerius",
    "Antonius", "Cassius", "Brutus", "Cato", "Cicero", "Gracchus", "Scipio",
    "Sulla", "Pompeius", "Crassus", "Lucullus", "Aemilius", "Fabius", "Marcellus"
]

APODOS_GLADIADOR = [
    "el Feroz", "el Invencible", "el Sanguinario", "el Veloz", "el Implacable",
    "el Terrible", "la Bestia", "el Carnicero", "el Demoledor", "el Furioso",
    "Mano de Hierro", "Espada Negra", "el Destructor", "el Despiadado",
    "el Conquistador", "Furia de Roma", "el Salvaje", "el Letal"
]


# ============================================
# GENERACIÓN DE NOMBRES
# ============================================

def generar_nombre_gladiador():
    """Genera un nombre romano aleatorio para gladiador."""
    nombre = random.choice(NOMBRES_ROMANOS)
    apellido = random.choice(APELLIDOS_ROMANOS)
    
    # 50% chance de tener apodo
    if random.random() < 0.5:
        apodo = random.choice(APODOS_GLADIADOR)
        return f"{nombre} {apellido} '{apodo}'"
    else:
        return f"{nombre} {apellido}"


# ============================================
# CLASES DE ENEMIGOS CON TIPOS
# ============================================

class EnemyVariant(Character):
    """Clase base para variantes de enemigos."""
    
    def __init__(self, nombre, hp, attack, defense, agilidad):
        super().__init__(hp, attack, defense, agilidad)
        self.nombre = nombre
        self.tipo_base = nombre
    
    def calcular_stats_finales(self):
        """Calcula stats finales considerando peso del equipo."""
        # Calcular peso total del equipo
        peso_equipo = 0
        if self.weapon:
            peso_equipo += self.weapon.peso
        if self.armor:
            peso_equipo += self.armor.peso
        
        # Agilidad efectiva = Agilidad base - penalidad de peso / fuerza
        penalidad_peso = peso_equipo / max(1, self.fuerza * 0.5)
        self.agilidad_efectiva = max(1, self.agilidad - penalidad_peso)
        
        # CRÍTICO = Fuerza * 0.3 + Agilidad efectiva * 0.4 - Peso * 0.5
        critico_base = (self.fuerza * 0.3 + self.agilidad_efectiva * 0.4) - (peso_equipo * 0.5)
        critico_arma = self.weapon.critico_bonus if self.weapon else 0
        self.critico = max(1, round(critico_base + critico_arma, 1))
        
        # ESQUIVA = Agilidad efectiva * 0.5 - Peso * 0.6
        esquiva_base = (self.agilidad_efectiva * 0.5) - (peso_equipo * 0.6)
        self.esquiva = max(0, round(esquiva_base, 1))


class Murmillo(EnemyVariant):
    """Tanque pesado: Alto HP y DEF, FUERZA alta, baja AGILIDAD."""
    
    def __init__(self):
        super().__init__(
            nombre=generar_nombre_gladiador(),
            hp=120,
            attack=15,
            defense=20,
            agilidad=10
        )
        self.tipo = "Murmillo"
        self.fuerza = 25
        self.critico = 7.5
        self.esquiva = 0.5
        self.calcular_stats_finales()


class Retiarius(EnemyVariant):
    """Rápido pero frágil: AGILIDAD alta, bajo HP, baja FUERZA."""
    
    def __init__(self):
        super().__init__(
            nombre=generar_nombre_gladiador(),
            hp=60,
            attack=22,
            defense=3,
            agilidad=22
        )
        self.tipo = "Retiarius"
        self.fuerza = 12
        self.critico = 11.5
        self.esquiva = 9.9
        self.calcular_stats_finales()


class Secutor(EnemyVariant):
    """Equilibrado: Stats balanceadas."""
    
    def __init__(self):
        super().__init__(
            nombre=generar_nombre_gladiador(),
            hp=90,
            attack=18,
            defense=10,
            agilidad=15
        )
        self.tipo = "Secutor"
        self.fuerza = 18
        self.critico = 7.5
        self.esquiva = 2.9
        self.calcular_stats_finales()


class Thraex(EnemyVariant):
    """Agresivo: FUERZA alta, AGILIDAD media, bajo HP."""
    
    def __init__(self):
        super().__init__(
            nombre=generar_nombre_gladiador(),
            hp=85,
            attack=25,
            defense=5,
            agilidad=14
        )
        self.tipo = "Thraex"
        self.fuerza = 20
        self.critico = 8.5
        self.esquiva = 1.8
        self.calcular_stats_finales()


class Hoplomachus(EnemyVariant):
    """Defensivo: Alta DEF y HP, FUERZA media, baja AGILIDAD."""
    
    def __init__(self):
        super().__init__(
            nombre=generar_nombre_gladiador(),
            hp=110,
            attack=16,
            defense=22,
            agilidad=12
        )
        self.tipo = "Hoplomachus"
        self.fuerza = 16
        self.critico = 6.5
        self.esquiva = 1.2
        self.calcular_stats_finales()


# ============================================
# GENERACIÓN DE ENEMIGOS
# ============================================

TIPOS_ENEMIGOS = [Murmillo, Retiarius, Secutor, Thraex, Hoplomachus]


def generar_enemigo(nivel=1):
    """
    Genera un enemigo aleatorio con posible equipo.
    
    Args:
        nivel: Nivel de dificultad (1-5, afecta equipo)
    
    Returns:
        EnemyVariant: Enemigo generado
    """
    
    # Seleccionar tipo de enemigo aleatorio
    tipo_enemigo = random.choice(TIPOS_ENEMIGOS)
    enemigo = tipo_enemigo()
    
    # Equipar armas/armaduras aleatorias según nivel
    if random.random() < 0.4 + (nivel * 0.1):  # 40% + (nivel * 10%)
        arma = Weapon(f"Arma {random.choice(['de Guerra', 'Común', 'Robusta'])}", 
                     attack=5 + nivel * 2)
        enemigo.equipar_arma(arma)
    
    if random.random() < 0.3 + (nivel * 0.1):  # 30% + (nivel * 10%)
        armadura = Armor(f"Armadura {random.choice(['de Cuero', 'de Bronce', 'Pesada'])}", 
                        defense=3 + nivel * 2)
        enemigo.equipar_armadura(armadura)
    
    return enemigo


def mostrar_info_enemigo(enemigo):
    """
    Muestra información formateada del enemigo.
    
    Args:
        enemigo: Objeto enemigo a mostrar
    """
    
    print(f"""
╔════════════════════════════════════════╗
║         ⚔️  ENEMIGO ENCONTRADO  ⚔️      ║
╠════════════════════════════════════════╣
║  Tipo:    {enemigo.tipo:<25} ║
║  Nombre:  {enemigo.nombre:<25} ║
║  ─────────────────────────────────── ║
║  HP:      {enemigo.hp_final():<25} ║
║  ATK:     {enemigo.ataque_final():<25} ║
║  DEF:     {enemigo.defensa_final():<25} ║
║  FUERZA:  {enemigo.fuerza:<25} ║
║  AGILIDAD:{enemigo.agilidad_final():<25} ║
║  CRÍTICO: {enemigo.critico:.1f}%{' ' * 21} ║
║  ESQUIVA: {enemigo.esquiva:.1f}%{' ' * 21} ║
╚════════════════════════════════════════╝
    """)
