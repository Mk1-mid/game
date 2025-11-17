from Character import Character, Weapon, Armor
import random

# ============================================
# GENERADOR DE NOMBRES ROMANOS
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

def generar_nombre_gladiador():
    """Genera un nombre romano aleatorio para gladiador"""
    nombre = random.choice(NOMBRES_ROMANOS)
    apellido = random.choice(APELLIDOS_ROMANOS)
    
    # 50% chance de tener apodo
    if random.random() < 0.5:
        apodo = random.choice(APODOS_GLADIADOR)
        return f"{nombre} {apellido} '{apodo}'"
    else:
        return f"{nombre} {apellido}"

# ============================================
# CLASES DE ENEMIGOS
# ============================================

class EnemyVariant(Character):
    """Clase base para enemigos con variantes"""
    def __init__(self, nombre, hp, attack, deffense, speed):
        super().__init__(hp, attack, deffense, speed)
        self.nombre = nombre
        self.tipo_base = nombre  # Guardar tipo original

class Murmillo(EnemyVariant):
    """Gladiador pesado - Alto HP y defensa, lento"""
    def __init__(self):
        super().__init__(
            nombre="Murmillo",
            hp=100,
            attack=15,
            deffense=8,
            speed=6
        )

class Retiarius(EnemyVariant):
    """Gladiador de red - Rápido pero frágil"""
    def __init__(self):
        super().__init__(
            nombre="Retiarius",
            hp=70,
            attack=20,
            deffense=3,
            speed=15
        )

class Secutor(EnemyVariant):
    """Gladiador equilibrado"""
    def __init__(self):
        super().__init__(
            nombre="Secutor",
            hp=85,
            attack=18,
            deffense=5,
            speed=10
        )

class Thraex(EnemyVariant):
    """Gladiador agresivo - Alto ataque"""
    def __init__(self):
        super().__init__(
            nombre="Thraex",
            hp=75,
            attack=22,
            deffense=4,
            speed=12
        )

class Hoplomachus(EnemyVariant):
    """Gladiador defensivo - Alta defensa"""
    def __init__(self):
        super().__init__(
            nombre="Hoplomachus",
            hp=90,
            attack=16,
            deffense=10,
            speed=8
        )

class Champion(EnemyVariant):
    """Campeón invicto del coliseo"""
    def __init__(self):
        super().__init__(
            nombre="CAMPEÓN INVICTO",
            hp=150,
            attack=25,
            deffense=15,
            speed=15
        )

# ============================================
# EQUIPO PARA ENEMIGOS
# ============================================

ARMAS_ENEMIGAS = [
    Weapon("Gladius Veterano", attack=5, speed=2),
    Weapon("Tridente Mortal", attack=8, speed=0),
    Weapon("Espada Corta", attack=3, speed=3),
    Weapon("Hacha de Guerra", attack=10, speed=-2),
]

ARMADURAS_ENEMIGAS = [
    Armor("Escudo Reforzado", deffense=5, hp=10),
    Armor("Armadura Ligera", deffense=3, hp=5),
    Armor("Armadura Pesada", deffense=8, hp=15),
    Armor("Protección Spartana", deffense=6, hp=8),
]

# ============================================
# GENERADOR DE ENEMIGOS
# ============================================

def generar_enemigo(numero_victoria):
    """
    Genera un enemigo con nombre aleatorio basado en victorias del jugador.
    A partir de victoria 5, enemigos pueden tener equipo.
    """
    tipos_enemigos = [Murmillo, Retiarius, Secutor, Thraex, Hoplomachus]
    
    # 20% chance de campeón si tienes más de 3 victorias
    if numero_victoria >= 3 and random.random() < 0.2:
        enemigo = Champion()
        enemigo.nombre = f" {generar_nombre_gladiador()} ⚔️"
        enemigo.weapon = random.choice(ARMAS_ENEMIGAS)
        enemigo.armor = random.choice(ARMADURAS_ENEMIGAS)
        return enemigo, True
    
    # Generar enemigo normal
    tipo_enemigo = random.choice(tipos_enemigos)
    enemigo = tipo_enemigo()
    
    # Asignar nombre único
    nombre_generado = generar_nombre_gladiador()
    enemigo.nombre = f"{nombre_generado} ({enemigo.tipo_base})"
    
    # Stats random (±15%)
    enemigo.hp = int(enemigo.hp * random.uniform(0.85, 1.15))
    enemigo.attack = int(enemigo.attack * random.uniform(0.85, 1.15))
    enemigo.deffense = int(enemigo.deffense * random.uniform(0.85, 1.15))
    enemigo.speed = int(enemigo.speed * random.uniform(0.85, 1.15))
    
    # Equipo después de victoria 5
    if numero_victoria >= 5:
        if random.random() < 0.6:
            enemigo.weapon = random.choice(ARMAS_ENEMIGAS)
            print(f"     Porta {enemigo.weapon.nombre}!")
        
        if random.random() < 0.4:
            enemigo.armor = random.choice(ARMADURAS_ENEMIGAS)
            print(f"     Viste {enemigo.armor.nombre}!")
    
    return enemigo, False

def mostrar_info_enemigo(enemigo, es_campeon):
    """Muestra información detallada del enemigo"""
    if es_campeon:
        print("     ¡¡¡HA ENTRADO EL CAMPEÓN !!!")
    print(f"    {enemigo.nombre}")
    print(f"     HP: {enemigo.hp_final()}")
    print(f"     ATK: {enemigo.ataque_final()}")
    print(f"     DEF: {enemigo.defensa_final()}")
    print(f"    VEL: {enemigo.velocidad_final()}")
    
    if enemigo.weapon:
        print(f"   Arma: {enemigo.weapon.nombre} (+{enemigo.weapon.attack} ATK)")
    if enemigo.armor:
        print(f"   Armadura: {enemigo.armor.nombre} (+{enemigo.armor.deffense} DEF)")
    
