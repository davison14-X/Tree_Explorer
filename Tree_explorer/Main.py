"""
main.py
Punto de entrada del sistema TreeExplorer.
Menú interactivo en consola para todas las funcionalidades.
"""

import os
import sys
from ArbolArchivos import ArbolArchivos
from BuscadorArchivos import BuscadorArchivos
from Analizador import Analizador
from Exportador import Exportador
from Benchmark import Benchmark
from GeneradorDemo import guardar_demo


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\n  Presiona Enter para continuar...")


def imprimir_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║         🌳  TREE EXPLORER — Analizador de Archivos   ║
║         DPAS 3 — Politécnico Colombiano JIC          ║
╚══════════════════════════════════════════════════════╝
    """)


def menu_principal():
    print("""
  ┌─────────────────────────────────────────┐
  │              MENÚ PRINCIPAL             │
  ├─────────────────────────────────────────┤
  │  1. 📂  Cargar estructura de archivos   │
  │  2. 🌳  Visualizar árbol (DFS)          │
  │  3. 📶  Explorar por niveles (BFS)      │
  │  4. 🔍  Buscar archivos                 │
  │  5. 📊  Reporte y estadísticas          │
  │  6. 🔁  Detectar duplicados             │
  │  7. 💾  Exportar árbol a JSON           │
  │  8. 📥  Importar árbol desde JSON       │
  │  9. ⏱️   Benchmarks de rendimiento      │
  │  D. 🎲  Cargar demo (100+ nodos)        │
  │  0. 🚪  Salir                           │
  └─────────────────────────────────────────┘
    """)


def menu_busqueda():
    print("""
  ┌─────────────────────────────────────────┐
  │            MENÚ DE BÚSQUEDA             │
  ├─────────────────────────────────────────┤
  │  1. 🔤  Buscar por nombre               │
  │  2. 📎  Buscar por extensión            │
  │  3. ⚖️   Buscar por tamaño              │
  │  4. 🔀  Búsqueda combinada (filtros)    │
  │  0. ↩️   Volver al menú principal       │
  └─────────────────────────────────────────┘
    """)


def solicitar_ruta() -> str:
    """Solicita y valida una ruta al usuario."""
    while True:
        ruta = input("  Ingresa la ruta de la carpeta a analizar\n  > ").strip()
        if not ruta:
            # Usar directorio actual como default
            ruta = os.getcwd()
            print(f"  ℹ️  Usando directorio actual: {ruta}")
        if os.path.exists(ruta):
            return ruta
        print(f"  ❌ La ruta '{ruta}' no existe. Intenta de nuevo.")


def flujo_cargar(estado: dict):
    """Flujo para cargar una nueva estructura de archivos."""
    print("\n  📂 CARGAR ESTRUCTURA DE ARCHIVOS")
    print("  " + "─" * 45)
    ruta = solicitar_ruta()

    print(f"\n  ⏳ Analizando estructura en: {ruta}")
    print("  (esto puede tomar unos segundos en carpetas grandes)\n")

    try:
        arbol = ArbolArchivos()
        arbol.construir_desde_ruta(ruta)
        arbol.calcular_tamaño()

        estado["arbol"] = arbol
        estado["buscador"] = BuscadorArchivos(arbol)
        estado["analizador"] = Analizador(arbol)
        estado["exportador"] = Exportador(arbol)

        conteo = arbol.contar_nodos()
        print(f"  ✅ Árbol construido exitosamente.")
        print(f"     📁 Carpetas encontradas : {conteo['carpetas']}")
        print(f"     📄 Archivos encontrados : {conteo['archivos']}")
        print(f"     🌳 Altura del árbol     : {arbol.altura()} niveles")
        print(f"     💾 Espacio total        : {arbol.raiz.tamaño_legible()}")
    except Exception as e:
        print(f"  ❌ Error al construir el árbol: {e}")

    pausar()


def flujo_visualizar_dfs(estado: dict):
    """Muestra el árbol visualmente usando DFS."""
    if not estado["arbol"]:
        print("\n  ⚠️  Primero debes cargar una carpeta (opción 1).")
        pausar()
        return

    print("\n  🌳 ÁRBOL DE ARCHIVOS — RECORRIDO DFS")
    print("  " + "─" * 45)
    estado["arbol"].imprimir_arbol_DFS()
    pausar()


def flujo_visualizar_bfs(estado: dict):
    """Muestra el árbol por niveles usando BFS."""
    if not estado["arbol"]:
        print("\n  ⚠️  Primero debes cargar una carpeta (opción 1).")
        pausar()
        return

    print("\n  📶 ÁRBOL POR NIVELES — RECORRIDO BFS")
    estado["arbol"].imprimir_por_niveles_BFS()
    pausar()


def flujo_busqueda(estado: dict):
    """Menú de búsqueda avanzada."""
    if not estado["buscador"]:
        print("\n  ⚠️  Primero debes cargar una carpeta (opción 1).")
        pausar()
        return

    buscador: BuscadorArchivos = estado["buscador"]

    while True:
        limpiar_pantalla()
        imprimir_banner()
        menu_busqueda()
        opcion = input("  Selecciona una opción: ").strip()

        if opcion == "1":
            nombre = input("\n  Nombre a buscar (parcial o exacto): ").strip()
            exacto = input("  ¿Búsqueda exacta? (s/n): ").strip().lower() == "s"
            resultados = buscador.buscar_por_nombre(nombre, exacto)
            buscador.imprimir_resultados(resultados, f"Búsqueda por nombre: '{nombre}'")
            pausar()

        elif opcion == "2":
            ext = input("\n  Extensión a buscar (ej: pdf, txt, py): ").strip()
            resultados = buscador.buscar_por_extension(ext)
            buscador.imprimir_resultados(resultados, f"Archivos .{ext}")
            pausar()

        elif opcion == "3":
            print("\n  Ingresa el rango de tamaño (deja vacío para sin límite):")
            min_str = input("  Tamaño mínimo en KB (Enter = 0): ").strip()
            max_str = input("  Tamaño máximo en KB (Enter = sin límite): ").strip()
            min_bytes = int(min_str) * 1024 if min_str else 0
            max_bytes = int(max_str) * 1024 if max_str else float("inf")
            resultados = buscador.buscar_por_tamaño(min_bytes, max_bytes)
            buscador.imprimir_resultados(resultados, f"Archivos entre {min_str or 0}KB y {max_str or '∞'}KB")
            pausar()

        elif opcion == "4":
            print("\n  Filtros combinados (deja vacío para omitir un filtro):")
            nombre = input("  Nombre contiene: ").strip() or None
            ext = input("  Extensión (ej: pdf): ").strip() or None
            min_str = input("  Tamaño mínimo en KB: ").strip()
            max_str = input("  Tamaño máximo en KB: ").strip()
            min_bytes = int(min_str) * 1024 if min_str else None
            max_bytes = int(max_str) * 1024 if max_str else None
            resultados = buscador.buscar_combinado(nombre, ext, min_bytes, max_bytes)
            buscador.imprimir_resultados(resultados, "Búsqueda combinada")
            pausar()

        elif opcion == "0":
            break
        else:
            print("  ❌ Opción inválida.")
            pausar()


def flujo_reporte(estado: dict):
    """Muestra el reporte completo de análisis."""
    if not estado["analizador"]:
        print("\n  ⚠️  Primero debes cargar una carpeta (opción 1).")
        pausar()
        return

    estado["analizador"].imprimir_reporte_completo()
    pausar()


def flujo_duplicados(estado: dict):
    """Detecta y muestra archivos duplicados."""
    if not estado["analizador"]:
        print("\n  ⚠️  Primero debes cargar una carpeta (opción 1).")
        pausar()
        return

    print("\n  🔁 DETECCIÓN DE DUPLICADOS")
    print("  " + "─" * 45)
    print("  1. Por nombre (rápido)")
    print("  2. Por contenido MD5 (preciso, más lento)")
    modo = input("\n  Selecciona modo (1/2): ").strip()

    analizador: Analizador = estado["analizador"]

    if modo == "1":
        dups = analizador.detectar_duplicados_por_nombre()
        titulo = "Posibles duplicados por nombre"
    else:
        print("\n  ⏳ Calculando hashes MD5, por favor espera...")
        dups = analizador.detectar_duplicados()
        titulo = "Duplicados confirmados por hash MD5"

    print(f"\n  {'═'*50}")
    print(f"  🔁 {titulo}")
    print(f"  {'═'*50}")

    if not dups:
        print("  ✅ No se encontraron archivos duplicados.")
    else:
        print(f"  ⚠️  Se encontraron {len(dups)} grupo(s) de duplicados:\n")
        for i, (clave, nodos) in enumerate(dups.items(), 1):
            print(f"  Grupo {i} — clave: {clave[:16]}...")
            for nodo in nodos:
                print(f"    📄 {nodo.nombre}  [{nodo.tamaño_legible()}]")
                print(f"       {nodo.ruta}")
            print()

    pausar()


def flujo_exportar(estado: dict):
    """Exporta el árbol actual a JSON."""
    if not estado["exportador"]:
        print("\n  ⚠️  Primero debes cargar una carpeta (opción 1).")
        pausar()
        return

    ruta_salida = input("\n  Nombre del archivo JSON de salida (ej: estructura.json): ").strip()
    if not ruta_salida.endswith(".json"):
        ruta_salida += ".json"

    try:
        estado["exportador"].exportar_json(ruta_salida)
    except Exception as e:
        print(f"  ❌ Error al exportar: {e}")

    pausar()


def flujo_benchmark(estado: dict):
    """Ejecuta benchmarks de rendimiento comparando DFS y BFS."""
    if not estado["arbol"]:
        print("\n  ⚠️  Primero debes cargar una carpeta (opción 1 o D para demo).")
        pausar()
        return

    conteo = estado["arbol"].contar_nodos()
    print(f"\n  ⏱️  BENCHMARKS — {conteo['total']} nodos en el árbol")
    print("  Ejecutando 50 repeticiones por algoritmo, espera un momento...")

    bench = Benchmark(estado["arbol"], repeticiones=50)
    resultados = bench.ejecutar_todos()
    bench.imprimir_reporte(resultados)
    pausar()


def flujo_cargar_demo(estado: dict):
    """Genera y carga automáticamente la demo de 100+ nodos."""
    print("\n  🎲 DEMO — Generando estructura con 100+ nodos")
    print("  " + "─" * 45)

    ruta_json = "demo_100nodos.json"
    guardar_demo(ruta_json)

    print("\n  ⏳ Cargando árbol desde el JSON generado...")
    try:
        exportador = Exportador(ArbolArchivos())
        arbol = exportador.importar_json(ruta_json)
        arbol.calcular_tamaño()

        estado["arbol"] = arbol
        estado["buscador"] = BuscadorArchivos(arbol)
        estado["analizador"] = Analizador(arbol)
        estado["exportador"] = Exportador(arbol)

        conteo = arbol.contar_nodos()
        print(f"\n  ✅ Demo lista para explorar:")
        print(f"     📁 Carpetas : {conteo['carpetas']}")
        print(f"     📄 Archivos : {conteo['archivos']}")
        print(f"     🌳 Altura   : {arbol.altura()} niveles")
        print(f"     💾 Espacio  : {arbol.raiz.tamaño_legible()}")
        print(f"\n  ➡️  Ahora puedes usar cualquier opción del menú.")
    except Exception as e:
        print(f"  ❌ Error al cargar la demo: {e}")

    pausar()


def flujo_importar(estado: dict):
    """Importa un árbol desde un archivo JSON."""
    if not estado:
        estado = {}

    ruta_entrada = input("\n  Ruta del archivo JSON a importar: ").strip()

    try:
        exportador = Exportador(ArbolArchivos())
        arbol = exportador.importar_json(ruta_entrada)
        arbol.calcular_tamaño()

        estado["arbol"] = arbol
        estado["buscador"] = BuscadorArchivos(arbol)
        estado["analizador"] = Analizador(arbol)
        estado["exportador"] = Exportador(arbol)

        conteo = arbol.contar_nodos()
        print(f"\n  📊 Árbol cargado:")
        print(f"     Carpetas : {conteo['carpetas']}")
        print(f"     Archivos : {conteo['archivos']}")
    except Exception as e:
        print(f"  ❌ Error al importar: {e}")

    pausar()


def main():
    estado = {
        "arbol": None,
        "buscador": None,
        "analizador": None,
        "exportador": None,
    }

    acciones = {
        "1": flujo_cargar,
        "2": flujo_visualizar_dfs,
        "3": flujo_visualizar_bfs,
        "4": flujo_busqueda,
        "5": flujo_reporte,
        "6": flujo_duplicados,
        "7": flujo_exportar,
        "8": flujo_importar,
        "9": flujo_benchmark,
        "d": flujo_cargar_demo,
        "D": flujo_cargar_demo,
    }

    while True:
        limpiar_pantalla()
        imprimir_banner()

        # Mostrar estado actual
        if estado["arbol"] and estado["arbol"].raiz:
            print(f"  📌 Carpeta activa: {estado['arbol'].raiz.ruta}")
        else:
            print("  📌 Sin carpeta cargada")

        menu_principal()
        opcion = input("  Selecciona una opción: ").strip()

        if opcion == "0":
            print("\n  👋 ¡Hasta luego!\n")
            sys.exit(0)
        elif opcion in acciones:
            limpiar_pantalla()
            imprimir_banner()
            acciones[opcion](estado)
        else:
            print("  ❌ Opción inválida. Intenta de nuevo.")
            pausar()


if __name__ == "__main__":
    main()