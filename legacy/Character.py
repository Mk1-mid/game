# Clase base para cualquier objeto equipable.
class Item:
    def __init__(self, nombre):
        self.nombre = nombre

# Clases derivadas
class Weapon(Item):
    # Afecta ataque y velocidad
    def __init__(self, nombre, attack=0, speed=0):
        super().__init__(nombre)
        self.attack = attack
        self.speed = speed

class Armor(Item):
    # Afecta defensa y HP
    def __init__(self, nombre, deffense=0, hp=0):
        super().__init__(nombre)
        self.deffense = deffense
        self.hp = hp

# Ejemplo de items disponibles  
objetos_disponibles = {
    "Espada de Acero": Weapon("Espada de Acero", attack=2, speed=1),
    "Armadura_cuero": Armor("Armadura de Cuero", deffense=3, hp=10)  # ← CORREGIDO: deffense
}

# Clase de personaje base
class Character:
    def __init__(self, hp, attack, deffense, speed):
        self.hp = hp
        self.attack = attack
        self.deffense = deffense
        self.speed = speed

        # Items actuales del personaje
        self.weapon = None
        self.armor = None

    # Función para calcular ataque final
    def ataque_final(self):
        return self.attack + (self.weapon.attack if self.weapon else 0)  # ← CORREGIDO: siempre retorna
    
    # Función para calcular defensa final
    def defensa_final(self):
        return self.deffense + (self.armor.deffense if self.armor else 0)  # ← CORREGIDO: siempre retorna
    
    # Función para calcular HP final
    def hp_final(self):
        return self.hp + (self.armor.hp if self.armor else 0)
    
    # Función para calcular velocidad final
    def velocidad_final(self):  # ← CORREGIDO: nombre del método
        return self.speed + (self.weapon.speed if self.weapon else 0)  # ← CORREGIDO: usa self.speed

# Clase jugador
class Player(Character):
    def __init__(self):
        super().__init__(hp=100, attack=20, deffense=5, speed=10)  # ← Stats mejoradas

# Enemigo normal
class Enemy_1(Character):
    def __init__(self):
        super().__init__(hp=80, attack=18, deffense=3, speed=8)

# Enemigo campeón
class Enemy_Champ(Character):
    def __init__(self):
        super().__init__(hp=150, attack=25, deffense=15, speed=15)