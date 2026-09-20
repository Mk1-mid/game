"""
Modelos de datos - Clases para personajes, armas y armaduras
============================================================
"""

# Importar sistema de habilidades
from src.habilidades import obtener_habilidades_arqueotipo

# ============================================
# CLASES BASE DE ITEMS
# ============================================

class Item:
    """Clase base para cualquier objeto equipable."""
    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f"{self.__class__.__name__}({self.nombre})"


class Weapon(Item):
    """Arma que afecta ataque, agilidad y critico."""
    def __init__(self, nombre, attack=0, agilidad=0, peso=0, critico_bonus=0, tier=1, str_requirement=10):
        super().__init__(nombre)
        self.attack = attack
        self.agilidad = agilidad
        self.peso = peso
        self.critico_bonus = critico_bonus
        self.tier = tier  # Tier 1-4 (1: basica, 4: legendaria)
        self.str_requirement = str_requirement  # Fuerza necesaria para usar
        self.nivel_mejora = 0  # Nivel de mejora del Herrero

        # === Fase 3.4: Forja Ampliada ===
        self.arquetipo = "desconocido"    # "daga", "espada_corta", "espada_larga", "tridente", 
                                          # "martillo", "lanza", "hacha", "hacha_grande", "desconocido"
        self.rareza = "comun"             # "comun" | "especial" | "mitica" | "historica"
        self.max_nivel_mejora = 3         # segun rareza: comun=3, especial=4, mitica=5, historica=0
        self.es_historica = False         # True para armas historicas (no mejorables, no reparables)
        self.efecto_especial = None       # dict con efecto especial para armas historicas

    def __repr__(self):
        return f"Weapon({self.nombre}, ATK:{self.attack}, AGI:{self.agilidad}, PESO:{self.peso}kg, CRI:{self.critico_bonus}%, Arq:{self.arquetipo}, Rareza:{self.rareza}, NvMej:{self.nivel_mejora}/{self.max_nivel_mejora})"


class Armor(Item):
    """Armadura que afecta defensa, HP y penaliza agilidad por peso."""
    def __init__(self, nombre, defense=0, hp=0, peso=0):
        super().__init__(nombre)
        self.defense = defense
        self.hp = hp
        self.peso = peso

    def __repr__(self):
        return f"Armor({self.nombre}, DEF:{self.defense}, HP:{self.hp}, PESO:{self.peso}kg)"


class Potion(Item):
    """Pocion consumible con efecto temporal o permanente."""
    def __init__(self, nombre, tipo, valor):
        """
        Args:
            nombre: Nombre de la pocion
            tipo: "heal" (cura HP), "attack" (ATK temporal), "defense" (DEF temporal), "speed" (SPD temporal)
            valor: Cantidad del efecto
        """
        super().__init__(nombre)
        self.tipo = tipo
        self.valor = valor
    
    def usar(self, personaje):
        """Aplica el efecto de la pocion al personaje."""
        if self.tipo == "heal":
            personaje.hp_actual = min(personaje.hp, personaje.hp_actual + self.valor)
            return f"[OK] {personaje.nombre} se curo {self.valor} HP (ahora: {personaje.hp_actual}/{personaje.hp})"
        elif self.tipo == "attack":
            return f"[SWORD]  {personaje.nombre} gano +{self.valor} ATK (efecto temporal)"
        elif self.tipo == "defense":
            return f"🛡️  {personaje.nombre} gano +{self.valor} DEF (efecto temporal)"
        elif self.tipo == "speed":
            return f"⚡ {personaje.nombre} gano +{self.valor} SPD (efecto temporal)"
        return "[FAIL] Pocion invalida"
    
    def __repr__(self):
        return f"Potion({self.nombre}, tipo:{self.tipo}, valor:{self.valor})"


class Material(Item):
    """Material de forja/trabajo con rareza (Fase 3.2+)."""
    RAREZAS = ("comun", "especial", "mitica")

    def __init__(self, nombre, rareza="comun", valor=0):
        """
        Args:
            nombre: Nombre del material (ej: "Mineral de Hierro")
            rareza: "comun" | "especial" | "mitica"
            valor: Valor base en oro (para venta/referencia)
        """
        super().__init__(nombre)
        self.rareza = rareza
        self.valor = valor

    def __repr__(self):
        return f"Material({self.nombre}, {self.rareza}, {self.valor}g)"


# Catalogo de materiales: nombre -> (rareza, valor base)
# La cantera/granja/aserradero de la Fase 3.3 produciran estos materiales.
CATALOGO_MATERIALES = {
    "Mineral de Hierro": ("comun", 20),
    "Mineral Raro": ("especial", 80),
    "Mithril": ("mitica", 300),
    "Cuero": ("comun", 15),
    "Cuero Endurecido": ("especial", 70),
    "Piel de Bestia": ("mitica", 280),
    "Madera de Roble": ("comun", 12),
    "Madera de Ebano": ("especial", 60),
    "Madera Ancestral": ("mitica", 250),
}


# ============================================
# CLASE BASE DE PERSONAJE
# ============================================

class Character:
    """Base para jugador y enemigos con sistema de equipo."""
    
    def __init__(self, hp, attack, defense, agilidad):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.agilidad = agilidad
        self.weapon = None
        self.armor = None

    def ataque_final(self):
        """Calcula ataque total (base + arma)."""
        bonus_arma = self.weapon.attack if self.weapon else 0
        return self.attack + bonus_arma

    def defensa_final(self):
        """Calcula defensa total (base + armadura)."""
        bonus_armadura = self.armor.defense if self.armor else 0
        return self.defense + bonus_armadura

    def hp_final(self):
        """Calcula HP total (base + armadura)."""
        bonus_hp = self.armor.hp if self.armor else 0
        return self.hp + bonus_hp

    @property
    def hp_maximo(self):
        """Alias del HP maximo (sin armadura) para compatibilidad."""
        return self.hp

    def agilidad_final(self):
        """Calcula agilidad total (base + arma)."""
        bonus_agilidad = self.weapon.agilidad if self.weapon else 0
        return self.agilidad + bonus_agilidad

    def equipar_arma(self, weapon):
        """Equipa un arma al personaje y recalcula stats."""
        if isinstance(weapon, Weapon):
            self.weapon = weapon
            # Recalcular si es Gladiador
            if hasattr(self, 'calcular_stats_finales'):
                self.calcular_stats_finales()
            return True
        return False

    def equipar_armadura(self, armor):
        """Equipa una armadura al personaje y recalcula stats."""
        if isinstance(armor, Armor):
            self.armor = armor
            # Recalcular si es Gladiador
            if hasattr(self, 'calcular_stats_finales'):
                self.calcular_stats_finales()
            return True
        return False

    def __repr__(self):
        agilidad_display = self.agilidad_final() if hasattr(self, 'agilidad_final') else self.agilidad
        return (f"{self.__class__.__name__}(HP:{self.hp_final()}, ATK:{self.ataque_final()}, "
                f"DEF:{self.defensa_final()}, AGI:{agilidad_display})")


# ============================================
# CLASES DE JUGADOR
# ============================================

class Player(Character):
    """Clase del jugador principal."""
    
    def __init__(self):
        super().__init__(
            hp=100,
            attack=20,
            defense=5,
            speed=10
        )
        # Progresion del jugador
        self.nivel = 1
        self.xp = 0

    def xp_para_siguiente_nivel(self):
        """XP necesario para alcanzar el siguiente nivel (curva suave)."""
        # Formula base: 100 * (1.1 ^ nivel_actual)
        return int(100 * (1.1 ** self.nivel))

    def subir_nivel(self):
        """Incrementa el nivel y mejora ligeramente las stats base."""
        self.nivel += 1
        # Mejora con rendimientos decrecientes aproximados
        self.hp = int(self.hp * 1.095)
        self.attack = int(self.attack * 1.085)
        self.defense = round(self.defense * 1.075, 2)
        self.speed = round(self.speed * 1.065, 2)

    def ganar_xp(self, cantidad):
        """Anade XP y gestiona subida de nivel. Devuelve True si subio nivel."""
        self.xp += int(max(0, cantidad))
        subio = False
        # Permite subir multiples niveles si se acumulo suficiente XP
        while self.xp >= self.xp_para_siguiente_nivel():
            self.xp -= self.xp_para_siguiente_nivel()
            self.subir_nivel()
            subio = True
        return subio

    def __repr__(self):
        return f"Player({super().__repr__()})"


# ============================================
# CLASE GLADIADOR (Para equipo)
# ============================================

class Gladiador(Character):
    """Gladiador individual con progresion y estado independiente."""
    
    def __init__(self, nombre, tipo_base, nivel=1):
        """
        Args:
            nombre: Nombre del gladiador (ej: "Ferox", "Velox")
            tipo_base: Tipo (Murmillo, Retiarius, Secutor, Thraex, Hoplomachus)
            nivel: Nivel inicial (default 1)
        """
        # Inicializar con stats base (hp, attack, defense, agilidad)
        super().__init__(hp=100, attack=20, defense=5, agilidad=10)
        
        self.nombre = nombre
        self.tipo = tipo_base
        self.nivel = nivel
        self.xp = 0
        
        # NUEVO: Stats principales
        self.fuerza = 15  # Capacidad de carga + dano
        self.critico = 12  # Probabilidad de critico (%)
        self.esquiva = 8   # Probabilidad de esquiva (%)
        
        # === Fase 4: Árbol de Talentos ===
        self.puntos_talento = 0
        self.arbol_talentos = {"fuerza": 0, "resistencia": 0, "agilidad": 0, "tecnica": 0}
        
        # Aplicar arquetipos iniciales por tipo
        self._aplicar_arquetipos_tipo()
        
        # Aplicar escalado del nivel
        for _ in range(nivel - 1):
            self.subir_nivel()
        
        # Recalcular stats derivados
        self.calcular_stats_finales()
        
        # Estado de salud individual
        self.hp_actual = self.hp  # Puede ser menor si esta herido
        self.estado = "sano"  # sano, herido, critico, muerto
        
        # Ocupacion temporal (entrenamiento, curacion)
        self.ocupacion = "disponible"  # disponible, ocupado
        self.dias_ocupado = 0  # Cuantos dias falta para disponible
        self.razon_ocupacion = None  # "entrenamiento", "curacion"
        
        # Historial
        self.combates_totales = 0
        self.combates_ganados = 0
        self.combates_perdidos = 0
        self.dinero_generado = 0
        
        # ⭐ NUEVO: SISTEMA DE HABILIDADES (Fase 2.2)
        # Mapeo entre tipos de gladiador y arquetipos de habilidades
        arqueotipos_mapping = {
            "Murmillo": "Guerrero",      # Fuerte y defensivo
            "Retiarius": "Velocista",    # Rapido y agil
            "Secutor": "Paladin",        # Balanceado
            "Thraex": "Asesino",         # Ofensivo y critico
            "Hoplomachus": "Tanque",     # Defensivo puro
        }
        
        arqueotipo_hab = arqueotipos_mapping.get(self.tipo, "Guerrero")
        self.habilidades = obtener_habilidades_arqueotipo(arqueotipo_hab)
        self.habilidades_activas = {}  # {"nombre": turnos_restantes}
        self.contadores_triggers = {   # Para rastrear triggers
            "esquivas": 0,
            "criticos_recibidos": 0,
            "criticos_propios": 0,
            "dano_recibido": 0,
            "turnos": 0
        }
    
    def _aplicar_arquetipos_tipo(self):
        """Aplica arquetipos iniciales segun tipo de gladiador."""
        arquetipos = {
            "Murmillo": {"fuerza": 25, "agilidad": 10},      # Guerrero fuerte
            "Retiarius": {"fuerza": 12, "agilidad": 22},     # Agil y rapido
            "Secutor": {"fuerza": 18, "agilidad": 15},       # Balanceado
            "Thraex": {"fuerza": 20, "agilidad": 14},        # Ofensivo
            "Hoplomachus": {"fuerza": 16, "agilidad": 12},   # Defensivo
        }
        
        if self.tipo in arquetipos:
            stats = arquetipos[self.tipo]
            self.fuerza = stats["fuerza"]
            self.agilidad = stats["agilidad"]
    
    def xp_para_siguiente_nivel(self):
        """XP necesario para siguiente nivel."""
        return int(100 * (1.1 ** self.nivel))
    
    def subir_nivel(self):
        """Sube de nivel e incrementa stats."""
        self.nivel += 1
        self.hp = int(self.hp * 1.095)
        self.attack = int(self.attack * 1.085)
        self.defense = round(self.defense * 1.075, 2)
        self.agilidad = round(self.agilidad * 1.065, 2)
        self.fuerza = round(self.fuerza * 1.070, 2)
        self.puntos_talento += 1  # NUEVO: Fuerza escala
    
    def calcular_stats_finales(self):
        """NUEVO: Calcula stats finales considerando peso del equipo."""
        # Calcular peso total del equipo
        peso_equipo = 0
        if self.weapon:
            peso_equipo += self.weapon.peso
        if self.armor:
            peso_equipo += self.armor.peso
        
        # Agilidad efectiva = Agilidad base - penalidad de peso / fuerza
        # A mayor fuerza, menos afecta el peso
        penalidad_peso = peso_equipo / max(1, self.fuerza * 0.5)
        self.agilidad_efectiva = max(1, self.agilidad - penalidad_peso)
        
        # CRITICO = Fuerza * 0.3 + Agilidad efectiva * 0.4 - Peso * 0.5
        critico_base = (self.fuerza * 0.3 + self.agilidad_efectiva * 0.4) - (peso_equipo * 0.5)
        
        # Bonus de critico del arma
        critico_arma = self.weapon.critico_bonus if self.weapon else 0
        self.critico = max(1, round(critico_base + critico_arma, 1))
        
        # ESQUIVA = Agilidad efectiva * 0.5 - Peso * 0.6
        esquiva_base = (self.agilidad_efectiva * 0.5) - (peso_equipo * 0.6)
        self.esquiva = max(0, round(esquiva_base, 1))
    
    def ganar_xp(self, cantidad):
        """Gana XP y maneja subidas automaticas."""
        self.xp += int(max(0, cantidad))
        subio = False
        while self.xp >= self.xp_para_siguiente_nivel():
            self.xp -= self.xp_para_siguiente_nivel()
            self.subir_nivel()
            self.calcular_stats_finales()  # Recalcular despues de subir
            subio = True
        return subio
    
    def aplicar_dano(self, dano):
        """Reduce HP actual y actualiza estado."""
        self.hp_actual = max(0, self.hp_actual - dano)
        if self.hp_actual == 0:
            self.estado = "muerto"
        elif self.hp_actual < self.hp * 0.25:
            self.estado = "critico"
        elif self.hp_actual < self.hp * 0.75:
            self.estado = "herido"
        else:
            self.estado = "sano"
    
    def curar(self, cantidad):
        """Cura al gladiador."""
        self.hp_actual = min(self.hp, self.hp_actual + cantidad)
        if self.hp_actual > self.hp * 0.75:
            self.estado = "sano"
        elif self.hp_actual > self.hp * 0.25:
            self.estado = "herido"
    
    def revivir(self):
        """Revive a un gladiador muerto (HP parcial)."""
        if self.estado == "muerto":
            self.hp_actual = int(self.hp * 0.75)
            self.estado = "herido"
    
    def ocupar(self, razon, dias):
        """Marca como ocupado por X dias."""
        self.ocupacion = "ocupado"
        self.dias_ocupado = dias
        self.razon_ocupacion = razon
    
    def pasar_dia(self):
        """Llamado al fin de cada dia."""
        if self.dias_ocupado > 0:
            self.dias_ocupado -= 1
            if self.dias_ocupado == 0:
                self.ocupacion = "disponible"
                self.razon_ocupacion = None
    
    def puede_luchar(self):
        """¿Puede participar en combate?"""
        return self.ocupacion == "disponible" and self.estado != "muerto"
    
    def generar_barra_hp(self):
        """Retorna barra visual de HP con emoji."""
        llenos = int((self.hp_actual / self.hp_final()) * 20)
        porcentaje = int((self.hp_actual / self.hp_final()) * 100)
        barra = "█" * llenos + "░" * (20 - llenos)
        return f"❤️  HP: {self.hp_actual}/{self.hp_final()} ({porcentaje}%)\n{barra}"
    
    def generar_barra_xp(self):
        """Retorna barra visual de XP."""
        xp_max = self.xp_para_siguiente_nivel()
        llenos = int((self.xp / xp_max) * 20)
        porcentaje = int((self.xp / xp_max) * 100)
        barra = "█" * llenos + "░" * (20 - llenos)
        return f"XP: {self.xp}/{xp_max} ({porcentaje}%)\n{barra}"
    
    def generar_string_stats(self):
        """Retorna stats formateados con emojis."""
        atk_final = self.ataque_final()
        def_final = self.defensa_final()
        return f"[SWORD]  ATK: {atk_final}  │  🛡️  DEF: {def_final}  │  ⚡ SPD: {self.agilidad_efectiva}"
    
    def animacion_nivel_up(self):
        """Retorna animacion de subida de nivel."""
        import time
        mensaje = "\n" + "="*50 + "\n"
        mensaje += "        ⭐ ¡SUBISTE DE NIVEL! ⭐\n"
        mensaje += "="*50 + "\n"
        mensaje += f"        Nivel {self.nivel - 1} -> Nivel {self.nivel}\n"
        # Mostrar aproximadamente los incrementos
        hp_inc = int(self.hp * 0.095)
        atk_inc = int(self.attack * 0.085)
        def_inc = int(self.defense * 0.075)
        spd_inc = int(self.agilidad_efectiva * 0.065)
        mensaje += f"        +{hp_inc} HP  │  +{atk_inc} ATK  │  +{def_inc} DEF  │  +{spd_inc} SPD\n"
        mensaje += "="*50 + "\n"
        return mensaje
    
    def __repr__(self):
        return f"Gladiador({self.nombre}, Lvl {self.nivel}, HP {self.hp_actual}/{self.hp}, {self.estado})"


# ============================================
# CLASE BARRACAS (Housing system)
# ============================================

class Barracas:
    """Sistema de barracas/literas para guardar gladiadores."""
    
    def __init__(self):
        """Comienza con 2 literas = 2 espacios."""
        self.literas = 2  # Cantidad de literas
        self.espacios_totales = 2 * 2  # Cada litera = 2 espacios
    
    @property
    def costo_proxima_litera(self):
        """Costo escalado para comprar siguiente litera."""
        # 500g, 1000g, 1500g, 2000g, 2500g...
        return 500 * self.literas
    
    @property
    def proxima_litera_disponible(self):
        """¿Puedes comprar otra litera? (max 5 literas = 10 espacios)."""
        return self.literas < 5
    
    def comprar_litera(self, dinero):
        """
        Intenta comprar una litera (agrega 2 espacios).
        Returns: (exito, dinero_restante, mensaje)
        """
        if not self.proxima_litera_disponible:
            return False, dinero, "[FAIL] Maximo de literas alcanzado (10 espacios)"
        
        costo = self.costo_proxima_litera
        if dinero < costo:
            return False, dinero, f"[FAIL] No tienes suficiente dinero ({costo}g)"
        
        self.literas += 1
        self.espacios_totales += 2
        dinero -= costo
        return True, dinero, f"[OK] Compraste una litera por {costo}g (+2 espacios)"
    
    def __repr__(self):
        return f"Barracas({self.literas} literas, {self.espacios_totales} espacios)"


# ============================================
# CLASE EQUIPO (Gestiona todos los gladiadores)
# ============================================

class Equipo:
    """Gestiona el equipo completo de gladiadores del jugador."""
    
    def __init__(self):
        self.gladiadores = []  # Lista de Gladiador
        self.barracas = Barracas()  # Sistema de literas (2 al inicio)
        self.dinero = 0  # Dinero global
        self.gladiador_activo = None  # Seleccionado para combate

        # === Fase 3.2: Honra, materiales y flags sociales ===
        self.honra = 50              # 0-100; ver titulo_honra() para bandas
        self.racha_victorias_limpias = 0  # se resetea a 0 con cualquier evento turbio
        self.materiales = {}         # {"Mineral de Hierro": 3, ...}
        self.habilitado_clandestino = False  # se activa con el "Rumor de soborno"
        self.rumor_ofrecido = False     # el rumor solo se ofrece UNA vez (gancho)
        self.fama = 0                   # fama publica (sube/baja con desafios)
        self.prestamos_pendientes = []  # [{"patricio", "monto", "dias_restantes"}]
        self.penitencia_fama_dias = 0   # dias con fama atada tras penitencia publica

        # === Fase 3.3: Instalaciones y trabajadores ===
        self.instalaciones = None  # GestorInstalaciones (se crea en main)
        self.trabajadores_activos = []  # [{"gladiador": g, "instalacion_tipo": str, "dias_restantes": int, "dias_totales": int}]

    # --- Honra (Fase 3.2) ---

    def titulo_honra(self):
        """Titulo narrativo segun honra (bandas sin huecos: 0-100)."""
        if self.honra >= 80:
            return "El Honorable"
        elif self.honra >= 60:
            return "El Respetable"
        elif self.honra >= 40:
            return None  # zona neutra, sin titulo
        elif self.honra >= 20:
            return "El Turbio"
        else:
            return "El Corrupto de Roma"  # 0-19

    def modificador_mercado(self):
        """Multiplicador de precios del mercado segun honra (Fase 3.2)."""
        if self.honra >= 70:
            return 0.90  # -10%: honorables inspiran confianza
        elif self.honra <= 19:
            return 1.15  # +15%: los mercaderes desconfian
        return 1.0

    def modificar_honra(self, delta):
        """Suma/resta honra manteniendo limites 0-100. Retorna el valor final."""
        self.honra = max(0, min(100, self.honra + delta))
        return self.honra

    def registrar_victoria_limpia(self):
        """
        Victoria en arena oficial: +1 honra (+2 con racha >= 5) y racha +1.
        Es el "camino lento" de redencion: subir honra sin eventos turbios.
        """
        self.racha_victorias_limpias += 1
        ganancia = 2 if self.racha_victorias_limpias >= 5 else 1
        return self.modificar_honra(ganancia)

    def registrar_evento_turbio(self, costo_honra):
        """
        Participacion en evento clandestino: baja honra Y reinicia la racha.
        La racha (no el numero de honra) es el compromiso real de redencion.
        """
        self.racha_victorias_limpias = 0
        return self.modificar_honra(-abs(costo_honra))

    # --- Materiales (Fase 3.2) ---

    def agregar_material(self, nombre, cantidad=1):
        """Anade materiales al inventario. Retorna la cantidad total actual."""
        if cantidad <= 0:
            return self.materiales.get(nombre, 0)
        self.materiales[nombre] = self.materiales.get(nombre, 0) + cantidad
        return self.materiales[nombre]

    def tiene_material(self, nombre, cantidad=1):
        """Verifica si hay suficiente de un material."""
        return self.materiales.get(nombre, 0) >= cantidad

    def consumir_material(self, nombre, cantidad=1):
        """
        Consume materiales del inventario.
        Retorna (exito, cantidad_consumida, mensaje) — patron de 3 valores.
        """
        if not self.tiene_material(nombre, cantidad):
            actual = self.materiales.get(nombre, 0)
            return False, 0, f"[FAIL] Faltan materiales: {nombre} ({actual}/{cantidad})"
        self.materiales[nombre] -= cantidad
        if self.materiales[nombre] <= 0:
            del self.materiales[nombre]
        return True, cantidad, f"[OK] Usados {cantidad}x {nombre}"
    
    @property
    def espacios_disponibles(self):
        """Espacios libres en barracas."""
        return self.barracas.espacios_totales - len(self.gladiadores)
    
    @property
    def equipo_lleno(self):
        """¿Ya no hay espacio?"""
        return len(self.gladiadores) >= self.barracas.espacios_totales
    
    def agregar_gladiador(self, gladiador):
        """Anade un gladiador al equipo si hay espacio."""
        if len(self.gladiadores) >= self.barracas.espacios_totales:
            return False, "[FAIL] Barracas llenas"
        self.gladiadores.append(gladiador)
        return True, f"[OK] {gladiador.nombre} se unio al equipo"
    
    def remover_gladiador(self, indice):
        """Elimina un gladiador del equipo."""
        if 0 <= indice < len(self.gladiadores):
            nombre = self.gladiadores[indice].nombre
            self.gladiadores.pop(indice)
            return True, f"[OK] {nombre} fue removido del equipo"
        return False, "[FAIL] Indice invalido"
    
    def calcular_nivel_promedio(self):
        """Nivel promedio del equipo."""
        if not self.gladiadores:
            return 0
        return sum(g.nivel for g in self.gladiadores) // len(self.gladiadores)
    
    def todos_muertos(self):
        """¿Perdiste? (todos los gladiadores muertos)."""
        if not self.gladiadores:
            return True
        return all(g.estado == "muerto" for g in self.gladiadores)
    
    def seleccionar_luchador(self, indice):
        """Selecciona que gladiador pelea ahora."""
        if 0 <= indice < len(self.gladiadores):
            if self.gladiadores[indice].puede_luchar():
                self.gladiador_activo = self.gladiadores[indice]
                return True, f"[OK] {self.gladiador_activo.nombre} seleccionado"
            else:
                return False, f"[FAIL] {self.gladiadores[indice].nombre} no puede luchar"
        return False, "[FAIL] Indice invalido"
    
    def pasar_dia(self):
        """Llamado al fin de cada dia - todos avanzan recuperacion."""
        for gladiador in self.gladiadores:
            gladiador.pasar_dia()

        # Fase 3.3: Procesar trabajadores en instalaciones
        if self.instalaciones:
            self._procesar_trabajadores()

    # --- Fase 3.3: Instalaciones y Trabajadores ---

    def _procesar_trabajadores(self):
        """Procesa el avance de los trabajadores en instalaciones (llamado en pasar_dia)."""
        if not self.instalaciones or not self.trabajadores_activos:
            return

        completados = []
        for i, trabajo in enumerate(self.trabajadores_activos):
            trabajo["dias_restantes"] -= 1
            if trabajo["dias_restantes"] <= 0:
                completados.append((i, trabajo))

        # Procesar completados en orden inverso para no romper indices
        for idx, trabajo in reversed(completados):
            self._finalizar_trabajo(idx, trabajo)

    def _finalizar_trabajo(self, idx: int, trabajo: Dict):
        """
        Procesa la finalizacion de un trabajo y otorga recompensas.
        Args:
            idx: indice en self.trabajadores_activos
            trabajo: dict con gladiador, instalacion_tipo, dias_totales
        """
        if not self.instalaciones:
            return

        gladiador = trabajo["gladiador"]
        tipo = trabajo["instalacion_tipo"]
        dias = trabajo["dias_totales"]

        instalacion = self.instalaciones.obtener_por_tipo(tipo)
        if not instalacion or not instalacion.comprada:
            # Instalacion ya no existe, solo devolver gladiador
            self.trabajadores_activos.pop(idx)
            return

        # Calcular recompensas
        materiales, xp, stat_gain = instalacion.calcular_recompensas_trabajo(trabajo["dias_totales"])

        # Otorgar materiales
        for mat in materiales:
            self.agregar_material(mat.nombre, 1)

        # Otorgar XP
        gladiador.ganar_xp(xp)

        # Otorgar stat
        stat = instalacion.stat_objetivo
        if stat == "hp":
            # Vitalidad = HP base + HP actual proporcional
            hp_antes = gladiador.hp
            gladiador.hp += stat_gain
            gladiador.hp_actual = min(gladiador.hp_actual + stat_gain, gladiador.hp)
            hp_ganado = gladiador.hp - hp_antes
            stat_msg = f"+{hp_ganado} HP (Vitalidad)"
        elif stat == "fuerza":
            gladiador.fuerza += stat_gain
            stat_msg = f"+{stat_gain} Fuerza"
        elif stat == "agilidad":
            gladiador.agilidad += stat_gain
            stat_msg = f"+{stat_gain} Agilidad"
        else:
            stat_msg = f"+{stat_gain} {stat}"

        # Recalcular stats derivados si cambio fuerza/agilidad
        if stat in ("fuerza", "agilidad"):
            gladiador.calcular_stats_finales()

        # Riesgo de herida
        msg_herida = None
        if instalacion.riesgo_herida(trabajo["dias_totales"]) > 0:
            msg_herida = instalacion.procesar_riesgo_herida(gladiador, trabajo["dias_totales"])

        # Generar mensaje de retorno
        mats_str = ", ".join(f"{m.nombre} ({m.rareza})" for m in materiales) if materiales else "nada"
        msg = (f"[MEDAL] {gladiador.nombre} volvio del trabajo en {instalacion.nombre}: "
               f"{len(materiales)} materiales ({mats_str}), +{xp} XP, {stat_msg}")
        if msg_herida:
            msg += f" | {msg_herida}"

        print(msg)

        # Remover de trabajadores
        self.trabajadores_activos.pop(idx)

    def asignar_trabajador(self, gladiador_idx: int, instalacion_tipo: str, dias: int) -> Tuple[bool, str]:
        """
        Asigna un gladiador a trabajar en una instalacion.

        Args:
            gladiador_idx: indice en self.gladiadores
            instalacion_tipo: "cantera", "granja", "aserradero"
            dias: 1, 3, o 5

        Returns:
            (exito, mensaje)
        """
        if not self.instalaciones:
            return False, "[FAIL] No hay instalaciones disponibles"

        if gladiador_idx < 0 or gladiador_idx >= len(self.gladiadores):
            return False, "[FAIL] Indice de gladiador invalido"

        gladiador = self.gladiadores[gladiador_idx]

        if not gladiador.puede_luchar():
            return False, f"[FAIL] {gladiador.nombre} no esta disponible (estado: {gladiador.estado})"

        if gladiador.ocupacion == "ocupado":
            return False, f"[FAIL] {gladiador.nombre} ya esta ocupado ({gladiador.razon_ocupacion})"

        if not self.instalaciones:
            return False, "[FAIL] No hay instalaciones construidas"

        instalacion = self.instalaciones.obtener_por_tipo(instalacion_tipo)
        if not instalacion or not instalacion.comprada:
            return False, f"[FAIL] Instalacion no disponible o no construida"

        if dias not in (1, 3, 5):
            return False, "[FAIL] Dias de trabajo invalidos (1, 3 o 5)"

        # Marcar como ocupado
        gladiador.ocupar("trabajo " + instalacion.nombre, dias)

        # Registrar trabajador
        self.trabajadores_activos.append({
            "gladiador": gladiador,
            "instalacion_tipo": instalacion_tipo,
            "dias_restantes": dias,
            "dias_totales": dias,
        })

        return True, f"[OK] {gladiador.nombre} enviado a {instalacion.nombre} por {dias} dia(s)"

    def obtener_trabajadores_info(self) -> List[Dict]:
        """Info de trabajadores para mostrar en menu."""
        info = []
        for t in self.trabajadores_activos:
            g = t["gladiador"]
            inst = self.instalaciones.obtener_por_tipo(t["instalacion_tipo"]) if self.instalaciones else None
            info.append({
                "gladiador": g.nombre,
                "instalacion": inst.nombre if inst else t["instalacion_tipo"],
                "dias_restantes": t["dias_restantes"],
                "dias_totales": t["dias_totales"],
            })
        return info
        return f"Equipo({len(self.gladiadores)}/{self.barracas.espacios_totales} gladiadores, {self.dinero}g)"


# ============================================
# CLASES DE ENEMIGOS BASICOS (Heredadas)
# ============================================

class EnemyBasic(Character):
    """Enemigo basico estandar."""
    
    def __init__(self):
        super().__init__(
            hp=80,
            attack=18,
            defense=3,
            speed=8
        )


class EnemyChampion(Character):
    """Enemigo campeon - version mejorada."""
    
    def __init__(self):
        super().__init__(
            hp=150,
            attack=25,
            defense=15,
            speed=15
        )


# ============================================
# FASE 2.4: SISTEMA DE LIGAS Y RANKING
# ============================================

from enum import Enum
from datetime import datetime

class Liga(Enum):
    """Categorias de liga."""
    BRONCE = "Bronce"      # 0-99 puntos
    PLATA = "Plata"        # 100-249 puntos
    ORO = "Oro"            # 250-499 puntos
    LEYENDA = "Leyenda"    # 500+ puntos


class CombateHistorial:
    """Registro de un combate completado."""
    
    def __init__(self, nombre_gladiador, nombre_enemigo, dificultad, victoria, 
                 puntos_ganados, xp_ganados, dinero_ganado, nivel_gladiador):
        self.nombre_gladiador = nombre_gladiador
        self.nombre_enemigo = nombre_enemigo
        self.dificultad = dificultad
        self.victoria = victoria
        self.puntos_ganados = puntos_ganados
        self.xp_ganados = xp_ganados
        self.dinero_ganado = dinero_ganado
        self.nivel_gladiador = nivel_gladiador
        self.fecha = datetime.now()
    
    def __repr__(self):
        resultado = "[OK]" if self.victoria else "✗"
        return f"{resultado} {self.nombre_gladiador} vs {self.nombre_enemigo} ({self.dificultad}) - {self.puntos_ganados}pts"


class SistemaLigas:
    """Gestiona ligas, ranking y competiciones."""
    
    def __init__(self):
        self.historial_combates = []  # Lista de CombateHistorial
        self.ranking = {}  # {nombre_gladiador: {"puntos": int, "victorias": int, "derrotas": int}}
    
    def registrar_combate(self, gladiador, nombre_enemigo, dificultad, victoria):
        """Registra un combate y actualiza ranking."""
        # Calcular puntos ganados segun dificultad y resultado
        puntos_base = {
            "🟢 NOVATO": 10,
            "🟡 NORMAL": 20,
            "🔴 EXPERTO": 40,
            "⭐ LEGENDARIA": 80
        }
        
        puntos = puntos_base.get(dificultad, 0)
        if not victoria:
            puntos = max(5, puntos // 2)  # Minimo 5 puntos por derrota
        
        xp_ganados = 50 if victoria else 25
        dinero_ganado = 100 if victoria else 0
        
        # Crear registro
        combate = CombateHistorial(
            nombre_gladiador=gladiador.nombre,
            nombre_enemigo=nombre_enemigo,
            dificultad=dificultad,
            victoria=victoria,
            puntos_ganados=puntos,
            xp_ganados=xp_ganados,
            dinero_ganado=dinero_ganado,
            nivel_gladiador=gladiador.nivel
        )
        
        self.historial_combates.append(combate)
        
        # Actualizar ranking
        if gladiador.nombre not in self.ranking:
            self.ranking[gladiador.nombre] = {
                "puntos": 0,
                "victorias": 0,
                "derrotas": 0,
                "combates_totales": 0,
                "liga": Liga.BRONCE
            }
        
        stats = self.ranking[gladiador.nombre]
        stats["puntos"] += puntos
        stats["combates_totales"] += 1
        
        if victoria:
            stats["victorias"] += 1
        else:
            stats["derrotas"] += 1
        
        # Actualizar liga segun puntos
        stats["liga"] = self._calcular_liga(stats["puntos"])
        
        return puntos, xp_ganados, dinero_ganado
    
    def _calcular_liga(self, puntos):
        """Calcula la liga segun puntos."""
        if puntos >= 500:
            return Liga.LEYENDA
        elif puntos >= 250:
            return Liga.ORO
        elif puntos >= 100:
            return Liga.PLATA
        else:
            return Liga.BRONCE
    
    def obtener_liga(self, nombre_gladiador):
        """Obtiene liga actual del gladiador."""
        if nombre_gladiador in self.ranking:
            return self.ranking[nombre_gladiador]["liga"]
        return Liga.BRONCE
    
    def obtener_puntos(self, nombre_gladiador):
        """Obtiene puntos del gladiador."""
        if nombre_gladiador in self.ranking:
            return self.ranking[nombre_gladiador]["puntos"]
        return 0
    
    def obtener_winrate(self, nombre_gladiador):
        """Calcula winrate (victorias/totales) en porcentaje."""
        if nombre_gladiador not in self.ranking:
            return 0
        
        stats = self.ranking[nombre_gladiador]
        if stats["combates_totales"] == 0:
            return 0
        
        return int((stats["victorias"] / stats["combates_totales"]) * 100)
    
    def obtener_ranking_top10(self):
        """Retorna top 10 de gladiadores por puntos."""
        ranking_ordenado = sorted(
            self.ranking.items(),
            key=lambda x: x[1]["puntos"],
            reverse=True
        )
        return ranking_ordenado[:10]
    
    def obtener_historial(self, nombre_gladiador=None, limite=10):
        """Retorna historial de combates (opcional filtrado por gladiador)."""
        historial = self.historial_combates
        
        if nombre_gladiador:
            historial = [c for c in historial if c.nombre_gladiador == nombre_gladiador]
        
        return historial[-limite:]  # Ultimos N combates
    
    def generar_reporte_estadisticas(self, nombre_gladiador):
        """Genera reporte completo de un gladiador."""
        if nombre_gladiador not in self.ranking:
            return None
        
        stats = self.ranking[nombre_gladiador]
        liga = stats["liga"]
        puntos = stats["puntos"]
        victorias = stats["victorias"]
        derrotas = stats["derrotas"]
        winrate = self.obtener_winrate(nombre_gladiador)
        
        return {
            "nombre": nombre_gladiador,
            "liga": liga.value,
            "puntos": puntos,
            "victorias": victorias,
            "derrotas": derrotas,
            "combates": stats["combates_totales"],
            "winrate": winrate
        }
    
    def __repr__(self):
        return f"SistemaLigas(gladiadores: {len(self.ranking)}, combates: {len(self.historial_combates)})"

# ============================================
# FASE 4: SISTEMA DE TORNEOS Y LIGAS AUTOMATICAS
# ============================================

from datetime import datetime, timedelta
import random

class Emparejamiento:
    """Representa un enfrentamiento (participante1 vs participante2)."""
    
    def __init__(self, participante1, participante2, numero_ronda):
        self.participante1 = participante1
        self.participante2 = participante2
        self.numero_ronda = numero_ronda
        self.ganador = None
        self.completado = False
    
    def completar(self, ganador):
        """Marca el emparejamiento como completado."""
        self.ganador = ganador
        self.completado = True
    
    def __repr__(self):
        if self.completado:
            return f"Ronda {self.numero_ronda}: {self.participante1} vs {self.participante2} -> [OK] {self.ganador}"
        return f"Ronda {self.numero_ronda}: {self.participante1} vs {self.participante2} (pendiente)"


class Torneo:
    """Sistema de torneos con brackets y rondas."""
    
    def __init__(self, nombre, participantes):
        self.nombre = nombre
        self.participantes = list(participantes)  # Lista de Gladiador
        self.rondas = []  # Lista de listas de Emparejamiento
        self.ganador = None
        self.estado = "creado"  # creado, en_progreso, finalizado
        self.fecha_creacion = datetime.now()
        self._generar_brackets()
    
    def _generar_brackets(self):
        """Genera el sistema de brackets (arbol de eliminacion directa)."""
        # Si no es potencia de 2, agregamos "byes" (avances automaticos)
        n = len(self.participantes)
        if n & (n - 1) != 0:  # No es potencia de 2
            # Calcular siguiente potencia de 2
            potencia = 1
            while potencia < n:
                potencia *= 2
            # Agregar byes ficticios
            byes_necesarios = potencia - n
            for _ in range(byes_necesarios):
                self.participantes.append(None)  # None representa bye
        
        # Shufflear para mayor variedad
        random.shuffle(self.participantes)
        
        # Crear primera ronda
        participantes_actuales = self.participantes[:]
        numero_ronda = 1
        
        while len(participantes_actuales) > 1:
            ronda = []
            for i in range(0, len(participantes_actuales), 2):
                p1 = participantes_actuales[i]
                p2 = participantes_actuales[i + 1] if i + 1 < len(participantes_actuales) else None
                
                if p1 is None or p2 is None:
                    # Uno tiene bye automatico, avanza sin jugar
                    if p1 is None:
                        participantes_actuales[i] = p2
                    # Si ambos None, mantener None
                else:
                    emparejamiento = Emparejamiento(p1.nombre, p2.nombre, numero_ronda)
                    ronda.append(emparejamiento)
            
            if ronda:
                self.rondas.append(ronda)
            
            # Preparar siguiente ronda
            participantes_actuales = [
                p for p in participantes_actuales if p is not None
            ]
            numero_ronda += 1
    
    def obtener_siguiente_emparejamiento_pendiente(self):
        """Retorna el siguiente emparejamiento sin completar."""
        for ronda in self.rondas:
            for emparejamiento in ronda:
                if not emparejamiento.completado:
                    return emparejamiento
        return None
    
    def completar_emparejamiento(self, ganador_nombre):
        """Marca un emparejamiento como completado."""
        emparejamiento = self.obtener_siguiente_emparejamiento_pendiente()
        if emparejamiento:
            emparejamiento.completar(ganador_nombre)
            # Avanzar ganador a siguiente ronda si existe
            self._avanzar_ganador(ganador_nombre, emparejamiento.numero_ronda)
            
            # Verificar si torneo termino
            if self._verificar_finalizado():
                self.estado = "finalizado"
                self.ganador = ganador_nombre
            
            return True
        return False
    
    def _avanzar_ganador(self, ganador, ronda_actual):
        """Avanza el ganador a la siguiente ronda."""
        if ronda_actual < len(self.rondas):
            siguiente_ronda = self.rondas[ronda_actual]
            # Buscar slot disponible en siguiente ronda
            for emparejamiento in siguiente_ronda:
                if ganador == emparejamiento.participante1 or ganador == emparejamiento.participante2:
                    return  # Ya esta asignado
    
    def _verificar_finalizado(self):
        """Verifica si todos los emparejamientos estan completados."""
        for ronda in self.rondas:
            for emparejamiento in ronda:
                if not emparejamiento.completado:
                    return False
        return True
    
    def obtener_estado_torneo(self):
        """Retorna estado actual del torneo."""
        total_emparejamientos = sum(len(ronda) for ronda in self.rondas)
        completados = sum(
            1 for ronda in self.rondas 
            for emp in ronda if emp.completado
        )
        return {
            "nombre": self.nombre,
            "total_participantes": len([p for p in self.participantes if p is not None]),
            "estado": self.estado,
            "emparejamientos_completados": completados,
            "emparejamientos_totales": total_emparejamientos,
            "ganador": self.ganador
        }
    
    def __repr__(self):
        return f"Torneo({self.nombre}, {len([p for p in self.participantes if p])} participantes, {self.estado})"


class Temporada:
    """Una temporada de ligas automaticas (puntos reseteables)."""
    
    def __init__(self, numero, fecha_inicio):
        self.numero = numero
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = None
        self.ranking_final = {}  # {nombre: puntos_finales}
        self.recompensas_entregadas = {}
        self.finalizada = False
    
    def __repr__(self):
        estado = "Finalizada" if self.finalizada else "Activa"
        return f"Temporada {self.numero} ({estado})"


class LigasAutomaticas:
    """Gestiona temporadas automaticas de ligas con resets."""
    
    def __init__(self):
        self.temporada_actual = 1
        self.temporadas = {}  # {numero: Temporada}
        self.fecha_ultima_reset = datetime.now()
        self.ranking_temporal = {}  # Puntos durante temporada actual
        self._iniciar_temporada()
    
    def _iniciar_temporada(self):
        """Inicia una nueva temporada."""
        self.temporadas[self.temporada_actual] = Temporada(
            self.temporada_actual,
            datetime.now()
        )
        self.ranking_temporal = {}
    
    def actualizar_puntos(self, nombre_gladiador, puntos_ganados):
        """Actualiza puntos durante la temporada actual."""
        if nombre_gladiador not in self.ranking_temporal:
            self.ranking_temporal[nombre_gladiador] = 0
        self.ranking_temporal[nombre_gladiador] += puntos_ganados
    
    def obtener_puntos_temporada(self, nombre_gladiador):
        """Obtiene puntos de la temporada actual."""
        return self.ranking_temporal.get(nombre_gladiador, 0)
    
    def obtener_liga_temporada(self, nombre_gladiador):
        """Obtiene liga segun puntos de temporada actual."""
        puntos = self.obtener_puntos_temporada(nombre_gladiador)
        if puntos >= 500:
            return Liga.LEYENDA
        elif puntos >= 250:
            return Liga.ORO
        elif puntos >= 100:
            return Liga.PLATA
        else:
            return Liga.BRONCE
    
    def obtener_ranking_temporada(self):
        """Retorna ranking actual ordenado por puntos."""
        return sorted(
            self.ranking_temporal.items(),
            key=lambda x: x[1],
            reverse=True
        )
    
    def calcular_recompensas_liga(self, nombre_gladiador, equipos_dict):
        """Calcula recompensas por liga alcanzada."""
        liga = self.obtener_liga_temporada(nombre_gladiador)
        recompensas = {
            "dinero": 0,
            "items": []
        }
        
        # Recompensas por liga
        if liga == Liga.BRONCE:
            recompensas["dinero"] = 100
        elif liga == Liga.PLATA:
            recompensas["dinero"] = 250
            recompensas["items"] = ["Pocion de Vida x2"]
        elif liga == Liga.ORO:
            recompensas["dinero"] = 500
            recompensas["items"] = ["Pocion de Vida x5", "Mineral Raro x1"]
        elif liga == Liga.LEYENDA:
            recompensas["dinero"] = 1000
            recompensas["items"] = ["Pocion de Vida x10", "Mineral Raro x3", "Equipo Legendario"]
        
        return recompensas
    
    def entregar_recompensas(self, nombre_gladiador, equipo):
        """Entrega recompensas al gladiador (asume que equipo lo contiene)."""
        recompensas = self.calcular_recompensas_liga(nombre_gladiador, None)
        
        # Buscar gladiador en equipo
        for gladiador in equipo.integrantes:
            if gladiador.nombre == nombre_gladiador:
                # Agregar dinero al equipo
                equipo.dinero += recompensas["dinero"]
                
                # Registrar entrega
                liga = self.obtener_liga_temporada(nombre_gladiador)
                self.temporadas[self.temporada_actual].recompensas_entregadas[
                    nombre_gladiador
                ] = {
                    "liga": liga.value,
                    "recompensas": recompensas,
                    "fecha": datetime.now()
                }
                
                return True
        
        return False
    
    def finalizar_temporada(self):
        """Finaliza la temporada actual y crea una nueva."""
        temporada = self.temporadas[self.temporada_actual]
        temporada.ranking_final = dict(self.ranking_temporal)
        temporada.fecha_fin = datetime.now()
        temporada.finalizada = True
        
        # Crear nueva temporada
        self.temporada_actual += 1
        self.fecha_ultima_reset = datetime.now()
        self._iniciar_temporada()
        
        return temporada
    
    def obtener_historial_temporadas(self):
        """Retorna historial de todas las temporadas finalizadas."""
        return {
            num: temp for num, temp in self.temporadas.items()
            if temp.finalizada
        }
    
    def __repr__(self):
        return f"LigasAutomaticas(temporada {self.temporada_actual}, {len(self.ranking_temporal)} gladiadores)"