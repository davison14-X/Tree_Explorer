"""
buscador_archivos.py
Búsquedas avanzadas sobre el árbol N-ario de archivos.
"""

from datetime import datetime
from NodoArchivo import NodoArchivo
from ArbolArchivos import ArbolArchivos


class BuscadorArchivos:
    """
    Realiza búsquedas avanzadas sobre el árbol.
    Soporta búsqueda por nombre, extensión, tamaño y fecha.
    """

    def __init__(self, arbol: ArbolArchivos):
        self.arbol = arbol

    def buscar_por_nombre(self, nombre: str, exacto: bool = False) -> list[NodoArchivo]:
        """
        Busca archivos/carpetas por nombre.
        Si exacto=False hace búsqueda parcial (contiene el texto).
        """
        nodos = self.arbol.recorrer_DFS()
        if exacto:
            return [n for n in nodos if n.nombre.lower() == nombre.lower()]
        else:
            return [n for n in nodos if nombre.lower() in n.nombre.lower()]

    def buscar_por_extension(self, extension: str) -> list[NodoArchivo]:
        """
        Busca archivos por extensión (ej: 'pdf', 'txt', 'py').
        Solo retorna archivos (no carpetas).
        """
        ext = extension.lower().lstrip(".")
        nodos = self.arbol.recorrer_DFS()
        return [n for n in nodos if n.tipo == "archivo" and n.extension == ext]

    def buscar_por_tamaño(self, min_bytes: int = 0,
                          max_bytes: int = float("inf")) -> list[NodoArchivo]:
        """
        Busca archivos cuyo tamaño esté en el rango [min_bytes, max_bytes].
        Solo aplica a archivos (no carpetas).
        """
        nodos = self.arbol.recorrer_DFS()
        return [
            n for n in nodos
            if n.tipo == "archivo" and min_bytes <= n.tamaño <= max_bytes
        ]

    def buscar_por_fecha(self, desde: datetime = None,
                         hasta: datetime = None) -> list[NodoArchivo]:
        """
        Busca archivos modificados en un rango de fechas.
        """
        nodos = self.arbol.recorrer_DFS()
        resultado = []
        for n in nodos:
            if desde and n.fecha_modificacion < desde:
                continue
            if hasta and n.fecha_modificacion > hasta:
                continue
            resultado.append(n)
        return resultado

    def buscar_combinado(self, nombre: str = None, extension: str = None,
                         min_bytes: int = None, max_bytes: int = None) -> list[NodoArchivo]:
        """
        Búsqueda con múltiples filtros combinados (AND lógico).
        Solo los parámetros que no sean None se aplican como filtro.
        """
        nodos = self.arbol.recorrer_DFS()

        if nombre:
            nodos = [n for n in nodos if nombre.lower() in n.nombre.lower()]
        if extension:
            ext = extension.lower().lstrip(".")
            nodos = [n for n in nodos if n.tipo == "archivo" and n.extension == ext]
        if min_bytes is not None:
            nodos = [n for n in nodos if n.tipo == "archivo" and n.tamaño >= min_bytes]
        if max_bytes is not None:
            nodos = [n for n in nodos if n.tipo == "archivo" and n.tamaño <= max_bytes]

        return nodos

    def imprimir_resultados(self, resultados: list[NodoArchivo], titulo: str = "Resultados"):
        """Imprime los resultados de una búsqueda de forma formateada."""
        print(f"\n{'═'*50}")
        print(f"  🔍 {titulo}")
        print(f"  {len(resultados)} resultado(s) encontrado(s)")
        print(f"{'═'*50}")

        if not resultados:
            print("  (sin resultados)")
        else:
            for i, nodo in enumerate(resultados, 1):
                icono = "📁" if nodo.tipo == "carpeta" else "📄"
                print(f"  {i}. {icono} {nodo.nombre}")
                print(f"      Ruta   : {nodo.ruta}")
                print(f"      Tamaño : {nodo.tamaño_legible()}")
                print(f"      Fecha  : {nodo.fecha_modificacion.strftime('%Y-%m-%d %H:%M')}")
                if nodo.extension:
                    print(f"      Tipo   : .{nodo.extension}")
                print()