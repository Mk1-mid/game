"""
Instalaciones de Recursos (Fase 3.3)
=====================================

Tres instalaciones productoras de materiales para la Forja (Fase 3.4):

- ⛏️ Cantera    → Minerales (Hierro, Raro, Mithril) → Stat: Fuerza
- 🐄 Granja     → Cueros (Común, Endurecido, Bestia) → Stat: Agilidad
- 🪵 Aserradero → Maderas (Roble, Ébano, Ancestral) → Stat: Vitalidad (HP)

Diseño:
- Todas requieren Herrero nivel 2 (prerequisito temático: materiales sin forja no sirven)
- Precio base 2500g c/u, mejoras escalonadas
- Rarezas con clamp duro: mítica ≤8%, común ≥60%, especial absorbe resto
- Trabajo: 1/3/5 días → XP/stat/materiales escalados, riesgo herida
- Ingreso pasivo diario por nivel
- Ocupación reusa sistema existente (ocupar/pasar_dia)
"""

import random
from typing import Dict, List, Tuple, Optional

# Importar Material del catálogo
from .models import Material, CATALOGO_MATERIALES


# ============================================
# CATÁLOGOS DE MATERIALES POR INSTALACIÓN
# ============================================

MATERIALES_CANTERA = {
    "comun": ["Mineral de Hierro"],
    "especial": ["Mineral Raro"],
    "mitica": ["Mithril"],
}

MATERIALES_GRANJA = {
    "comun": ["Cuero"],
    "especial": ["Cuero Endurecido"],
    "mitica": ["Piel de Bestia"],
}

MATERIALES_ASERRADERO = {
    "comun": ["Madera de Roble"],
    "especial": ["Madera de Ébano"],
    "mitica": ["Madera Ancestral"],
}

CATALOGO_POR_INSTALACION = {
    "cantera": MATERIALES_CANTERA,
    "granja": MATERIALES_GRANJA,
    "aserradero": MATERIALES_ASERRADERO,
}

# Nombres legibles
NOMBRES_INSTALACION = {
    "cantera": "⛏️ Cantera",
    "granja": "🐄 Granja",
    "aserradero": "🪵 Aserradero",
}

# Stat que mejora cada instalación
STAT_POR_INSTALACION = {
    "cantera": "fuerza",
    "granja": "agilidad",
    "aserradero": "hp",  # Vitalidad = HP
}

# Nombres de stat para mensajes
NOMBRE_STAT = {
    "fuerza": "Fuerza",
    "agilidad": "Agilidad",
    "hp": "Vitalidad",
}

# Ingreso pasivo por nivel
INGRESO_POR_NIVEL = {
    1: 50,
    2: 75,
    3: 100,
    4: 125,
    5: 150,
}

# Precios de compra y mejoras
PRECIO_BASE = 2500
COSTOS_MEJORA = {
    1: 1200,   # 1 → 2
    2: 2200,   # 2 → 3
    3: 3500,   # 3 → 4
    4: 5000,   # 4 → 5
}

# Probabilidades base por nivel (sin días extra)
PROBABILIDADES_BASE = {
    1: {"comun": 75, "especial": 20, "mitica": 5},
    2: {"comun": 70, "especial": 25, "mitica": 5},
    3: {"comun": 65, "especial": 28, "mitica": 7},
    4: {"comun": 62, "especial": 30, "mitica": 8},
    5: {"comun": 60, "especial": 32, "mitica": 8},
}

# Multiplicadores por días de trabajo
MULTIPLICADORES_DIAS = {
    1: {"especial": 1.0, "mitica": 1.0, "yield": 1},
    3: {"especial": 1.5, "mitica": 1.2, "yield": 2},
    5: {"especial": 2.5, "mitica": 1.8, "yield": 3},
}

# Riesgo de herida por días
RIESGO_HERIDA = {
    1: 0.05,
    3: 0.12,
    5: 0.20,
}

# Herrero mínimo requerido
HERRERO_MINIMO = 2


# ============================================
# FUNCIÓN DE PROBABILIDADES (con clamp duro)
# ============================================

def calcular_probabilidades(nivel: int, dias: int) -> Dict[str, float]:
    """
    Calcula probabilidades de rareza con clamp duro post-normalización.

    Proceso:
    1. Base por nivel
    2. Aplicar multiplicadores por días (especial, mítica)
    3. Normalizar a 100%
    4. CLAMP: mítica ≤8%, común ≥60%
    5. Especial absorbe el resto
    """
    if nivel not in PROBABILIDADES_BASE:
        nivel = 1
    if dias not in MULTIPLICADORES_DIAS:
        dias = 1

    base = PROBABILIDADES_BASE[nivel].copy()
    mult = MULTIPLICADORES_DIAS[dias]

    # Aplicar multiplicadores
    base["especial"] *= mult["especial"]
    base["mitica"] *= mult["mitica"]
    # común no cambia (×1.0)

    # Normalizar a 100%
    total = base["comun"] + base["especial"] + base["mitica"]
    for k in base:
        base[k] = (base[k] / total) * 100.0

    # CLAMP DURO post-normalización
    # Mítica nunca > 8%
    if base["mitica"] > 8.0:
        exceso = base["mitica"] - 8.0
        base["mitica"] = 8.0
        base["especial"] += exceso

    # Común nunca < 60%
    if base["comun"] < 60.0:
        deficit = 60.0 - base["comun"]
        base["comun"] = 60.0
        base["especial"] -= deficit
        # Si especial baja mucho, asegurar mínimo
        if base["especial"] < 0:
            base["especial"] = 0

    # Especial absorbe el resto (asegura suma = 100)
    base["especial"] = 100.0 - base["comun"] - base["mitica"]

    # Redondear a 1 decimal
    return {k: round(v, 1) for k, v in base.items()}


# ============================================
# CLASE INSTALACIÓN INDIVIDUAL
# ============================================

class InstalacionRecursos:
    """
    Una instalación de recursos (Cantera/Granja/Aserradero).

    Responsabilidades:
    - Estado: comprada, nivel, tipo
    - Compra/mejora con validación de dinero y prerequisitos
    - Cálculo de probabilidades con clamp duro
    - Generación de drops (materiales)
    - Ingreso pasivo diario
    """

    def __init__(self, tipo: str):
        """
        Args:
            tipo: "cantera" | "granja" | "aserradero"
        """
        if tipo not in CATALOGO_POR_INSTALACION:
            raise ValueError(f"Tipo de instalación inválido: {tipo}")

        self.tipo = tipo
        self.comprada = False
        self.nivel = 0

    @property
    def nombre(self) -> str:
        return NOMBRES_INSTALACION[self.tipo]

    @property
    def stat_objetivo(self) -> str:
        return STAT_POR_INSTALACION[self.tipo]

    @property
    def nombre_stat(self) -> str:
        return NOMBRE_STAT[self.stat_objetivo]

    @property
    def catalogo_materiales(self) -> Dict[str, List[str]]:
        return CATALOGO_POR_INSTALACION[self.tipo]

    @property
    def ingreso_diario(self) -> int:
        if not self.comprada or self.nivel == 0:
            return 0
        return INGRESO_POR_NIVEL.get(self.nivel, 0)

    @property
    def puede_mejorar(self) -> bool:
        return self.comprada and self.nivel < 5

    @property
    def costo_proxima_mejora(self) -> int:
        if self.puede_mejorar:
            return COSTOS_MEJORA[self.nivel]
        return 0

    def puede_comprar(self, herrero_nivel: int) -> Tuple[bool, str]:
        """Verifica si se puede comprar (prerequisito de herrero)."""
        if self.comprada:
            return False, f"❌ {self.nombre} ya está comprada"
        if herrero_nivel < HERRERO_MINIMO:
            return False, f"🔒 Requiere Herrero nivel {HERRERO_MINIMO} (actual: {herrero_nivel})"
        return True, ""

    def comprar(self, dinero: int, herrero_nivel: int) -> Tuple[bool, int, str]:
        """
        Intenta comprar la instalación.

        Returns:
            (éxito, costo, mensaje)
        """
        puede, msg = self.puede_comprar(herrero_nivel)
        if not puede:
            return False, 0, msg

        if dinero < PRECIO_BASE:
            return False, 0, f"💰 {self.nombre} cuesta {PRECIO_BASE}g (tienes {dinero}g)"

        self.comprada = True
        self.nivel = 1
        return True, PRECIO_BASE, f"✅ {self.nombre} construida! Nivel 1. Ingreso diario: {self.ingreso_diario}g"

    def mejorar(self, dinero: int) -> Tuple[bool, int, str]:
        """
        Intenta mejorar la instalación al siguiente nivel.

        Returns:
            (éxito, costo, mensaje)
        """
        if not self.comprada:
            return False, 0, f"❌ {self.nombre} no está construida"

        if not self.puede_mejorar:
            return False, 0, f"❌ {self.nombre} ya está en nivel máximo (5)"

        costo = self.costo_proxima_mejora
        if dinero < costo:
            return False, 0, f"💰 Mejora cuesta {costo}g (tienes {dinero}g)"

        self.nivel += 1
        msg = (f"🔨 {self.nombre} mejorada a nivel {self.nivel}! "
               f"Ingreso diario: {self.ingreso_diario}g | "
               f"Probabilidades: {self.obtener_probabilidades_resumen()}")
        return True, costo, msg

    def obtener_probabilidades(self, dias: int = 1) -> Dict[str, float]:
        """Probabilidades con clamp duro para los días dados."""
        if not self.comprada:
            return {"comun": 0.0, "especial": 0.0, "mitica": 0.0}
        return calcular_probabilidades(self.nivel, dias)

    def obtener_probabilidades_resumen(self) -> str:
        """String resumido de probabilidades para 1 día."""
        p = self.obtener_probabilidades(1)
        return f"C:{p['comun']}% E:{p['especial']}% M:{p['mitica']}%"

    def generar_drop(self, dias: int = 1) -> Optional[Material]:
        """
        Genera un material aleatorio según probabilidades.
        Returns Material instance o None si no comprada.
        """
        if not self.comprada:
            return None

        probs = self.obtener_probabilidades(dias)
        catalogo = self.catalogo_materiales

        # Elegir rareza
        r = random.random() * 100
        if r < probs["comun"]:
            rareza = "comun"
        elif r < probs["comun"] + probs["especial"]:
            rareza = "especial"
        else:
            rareza = "mitica"

        nombre = random.choice(catalogo[rareza])
        valor_base = CATALOGO_MATERIALES[nombre][1]
        return Material(nombre, rareza, valor_base)

    def generar_drops_multiples(self, dias: int) -> List[Material]:
        """
        Genera múltiples drops según yield de los días.
        1 día → 1, 3 días → 2, 5 días → 3
        """
        if not self.comprada:
            return []

        mult = MULTIPLICADORES_DIAS.get(dias, MULTIPLICADORES_DIAS[1])
        cantidad = mult["yield"]
        return [self.generar_drop(dias) for _ in range(cantidad)]

    def calcular_recompensas_trabajo(self, dias: int) -> Tuple[List[Material], int, int]:
        """
        Calcula recompensas completas del trabajo: materiales + XP + stat.
        Returns: (materiales, xp_ganada, stat_ganada)
        """
        if not self.comprada:
            return [], 0, 0

        mult = MULTIPLICADORES_DIAS.get(dias, MULTIPLICADORES_DIAS[1])
        materiales = self.generar_drops_multiples(dias)
        xp = 50 * dias  # 50, 150, 250
        stat_gain = dias  # 1, 3, 5
        return materiales, xp, stat_gain

    def riesgo_herida(self, dias: int) -> float:
        """Probabilidad de herida según días."""
        return RIESGO_HERIDA.get(dias, 0.05)

    def procesar_riesgo_herida(self, gladiador, dias: int) -> Optional[str]:
        """
        Aplica riesgo de herida si corresponde.
        Returns mensaje si hubo herida, None si no.
        """
        if random.random() < self.riesgo_herida(dias):
            daño = int(gladiador.hp * 0.15)
            gladiador.aplicar_daño(daño)
            return f"💀 ¡{gladiador.nombre} sufrió un accidente! -{daño} HP (ocupado 1 día extra)"
        return None

    # ============================================
    # PERSISTENCIA
    # ============================================

    def serializar(self) -> Dict:
        return {
            "tipo": self.tipo,
            "comprada": self.comprada,
            "nivel": self.nivel,
        }

    def deserializar(self, data: Dict):
        self.comprada = data.get("comprada", False)
        self.nivel = data.get("nivel", 0)

    def __repr__(self):
        estado = f"Nivel {self.nivel}" if self.comprada else "No comprada"
        return f"{self.nombre} ({estado})"


# ============================================
# GESTOR DE INSTALACIONES
# ============================================

class GestorInstalaciones:
    """Gestiona las tres instalaciones del jugador."""

    def __init__(self):
        self.cantera = InstalacionRecursos("cantera")
        self.granja = InstalacionRecursos("granja")
        self.aserradero = InstalacionRecursos("aserradero")

    def obtener_todas(self) -> List[InstalacionRecursos]:
        return [self.cantera, self.granja, self.aserradero]

    def obtener_por_tipo(self, tipo: str) -> Optional[InstalacionRecursos]:
        return getattr(self, tipo, None)

    def obtener_compradas(self) -> List[InstalacionRecursos]:
        return [i for i in self.obtener_todas() if i.comprada]

    def ingreso_total_diario(self) -> int:
        return sum(i.ingreso_diario for i in self.obtener_todas())

    def puede_comprar(self, tipo: str, herrero_nivel: int) -> Tuple[bool, str]:
        inst = self.obtener_por_tipo(tipo)
        if inst:
            return inst.puede_comprar(herrero_nivel)
        return False, "❌ Tipo inválido"

    def comprar(self, tipo: str, dinero: int, herrero_nivel: int) -> Tuple[bool, int, str]:
        inst = self.obtener_por_tipo(tipo)
        if inst:
            return inst.comprar(dinero, herrero_nivel)
        return False, 0, "❌ Tipo inválido"

    def mejorar(self, tipo: str, dinero: int) -> Tuple[bool, int, str]:
        inst = self.obtener_por_tipo(tipo)
        if inst:
            return inst.mejorar(dinero)
        return False, 0, "❌ Tipo inválido"

    def ingreso_total(self) -> int:
        return self.ingreso_total_diario()

    def obtener_trabajo_disponible(self) -> List[Dict]:
        """Lista de instalaciones donde se puede trabajar."""
        trabajos = []
        for inst in self.obtener_compradas():
            trabajos.append({
                "tipo": inst.tipo,
                "nombre": inst.nombre,
                "stat": inst.nombre_stat,
            })
        return trabajos

    # ============================================
    # PERSISTENCIA
    # ============================================

    def serializar(self) -> Dict:
        return {
            "cantera": self.cantera.serializar(),
            "granja": self.granja.serializar(),
            "aserradero": self.aserradero.serializar(),
        }

    def deserializar(self, data: Dict):
        if not data:
            return
        self.cantera.deserializar(data.get("cantera", {}))
        self.granja.deserializar(data.get("granja", {}))
        self.aserradero.deserializar(data.get("aserradero", {}))

    def __repr__(self):
        compradas = len(self.obtener_compradas())
        return f"GestorInstalaciones({compradas}/3 compradas)"


# ============================================
# FUNCIONES DE NIVEL MÓDULO (patrón proyecto)
# ============================================

def guardar_instalaciones(gestor: GestorInstalaciones, usuario: str) -> bool:
    """Guarda instalaciones en el save del usuario (fusiona con datos existentes)."""
    import json
    import os

    archivo = os.path.join("data/saves", f"save_{usuario}.json")
    try:
        datos = {}
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)

        datos["instalaciones"] = gestor.serializar()

        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error guardando instalaciones: {e}")
        return False


def cargar_instalaciones(datos: Dict) -> 'GestorInstalaciones':
    """Carga instalaciones desde datos de save."""
    gestor = GestorInstalaciones()
    if datos and "instalaciones" in datos:
        gestor.deserializar(datos["instalaciones"])
    return gestor