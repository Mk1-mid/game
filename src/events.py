"""
Sistema de Eventos Aleatorios (Fase 3.2)
=========================================

Por qué: dar vida al mundo entre combates y abrir las dos caras del juego —
el camino honorable y el camino turbio — como decisión estratégica real.

Los eventos se disparan al pasar el día (tras cada combate de arena) con
probabilidad global ~35%. Tres tipos:
- A: decisión sí/no
- B: decisión múltiple
- C: notificación automática (sin input del jugador)

El módulo NUNCA pide input: expone el evento, main.py muestra y elige,
y `resolver_opcion()` aplica efectos. Así los tests corren sin consola.
"""

import json
import os
import random

from .models import CATALOGO_MATERIALES


# ============================================
# CONSTANTES DE DISEÑO
# ============================================

PROBABILIDAD_EVENTO = 0.35  # ~1 de cada 3 días hay evento

# Umbrales de honra (sincronizar con Equipo.titulo_honra())
HONRA_EVENTOS_HONORABLES = 70   # >= 70: eventos honorable-only
HONRA_PARTICIPAR_TURBIO = 40    # < 40: te invitan a lo turbio
HONRA_ORGANIZAR_TURBIO = 30     # < 30: puedes organizar

# Costos/ganancias de honra
COSTO_HONRA_APUESTA = 6
COSTO_HONRA_TORNEO_PARTICIPAR = 8
COSTO_HONRA_TORNEO_ORGANIZAR = 12
COSTO_HONRA_RUMOR_ACEPTAR = 10
PREMIO_HONRA_DESAFIO_GANADO = 3

# Penitencia pública (redención instantánea, cara)
COSTO_PENITENCIA_ORO = 600
GANANCIA_PENITENCIA = 20
DIAS_FAMA_ATADA = 1  # tras penitencia, fama pausada 1 día


# ============================================
# HELPERS DE EFECTOS (retornan mensajes)
# ============================================

def material_aleatorio(rareza_max="especial"):
    """
    Material al azar del catálogo, hasta una rareza máxima.
    La mítica casi nunca es regalo — se consigue minando/forjando.
    """
    orden = ["comun", "especial", "mitica"]
    tope = orden.index(rareza_max)
    candidatos = [nombre for nombre, (rareza, _) in CATALOGO_MATERIALES.items()
                  if rareza in orden[:tope + 1]]
    return random.choice(candidatos) if candidatos else None


def _msg_dinero(equipo, cantidad):
    """Aplica oro (+ o -) y retorna mensaje."""
    equipo.dinero += cantidad
    signo = "+" if cantidad >= 0 else ""
    return f"💰 {signo}{cantidad}g (total: {equipo.dinero}g)"


def _msg_material(equipo, nombre, cantidad=1):
    """Aplica material y retorna mensaje."""
    total = equipo.agregar_material(nombre, cantidad)
    return f"📦 +{cantidad}x {nombre} (tienes {total})"


def _msg_honra(equipo, delta, motivo=""):
    """Aplica cambio de honra y retorna mensaje con contexto."""
    anterior = equipo.honra
    equipo.modificar_honra(delta)
    signo = "+" if delta >= 0 else ""
    msg = f"👑 Honra: {anterior} → {equipo.honra} ({signo}{delta})"
    if motivo:
        msg += f" — {motivo}"
    return msg


def _lista_patricios(patricios):
    """Extrae la lista viva de patricios del gestor (o lista vacía)."""
    if patricios is None:
        return []
    return patricios.patricios


def _patricio_por_afinidad(patricios, minima=-100, maxima=100):
    """Patricio aleatorio dentro de un rango de afinidad. None si no hay."""
    candidatos = [p for p in _lista_patricios(patricios)
                  if minima <= p.afinidad <= maxima]
    return random.choice(candidatos) if candidatos else None


# ============================================
# RESOLVERS (lógica de cada evento)
# ============================================
# Firma común: resolver(opcion_idx, equipo, patricios) -> list[str]
# Si el evento es tipo C, opcion_idx se ignora.


def _resolver_mercader(opcion, equipo, patricios):
    if opcion == 1:  # mineral común
        if equipo.dinero < 80:
            return ["💰 No tienes 80g para el mineral"]
        return [_msg_dinero(equipo, -80),
                _msg_material(equipo, "Mineral de Hierro", 2),
                "✓ El mercader asiente y desaparece entre la multitud"]
    elif opcion == 2:  # mineral especial
        if equipo.dinero < 250:
            return ["💰 No tienes 250g para el mineral raro"]
        pago = int(250 * equipo.modificador_mercado())
        return [_msg_dinero(equipo, -pago),
                _msg_material(equipo, "Mineral Raro", 1),
                "✓ Un buen trato... si sabes usarlo"]
    return ["✓ Te despides del mercader con una reverencia"]


def _resolver_prestamo(opcion, equipo, patricios):
    patricio = _patricio_por_afinidad(patricios, minima=20)
    if opcion == 1:
        if equipo.dinero < 500:
            return ["💰 No tienes 500g para prestar"]
        equipo.prestamos_pendientes.append({
            "patricio": patricio.nombre if patricio else "un patricio",
            "monto": 500,
            "devuelve": 650,  # interés del 30%
            "dias_restantes": 3,
        })
        msgs = [_msg_dinero(equipo, -500),
                _msg_honra(equipo, 1, "un patricio te debe un favor")]
        if patricio:
            patricio.modificar_afinidad(10)
            msgs.append(f"🤝 {patricio.nombre}: afinidad {patricio.afinidad} (+10)")
        msgs.append("📜 Te devolverá 650g en 3 días")
        return msgs
    # Rechazar: afinidad y honra caen levemente (no solidario)
    if patricio:
        patricio.modificar_afinidad(-5)
    return [_msg_honra(equipo, -3, "rome recuerda a los que cierran el puño"),
            "😒 El patricio se marcha sin despedirse"]


def _resolver_donacion(opcion, equipo, patricios):
    donacion_oro = random.randint(100, 400)
    mat = material_aleatorio("comun")
    msgs = [_msg_dinero(equipo, donacion_oro)]
    if mat:
        msgs.append(_msg_material(equipo, mat, 1))
    # Con fama alta, hay probabilidad de poción
    if random.random() < 0.3:
        msgs.append("🧪 ¡También dejó una Curación Menor entre los regalos!")
    msgs.append("✓ Roma ama a sus héroes de arena")
    return msgs


def _resolver_apuesta(opcion, equipo, patricios):
    if opcion != 1:
        return ["✓ Te guardas el oro. Esta vez."]
    if equipo.dinero < 200:
        return ["💰 Necesitas 200g para apostar"]
    equipo.registrar_evento_turbio(COSTO_HONRA_APUESTA)
    msgs = [_msg_dinero(equipo, -200),
            f"👑 Honra: {equipo.honra} (-{COSTO_HONRA_APUESTA}, racha reiniciada)"]
    if random.random() < 0.5:
        msgs += [_msg_dinero(equipo, 400),
                 "🎉 ¡Tu gladiador ganó! +200g de ganancia"]
    else:
        msgs.append("💀 Perdiste la apuesta. El crupier sonríe.")
    return msgs


def _resolver_torneo(opcion, equipo, patricios):
    if opcion == 1:
        # Participar con tu mejor gladiador disponible vs patricio turbio
        rival = _patricio_por_afinidad(patricios, maxima=30)
        disponibles = [g for g in equipo.gladiadores if g.puede_luchar()]
        if not disponibles:
            return ["❌ No tienes gladiadores disponibles para el torneo"]
        gladiador = max(disponibles, key=lambda g: g.nivel + g.combates_ganados)
        equipo.registrar_evento_turbio(COSTO_HONRA_TORNEO_PARTICIPAR)
        msgs = [f"🌑 {gladiador.nombre} entra al torneo clandestino...",
                f"👑 Honra: {equipo.honra} (-{COSTO_HONRA_TORNEO_PARTICIPAR})"]
        # Resolución simplificada por poder (el combate real vs patricio
        # sería demasiado largo dentro de un evento — se simula)
        poder_propio = gladiador.nivel + gladiador.combates_ganados + gladiador.ataque_final()
        poder_rival = 0
        nombre_rival = "un luchador anónimo"
        if rival and rival.mejor_gladiador():
            g_rival = rival.mejor_gladiador()
            poder_rival = g_rival.nivel + g_rival.combates_ganados + g_rival.ataque_final()
            nombre_rival = f"{g_rival.nombre} (de {rival.nombre})"
        prob_victoria = poder_propio / max(1, poder_propio + poder_rival)
        msgs.append(f"⚔️ Tu rival: {nombre_rival}")
        if random.random() < prob_victoria:
            bolsa = random.randint(300, 600)
            msgs += [_msg_dinero(equipo, bolsa),
                     f"🏆 ¡{gladiador.nombre} GANA el torneo clandestino!"]
            gladiador.combates_ganados += 1
            equipo.fama += 2
            msgs.append("⭐ Fama +2 (el bajo mundo habla de ti)")
        else:
            gladiador.aplicar_daño(int(gladiador.hp * 0.5))
            msgs.append(f"💀 Derrota brutal. {gladiador.nombre} queda muy herido")
        return msgs
    elif opcion == 2:
        return ["✓ Prefieres no mezclarte con esa gente. Por ahora."]
    elif opcion == 3:
        if equipo.honra >= HONRA_ORGANIZAR_TURBIO:
            return ["❌ Tu honra aún es demasiado alta para organizar eventos turbios"]
        equipo.registrar_evento_turbio(COSTO_HONRA_TORNEO_ORGANIZAR)
        return [_msg_dinero(equipo, 400),
                f"🎲 Organizaste el torneo: cobras las cuotas. Honra: {equipo.honra}",
                "🌑 Tu nombre ya circula en los bajos fondos de Roma"]
    return ["❌ Opción inválida"]


def _resolver_desafio(opcion, equipo, patricios):
    rival = _patricio_por_afinidad(patricios, maxima=-50)
    if not rival:
        return ["✓ El desafío se disuelve (no hay rival presente)"]
    if opcion != 1:
        rival.modificar_afinidad(5)  # te ve débil pero le quitas presión
        equipo.fama = max(0, equipo.fama - 3)
        return [f"🐔 Rechazaste el desafío de {rival.nombre}",
                "⭐ Fama -3 (Roma lo comenta)"]
    disponibles = [g for g in equipo.gladiadores if g.puede_luchar()]
    if not disponibles:
        return ["❌ No tienes gladiadores disponibles para el duelo"]
    propio = max(disponibles, key=lambda g: g.nivel + g.combates_ganados)
    g_rival = rival.mejor_gladiador()
    poder_propio = propio.nivel + propio.combates_ganados + propio.ataque_final()
    poder_rival = (g_rival.nivel + g_rival.combates_ganados + g_rival.ataque_final()
                   if g_rival else 5)
    msgs = [f"⚔️ DUELO: {propio.nombre} vs {g_rival.nombre if g_rival else '?'} de {rival.nombre}"]
    prob = poder_propio / max(1, poder_propio + poder_rival)
    if random.random() < prob:
        # Victoria: tu rival te respeta (rivalidad -70%), fama y honra limpia
        vieja_afinidad = rival.afinidad
        rival.modificar_afinidad(int(-rival.afinidad * 0.70))  # acerca a 0 un 70%
        propio.combates_ganados += 1
        equipo.fama += 5
        equipo.registrar_victoria_limpia()
        msgs += [f"🏆 ¡Victoria! {rival.nombre} te mira distinto "
                 f"(afinidad: {vieja_afinidad} → {rival.afinidad})",
                 f"⭐ Fama +5 | " + msgs_honra_victoria(equipo)]
    else:
        # Derrota: la rivalidad CRECE (te quiere volver a humillar) y fama cae
        rival.modificar_afinidad(int(rival.afinidad * 0.20))  # se aleja más un 20%
        propio.aplicar_daño(int(propio.hp * 0.6))
        equipo.fama = max(0, equipo.fama - 5)
        msgs += [f"💀 Derrota ante {rival.nombre}. Tu gladiador queda malherido",
                 f"⭐ Fama -5 | Su rivalidad hacia ti aumenta (afinidad: {rival.afinidad})"]
    return msgs


def msgs_honra_victoria(equipo):
    """Mensaje de honra tras victoria limpia (helper del desafío)."""
    return f"👑 Honra: {equipo.honra} (victoria limpia, racha: {equipo.racha_victorias_limpias})"


def _resolver_libertad(opcion, equipo, patricios):
    # El gladiador con más XP que no peleó hoy se dio "el día libre"
    candidatos = [g for g in equipo.gladiadores if g.puede_luchar()]
    if not candidatos:
        return ["✓ Nadie estaba de humor para salir"]
    famoso = max(candidatos, key=lambda g: g.xp + g.nivel * 50)
    actividad = random.choice(["mercado", "entrenamiento", "mina"])
    msgs = [f"🏺 {famoso.nombre} tuvo el día libre y salió por Roma..."]
    if actividad == "mercado":
        if random.random() < 0.5:
            msgs += [_msg_dinero(equipo, random.randint(50, 150)),
                     f"   Un mercader admirador le regaló propina por su fama"]
        else:
            msgs.append("   Volvió con una poción que le regalaron en el mercado")
    elif actividad == "entrenamiento":
        xp = random.randint(30, 80)
        famoso.ganar_xp(xp)
        msgs.append(f"   Entrenó con viejos compañeros: +{xp} XP")
    else:
        mat = material_aleatorio("comun")
        msgs.append(f"   " + _msg_material(equipo, mat, random.randint(1, 2)))
        famoso.ganar_xp(20)
        msgs.append(f"   Trabajó la mañana en la mina (+20 XP extra)")
    return msgs


def _resolver_relaciones(opcion, equipo, patricios):
    lista = _lista_patricios(patricios)
    if len(lista) < 2:
        return ["✓ No hubo novedades sociales hoy"]
    a, b = random.sample(lista, 2)
    # Cena patricia: dos relaciones se mueven al azar, te puede tocar
    msgs = ["🍷 Cena de patricios en las colinas de Roma..."]
    cambio = random.randint(-10, 15)
    a.modificar_afinidad(cambio)
    msgs.append(f"   {a.nombre} ahora siente {a.afinidad} hacia ti "
                f"({'+' if cambio >= 0 else ''}{cambio})")
    if random.random() < 0.4:
        b.modificar_afinidad(-5)
        msgs.append(f"   {b.nombre} habló mal de tu equipo (-5 afinidad)")
    return msgs


def _resolver_epidemia(opcion, equipo, patricios):
    sanos = [g for g in equipo.gladiadores if g.estado != "muerto"]
    if not sanos:
        return ["✓ (La epidemia evita tu ludus — no hay nadie a quién afectar)"]
    enfermo = random.choice(sanos)
    enfermo.aplicar_daño(int(enfermo.hp * 0.10))
    enfermo.ocupar("enfermedad", 1)
    return [f"🤒 Epidemia menor: {enfermo.nombre} cayó enfermo "
            f"(-10% HP, ocupado 1 día)"]


def _resolver_rumor_soborno(opcion, equipo, patricios):
    equipo.rumor_ofrecido = True
    if opcion == 1:
        equipo.habilitado_clandestino = True
        equipo.modificar_honra(-COSTO_HONRA_RUMOR_ACEPTAR)
        return [f"🌑 \"...te interesa, ¿verdad?\" El intermediario sonríe.",
                f"👑 Honra: {equipo.honra} (-{COSTO_HONRA_RUMOR_ACEPTAR})",
                "🔓 Ahora tienes acceso al mundo clandestino de Roma"]
    return [_msg_honra(equipo, 2, "rechazaste el contacto turbio"),
            "✓ Roma premia a los que no se venden. Por ahora."]


def _resolver_patrocinio(opcion, equipo, patricios):
    patricio = _patricio_por_afinidad(patricios, minima=30)
    bono = random.randint(150, 400) + equipo.fama * 10
    msgs = [_msg_dinero(equipo, bono),
            f"🏛️ {(patricio.nombre if patricio else 'Un patricio honorable')} "
            f"patrocina tu ludus por tu conducta intachable"]
    return msgs


def _resolver_penitencia(opcion, equipo, patricios):
    if opcion != 1:
        return ["✓ Sigues con tu vida, turbio pero tuyo"]
    if equipo.dinero < COSTO_PENITENCIA_ORO:
        return [f"💰 La penitencia cuesta {COSTO_PENITENCIA_ORO}g "
                f"(tienes {equipo.dinero}g)"]
    msgs = [_msg_dinero(equipo, -COSTO_PENITENCIA_ORO)]
    anterior = equipo.honra
    equipo.modificar_honra(GANANCIA_PENITENCIA)
    equipo.penitencia_fama_dias = DIAS_FAMA_ATADA
    msgs += [f"🕊️ Donaste a los templos y tu mejor gladiador luchó por caridad",
             f"👑 Honra: {anterior} → {equipo.honra} (+{GANANCIA_PENITENCIA})",
             f"⭐ Fama atada {DIAS_FAMA_ATADA} día(s) — Roma observa",
             "   ¨Roma perdona… una vez.\""]
    return msgs


# ============================================
# CATÁLOGO DE EVENTOS
# ============================================
# condicion(equipo, patricios) decides si PUEDE aparecer hoy

EVENTOS = [
    # --- gancho de arranque del sistema turbio (bootstrap) ---
    {
        "id": "rumor_soborno",
        "nombre": "🌑 Rumor de soborno",
        "tipo": "A",
        "condicion": lambda eq, pt: not eq.rumor_ofrecido,
        "descripcion": ("Un intermediario te susurra al oído: \"conozco a quien "
                        "organiza peleas sin reglas... ¿te interesa?\""),
        "opciones": ["Seguir el rumor (accedes a lo clandestino, -10 honra)",
                     "Ignorarlo (+2 honra)"],
        "resolver": _resolver_rumor_soborno,
    },

    # --- económicos con lore ---
    {
        "id": "mercader_ambulante",
        "nombre": "🏪 Mercader ambulante",
        "tipo": "B",
        "condicion": lambda eq, pt: True,
        "descripcion": ("Un mercader del Este ofrece minerales y mercancía rara "
                        "a precio de viajero."),
        "opciones": ["Comprar Mineral de Hierro x2 (80g)",
                     "Comprar Mineral Raro (250g, ajustado por honra)",
                     "Marcharse"],
        "resolver": _resolver_mercader,
    },
    {
        "id": "prestamo_patricio",
        "nombre": "🤝 Préstamo a patricio",
        "tipo": "A",
        "condicion": lambda eq, pt: eq.honra >= 50 and len(_lista_patricios(pt)) > 0,
        "descripcion": ("Un patricio cercano te pide 500g para expandir su ludus. "
                        "Te devolverá 650g en 3 días."),
        "opciones": ["Prestar 500g (+10 afinidad, +1 honra)",
                     "Rechazar (-5 afinidad, -3 honra)"],
        "resolver": _resolver_prestamo,
    },
    {
        "id": "donacion_admirador",
        "nombre": "🎁 Donación de admirador",
        "tipo": "C",
        "condicion": lambda eq, pt: sum(g.combates_ganados for g in eq.gladiadores) >= 3,
        "descripcion": "Un admirador dejó regalos en tu ludus.",
        "opciones": [],
        "resolver": _resolver_donacion,
    },

    # --- turbios (requieren acceso clandestino) ---
    {
        "id": "apuesta_clandestina",
        "nombre": "🎲 Apuesta clandestina",
        "tipo": "A",
        "condicion": lambda eq, pt: eq.habilitado_clandestino and eq.honra < HONRA_PARTICIPAR_TURBIO,
        "descripcion": ("Te invitan a apostar 200g en una pelea sin reglas. "
                        "50% de duplicar, 50% de perder todo."),
        "opciones": ["Apostar 200g (-6 honra)", "No apostar"],
        "resolver": _resolver_apuesta,
    },
    {
        "id": "torneo_clandestino",
        "nombre": "🌑 Torneo clandestino",
        "tipo": "B",
        "condicion": lambda eq, pt: eq.habilitado_clandestino and eq.honra < HONRA_PARTICIPAR_TURBIO,
        "descripcion": ("Se rumorea un torneo ilegal en los sótanos del mercado. "
                        "Grandes bolsas, peores compañías."),
        "opciones": ["Participar con tu mejor gladiador (-8 honra)",
                     "Rechazar",
                     "Organizar tú el torneo (+400g, -12 honra, requiere honra < 30)"],
        "resolver": _resolver_torneo,
    },

    # --- rivalidad y fama ---
    {
        "id": "desafio_rival",
        "nombre": "⚔️ Desafío de patricio rival",
        "tipo": "A",
        "condicion": lambda eq, pt: any(p.afinidad <= -50 for p in _lista_patricios(pt)),
        "descripcion": ("Un patricio que te odia te reta a duelo público ante toda Roma. "
                        "Si ganas, te respetará. Si pierdes, te humillará."),
        "opciones": ["Aceptar el duelo", "Rechazar"],
        "resolver": _resolver_desafio,
    },
    {
        "id": "libertad_gladiador",
        "nombre": "🏺 Libertad del gladiador famoso",
        "tipo": "C",
        "condicion": lambda eq, pt: any(g.puede_luchar() for g in eq.gladiadores),
        "descripcion": ("Tu gladiador más experimentado tenía el día libre "
                        "y salió por Roma..."),
        "opciones": [],
        "resolver": _resolver_libertad,
    },
    {
        "id": "relaciones_patricias",
        "nombre": "🍷 Reuniones de patricios",
        "tipo": "C",
        "condicion": lambda eq, pt: len(_lista_patricios(pt)) >= 2,
        "descripcion": "Los patricios cenan, charlan y se maquinan unos contra otros.",
        "opciones": [],
        "resolver": _resolver_relaciones,
    },
    {
        "id": "epidemia_menor",
        "nombre": "🤒 Epidemia menor",
        "tipo": "C",
        "condicion": lambda eq, pt: any(g.estado != "muerto" for g in eq.gladiadores),
        "descripcion": "Una fiebre recorre los ludi de Roma.",
        "opciones": [],
        "resolver": _resolver_epidemia,
    },

    # --- honorables ---
    {
        "id": "patrocinio_honorable",
        "nombre": "🏛️ Patrocinio honorable",
        "tipo": "C",
        "condicion": lambda eq, pt: eq.honra >= HONRA_EVENTOS_HONORABLES,
        "descripcion": ("Un patricio honorable admira tu conducta y decide "
                        "patrocinar tu ludus."),
        "opciones": [],
        "resolver": _resolver_patrocinio,
    },

    # --- redención ---
    {
        "id": "penitencia_publica",
        "nombre": "🕊️ Penitencia pública",
        "tipo": "A",
        "condicion": lambda eq, pt: eq.honra < 25,
        "descripcion": (f"Tu nombre hiede en Roma. Puedes donar {COSTO_PENITENCIA_ORO}g "
                        f"a los templos y ofrecer un combate de caridad para "
                        f"recuperar algo de tu honor. (+{GANANCIA_PENITENCIA} honra)"),
        "opciones": [f"Realizar la penitencia ({COSTO_PENITENCIA_ORO}g)",
                     "Seguir siendo quien eres"],
        "resolver": _resolver_penitencia,
    },
]


# ============================================
# GESTOR DE EVENTOS
# ============================================

class GestorEventos:
    """
    Puerta entre el motor de eventos y el juego.

    Por qué existe como clase y no como funciones sueltas: debe llevar
    historial por usuario y persistirlo (igual que GestorMisiones).
    main.py solo hace: `tirar_evento_dia()` → mostrar → `resolver_opcion()`.
    """

    ARCHIVO_DEFAULT = None  # se pasa al guardar/cargar (por usuario)

    def __init__(self):
        self.historial = []  # [{"evento", "opcion"} ...]

    def _candidatos(self, equipo, patricios):
        """Eventos cuya condición se cumple hoy."""
        return [e for e in EVENTOS if e["condicion"](equipo, patricios)]

    def evento_posible(self, equipo, patricios, evento):
        """Evalúa si un evento específico puede ocurrir hoy."""
        try:
            return evento["condicion"](equipo, patricios.patricios if patricios else [])
        except Exception:
            return False

    def tirar_evento_dia(self, equipo, patricios):
        """
        Tira los dados del día: ~35% de que ocurra un evento.

        Returns:
            dict del evento o None si hoy no pasa nada.
        """
        if random.random() > PROBABILIDAD_EVENTO:
            return None
        candidatos = self._candidatos(equipo, patricios)
        return random.choice(candidatos) if candidatos else None

    def resolver_opcion(self, evento, opcion_idx, equipo, patricios):
        """
        Aplica los efectos de la elección del jugador.

        Args:
            evento: dict del catálogo
            opcion_idx: 1-based (o ignorado si el evento es tipo C)
            equipo, patricios: estado del mundo

        Returns:
            list[str]: mensajes para mostrar al jugador
        """
        if evento["tipo"] == "C":
            msg = evento["resolver"](1, equipo, patricios)
        else:
            msg = evento["resolver"](opcion_idx, equipo, patricios)

        self.historial.append({
            "evento": evento["id"],
            "opcion": opcion_idx if evento["tipo"] != "C" else "auto",
        })
        return msg

    def procesar_prestamos(self, equipo):
        """
        Cobra/paga préstamos vencidos. Se llama al pasar cada día.

        Returns:
            list[str]: mensajes de préstamos que vencieron hoy
        """
        msgs = []
        pendientes = []
        for prestamo in equipo.prestamos_pendientes:
            prestamo["dias_restantes"] -= 1
            if prestamo["dias_restantes"] <= 0:
                equipo.dinero += prestamo["devuelve"]
                msgs.append(f"📜 {prestamo['patricio']} te devolvió "
                            f"{prestamo['devuelve']}g (préstamo de {prestamo['monto']}g)")
            else:
                pendientes.append(prestamo)
        equipo.prestamos_pendientes = pendientes
        return msgs

    def reducir_fama_atada(self, equipo):
        """Pasa un día: la fama atada por penitencia se libera."""
        if equipo.penitencia_fama_dias > 0:
            equipo.penitencia_fama_dias -= 1
            if equipo.penitencia_fama_dias == 0:
                return "🕊️ Tu fama queda liberada tras la penitencia"
        return None

    # --- Persistencia ---

    def serializar(self):
        """Convierte historial a dict para JSON."""
        return {"historial": self.historial[-50:]}  # solo lo reciente

    def deserializar(self, data):
        """Restaura historial desde dict JSON (tolerante a faltantes)."""
        self.historial = data.get("historial", []) if data else []

    def guardar_estado(self, archivo):
        """Guarda historial en JSON. Retorna True si ok."""
        try:
            os.makedirs(os.path.dirname(archivo) or ".", exist_ok=True)
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(self.serializar(), f, indent=2, ensure_ascii=False)
            return True
        except OSError:
            return False

    def cargar_estado(self, archivo):
        """Carga historial desde JSON. Retorna True si ok (False si no existe)."""
        if not os.path.exists(archivo):
            return False
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                self.deserializar(json.load(f))
            return True
        except (json.JSONDecodeError, OSError):
            return False

    def __repr__(self):
        return f"GestorEventos({len(self.historial)} eventos en historial)"
