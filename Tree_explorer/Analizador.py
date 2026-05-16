"""
analizador.py
Genera estadísticas del sistema de archivos y detecta duplicados.
"""

import hashlib
import os
from collections import defaultdict
from NodoArchivo import NodoArchivo
from ArbolArchivos import ArbolArchivos


class Analizador:
    """
    Analiza el árbol de archivos para generar estadísticas
    y detectar archivos duplicados.
    """

    def __init__(self, arbol: ArbolArchivos):
        self.arbol = arbol

    # ──────────────────────────────────────────────
    # ESTADÍSTICAS
    # ──────────────────────────────────────────────

    def calcular_espacio_total(self) -> dict:
        """
        Calcula el espacio total, ocupado y distribución por carpeta.
        Retorna un dict con las métricas principales.
        """
        self.arbol.calcular_tamaño()  # Actualiza tamaños de carpetas
        nodos = self.arbol.recorrer_DFS()
        archivos = [n for n in nodos if n.tipo == "archivo"]

        total_bytes = sum(n.tamaño for n in archivos)
        archivo_mas_grande = max(archivos, key=lambda n: n.tamaño, default=None)
        archivo_mas_pequeño = min(archivos, key=lambda n: n.tamaño, default=None)
        promedio = total_bytes / len(archivos) if archivos else 0

        return {
            "total_bytes": total_bytes,
            "total_legible": self._bytes_a_legible(total_bytes),
            "num_archivos": len(archivos),
            "promedio_bytes": promedio,
            "promedio_legible": self._bytes_a_legible(promedio),
            "mas_grande": archivo_mas_grande,
            "mas_pequeño": archivo_mas_pequeño,
        }

    def contar_tipos_archivos(self) -> dict[str, dict]:
        """
        Cuenta archivos agrupados por extensión.
        Retorna dict: {extension: {cantidad, bytes_total}}
        Ordenado de mayor a menor cantidad.
        """
        nodos = self.arbol.recorrer_DFS()
        conteo = defaultdict(lambda: {"cantidad": 0, "bytes_total": 0})

        for nodo in nodos:
            if nodo.tipo == "archivo":
                ext = nodo.extension if nodo.extension else "(sin extensión)"
                conteo[ext]["cantidad"] += 1
                conteo[ext]["bytes_total"] += nodo.tamaño

        # Ordenar por cantidad descendente
        return dict(sorted(conteo.items(), key=lambda x: x[1]["cantidad"], reverse=True))

    def carpetas_por_tamaño(self) -> list[tuple[NodoArchivo, int]]:
        """
        Retorna carpetas ordenadas por tamaño total (de mayor a menor).
        Útil para encontrar dónde se concentra el espacio en disco.
        """
        self.arbol.calcular_tamaño()
        nodos = self.arbol.recorrer_DFS()
        carpetas = [(n, n.tamaño) for n in nodos if n.tipo == "carpeta"]
        return sorted(carpetas, key=lambda x: x[1], reverse=True)

    def profundidad_por_nodo(self) -> dict[str, int]:
        """
        Calcula la profundidad de cada nodo en el árbol.
        La raíz tiene profundidad 0.
        """
        profundidades = {}
        nodos_con_nivel = [(self.arbol.raiz, 0)]
        from collections import deque
        cola = deque(nodos_con_nivel)

        while cola:
            nodo, nivel = cola.popleft()
            if nodo:
                profundidades[nodo.ruta] = nivel
                for hijo in nodo.hijos:
                    cola.append((hijo, nivel + 1))

        return profundidades

    # ──────────────────────────────────────────────
    # DETECCIÓN DE DUPLICADOS
    # ──────────────────────────────────────────────

    def detectar_duplicados(self) -> dict[str, list[NodoArchivo]]:
        """
        Detecta archivos duplicados comparando primero por tamaño,
        luego por hash MD5 del contenido real.

        Algoritmo:
        1. Agrupar archivos con el mismo tamaño (candidatos).
        2. Para cada grupo de candidatos, calcular hash MD5.
        3. Archivos con el mismo hash → duplicados confirmados.

        Retorna dict: {hash_md5: [lista de nodos duplicados]}
        """
        nodos = self.arbol.recorrer_DFS()
        archivos = [n for n in nodos if n.tipo == "archivo"]

        # Paso 1: Agrupar por tamaño
        por_tamaño = defaultdict(list)
        for nodo in archivos:
            por_tamaño[nodo.tamaño].append(nodo)

        # Solo los grupos con más de un archivo son candidatos
        candidatos = [grupo for grupo in por_tamaño.values() if len(grupo) > 1]

        # Paso 2: Calcular hash para candidatos
        por_hash = defaultdict(list)
        for grupo in candidatos:
            for nodo in grupo:
                hash_md5 = self._calcular_hash(nodo.ruta)
                if hash_md5:
                    por_hash[hash_md5].append(nodo)

        # Paso 3: Solo los que tienen más de un archivo con el mismo hash
        duplicados = {h: nodos for h, nodos in por_hash.items() if len(nodos) > 1}
        return duplicados

    def detectar_duplicados_por_nombre(self) -> dict[str, list[NodoArchivo]]:
        """
        Detección rápida de posibles duplicados solo por nombre de archivo.
        Menos precisa que por hash, pero más rápida.
        """
        nodos = self.arbol.recorrer_DFS()
        archivos = [n for n in nodos if n.tipo == "archivo"]

        por_nombre = defaultdict(list)
        for nodo in archivos:
            por_nombre[nodo.nombre.lower()].append(nodo)

        return {nombre: lista for nombre, lista in por_nombre.items() if len(lista) > 1}

    def _calcular_hash(self, ruta: str) -> str | None:
        """Calcula el hash MD5 de un archivo. Retorna None si hay error."""
        try:
            hasher = hashlib.md5()
            with open(ruta, "rb") as f:
                # Leer en bloques para no sobrecargar la memoria
                for bloque in iter(lambda: f.read(65536), b""):
                    hasher.update(bloque)
            return hasher.hexdigest()
        except (IOError, OSError):
            return None

    # ──────────────────────────────────────────────
    # COMPARACIÓN DE ESTRUCTURAS
    # ──────────────────────────────────────────────

    def comparar_estructuras(self, otro_arbol: ArbolArchivos) -> dict:
        """
        Compara dos árboles e identifica archivos únicos en cada uno
        y archivos comunes (presentes en ambos).
        """
        nodos_a = {n.nombre for n in self.arbol.recorrer_DFS() if n.tipo == "archivo"}
        nodos_b = {n.nombre for n in otro_arbol.recorrer_DFS() if n.tipo == "archivo"}

        return {
            "solo_en_a": sorted(nodos_a - nodos_b),
            "solo_en_b": sorted(nodos_b - nodos_a),
            "en_ambos": sorted(nodos_a & nodos_b),
        }

    # ──────────────────────────────────────────────
    # IMPRESIÓN DE REPORTES
    # ──────────────────────────────────────────────

    def imprimir_reporte_completo(self):
        """Imprime un reporte completo del análisis del árbol."""
        print("\n" + "═" * 55)
        print("  📊 REPORTE DE ANÁLISIS — TREE EXPLORER")
        print("═" * 55)

        # Espacio total
        espacio = self.calcular_espacio_total()
        print(f"\n  💾 ESPACIO EN DISCO")
        print(f"  {'─'*45}")
        print(f"  Total ocupado   : {espacio['total_legible']}")
        print(f"  N° de archivos  : {espacio['num_archivos']}")
        print(f"  Tamaño promedio : {espacio['promedio_legible']}")
        if espacio["mas_grande"]:
            print(f"  Archivo más grande  : {espacio['mas_grande'].nombre} "
                  f"({espacio['mas_grande'].tamaño_legible()})")
        if espacio["mas_pequeño"]:
            print(f"  Archivo más pequeño : {espacio['mas_pequeño'].nombre} "
                  f"({espacio['mas_pequeño'].tamaño_legible()})")

        # Tipos de archivos
        tipos = self.contar_tipos_archivos()
        print(f"\n  📂 TIPOS DE ARCHIVOS (top 10)")
        print(f"  {'─'*45}")
        print(f"  {'Extensión':<20} {'Cantidad':>8}  {'Espacio':>10}")
        print(f"  {'─'*45}")
        for ext, datos in list(tipos.items())[:10]:
            print(f"  .{ext:<19} {datos['cantidad']:>8}  "
                  f"{self._bytes_a_legible(datos['bytes_total']):>10}")

        # Conteo general
        conteo = self.arbol.contar_nodos()
        print(f"\n  🌳 ESTRUCTURA DEL ÁRBOL")
        print(f"  {'─'*45}")
        print(f"  Total nodos  : {conteo['total']}")
        print(f"  Carpetas     : {conteo['carpetas']}")
        print(f"  Archivos     : {conteo['archivos']}")
        print(f"  Altura árbol : {self.arbol.altura()} niveles")

        # Duplicados por nombre
        dups = self.detectar_duplicados_por_nombre()
        print(f"\n  🔁 POSIBLES DUPLICADOS (por nombre)")
        print(f"  {'─'*45}")
        if dups:
            for nombre, lista in list(dups.items())[:5]:
                print(f"  ⚠️  '{nombre}' → {len(lista)} copias")
        else:
            print("  ✅ No se encontraron posibles duplicados.")

        print("\n" + "═" * 55)

    def _bytes_a_legible(self, b: float) -> str:
        """Convierte bytes a string legible."""
        for unidad in ["B", "KB", "MB", "GB", "TB"]:
            if b < 1024:
                return f"{b:.1f} {unidad}"
            b /= 1024
        return f"{b:.1f} PB"