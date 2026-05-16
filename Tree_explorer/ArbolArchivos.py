"""
arbol_archivos.py
Gestiona el árbol N-ario completo del sistema de archivos.
Incluye algoritmos DFS y BFS para recorrido y búsqueda.
"""

import os
from collections import deque
from datetime import datetime
from NodoArchivo import NodoArchivo


class ArbolArchivos:
    """
    Árbol N-ario que representa la jerarquía de un sistema de archivos.
    Implementa DFS y BFS para recorridos y búsquedas.
    """

    def __init__(self):
        self.raiz: NodoArchivo | None = None

    # ──────────────────────────────────────────────
    # CONSTRUCCIÓN DEL ÁRBOL
    # ──────────────────────────────────────────────

    def construir_desde_ruta(self, ruta: str) -> NodoArchivo:
        """
        Construye el árbol N-ario leyendo el sistema de archivos real.
        Usa recursión (DFS implícito) para recorrer subdirectorios.
        """
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"La ruta no existe: {ruta}")

        self.raiz = self._construir_nodo(ruta)
        return self.raiz

    def _construir_nodo(self, ruta: str) -> NodoArchivo:
        """Crea un NodoArchivo y recursivamente agrega sus hijos."""
        stat = os.stat(ruta)
        nombre = os.path.basename(ruta) or ruta
        tipo = "carpeta" if os.path.isdir(ruta) else "archivo"
        fecha = datetime.fromtimestamp(stat.st_mtime)
        tamaño = stat.st_size if tipo == "archivo" else 0

        nodo = NodoArchivo(nombre, tipo, tamaño, fecha, ruta)

        if tipo == "carpeta":
            try:
                entradas = sorted(os.scandir(ruta), key=lambda e: (e.is_file(), e.name.lower()))
                for entrada in entradas:
                    hijo = self._construir_nodo(entrada.path)
                    nodo.agregar_hijo(hijo)
                # El tamaño de la carpeta = suma de todos sus hijos (se calcula después)
            except PermissionError:
                pass  # Carpetas sin permiso se omiten silenciosamente

        return nodo

    def agregar_nodo(self, ruta_padre: str, nuevo_nodo: NodoArchivo) -> bool:
        """Agrega un nodo manualmente buscando el padre por ruta."""
        padre = self.buscar_por_ruta(ruta_padre)
        if padre:
            padre.agregar_hijo(nuevo_nodo)
            return True
        return False

    # ──────────────────────────────────────────────
    # RECORRIDO DFS — Depth First Search
    # ──────────────────────────────────────────────

    def recorrer_DFS(self, nodo: NodoArchivo = None, nivel: int = 0) -> list[NodoArchivo]:
        """
        Recorrido DFS recursivo (preorden).
        Visita el nodo actual antes que sus hijos.
        Retorna lista de todos los nodos en orden DFS.
        """
        if nodo is None:
            nodo = self.raiz
        if nodo is None:
            return []

        resultado = [nodo]
        for hijo in nodo.hijos:
            resultado.extend(self.recorrer_DFS(hijo, nivel + 1))
        return resultado

    def recorrer_DFS_iterativo(self) -> list[NodoArchivo]:
        """
        Recorrido DFS iterativo usando una pila (stack).
        Equivalente al recursivo pero sin riesgo de stack overflow.
        """
        if not self.raiz:
            return []

        resultado = []
        pila = [self.raiz]  # Stack: LIFO

        while pila:
            nodo = pila.pop()
            resultado.append(nodo)
            # Se agregan hijos en orden inverso para mantener el orden correcto
            for hijo in reversed(nodo.hijos):
                pila.append(hijo)

        return resultado

    def imprimir_arbol_DFS(self, nodo: NodoArchivo = None, nivel: int = 0, prefijo: str = ""):
        """Imprime el árbol visualmente usando DFS."""
        if nodo is None:
            nodo = self.raiz
        if nodo is None:
            print("Árbol vacío.")
            return

        if nivel == 0:
            print(f"📁 {nodo.nombre}/")
        else:
            conector = "└── " if prefijo.endswith("    ") else "├── "
            icono = "📁" if nodo.tipo == "carpeta" else "📄"
            print(f"{prefijo}{conector}{icono} {nodo.nombre}  [{nodo.tamaño_legible()}]")

        for i, hijo in enumerate(nodo.hijos):
            es_ultimo = i == len(nodo.hijos) - 1
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            self.imprimir_arbol_DFS(hijo, nivel + 1, nuevo_prefijo)

    # ──────────────────────────────────────────────
    # RECORRIDO BFS — Breadth First Search
    # ──────────────────────────────────────────────

    def recorrer_BFS(self) -> list[NodoArchivo]:
        """
        Recorrido BFS usando una cola (queue).
        Visita todos los nodos nivel por nivel.
        Retorna lista de todos los nodos en orden BFS.
        """
        if not self.raiz:
            return []

        resultado = []
        cola = deque([self.raiz])  # Queue: FIFO

        while cola:
            nodo = cola.popleft()
            resultado.append(nodo)
            for hijo in nodo.hijos:
                cola.append(hijo)

        return resultado

    def imprimir_por_niveles_BFS(self):
        """Imprime el árbol nivel por nivel usando BFS."""
        if not self.raiz:
            print("Árbol vacío.")
            return

        cola = deque([(self.raiz, 0)])
        nivel_actual = -1

        while cola:
            nodo, nivel = cola.popleft()

            if nivel != nivel_actual:
                nivel_actual = nivel
                print(f"\n{'─'*40}")
                print(f"  NIVEL {nivel}")
                print(f"{'─'*40}")

            icono = "📁" if nodo.tipo == "carpeta" else "📄"
            print(f"  {icono} {nodo.nombre}  [{nodo.tamaño_legible()}]")

            for hijo in nodo.hijos:
                cola.append((hijo, nivel + 1))

    # ──────────────────────────────────────────────
    # BÚSQUEDA
    # ──────────────────────────────────────────────

    def buscar_por_nombre_DFS(self, nombre: str) -> list[NodoArchivo]:
        """Busca nodos por nombre exacto usando DFS recursivo."""
        return [n for n in self.recorrer_DFS() if n.nombre.lower() == nombre.lower()]

    def buscar_por_nombre_BFS(self, nombre: str) -> list[NodoArchivo]:
        """Busca nodos por nombre exacto usando BFS."""
        return [n for n in self.recorrer_BFS() if n.nombre.lower() == nombre.lower()]

    def buscar_por_ruta(self, ruta: str) -> NodoArchivo | None:
        """Busca un nodo por su ruta completa."""
        for nodo in self.recorrer_DFS():
            if nodo.ruta == ruta:
                return nodo
        return None

    # ──────────────────────────────────────────────
    # CÁLCULOS
    # ──────────────────────────────────────────────

    def calcular_tamaño(self, nodo: NodoArchivo = None) -> int:
        """
        Calcula el tamaño total de un nodo (y sus descendientes) usando DFS.
        Para archivos retorna su tamaño directo.
        Para carpetas suma recursivamente todos los hijos.
        """
        if nodo is None:
            nodo = self.raiz
        if nodo is None:
            return 0

        if nodo.tipo == "archivo":
            return nodo.tamaño

        total = sum(self.calcular_tamaño(hijo) for hijo in nodo.hijos)
        nodo.tamaño = total  # Actualiza el campo para uso futuro
        return total

    def contar_nodos(self) -> dict:
        """Cuenta archivos y carpetas totales en el árbol."""
        nodos = self.recorrer_DFS()
        carpetas = sum(1 for n in nodos if n.tipo == "carpeta")
        archivos = sum(1 for n in nodos if n.tipo == "archivo")
        return {"total": len(nodos), "carpetas": carpetas, "archivos": archivos}

    def altura(self, nodo: NodoArchivo = None) -> int:
        """Calcula la altura del árbol (nivel más profundo)."""
        if nodo is None:
            nodo = self.raiz
        if nodo is None or nodo.es_hoja():
            return 0
        return 1 + max(self.altura(hijo) for hijo in nodo.hijos)