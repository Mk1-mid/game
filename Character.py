#Clase base para cualquier objeto equipable.
class Item:
    def __init__(self, nombre):
        self.nombre = nombre

#Clases derivadas
class Weapon(Item):
    #Afecta ataque y velocidad
    def __init__(self, nombre, attack=0, speed=0):
        super().__init__(nombre)
        self.attack = attack
        self.speed = speed
class Armor(Item):
    #Afecta defensa y velocidad
    def __init__(self, nombre, deffense=0, hp=0):
        super().__init__(nombre)
        self.deffense = deffense
        self.hp = hp

#Ejemplo de items disponibles  
objetos_disponibles = {
    "Espada de Acero": Weapon("Espada de Acero", attack=2,speed=1),
    "Armadura_cuero": Armor("Armadura de Cuero", defensa=3, hp=10)
}

#Clase de personaje que se usa como molde para hacer a los demas
class Character:
    def __init__(self, hp, attack, deffense, speed):
        self.hp = hp
        self.attack = attack
        self.deffense = deffense
        self.speed = speed

        #Los items actuales del personaje
        self.weapon=None
        self.armor=None

    #Función para calcular la cantidad de ataque final del personaje al pelear
    def ataque_final(self):
        if self.weapon:
            return self.attack + (self.weapon.attack if self.weapon else 0)
    #Función para calcular la cantidad de defensa final del personaje al pelear
    def defensa_final(self):
        if self.armor:
            return self.deffense + (self.armor.deffense if self.armor else 0)
    #Función para calcular la cantidad de vida final del personaje al pelear
    def hp_final(self):
        return self.hp + (self.armor.hp if self.armor else 0)
    #Función para calcular la cantidad de velocidad final del personaje al pelear
    def velocidad(self):
        return self.velocidad_base + (self.weapon.velocidad if self.weapon else 0)



#Clase jugador
class Player(Character):
    def __init__(self):
        #Se define cuales son las estadisticas base del jugador
        super().__init__(hp=10, attack=1, deffense=1, speed=1,)

#Se define la clase enemigo 
class Enemy_1(Character):
    def __init__(self):
        #Se define cuales son las estadisticas base del enemigo
        super().__init__(hp=12, attack=1, deffense=1, speed=1)
#Se debe especificar a cual envia dependiendo de la situacion
class Enemy_Champ(Character):
    def __init__(self):
        #Se define cuales son las estadisticas base del enemigo
        super().__init__(hp=30, attack=10, deffense=10, speed=15)

