"""
benchmark.py
Mide y compara el rendimiento de los algoritmos DFS y BFS
sobre el árbol N-ario de archivos.
"""

import time
import statistics
from ArbolArchivos import ArbolArchivos
from BuscadorArchivos import BuscadorArchivos


class Benchmark:
    """
    Ejecuta pruebas de rendimiento sobre DFS y BFS
    y genera un reporte comparativo con métricas reales.
    """

    def __init__(self, arbol: ArbolArchivos, repeticiones: int = 50):
        self.arbol = arbol
        self.repeticiones = repeticiones
        self.buscador = BuscadorArchivos(arbol)

    def _medir(self, funcion, *args) -> dict:
        """
        Ejecuta una función N veces y retorna métricas estadísticas
        de los tiempos de ejecución en milisegundos.
        """
        tiempos = []
        for _ in range(self.repeticiones):
            inicio = time.perf_counter()
            resultado = funcion(*args)
            fin = time.perf_counter()
            tiempos.append((fin - inicio) * 1000)  # ms

        return {
            "min_ms":    min(tiempos),
            "max_ms":    max(tiempos),
            "promedio_ms": statistics.mean(tiempos),
            "mediana_ms":  statistics.median(tiempos),
            "desviacion_ms": statistics.stdev(tiempos) if len(tiempos) > 1 else 0,
            "resultado":  resultado,
        }

    def ejecutar_todos(self) -> dict:
        """
        Ejecuta todos los benchmarks y retorna los resultados
        organizados por categoría.
        """
        total_nodos = len(self.arbol.recorrer_DFS())
        resultados = {"total_nodos": total_nodos, "repeticiones": self.repeticiones, "pruebas": {}}

        # ── RECORRIDO COMPLETO ──────────────────────────
        resultados["pruebas"]["dfs_recursivo"] = self._medir(self.arbol.recorrer_DFS)
        resultados["pruebas"]["dfs_iterativo"] = self._medir(self.arbol.recorrer_DFS_iterativo)
        resultados["pruebas"]["bfs"]           = self._medir(self.arbol.recorrer_BFS)

        # ── BÚSQUEDA ────────────────────────────────────
        # Tomamos el nombre de un nodo del árbol para buscar algo real
        todos = self.arbol.recorrer_DFS()
        archivos = [n for n in todos if n.tipo == "archivo"]

        if archivos:
            nombre_objetivo = archivos[len(archivos) // 2].nombre
            resultados["pruebas"]["busqueda_dfs"] = self._medir(
                self.arbol.buscar_por_nombre_DFS, nombre_objetivo)
            resultados["pruebas"]["busqueda_bfs"] = self._medir(
                self.arbol.buscar_por_nombre_BFS, nombre_objetivo)
            resultados["nombre_buscado"] = nombre_objetivo

        # ── CÁLCULO DE TAMAÑO ───────────────────────────
        resultados["pruebas"]["calcular_tamaño"] = self._medir(self.arbol.calcular_tamaño)

        # ── ALTURA DEL ÁRBOL ────────────────────────────
        resultados["pruebas"]["altura"] = self._medir(self.arbol.altura)

        return resultados

    def imprimir_reporte(self, resultados: dict = None):
        """Imprime el reporte comparativo de benchmarks."""
        if resultados is None:
            resultados = self.ejecutar_todos()

        r = resultados
        p = r["pruebas"]

        print(f"\n{'═'*62}")
        print(f"  ⏱️  BENCHMARKS DE RENDIMIENTO — TREE EXPLORER")
        print(f"{'═'*62}")
        print(f"  Nodos en el árbol : {r['total_nodos']}")
        print(f"  Repeticiones      : {r['repeticiones']}")
        print(f"{'─'*62}")

        # Tabla de recorridos
        print(f"\n  📊 RECORRIDO COMPLETO ({r['total_nodos']} nodos)")
        self._tabla_encabezado()
        self._tabla_fila("DFS Recursivo",  p["dfs_recursivo"])
        self._tabla_fila("DFS Iterativo",  p["dfs_iterativo"])
        self._tabla_fila("BFS (cola)",     p["bfs"])

        # Ganador recorrido
        tiempos_rec = {
            "DFS Recursivo": p["dfs_recursivo"]["promedio_ms"],
            "DFS Iterativo": p["dfs_iterativo"]["promedio_ms"],
            "BFS":           p["bfs"]["promedio_ms"],
        }
        ganador_rec = min(tiempos_rec, key=tiempos_rec.get)
        print(f"\n  🏆 Más rápido en recorrido: {ganador_rec}")

        # Tabla búsqueda
        if "busqueda_dfs" in p:
            nombre = r.get("nombre_buscado", "?")
            print(f"\n  🔍 BÚSQUEDA por nombre: '{nombre}'")
            self._tabla_encabezado()
            self._tabla_fila("Búsqueda DFS", p["busqueda_dfs"])
            self._tabla_fila("Búsqueda BFS", p["busqueda_bfs"])

            ganador_bus = (
                "DFS" if p["busqueda_dfs"]["promedio_ms"] <= p["busqueda_bfs"]["promedio_ms"]
                else "BFS"
            )
            print(f"\n  🏆 Más rápido en búsqueda: {ganador_bus}")

        # Tabla otras operaciones
        print(f"\n  🔧 OTRAS OPERACIONES")
        self._tabla_encabezado()
        self._tabla_fila("Calcular tamaño total", p["calcular_tamaño"])
        self._tabla_fila("Calcular altura",       p["altura"])

        # Análisis comparativo DFS vs BFS
        print(f"\n  💡 ANÁLISIS DFS vs BFS")
        print(f"  {'─'*58}")
        dfs_ms = p["dfs_recursivo"]["promedio_ms"]
        bfs_ms = p["bfs"]["promedio_ms"]
        diff = abs(dfs_ms - bfs_ms)
        pct  = (diff / max(dfs_ms, bfs_ms)) * 100

        if dfs_ms < bfs_ms:
            print(f"  DFS es {pct:.1f}% más rápido que BFS en este árbol.")
        else:
            print(f"  BFS es {pct:.1f}% más rápido que DFS en este árbol.")

        print(f"\n  📌 Conclusión de uso:")
        print(f"  • DFS  → Ideal para búsquedas en profundidad,")
        print(f"           detectar rutas largas, archivos anidados.")
        print(f"  • BFS  → Ideal para encontrar nodos en niveles")
        print(f"           superiores, listar contenido de carpeta.")
        print(f"{'═'*62}\n")

    def _tabla_encabezado(self):
        print(f"\n  {'Algoritmo':<25} {'Mín(ms)':>8} {'Prom(ms)':>9} {'Máx(ms)':>8} {'σ(ms)':>8}")
        print(f"  {'─'*60}")

    def _tabla_fila(self, nombre: str, datos: dict):
        print(
            f"  {nombre:<25}"
            f" {datos['min_ms']:>8.4f}"
            f" {datos['promedio_ms']:>9.4f}"
            f" {datos['max_ms']:>8.4f}"
            f" {datos['desviacion_ms']:>8.4f}"
        )