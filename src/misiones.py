"""
Sistema de Misiones - Sangre por Fortuna
==========================================
Misiones con 4 capas: CORE, CHAINS, SIDE QUESTS, AUTO QUESTS
Extensible para agregar más misiones en futuras expansiones
"""

from enum import Enum
from typing import List, Dict, Optional
import json


class TipoMision(Enum):
    """Tipos de misiones disponibles."""
    COMBATE = "combate"
    NIVEL = "nivel"
    DINERO = "dinero"
    ITEMS = "items"
    ESPECIAL = "especial"


class CapaMision(Enum):
    """Capas del sistema de misiones."""
    CORE = "core"                    # Misiones básicas
    ENCADENADA = "encadenada"        # Desbloqueadas por otras
    SECUNDARIA = "secundaria"        # Side quests únicas
    AUTOMATICA = "automatica"        # Se activan por eventos


class DificultadMision(Enum):
    """Niveles de dificultad."""
    TIER_1 = "tier_1"                # Fácil
    TIER_2 = "tier_2"                # Intermedio
    TIER_3 = "tier_3"                # Difícil


class EstadoMision(Enum):
    """Estados posibles de una misión."""
    BLOQUEADA = "bloqueada"          # No disponible (requisitos no cumplidos)
    ACTIVA = "activa"                # En progreso
    COMPLETADA = "completada"        # Finalizada, pendiente de reclamar
    RECLAMADA = "reclamada"          # Recompensa ya recibida


# ============================================
# CLASE MISION
# ============================================

class Mision:
    """Representa una misión individual."""
    
    def __init__(
        self,
        id_mision: str,
        nombre: str,
        descripcion: str,
        tipo: TipoMision,
        capa: CapaMision,
        dificultad: DificultadMision,
        objetivo: int,
        recompensas: Dict
    ):
        """
        Args:
            id_mision: Identificador único (ej: "combate_1", "cadena_gloria_1")
            nombre: Nombre visible
            descripcion: Texto narrativo
            tipo: Tipo de misión (combate, nivel, dinero, items, especial)
            capa: En qué capa está (core, encadenada, secundaria, automatica)
            dificultad: Tier de dificultad
            objetivo: Número a alcanzar
            recompensas: Dict con {dinero, xp, items, buffs}
        """
        self.id = id_mision
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo = tipo
        self.capa = capa
        self.dificultad = dificultad
        self.objetivo = objetivo
        self.progreso = 0
        self.recompensas = recompensas
        
        # Estado y control
        self.estado = EstadoMision.BLOQUEADA
        self.mision_padre_id = None               # ID de mision que desbloquea esta
        self.misiones_hijo_ids = []               # IDs de misiones desbloqueadas al completar
        self.se_activa_sola = False               # Si es automatica
        self.fecha_disponible_desde = None        # Para temporal quests
        self.fecha_disponible_hasta = None        # Para temporal quests
        
        # Bonus especiales
        self.tiene_bonus = False
        self.descripcion_bonus = None
        self.bonus_extra_recompensa = 0           # Dinero/XP extra si se completa con bonus
    
    def esta_completada(self) -> bool:
        """¿Misión completada?"""
        return self.progreso >= self.objetivo
    
    def porcentaje_progreso(self) -> float:
        """Retorna progreso como porcentaje."""
        if self.objetivo == 0:
            return 0.0
        return min(100.0, (self.progreso / self.objetivo) * 100)
    
    def incrementar_progreso(self, cantidad: int = 1) -> bool:
        """
        Aumenta progreso. Retorna True si se completó la misión.
        """
        self.progreso = min(self.progreso + cantidad, self.objetivo)
        
        if self.esta_completada() and self.estado == EstadoMision.ACTIVA:
            self.estado = EstadoMision.COMPLETADA
            return True
        
        return False
    
    def reclamar_recompensas(self) -> Dict:
        """
        Retorna recompensas y marca como reclamada.
        Retorna None si no está completada.
        """
        if self.estado != EstadoMision.COMPLETADA:
            return None
        
        self.estado = EstadoMision.RECLAMADA
        return self.recompensas
    
    def generar_string_progreso(self) -> str:
        """Retorna barra visual de progreso."""
        barra_llena = int((self.progreso / self.objetivo) * 20)
        barra = "█" * barra_llena + "░" * (20 - barra_llena)
        return f"{barra} ({self.progreso}/{self.objetivo})"
    
    def generar_string_completo(self) -> str:
        """Retorna representación completa formateada."""
        icon_estado = {
            EstadoMision.BLOQUEADA: "🔒",
            EstadoMision.ACTIVA: "⭐",
            EstadoMision.COMPLETADA: "✓",
            EstadoMision.RECLAMADA: "✓✓"
        }.get(self.estado, "?")
        
        icon_dificultad = {
            DificultadMision.TIER_1: "⭐",
            DificultadMision.TIER_2: "⭐⭐",
            DificultadMision.TIER_3: "⭐⭐⭐"
        }.get(self.dificultad, "")
        
        texto = f"\n{icon_estado} {self.nombre} {icon_dificultad}\n"
        texto += f"   {self.descripcion}\n"
        texto += f"   Progreso: {self.generar_string_progreso()}\n"
        texto += f"   Recompensas: {self.recompensas['dinero']}g + {self.recompensas['xp']} XP"
        
        if self.tiene_bonus:
            texto += f"\n   ✨ BONUS: {self.descripcion_bonus} (+{self.bonus_extra_recompensa}g)"
        
        return texto
    
    def __repr__(self):
        return f"Mision({self.id}, {self.estado.value}, {self.progreso}/{self.objetivo})"


# ============================================
# GESTOR DE MISIONES
# ============================================

class GestorMisiones:
    """Gestiona todas las misiones del juego."""
    
    def __init__(self):
        self.misiones: Dict[str, Mision] = {}
        self.misiones_activas: List[str] = []
        self.misiones_completadas: List[str] = []
        
        # Inicializar misiones del juego
        self._crear_misiones_core()
        self._crear_misiones_encadenadas()
        self._crear_misiones_secundarias()
        self._crear_misiones_automaticas()
    
    def _crear_misiones_core(self):
        """CAPA 1: Misiones básicas de progresión."""
        
        # COMBATE
        m1 = Mision(
            "combate_1", "Primer Paso", 
            "Gana tu primer combate en la arena",
            TipoMision.COMBATE, CapaMision.CORE, DificultadMision.TIER_1,
            objetivo=1,
            recompensas={"dinero": 100, "xp": 50, "items": []}
        )
        m1.estado = EstadoMision.ACTIVA
        m1.se_activa_sola = True
        
        m2 = Mision(
            "combate_2", "Sparring",
            "Gana 3 combates consecutivos",
            TipoMision.COMBATE, CapaMision.CORE, DificultadMision.TIER_1,
            objetivo=3,
            recompensas={"dinero": 250, "xp": 150, "items": []}
        )
        m2.tiene_bonus = True
        m2.descripcion_bonus = "Gana 5 combates sin perder"
        m2.bonus_extra_recompensa = 100
        
        m3 = Mision(
            "combate_3", "Champion Local",
            "Gana 10 combates",
            TipoMision.COMBATE, CapaMision.CORE, DificultadMision.TIER_1,
            objetivo=10,
            recompensas={"dinero": 500, "xp": 300, "items": []}
        )
        
        # NIVEL
        m4 = Mision(
            "nivel_1", "Aprendiz",
            "Alcanza nivel 3",
            TipoMision.NIVEL, CapaMision.CORE, DificultadMision.TIER_1,
            objetivo=3,
            recompensas={"dinero": 150, "xp": 100, "items": []}
        )
        m4.se_activa_sola = True
        
        m5 = Mision(
            "nivel_2", "Veterano",
            "Alcanza nivel 5",
            TipoMision.NIVEL, CapaMision.CORE, DificultadMision.TIER_1,
            objetivo=5,
            recompensas={"dinero": 300, "xp": 200, "items": []}
        )
        
        # DINERO
        m6 = Mision(
            "dinero_1", "Primeras Ganancias",
            "Acumula 500g",
            TipoMision.DINERO, CapaMision.CORE, DificultadMision.TIER_1,
            objetivo=500,
            recompensas={"dinero": 200, "xp": 100, "items": []}
        )
        m6.se_activa_sola = True
        
        m7 = Mision(
            "dinero_2", "Hombre Acaudalado",
            "Acumula 1000g",
            TipoMision.DINERO, CapaMision.CORE, DificultadMision.TIER_1,
            objetivo=1000,
            recompensas={"dinero": 500, "xp": 250, "items": []}
        )
        
        # ITEMS
        m8 = Mision(
            "items_1", "Equipero",
            "Compra 5 items",
            TipoMision.ITEMS, CapaMision.CORE, DificultadMision.TIER_1,
            objetivo=5,
            recompensas={"dinero": 200, "xp": 150, "items": []}
        )
        
        m9 = Mision(
            "items_2", "Coleccionista",
            "Compra 10 items diferentes",
            TipoMision.ITEMS, CapaMision.CORE, DificultadMision.TIER_1,
            objetivo=10,
            recompensas={"dinero": 400, "xp": 300, "items": []}
        )
        
        # Agregar todas
        for mision in [m1, m2, m3, m4, m5, m6, m7, m8, m9]:
            self.misiones[mision.id] = mision
    
    def _crear_misiones_encadenadas(self):
        """CAPA 2: Misiones que desbloquean otras (chains)."""
        
        # CADENA "LA GLORIA DEL GLADIADOR"
        m1 = Mision(
            "cadena_gloria_1", "La Gloria del Gladiador",
            "Gana 5 combates en la arena legendaria",
            TipoMision.COMBATE, CapaMision.ENCADENADA, DificultadMision.TIER_2,
            objetivo=5,
            recompensas={"dinero": 750, "xp": 500, "items": []}
        )
        m1.estado = EstadoMision.BLOQUEADA
        m1.misiones_hijo_ids.append("cadena_gloria_2")
        
        m2 = Mision(
            "cadena_gloria_2", "Campeón Indiscutible",
            "Gana 25 combates totales",
            TipoMision.COMBATE, CapaMision.ENCADENADA, DificultadMision.TIER_2,
            objetivo=25,
            recompensas={"dinero": 1500, "xp": 1000, "items": ["espada_legendaria"]}
        )
        m2.estado = EstadoMision.BLOQUEADA
        m2.mision_padre_id = "cadena_gloria_1"
        
        # CADENA "ASCENSO DE PODER"
        m3 = Mision(
            "cadena_poder_1", "Ascenso Inicial",
            "Alcanza nivel 10",
            TipoMision.NIVEL, CapaMision.ENCADENADA, DificultadMision.TIER_2,
            objetivo=10,
            recompensas={"dinero": 500, "xp": 400, "items": []}
        )
        m3.estado = EstadoMision.BLOQUEADA
        m3.misiones_hijo_ids.append("cadena_poder_2")
        
        m4 = Mision(
            "cadena_poder_2", "Leyenda Menor",
            "Alcanza nivel 20",
            TipoMision.NIVEL, CapaMision.ENCADENADA, DificultadMision.TIER_3,
            objetivo=20,
            recompensas={"dinero": 1000, "xp": 800, "items": ["pocion_especial"]}
        )
        m4.estado = EstadoMision.BLOQUEADA
        m4.mision_padre_id = "cadena_poder_1"
        
        # CADENA "IMPERIO ECONÓMICO"
        m5 = Mision(
            "cadena_dinero_1", "Negociante",
            "Acumula 5000g",
            TipoMision.DINERO, CapaMision.ENCADENADA, DificultadMision.TIER_2,
            objetivo=5000,
            recompensas={"dinero": 1000, "xp": 600, "items": []}
        )
        m5.estado = EstadoMision.BLOQUEADA
        m5.misiones_hijo_ids.append("cadena_dinero_2")
        
        m6 = Mision(
            "cadena_dinero_2", "Magnate Romano",
            "Acumula 15000g",
            TipoMision.DINERO, CapaMision.ENCADENADA, DificultadMision.TIER_3,
            objetivo=15000,
            recompensas={"dinero": 2000, "xp": 1000, "items": ["descuento_tienda"]}
        )
        m6.estado = EstadoMision.BLOQUEADA
        m6.mision_padre_id = "cadena_dinero_1"
        
        # Agregar todas
        for mision in [m1, m2, m3, m4, m5, m6]:
            self.misiones[mision.id] = mision
    
    def _crear_misiones_secundarias(self):
        """CAPA 3: Side quests - Misiones únicas y narrativas."""
        
        m1 = Mision(
            "side_apuesta", "La Apuesta del Ludópata",
            "Gana 3 combates seguidos sin perder ninguno. Riesgo alto, recompensa mayor.",
            TipoMision.ESPECIAL, CapaMision.SECUNDARIA, DificultadMision.TIER_2,
            objetivo=3,
            recompensas={"dinero": 600, "xp": 400, "items": ["pocion_especial"]}
        )
        m1.tiene_bonus = True
        m1.descripcion_bonus = "Gana 5 sin perder"
        m1.bonus_extra_recompensa = 200
        
        m2 = Mision(
            "side_coleccionista", "El Coleccionista",
            "Equipa todos los items de Tier 2",
            TipoMision.ITEMS, CapaMision.SECUNDARIA, DificultadMision.TIER_2,
            objetivo=1,
            recompensas={"dinero": 800, "xp": 500, "items": ["caja_sorpresa"]}
        )
        
        m3 = Mision(
            "side_venganza", "Venganza",
            "Derrota al mismo tipo de enemigo que te ha ganado 3 veces",
            TipoMision.ESPECIAL, CapaMision.SECUNDARIA, DificultadMision.TIER_2,
            objetivo=1,
            recompensas={"dinero": 500, "xp": 350, "items": []}
        )
        
        m4 = Mision(
            "side_ascetismo", "La Vida Austera",
            "Gana 5 combates sin comprar ningún item",
            TipoMision.ESPECIAL, CapaMision.SECUNDARIA, DificultadMision.TIER_1,
            objetivo=5,
            recompensas={"dinero": 400, "xp": 300, "items": []}
        )
        
        # Agregar todas
        for mision in [m1, m2, m3, m4]:
            self.misiones[mision.id] = mision
    
    def _crear_misiones_automaticas(self):
        """CAPA 4: Auto quests - Se activan automáticamente por eventos."""
        
        m1 = Mision(
            "auto_primer_victima", "¡Primer Golpe!",
            "Gana tu primer combate (se activa automáticamente)",
            TipoMision.COMBATE, CapaMision.AUTOMATICA, DificultadMision.TIER_1,
            objetivo=1,
            recompensas={"dinero": 50, "xp": 25, "items": []}
        )
        m1.se_activa_sola = True
        
        m2 = Mision(
            "auto_racha_10", "Racha Ganadora (x10)",
            "Gana 10 combates seguidos (se activa después de 5 victorias)",
            TipoMision.COMBATE, CapaMision.AUTOMATICA, DificultadMision.TIER_2,
            objetivo=10,
            recompensas={"dinero": 1000, "xp": 600, "items": ["medal_oro"]}
        )
        
        m3 = Mision(
            "auto_comeback", "¡Comeback!",
            "Gana después de 3 derrotas seguidas (se activa automáticamente)",
            TipoMision.ESPECIAL, CapaMision.AUTOMATICA, DificultadMision.TIER_2,
            objetivo=1,
            recompensas={"dinero": 300, "xp": 200, "items": []}
        )
        
        m4 = Mision(
            "auto_nivel_up", "¡Evolución!",
            "Sube de nivel (se activa cada vez que subes)",
            TipoMision.NIVEL, CapaMision.AUTOMATICA, DificultadMision.TIER_1,
            objetivo=999,  # Se dispara múltiples veces
            recompensas={"dinero": 100, "xp": 50, "items": []}
        )
        m4.se_activa_sola = True
        
        # Agregar todas
        for mision in [m1, m2, m3, m4]:
            self.misiones[mision.id] = mision
    
    def obtener_mision(self, id_mision: str) -> Optional[Mision]:
        """Obtiene una misión por ID."""
        return self.misiones.get(id_mision)
    
    def obtener_misiones_activas(self) -> List[Mision]:
        """Retorna todas las misiones activas."""
        return [m for m in self.misiones.values() if m.estado == EstadoMision.ACTIVA]
    
    def obtener_misiones_completadas(self) -> List[Mision]:
        """Retorna todas las misiones completadas."""
        return [m for m in self.misiones.values() if m.estado == EstadoMision.COMPLETADA]
    
    def obtener_misiones_por_capa(self, capa: CapaMision) -> List[Mision]:
        """Retorna todas las misiones de una capa."""
        return [m for m in self.misiones.values() if m.capa == capa]
    
    def obtener_misiones_por_tipo(self, tipo: TipoMision) -> List[Mision]:
        """Retorna todas las misiones de un tipo."""
        return [m for m in self.misiones.values() if m.tipo == tipo]
    
    def activar_mision(self, id_mision: str) -> bool:
        """Activa una misión si cumple requisitos."""
        mision = self.obtener_mision(id_mision)
        if not mision:
            return False
        
        # Si tiene padre, verificar que esté completada
        if mision.mision_padre_id:
            padre = self.obtener_mision(mision.mision_padre_id)
            if not padre or padre.estado != EstadoMision.COMPLETADA:
                return False
        
        if mision.estado == EstadoMision.BLOQUEADA:
            mision.estado = EstadoMision.ACTIVA
            self.misiones_activas.append(id_mision)
            return True
        
        return False
    
    def incrementar_progreso_mision(self, id_mision: str, cantidad: int = 1) -> bool:
        """
        Incrementa progreso de una misión.
        Retorna True si se completó.
        """
        mision = self.obtener_mision(id_mision)
        if not mision or mision.estado != EstadoMision.ACTIVA:
            return False
        
        completada = mision.incrementar_progreso(cantidad)
        
        if completada:
            # Desbloquear misiones hijo si existen
            for hijo_id in mision.misiones_hijo_ids:
                self.activar_mision(hijo_id)
        
        return completada
    
    def reclamar_recompensas_mision(self, id_mision: str) -> Optional[Dict]:
        """Reclama recompensas de una misión completada."""
        mision = self.obtener_mision(id_mision)
        if not mision:
            return None
        
        recompensas = mision.reclamar_recompensas()
        if recompensas:
            self.misiones_completadas.append(id_mision)
        
        return recompensas
    
    def mostrar_todas_misiones(self):
        """Muestra resumen de todas las misiones."""
        print("\n" + "="*70)
        print("📋 CATÁLOGO COMPLETO DE MISIONES")
        print("="*70)
        
        for capa in CapaMision:
            misiones = self.obtener_misiones_por_capa(capa)
            if misiones:
                print(f"\n🔹 {capa.value.upper()}: ({len(misiones)} misiones)")
                for m in misiones:
                    print(m.generar_string_completo())
    
    def __repr__(self):
        activas = len(self.obtener_misiones_activas())
        completadas = len(self.obtener_misiones_completadas())
        return f"GestorMisiones({len(self.misiones)} total, {activas} activas, {completadas} completadas)"
    
    # ============================================
    # AUTO-TRACKING: Eventos que actualizan misiones
    # ============================================
    
    def evento_combate_ganado(self) -> List[str]:
        """
        Llamado cuando el gladiador GANA un combate.
        Retorna lista de IDs de misiones completadas en este evento.
        """
        misiones_completadas = []
        
        # Incrementar todas las misiones de combate activas
        misiones_combate = [m for m in self.misiones.values() 
                           if m.tipo == TipoMision.COMBATE and 
                           m.estado == EstadoMision.ACTIVA]
        
        for m in misiones_combate:
            completada = self.incrementar_progreso_mision(m.id)
            if completada:
                misiones_completadas.append(m.id)
        
        return misiones_completadas
    
    def evento_gladiador_sube_nivel(self) -> List[str]:
        """
        Llamado cuando un gladiador SUBE DE NIVEL.
        Retorna lista de IDs de misiones completadas en este evento.
        """
        misiones_completadas = []
        
        # Incrementar todas las misiones de nivel activas
        misiones_nivel = [m for m in self.misiones.values() 
                         if m.tipo == TipoMision.NIVEL and 
                         m.estado == EstadoMision.ACTIVA]
        
        for m in misiones_nivel:
            completada = self.incrementar_progreso_mision(m.id)
            if completada:
                misiones_completadas.append(m.id)
        
        return misiones_completadas
    
    def evento_dinero_acumulado(self, cantidad: int) -> List[str]:
        """
        Llamado cuando se ACUMULA DINERO.
        Retorna lista de IDs de misiones completadas en este evento.
        """
        misiones_completadas = []
        
        # Incrementar misiones de dinero por cantidad acumulada
        misiones_dinero = [m for m in self.misiones.values() 
                          if m.tipo == TipoMision.DINERO and 
                          m.estado == EstadoMision.ACTIVA]
        
        for m in misiones_dinero:
            completada = self.incrementar_progreso_mision(m.id, cantidad)
            if completada:
                misiones_completadas.append(m.id)
        
        return misiones_completadas
    
    def evento_items_comprados(self, cantidad: int = 1) -> List[str]:
        """
        Llamado cuando se COMPRAN ITEMS.
        Retorna lista de IDs de misiones completadas en este evento.
        """
        misiones_completadas = []
        
        # Incrementar misiones de items
        misiones_items = [m for m in self.misiones.values() 
                         if m.tipo == TipoMision.ITEMS and 
                         m.estado == EstadoMision.ACTIVA]
        
        for m in misiones_items:
            completada = self.incrementar_progreso_mision(m.id, cantidad)
            if completada:
                misiones_completadas.append(m.id)
        
        return misiones_completadas
    
    def generar_notificacion_misiones(self, misiones_ids: List[str]) -> str:
        """
        Genera notificación visual para misiones completadas.
        Retorna string formateado para mostrar al usuario.
        """
        if not misiones_ids:
            return ""
        
        notificacion = "\n" + "="*70 + "\n"
        notificacion += "        ✨ ¡MISIONES COMPLETADAS! ✨\n"
        notificacion += "="*70 + "\n"
        
        dinero_total = 0
        xp_total = 0
        
        for id_mision in misiones_ids:
            m = self.obtener_mision(id_mision)
            if m:
                dinero_total += m.recompensas['dinero']
                xp_total += m.recompensas['xp']
                
                notificacion += f"\n✓ {m.nombre}\n"
                notificacion += f"  💰 {m.recompensas['dinero']}g | 📈 {m.recompensas['xp']} XP\n"
                
                if m.tiene_bonus:
                    notificacion += f"  ✨ BONUS: {m.descripcion_bonus} (+{m.bonus_extra_recompensa}g)\n"
                    dinero_total += m.bonus_extra_recompensa
        
        notificacion += "\n" + "-"*70 + "\n"
        notificacion += f"📊 TOTAL: {dinero_total}g + {xp_total} XP\n"
        notificacion += "="*70 + "\n"
        notificacion += "💡 Puedes reclamar recompensas en el menú de Misiones\n"
        
        return notificacion
    
    # ============================================
    # PERSISTENCIA: Guardar y cargar misiones
    # ============================================
    
    def guardar_estado(self, archivo: str = "datos/misiones.json") -> bool:
        """
        Guarda el estado de todas las misiones a un archivo JSON.
        Retorna True si se guardó correctamente.
        """
        import os
        
        try:
            # Crear carpeta si no existe
            os.makedirs(os.path.dirname(archivo), exist_ok=True)
            
            # Serializar misiones
            datos = {
                "misiones": {},
                "activas": self.misiones_activas,
                "completadas": self.misiones_completadas,
                "timestamp": str(__import__('datetime').datetime.now())
            }
            
            for id_mision, mision in self.misiones.items():
                datos["misiones"][id_mision] = {
                    "id": mision.id,
                    "nombre": mision.nombre,
                    "progreso": mision.progreso,
                    "objetivo": mision.objetivo,
                    "estado": mision.estado.value,
                    "tipo": mision.tipo.value,
                    "capa": mision.capa.value,
                    "dificultad": mision.dificultad.value,
                    "recompensas": mision.recompensas,
                    "mision_padre_id": mision.mision_padre_id,
                    "misiones_hijo_ids": mision.misiones_hijo_ids,
                    "tiene_bonus": mision.tiene_bonus,
                    "descripcion_bonus": mision.descripcion_bonus,
                    "bonus_extra_recompensa": mision.bonus_extra_recompensa
                }
            
            # Guardar a JSON
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            
            return True
        
        except Exception as e:
            print(f"❌ Error al guardar misiones: {e}")
            return False
    
    def cargar_estado(self, archivo: str = "datos/misiones.json") -> bool:
        """
        Carga el estado de misiones desde un archivo JSON.
        Retorna True si se cargó correctamente.
        """
        import os
        
        try:
            if not os.path.exists(archivo):
                return False
            
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Restaurar estado de misiones
            for id_mision, datos_mision in datos["misiones"].items():
                if id_mision in self.misiones:
                    m = self.misiones[id_mision]
                    m.progreso = datos_mision["progreso"]
                    m.estado = EstadoMision(datos_mision["estado"])
                    m.tiene_bonus = datos_mision["tiene_bonus"]
                    m.descripcion_bonus = datos_mision["descripcion_bonus"]
                    m.bonus_extra_recompensa = datos_mision["bonus_extra_recompensa"]
            
            # Restaurar listas
            self.misiones_activas = datos["activas"]
            self.misiones_completadas = datos["completadas"]
            
            return True
        
        except Exception as e:
            print(f"❌ Error al cargar misiones: {e}")
            return False
    
    def resetear_misiones(self):
        """Reinicia todas las misiones a su estado original."""
        for mision in self.misiones.values():
            if mision.capa.value == "automatica" or mision.capa.value == "core":
                mision.progreso = 0
                if mision.se_activa_sola and mision.capa.value == "core":
                    mision.estado = EstadoMision.ACTIVA
                else:
                    mision.estado = EstadoMision.BLOQUEADA
            else:
                mision.progreso = 0
                mision.estado = EstadoMision.BLOQUEADA
        
        self.misiones_activas = []
        self.misiones_completadas = []
        
        # Reactivar misiones CORE que se activan solas
        for mision in self.misiones.values():
            if mision.se_activa_sola and mision.capa.value == "core":
                mision.estado = EstadoMision.ACTIVA
                self.misiones_activas.append(mision.id)
