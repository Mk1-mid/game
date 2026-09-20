input("\nPresiona ENTER para continuar...")


# ============================================
# INSTALACIONES DE RECURSOS (Fase 3.3)
# ============================================

def menu_instalaciones(equipo, facilities):
    """Menú principal de instalaciones de recursos."""
    while True:
        if not hasattr(equipo, 'instalaciones') or not equipo.instalaciones:
            print("\n❌ Sistema de instalaciones no disponible")
            break

        inst = equipo.instalaciones
        compradas = inst.obtener_compradas()

        print("\n" + "="*70)
        print("🏗️  INSTALACIONES DE RECURSOS")
        print("="*70)

        # Mostrar estado de cada instalación
        for i in inst.obtener_todas():
            if i.comprada:
                estado = f"✅ Nivel {i.nivel} | Ingreso: {i.ingreso_diario}g/día | {i.obtener_probabilidades_resumen()}"
            else:
                estado = "🔒 No construida"
            print(f"  {i.nombre:<18} {estado}")

        ingreso_total = inst.ingreso_total()
        if ingreso_total > 0:
            print(f"\n💰 Ingreso pasivo total: {ingreso_total}g/día")

        # Trabajadores activos
        if equipo.trabajadores_activos:
            print(f"\n👷 Trabajadores activos ({len(equipo.trabajadores_activos)}):")
            for t in equipo.trabajadores_activos:
                g = t["gladiador"]
                inst_t = t["instalacion_tipo"]
                dias = t["dias_restantes"]
                inst_obj = inst.obtener_por_tipo(inst_t)
                print(f"  • {g.nombre} en {inst_obj.nombre}: {dias} día(s) restantes")

        print(f"\n🔹 OPCIONES:")
        print(f"   1. 🏗️  Construir/Mejorar instalación")
        print(f"   2. 👷 Asignar gladiador a trabajo")
        print(f"   3. 📊 Ver detalles de producción")
        print(f"   0. Volver al menú principal")

        opcion = input("\n➤ Elige una opción [0-3]: ").strip()

        if opcion == "0":
            break

        elif opcion == "1":
            menu_construir_mejorar(equipo, facilities)

        elif opcion == "2":
            menu_asignar_trabajador(equipo)

        elif opcion == "3":
            menu_detalles_instalaciones(equipo)

        else:
            print("❌ Opción inválida")

        input("\nPresiona ENTER para continuar...")


def menu_construir_mejorar(equipo, facilities):
    """Submenú para construir o mejorar instalaciones."""
    if not hasattr(equipo, 'instalaciones') or not equipo.instalaciones:
        return

    inst = equipo.instalaciones

    while True:
        print("\n" + "="*60)
        print("🏗️  CONSTRUIR / MEJORAR")
        print("="*60)
        print(f"💰 Dinero disponible: {equipo.dinero}g")
        print()

        for i, inst_obj in enumerate(inst.obtener_todas(), 1):
            if inst_obj.comprada:
                if inst_obj.nivel < 5:
                    costo = inst_obj.costo_proxima_mejora
                    print(f"  [{i}] {inst_obj.nombre} (Nivel {inst_obj.nivel} → {inst_obj.nivel + 1}) - {costo}g")
                else:
                    print(f"  [{i}] {inst_obj.nombre} (Nivel 5 - MÁXIMO)")
            else:
                fm = FacilitiesManager()
                fm.herrero.nivel = facilities.herrero.nivel if facilities else 1
                puede, msg = inst_obj.puede_comprar(fm.herrero.nivel)
                estado = ""
                if not puede:
                    estado = f" ({msg})"
                print(f"  [{i}] {inst_obj.nombre} (Comprar: 2500g){estado}")

        print("  [0] Volver")

        try:
            opcion = int(input("\n➤ Elige instalación [0-3]: ").strip())
        except ValueError:
            print("❌ Entrada inválida")
            continue

        if opcion == 0:
            break

        if 1 <= opcion <= 3:
            inst_obj = list(inst.obtener_todas())[opcion - 1]
            if inst_obj.comprada:
                exito, costo, msg = inst.mejorar(inst_obj.tipo, equipo.dinero)
                if exito:
                    equipo.dinero -= costo
                    print(f"✅ {msg}")
                else:
                    print(msg)
            else:
                fm = FacilitiesManager()
                fm.herrero.nivel = facilities.herrero.nivel if facilities else 1
                exito, costo, msg = inst.comprar(inst_obj.tipo, equipo.dinero, fm.herrero.nivel)
                if exito:
                    equipo.dinero -= costo
                    print(f"✅ {msg}")
                else:
                    print(msg)
        else:
            print("❌ Opción inválida")


def menu_asignar_trabajador(equipo):
    """Submenú para asignar gladiador a trabajo."""
    if not hasattr(equipo, 'instalaciones') or not equipo.instalaciones:
        return

    inst = equipo.instalaciones
    compradas = inst.obtener_compradas()

    if not compradas:
        print("❌ No hay instalaciones construidas")
        return

    disponibles = [(i, g) for i, g in enumerate(equipo.gladiadores) if g.puede_luchar()]
    if not disponibles:
        print("❌ No hay gladiadores disponibles para trabajar")
        return

    print("\n" + "="*60)
    print("👷 ASIGNAR TRABAJADOR")
    print("="*60)

    print("\n🏗️  Instalaciones disponibles:")
    for i, inst_obj in enumerate(compradas, 1):
        print(f"  [{i}] {inst_obj.nombre} → +{inst_obj.nombre_stat}")

    print("[0] Volver")
    try:
        inst_idx = int(input("\n➤ Elige instalación [0-{}]: ".format(len(compradas))).strip())
    except ValueError:
        print("❌ Entrada inválida")
        return

    if inst_idx == 0:
        return
    if not (1 <= inst_idx <= len(compradas)):
        print("❌ Opción inválida")
        return

    inst_elegida = compradas[inst_idx - 1]

    print(f"\n🏷️  {inst_elegida.nombre} → Stat: +{inst_elegida.nombre_stat}")
    print("Días de trabajo:")
    print("  [1] 1 día  → 1 material, 50 XP, +1 stat, 5% riesgo herida")
    print("  [2] 3 días → 2 materiales, 150 XP, +3 stat, 12% riesgo herida")
    print("  [3] 5 días → 3 materiales, 250 XP, +5 stat, 20% riesgo herida")
    print("  [0] Volver")

    try:
        dias_opcion = int(input("\n➤ Elige duración [0-3]: ").strip())
    except ValueError:
        print("❌ Entrada inválida")
        return

    if dias_opcion == 0:
        return
    dias_map = {1: 1, 2: 3, 3: 5}
    if dias_opcion not in dias_map:
        print("❌ Opción inválida")
        return
    dias = dias_map[dias_opcion]

    print("\n👥 Gladiadores disponibles:")
    for i, (idx, g) in enumerate([(i, g) for i, g in enumerate(equipo.gladiadores) if g.puede_luchar()], 1):
        print(f"  [{i}] {g.nombre} (Lvl {g.nivel}) - HP: {g.hp_actual}/{g.hp} - {g.estado.upper()}")

    print("[0] Volver")
    try:
        glad_idx = int(input("\n➤ Elige gladiador [0-{}]: ".format(len(disponibles))).strip())
    except ValueError:
        print("❌ Entrada inválida")
        return

    if glad_idx == 0:
        return
    if not (1 <= glad_idx <= len(disponibles)):
        print("❌ Opción inválida")
        return

    gladiador_idx = disponibles[glad_idx - 1][0]
    exito, msg = equipo.asignar_trabajador(gladiador_idx, inst_elegida.tipo, dias)
    print(msg)


def menu_detalles_instalaciones(equipo):
    """Muestra detalles de probabilidades y producción."""
    if not hasattr(equipo, 'instalaciones') or not equipo.instalaciones:
        return

    inst = equipo.instalaciones

    print("\n" + "="*70)
    print("📊 DETALLES DE PRODUCCIÓN")
    print("="*70)

    for inst_obj in inst.obtener_todas():
        if not inst_obj.comprada:
            continue
        print(f"\n{inst_obj.nombre} (Nivel {inst_obj.nivel})")
        print(f"  Stat: +{inst_obj.nombre_stat} | Ingreso: {inst_obj.ingreso_diario}g/día")

        for dias in [1, 3, 5]:
            probs = inst_obj.obtener_probabilidades(dias)
            mult = MULTIPLICADORES_DIAS[dias]["yield"]
            riesgo = RIESGO_HERIDA[dias] * 100
            print(f"  {dias} día(s): {mult} materiales | C:{probs['comun']}% E:{probs['especial']}% M:{probs['mitica']}% | Riesgo: {riesgo:.0f}%")


# ============================================
# FORJA (Fase 3.4)
# ============================================

def menu_forja(equipo, facilities):
    """Menú principal de la Forja - mejora de armas y armaduras."""
    from src.facilities import FacilitiesManager
    from src.models import Weapon, Armor
    
    if not hasattr(equipo, 'instalaciones') or not equipo.instalaciones:
        print("\n❌ Sistema de instalaciones no disponible")
        return
    
    fm = FacilitiesManager()
    fm.herrero.nivel = facilities.herrero.nivel if facilities else 1
    
    while True:
        print("\n" + "="*70)
        print("⚒️  FORJA DEL HERRERO")
        print("="*70)
        print(f"🔨 Herrero: Nivel {fm.herrero.nivel}")
        print(f"💰 Dinero disponible: {equipo.dinero}g")
        print()
        
        print("🔹 OPCIONES:")
        print("   1. ⚔️  Mejorar arma")
        print("   2. 🛡️  Mejorar armadura")
        print("   3. 🔧 Reparar equipo")
        print("   4. 📋 Ver equipo disponible")
        print("   0. Volver al menú principal")
        
        opcion = input("\n➤ Elige una opción [0-4]: ").strip()
        
        if opcion == "0":
            break
        
        elif opcion == "1":
            _menu_mejorar_arma(equipo, fm)
        
        elif opcion == "2":
            _menu_mejorar_armadura(equipo, fm)
        
        elif opcion == "3":
            _menu_reparar(equipo, fm)
        
        elif opcion == "4":
            _menu_ver_equipo(equipo)
        
        else:
            print("❌ Opción inválida")
        
        input("\nPresiona ENTER para continuar...")


def _menu_mejorar_arma(equipo, fm):
    """Submenú para mejorar armas."""
    armas = [item for item in equipo.inventario if isinstance(item, Weapon)]
    if not armas:
        print("\n❌ No tienes armas en el inventario")
        return
    
    print("\n⚔️  ARMAS DISPONIBLES:")
    for i, arma in enumerate(armas, 1):
        tier_str = f" (Tier {arma.tier})" if hasattr(arma, 'tier') else ""
        print(f"  [{i}] {arma.nombre} - ATK: {arma.atk}{tier_str}")
    
    print("  [0] Volver")
    try:
        idx = int(input("\n➤ Elige arma [0-{}]: ".format(len(armas))).strip())
    except ValueError:
        print("❌ Entrada inválida")
        return
    
    if idx == 0 or idx > len(armas):
        return
    
    arma = armas[idx - 1]
    exito, costo, msg = fm.herrero.mejorar_arma(arma, equipo.dinero)
    if exito:
        equipo.dinero -= costo
        print(f"✅ {msg}")
    else:
        print(msg)


def _menu_mejorar_armadura(equipo, fm):
    """Submenú para mejorar armaduras."""
    armaduras = [item for item in equipo.inventario if isinstance(item, Armor)]
    if not armaduras:
        print("\n❌ No tienes armaduras en el inventario")
        return
    
    print("\n🛡️  ARMADURAS DISPONIBLES:")
    for i, arm in enumerate(armaduras, 1):
        print(f"  [{i}] {arm.nombre} - DEF: {arm.defensa}")
    
    print("  [0] Volver")
    try:
        idx = int(input("\n➤ Elige armadura [0-{}]: ".format(len(armaduras))).strip())
    except ValueError:
        print("❌ Entrada inválida")
        return
    
    if idx == 0 or idx > len(armaduras):
        return
    
    armadura = armaduras[idx - 1]
    exito, costo, msg = fm.herrero.mejorar_armadura(armadura, equipo.dinero)
    if exito:
        equipo.dinero -= costo
        print(f"✅ {msg}")
    else:
        print(msg)


def _menu_reparar(equipo, fm):
    """Submenú para reparar equipo dañado."""
    dañado = [item for item in equipo.inventario if hasattr(item, 'durabilidad_actual') and item.durabilidad_actual < item.durabilidad_max]
    if not dañado:
        print("\n✅ Todo el equipo está en perfecto estado")
        return
    
    print("\n🔧 EQUIPO DAÑADO:")
    for i, item in enumerate(dañado, 1):
        pct = int(item.durabilidad_actual / item.durabilidad_max * 100)
        tipo = "⚔️" if isinstance(item, Weapon) else "🛡️"
        print(f"  [{i}] {tipo} {item.nombre} - Durabilidad: {pct}% ({item.durabilidad_actual}/{item.durabilidad_max})")
    
    print("  [0] Volver")
    try:
        idx = int(input("\n➤ Elige item a reparar [0-{}]: ".format(len(dañado))).strip())
    except ValueError:
        print("❌ Entrada inválida")
        return
    
    if idx == 0 or idx > len(dañado):
        return
    
    item = dañado[idx - 1]
    exito, costo, msg = fm.herrero.reparar(item, equipo.dinero)
    if exito:
        equipo.dinero -= costo
        print(f"✅ {msg}")
    else:
        print(msg)


def _menu_ver_equipo(equipo):
    """Muestra todo el equipo del inventario."""
    if not equipo.inventario:
        print("\n📦 Inventario vacío")
        return
    
    print("\n📋 INVENTARIO COMPLETO:")
    for item in equipo.inventario:
        if isinstance(item, Weapon):
            tier_str = f" (Tier {item.tier})" if hasattr(item, 'tier') else ""
            dur_str = f" | Dur: {item.durabilidad_actual}/{item.durabilidad_max}" if hasattr(item, 'durabilidad_actual') else ""
            print(f"  ⚔️ {item.nombre} - ATK: {item.atk}{tier_str}{dur_str}")
        elif isinstance(item, Armor):
            dur_str = f" | Dur: {item.durabilidad_actual}/{item.durabilidad_max}" if hasattr(item, 'durabilidad_actual') else ""
            print(f"  🛡️ {item.nombre} - DEF: {item.defensa}{dur_str}")
        else:
            print(f"  📦 {item.nombre}")


# ============================================
# SISTEMA DE TALENTOS (Fase 4)
# ============================================

def menu_talentos(equipo):
    """Menú de asignación de talentos por gladiador.

    Args:
        equipo: Instancia de Equipo con gladiadores
    """
    if not equipo.gladiadores:
        print("\n❌ No hay gladiadores en el equipo")
        return

    while True:
        print("\n" + "="*70)
        print("🔰 ÁRBOL DE TALENTOS")
        print("="*70)
        print(f"💡 Puntos de talento disponibles: {equipo.gladiadores[0].puntos_talento if equipo.gladiadores else 0}")
        print()

        for i, g in enumerate(equipo.gladiadores, 1):
            arbol = g.arbol_talentos
            pts = g.puntos_talento
            niveles = f"F:{arbol['fuerza']} R:{arbol['resistencia']} A:{arbol['agilidad']} T:{arbol['tecnica']}"
            print(f"  [{i}] {g.nombre} (Lvl {g.nivel}) | Talents: {niveles} | Puntos: {pts}")

        print(f"\n  [0] Volver al menú principal")

        opcion = input("\n➤ Elige gladiador [0-{}]: ".format(len(equipo.gladiadores))).strip()

        if opcion == "0":
            break

        try:
            idx = int(opcion) - 1
        except ValueError:
            print("❌ Entrada inválida")
            continue

        if not (0 <= idx < len(equipo.gladiadores)):
            print("❌ Índice inválido")
            continue

        gladiador = equipo.gladiadores[idx]
        _submenu_asignar_talento(equipo, gladiador)

        input("\nPresiona ENTER para continuar...")


def _submenu_asignar_talento(equipo, gladiador):
    """Submenú para asignar puntos de talento a un gladiador.

    Args:
        equipo: Instancia de Equipo
        gladiador: Instancia de Gladiador
    """
    from src.talents import RAMAS, NIVEL_MAXIMO, NOMBRE_RAMA, EMOJI_RAMA, asignar_talento, obtener_resumen_talentos

    while True:
        resumen = obtener_resumen_talentos(gladiador)
        print("\n" + "-"*60)
        print(f"🔰 {gladiador.nombre} (Lvl {gladiador.nivel})")
        print(f"💡 Puntos disponibles: {resumen['puntos_disponibles']}")
        print("-"*60)

        for rama in RAMAS:
            nivel = resumen["arbol"][rama]
            nombre = NOMBRE_RAMA[rama]
            emoji = EMOJI_RAMA[rama]
            print(f"  {emoji} {nombre:<14} Nivel {nivel}/{NIVEL_MAXIMO}")

        print(f"\n  [0] Volver")

        opcion = input("\n➤ Elige rama [0-4]: ").strip()

        if opcion == "0":
            break

        rama_idx = {"1": "fuerza", "2": "resistencia", "3": "agilidad", "4": "tecnica"}.get(opcion)

        if rama_idx is None:
            print("❌ Opción inválida")
            continue

        exito, costo, msg = asignar_talento(gladiador, rama_idx)
        print(f"\n{msg}")

        if exito and resumen["puntos_disponibles"] == 0:
            print("\n📊 Resumen de talentos:")
            nuevo_resumen = obtener_resumen_talentos(gladiador)
            for stat, bonus in nuevo_resumen["bonus_total"].items():
                if bonus > 0:
                    print(f"  • {stat}: +{int(bonus*100)}%")
            hablis = nuevo_resumen["habilidades_unicas"]
            if hablis:
                print(f"  ⭐ Habilidades únicas: {', '.join(hablis)}")


# ============================================
# SISTEMA DE MISIONES
# ============================================