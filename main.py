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
# SISTEMA DE MISIONES
# ============================================