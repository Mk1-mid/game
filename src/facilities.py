"""
SISTEMA DE MEJORAS DE FACILIDADES
Médico y Herrero con sistema de niveles progresivos
"""

class Medico:
    """Facilidad Médico - Sistema de curación progresiva con tipos escalados"""
    
    def __init__(self, nivel=1):
        self.nivel = nivel
        self.nivel_maximo = 5
        
        # Costos de mejora (para pasar al siguiente nivel)
        self.costos_mejora = {
            1: 500,    # Nivel 1 -> 2 (cuesta 500g)
            2: 1000,   # Nivel 2 -> 3
            3: 2000,   # Nivel 3 -> 4
            4: 3500,   # Nivel 4 -> 5
        }
        
        # CURACIÓN PORCENTUAL PROGRESIVA
        # Básica: restaura % HP, ocupación 2-1 día, costo 35g estable
        self.curacion_basica = {
            1: (0.35, 2, 35),   # (%, días, costo)
            2: (0.36, 2, 35),
            3: (0.37, 2, 35),
            4: (0.38, 1, 35),
            5: (0.40, 1, 35),
        }
        
        # Profunda: restaura % HP, ocupación 3-2 días, costo variable
        self.curacion_profunda = {
            1: (0.65, 3, 150),  # (%, días, costo base)
            2: (0.66, 3, 150),
            3: (0.67, 2, 150),
            4: (0.68, 2, 150),
            5: (0.70, 2, 150),
        }
        
        # Completa: 100% HP, ocupación 4-3 días, costo variable
        self.curacion_completa = {
            1: (1.00, 4, 300),  # (%, días, costo base)
            2: (1.00, 4, 300),
            3: (1.00, 3, 300),
            4: (1.00, 3, 300),
            5: (1.00, 3, 300),
        }
        
        # CURACIÓN RÁPIDA (Inmediata, 0 días)
        # Desbloquea en nivel 2, escala por nivel
        self.curacion_rapida = {
            1: None,             # Bloqueada
            2: (0.40, 150),      # (%, costo)
            3: (0.50, 140),
            4: (0.60, 130),
            5: (0.70, 120),
        }
        
        # Porcentaje de revivir según nivel
        self.revive_hp = {
            1: 0.25,   # Revive a 25% HP
            2: 0.35,   # Revive a 35% HP
            3: 0.50,   # Revive a 50% HP
            4: 0.65,   # Revive a 65% HP
            5: 0.80,   # Revive a 80% HP
        }
        
        # Costo de revivir según nivel
        self.costo_revive = {
            1: 200,
            2: 200,
            3: 250,
            4: 300,
            5: 350,
        }
        
        # Curación Rápida disponible desde nivel 2
        self.curacion_rapida_desbloqueada = nivel >= 2
        self.curacion_rapida_usado = False  # 1 uso por día
        
        # Estadísticas del médico
        self.gladiadores_curados = 0
        self.hp_total_restaurado = 0
        self.revividas = 0
        self.curacion_rapida_usos = 0
    
    def puede_mejorar(self):
        """Verifica si se puede mejorar al siguiente nivel"""
        return self.nivel < self.nivel_maximo
    
    def costo_proximo_nivel(self):
        """Retorna el costo para el próximo nivel"""
        if self.nivel < self.nivel_maximo:
            return self.costos_mejora[self.nivel]
        return 0
    
    def mejorar(self, dinero):
        """Intenta mejorar el Médico"""
        if not self.puede_mejorar():
            return False, "🏥 El Médico ya alcanzó nivel máximo (5)"
        
        costo = self.costo_proximo_nivel()
        if dinero < costo:
            return False, f"💰 No tienes suficiente dinero. Necesitas {costo}g (tienes {dinero}g)"
        
        self.nivel += 1
        if self.nivel >= 2:
            self.curacion_rapida_desbloqueada = True
        
        return True, f"✅ Médico mejorado a nivel {self.nivel}!"
    
    def _calcular_costo_dinamico(self, costo_base, hp_actual, hp_max):
        """
        Calcula costo dinámico basado en estado crítico
        En crítico (< 30%): +50% costo
        """
        porcentaje_hp = (hp_actual / hp_max) * 100
        if porcentaje_hp < 30:
            return int(costo_base * 1.5)  # +50% por urgencia
        return costo_base
    
    def curar_basica(self, gladiador, dinero):
        """
        Curación Básica (35-40% HP)
        Ocupación: 2 días (Lvl 1-3) → 1 día (Lvl 4-5)
        Costo: 35g (ESTABLE, sin variación)
        """
        porcentaje, dias_ocupado, costo = self.curacion_basica[self.nivel]
        
        if dinero < costo:
            return False, 0, 0, f"💰 Curación Básica cuesta {costo}g"
        
        # Cura
        hp_antes = gladiador.hp_actual
        cantidad_restaurar = int(gladiador.hp * porcentaje)
        gladiador.hp_actual = min(gladiador.hp_actual + cantidad_restaurar, gladiador.hp)
        hp_restaurado = gladiador.hp_actual - hp_antes
        
        # Estadísticas
        self.gladiadores_curados += 1
        self.hp_total_restaurado += hp_restaurado
        
        return True, costo, dias_ocupado, f"❤️  Curación Básica: {hp_antes} → {gladiador.hp_actual} HP ({porcentaje*100:.0f}%) | {dias_ocupado} día(s) | {costo}g"
    
    def curar_profunda(self, gladiador, dinero):
        """
        Curación Profunda (65-70% HP)
        Ocupación: 3 días (Lvl 1-3) → 2 días (Lvl 4-5)
        Costo: 150g base, +50% si está en crítico
        """
        porcentaje, dias_ocupado, costo_base = self.curacion_profunda[self.nivel]
        costo = self._calcular_costo_dinamico(costo_base, gladiador.hp_actual, gladiador.hp)
        
        if dinero < costo:
            return False, 0, 0, f"💰 Curación Profunda cuesta {costo}g"
        
        # Cura
        hp_antes = gladiador.hp_actual
        cantidad_restaurar = int(gladiador.hp * porcentaje)
        gladiador.hp_actual = min(gladiador.hp_actual + cantidad_restaurar, gladiador.hp)
        hp_restaurado = gladiador.hp_actual - hp_antes
        
        # Estadísticas
        self.gladiadores_curados += 1
        self.hp_total_restaurado += hp_restaurado
        
        costo_info = f"{costo_base}g" if costo == costo_base else f"{costo_base}g → {costo}g (+50% urgencia)"
        return True, costo, dias_ocupado, f"💪 Curación Profunda: {hp_antes} → {gladiador.hp_actual} HP ({porcentaje*100:.0f}%) | {dias_ocupado} días | {costo_info}"
    
    def curar_completa(self, gladiador, dinero):
        """
        Curación Completa (100% HP)
        Ocupación: 4 días (Lvl 1-3) → 3 días (Lvl 4-5)
        Costo: 300g base, +50% si está en crítico
        """
        porcentaje, dias_ocupado, costo_base = self.curacion_completa[self.nivel]
        costo = self._calcular_costo_dinamico(costo_base, gladiador.hp_actual, gladiador.hp)
        
        if dinero < costo:
            return False, 0, 0, f"💰 Curación Completa cuesta {costo}g"
        
        # Cura
        hp_antes = gladiador.hp_actual
        gladiador.hp_actual = gladiador.hp
        hp_restaurado = gladiador.hp_actual - hp_antes
        
        # Estadísticas
        self.gladiadores_curados += 1
        self.hp_total_restaurado += hp_restaurado
        
        costo_info = f"{costo_base}g" if costo == costo_base else f"{costo_base}g → {costo}g (+50% urgencia)"
        return True, costo, dias_ocupado, f"✨ Curación Completa: {hp_antes} → {gladiador.hp_actual} HP (100%) | {dias_ocupado} días | {costo_info}"
    
    def curar_rapida(self, gladiador, dinero):
        """
        Curación Rápida (40-70% HP)
        Desbloquea en nivel 2
        Ocupación: 0 días (INMEDIATA)
        Costo: 150g (Lvl 2) → 120g (Lvl 5)
        1 uso por día
        """
        if not self.curacion_rapida_desbloqueada:
            return False, 0, 0, "🔒 Curación Rápida bloqueada. Mejora el Médico a nivel 2+"
        
        if self.curacion_rapida_usado:
            return False, 0, 0, "⏰ Ya usaste Curación Rápida hoy. Mañana disponible de nuevo."
        
        porcentaje_hp_data = self.curacion_rapida[self.nivel]
        if porcentaje_hp_data is None:
            return False, 0, 0, "🔒 Curación Rápida no disponible en este nivel"
        
        porcentaje, costo_base = porcentaje_hp_data
        costo = self._calcular_costo_dinamico(costo_base, gladiador.hp_actual, gladiador.hp)
        
        if dinero < costo:
            return False, 0, 0, f"💰 Curación Rápida cuesta {costo}g"
        
        # Cura instantánea
        hp_antes = gladiador.hp_actual
        cantidad_restaurar = int(gladiador.hp * porcentaje)
        gladiador.hp_actual = min(gladiador.hp_actual + cantidad_restaurar, gladiador.hp)
        hp_restaurado = gladiador.hp_actual - hp_antes
        
        # Estadísticas
        self.gladiadores_curados += 1
        self.hp_total_restaurado += hp_restaurado
        self.curacion_rapida_usos += 1
        self.curacion_rapida_usado = True
        
        costo_info = f"{costo_base}g" if costo == costo_base else f"{costo_base}g → {costo}g (+100% urgencia)"
        return True, costo, 0, f"⚡ ¡CURACIÓN RÁPIDA! {hp_antes} → {gladiador.hp_actual} HP ({porcentaje*100:.0f}%) | INMEDIATA | {costo_info}"
    
    def revivir(self, gladiador, dinero):
        """Revive un gladiador caído"""
        if gladiador.hp_actual > 0:
            return False, 0, "El gladiador aún está vivo"
        
        costo = self.costo_revive[self.nivel]
        if dinero < costo:
            return False, 0, f"💰 Revivir cuesta {costo}g"
        
        # Revive con porcentaje según nivel
        hp_revive = int(gladiador.hp_maximo * self.revive_hp[self.nivel])
        gladiador.hp_actual = hp_revive
        
        # Estadísticas
        self.revividas += 1
        
        return True, costo, f"✅ {gladiador.nombre} revivido a {hp_revive} HP (gastó {costo}g)"
    
    def resetear_curacion_rapida(self):
        """Resetea Curación Rápida para nuevo día"""
        self.curacion_rapida_usado = False
    
    def generar_string(self):
        """Retorna string de estado del Médico"""
        linea = f"🏥 Médico Nivel {self.nivel}/5"
        if self.puede_mejorar():
            linea += f" | Mejora: {self.costo_proximo_nivel()}g"
        if self.curacion_rapida_desbloqueada:
            linea += " | ⚡ Curación Rápida: DISPONIBLE"
        return linea
    
    def generar_resumen_estadisticas(self):
        """Genera resumen visual de estadísticas del Médico"""
        resumen = f"""
🏥 ESTADÍSTICAS DEL MÉDICO
├─ Nivel: {self.nivel}/5
├─ Gladiadores curados: {self.gladiadores_curados}
├─ HP total restaurado: {self.hp_total_restaurado}
├─ Revividas: {self.revividas}
└─ Curación Rápida usada hoy: {'✅ Sí' if self.curacion_rapida_usado else '❌ No'}
"""
        return resumen


class Herrero:
    """Facilidad Herrero - Sistema de mejora de armas con % ATK, costos cuadráticos y durabilidad"""
    
    def __init__(self, nivel=1):
        self.nivel = nivel
        self.nivel_maximo = 5
        
        # Costos de mejora del Herrero para pasar nivel
        self.costos_mejora = {
            1: 600,    # Nivel 1 -> 2
            2: 1200,   # Nivel 2 -> 3
            3: 2500,   # Nivel 3 -> 4
            4: 4000,   # Nivel 4 -> 5
        }
        
        # Tier de armas desbloqueado por nivel (para compra en tienda)
        self.tier_desbloqueado = {
            1: 1,      # Nivel 1: solo Tier 1
            2: 2,      # Nivel 2: Tier 1-2
            3: 3,      # Nivel 3: Tier 1-3
            4: 4,      # Nivel 4: Tier 1-4 (Legendario)
            5: 4,      # Nivel 5: Todo
        }
        
        # PORCENTAJE DE MEJORA por Tier
        # Cada mejora suma este % al ATK actual del arma
        self.porcentaje_atk = {
            1: 0.08,   # Tier 1: +8% ATK
            2: 0.12,   # Tier 2: +12% ATK
            3: 0.15,   # Tier 3: +15% ATK
            4: 0.20,   # Tier 4: +20% ATK
        }
        
        # COSTO BASE por Tier (para calcular costo de mejora)
        self.costo_base_mejora = {
            1: 100,    # Tier 1
            2: 200,    # Tier 2
            3: 400,    # Tier 3
            4: 800,    # Tier 4 (Legendario)
        }
        
        # MULTIPLICADOR por tipo de arma (tamaño/peso)
        self.multiplicador_tipo = {
            "corta": 0.8,     # Daga, Espada Corta: -20% costo
            "media": 1.0,     # Espada, Tridente, Martillo: normal
            "grande": 1.3,    # Lanza, Hacha, Lanza del Destino: +30% costo
        }
        
        # Estadísticas del Herrero
        self.armas_mejoradas = 0
        self.ataque_total_otorgado = 0
        self.armas_reparadas = 0
        self.durabilidad_restaurada = 0
    
    def puede_mejorar(self):
        """Verifica si se puede mejorar al siguiente nivel"""
        return self.nivel < self.nivel_maximo
    
    def costo_proximo_nivel(self):
        """Retorna el costo para el próximo nivel"""
        if self.nivel < self.nivel_maximo:
            return self.costos_mejora[self.nivel]
        return 0
    
    def mejorar(self, dinero):
        """Intenta mejorar el Herrero de nivel"""
        if not self.puede_mejorar():
            return False, "⚒️  El Herrero ya alcanzó nivel máximo (5)"
        
        costo = self.costo_proximo_nivel()
        if dinero < costo:
            return False, f"💰 No tienes suficiente dinero. Necesitas {costo}g"
        
        self.nivel += 1
        # Actualiza desbloqueos al subir nivel
        return True, f"✅ ⚒️  Herrero mejorado a nivel {self.nivel}! Tier {self.tier_desbloqueado[self.nivel]} desbloqueado"
    
    def _obtener_tipo_arma(self, arma):
        """Determina el tipo de arma (corta/media/grande) por nombre o propiedades"""
        nombre = arma.nombre.lower()
        
        # Armas cortas
        if any(x in nombre for x in ["daga", "corta", "pequeña"]):
            return "corta"
        
        # Armas grandes
        if any(x in nombre for x in ["lanza", "hacha", "doble", "destino", "neptuno", "marte"]):
            return "grande"
        
        # Por defecto: media (Espada, Tridente, Martillo, etc)
        return "media"
    
    def _calcular_costo_mejora(self, arma):
        """
        Calcula costo de mejora con fórmula: base × tipo_mult × nivel_mejora²
        nivel_mejora² hace que escale cuadráticamente
        """
        if not hasattr(arma, 'tier'):
            return 0
        
        tier = arma.tier
        costo_base = self.costo_base_mejora.get(tier, 100)
        tipo_mult = self.multiplicador_tipo[self._obtener_tipo_arma(arma)]
        
        # Nivel_mejora actual (para calcular el PRÓXIMO costo)
        nivel_actual = getattr(arma, 'nivel_mejora', 0)
        proximo_nivel = nivel_actual + 1
        
        # Fórmula: costo_base × tipo_mult × (próximo_nivel)²
        costo = int(costo_base * tipo_mult * (proximo_nivel ** 2))
        
        return costo
    
    def _actualizar_durabilidad(self, arma, degradar=True):
        """
        Actualiza durabilidad del arma
        Si degradar=True: reduce -5% por cada mejora
        Si degradar=False: se mantiene igual
        """
        if not hasattr(arma, 'durabilidad'):
            arma.durabilidad = 100.0
        
        if degradar:
            # Cada mejora reduce -5% durabilidad
            arma.durabilidad = max(0.0, arma.durabilidad - 5.0)
    
    def mejorar_arma(self, arma, dinero):
        """
        Mejora un arma aumentando su ATK por porcentaje
        Retorna: (exito, costo, mensaje)
        """
        if not hasattr(arma, 'tier'):
            return False, 0, "❌ Este arma no puede mejorarse"
        
        costo = self._calcular_costo_mejora(arma)
        
        if dinero < costo:
            return False, 0, f"💰 Mejora cuesta {costo}g (no tienes suficiente)"
        
        # Obtiene ATK actual y porcentaje a aplicar
        atk_actual = arma.attack
        porcentaje = self.porcentaje_atk[arma.tier]
        bonus_atk = max(1, int(atk_actual * porcentaje))  # Mínimo +1 ATK garantizado
        
        # Mejora el arma
        arma.attack += bonus_atk
        nivel_anterior = getattr(arma, 'nivel_mejora', 0)
        arma.nivel_mejora = nivel_anterior + 1
        
        # Degrada durabilidad por mejora
        self._actualizar_durabilidad(arma, degradar=True)
        
        # Actualiza estadísticas
        self.armas_mejoradas += 1
        self.ataque_total_otorgado += bonus_atk
        
        msg = f"⚔️  {arma.nombre} mejorado! [{nivel_anterior}→{arma.nivel_mejora}] | "
        msg += f"ATK: {atk_actual} → {arma.attack} (+{bonus_atk}) | "
        msg += f"Durabilidad: {getattr(arma, 'durabilidad', 100):.0f}% | Costo: {costo}g"
        
        return True, costo, msg
    
    def reparar_arma(self, arma, dinero):
        """
        Repara un arma restaurando su durabilidad
        Costo dinámico: (100 - durabilidad_actual) × precio_base / 10
        Retorna: (exito, costo, mensaje)
        """
        if not hasattr(arma, 'durabilidad'):
            arma.durabilidad = 100.0
        
        if arma.durabilidad >= 100.0:
            return False, 0, f"✅ {arma.nombre} está en perfectas condiciones (100%)"
        
        # Calcula costo dinámico
        # Más bajo si está poco degradado, más alto si está muy degradado
        perdida_durabilidad = 100.0 - arma.durabilidad
        tier = getattr(arma, 'tier', 1)
        precio_base = self.costo_base_mejora.get(tier, 100)
        
        costo_reparacion = int((perdida_durabilidad * precio_base) / 10)
        
        if dinero < costo_reparacion:
            return False, 0, f"💰 Reparación cuesta {costo_reparacion}g (no tienes suficiente)"
        
        # Repara el arma
        durabilidad_anterior = arma.durabilidad
        arma.durabilidad = 100.0
        restaurada = 100.0 - durabilidad_anterior
        
        # Actualiza estadísticas
        self.armas_reparadas += 1
        self.durabilidad_restaurada += int(restaurada)
        
        msg = f"🔧 {arma.nombre} reparado! Durabilidad: {durabilidad_anterior:.0f}% → 100% (+{restaurada:.0f}%) | Costo: {costo_reparacion}g"
        
        return True, costo_reparacion, msg
    
    def generar_resumen_estadisticas(self):
        """Retorna resumen formateado de estadísticas del Herrero"""
        resultado = "\n"
        resultado += "⚒️  ESTADÍSTICAS DEL HERRERO\n"
        resultado += "├─ Nivel: {}/5\n".format(self.nivel)
        resultado += "├─ Armas mejoradas: {}\n".format(self.armas_mejoradas)
        resultado += "├─ ATK total otorgado: {} puntos\n".format(self.ataque_total_otorgado)
        resultado += "├─ Armas reparadas: {}\n".format(self.armas_reparadas)
        resultado += "└─ Durabilidad restaurada: {} puntos\n".format(self.durabilidad_restaurada)
        return resultado
    
    def arma_desbloqueada(self, tier_arma):
        """Verifica si un tier de arma está desbloqueado para compra"""
        tier_max = self.tier_desbloqueado[self.nivel]
        return tier_arma <= tier_max
    
    def obtener_tier_desbloqueado(self):
        """Retorna el tier máximo desbloqueado"""
        return self.tier_desbloqueado[self.nivel]
    
    def generar_string(self):
        """Retorna string de estado del Herrero"""
        tier_max = self.tier_desbloqueado[self.nivel]
        linea = f"⚒️  Herrero Nivel {self.nivel}/5 | Tier desbloqueado: {tier_max}"
        if self.puede_mejorar():
            linea += f" | Mejora: {self.costo_proximo_nivel()}g"
        return linea


class FacilitiesManager:
    """Gestor de todas las facilities"""
    
    def __init__(self):
        self.medico = Medico(nivel=1)
        self.herrero = Herrero(nivel=1)
    
    def obtener_estado(self):
        """Retorna estado de todas las facilities"""
        return {
            "medico_nivel": self.medico.nivel,
            "herrero_nivel": self.herrero.nivel,
            "medico_curacion_rapida_usado": self.medico.curacion_rapida_usado,
        }
    
    def cargar_estado(self, estado):
        """Carga estado desde diccionario"""
        if estado:
            self.medico.nivel = estado.get("medico_nivel", 1)
            self.herrero.nivel = estado.get("herrero_nivel", 1)
            self.medico.curacion_rapida_usado = estado.get("medico_curacion_rapida_usado", False)
            
            # Actualiza desbloqueos
            if self.medico.nivel >= 2:
                self.medico.curacion_rapida_desbloqueada = True
    
    def resetear_dia(self):
        """Se llama cada día para resetear counters"""
        self.medico.resetear_curacion_rapida()
    
    def generar_resumen(self):
        """Retorna resumen formateado de facilities"""
        resultado = "\n"
        resultado += "=" * 70 + "\n"
        resultado += "                   ⚔️  MEJORAS DE FACILIDADES\n"
        resultado += "=" * 70 + "\n\n"
        resultado += self.medico.generar_string() + "\n"
        resultado += self.herrero.generar_string() + "\n\n"
        resultado += "=" * 70 + "\n"
        return resultado
