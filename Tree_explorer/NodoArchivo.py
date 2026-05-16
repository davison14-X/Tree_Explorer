"""
nodo_archivo.py
Representa cada nodo del árbol N-ario (archivo o carpeta).
"""

from datetime import datetime


class NodoArchivo:
    """
    Nodo del árbol N-ario que representa un archivo o carpeta
    dentro del sistema de archivos.
    """

    def __init__(self, nombre: str, tipo: str, tamaño: int = 0,
                 fecha_modificacion: datetime = None, ruta: str = ""):
        self.nombre = nombre
        self.tipo = tipo  # "carpeta" o "archivo"
        self.tamaño = tamaño  # en bytes
        self.fecha_modificacion = fecha_modificacion or datetime.now()
        self.ruta = ruta
        self.extension = self._obtener_extension()
        self.hijos: list["NodoArchivo"] = []
        self.padre: "NodoArchivo | None" = None

    def _obtener_extension(self) -> str:
        """Extrae la extensión del archivo (vacía si es carpeta)."""
        if self.tipo == "carpeta":
            return ""
        partes = self.nombre.rsplit(".", 1)
        return partes[1].lower() if len(partes) == 2 else ""

    def agregar_hijo(self, nodo: "NodoArchivo"):
        """Agrega un nodo hijo y establece su referencia al padre."""
        nodo.padre = self
        self.hijos.append(nodo)

    def eliminar_hijo(self, nombre: str) -> bool:
        """Elimina un hijo por nombre. Retorna True si lo encontró."""
        for i, hijo in enumerate(self.hijos):
            if hijo.nombre == nombre:
                self.hijos.pop(i)
                return True
        return False

    def es_hoja(self) -> bool:
        """Retorna True si el nodo no tiene hijos (es archivo o carpeta vacía)."""
        return len(self.hijos) == 0

    def tamaño_legible(self) -> str:
        """Convierte el tamaño a formato legible (KB, MB, GB)."""
        t = self.tamaño
        for unidad in ["B", "KB", "MB", "GB", "TB"]:
            if t < 1024:
                return f"{t:.1f} {unidad}"
            t /= 1024
        return f"{t:.1f} PB"

    def __repr__(self):
        icono = "📁" if self.tipo == "carpeta" else "📄"
        return f"{icono} {self.nombre} ({self.tamaño_legible()})"