"""
exportador.py
Importa y exporta la estructura del árbol en formato JSON.
"""

import json
from datetime import datetime
from NodoArchivo import NodoArchivo
from ArbolArchivos import ArbolArchivos


class Exportador:
    """
    Serializa y deserializa el árbol N-ario a/desde JSON.
    Permite guardar, compartir e importar estructuras analizadas.
    """

    def __init__(self, arbol: ArbolArchivos):
        self.arbol = arbol

    def exportar_json(self, ruta_salida: str):
        """
        Exporta todo el árbol a un archivo JSON.
        """
        if not self.arbol.raiz:
            raise ValueError("El árbol está vacío, no hay nada que exportar.")

        datos = self._nodo_a_dict(self.arbol.raiz)

        with open(ruta_salida, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

        print(f"✅ Árbol exportado exitosamente a: {ruta_salida}")

    def importar_json(self, ruta_entrada: str) -> ArbolArchivos:
        """
        Importa un árbol desde un archivo JSON previamente exportado.
        """
        with open(ruta_entrada, "r", encoding="utf-8") as f:
            datos = json.load(f)

        arbol = ArbolArchivos()
        arbol.raiz = self._dict_a_nodo(datos)
        self.arbol = arbol
        print(f"✅ Árbol importado exitosamente desde: {ruta_entrada}")
        return arbol

    def _nodo_a_dict(self, nodo: NodoArchivo) -> dict:
        """Convierte recursivamente un nodo a diccionario serializable."""
        return {
            "nombre": nodo.nombre,
            "tipo": nodo.tipo,
            "tamaño": nodo.tamaño,
            "fecha_modificacion": nodo.fecha_modificacion.isoformat(),
            "ruta": nodo.ruta,
            "extension": nodo.extension,
            "hijos": [self._nodo_a_dict(hijo) for hijo in nodo.hijos]
        }

    def _dict_a_nodo(self, datos: dict, padre: NodoArchivo = None) -> NodoArchivo:
        """Reconstruye recursivamente un nodo desde un diccionario."""
        fecha = datetime.fromisoformat(datos["fecha_modificacion"])
        nodo = NodoArchivo(
            nombre=datos["nombre"],
            tipo=datos["tipo"],
            tamaño=datos["tamaño"],
            fecha_modificacion=fecha,
            ruta=datos["ruta"]
        )
        nodo.padre = padre
        for hijo_dict in datos.get("hijos", []):
            hijo = self._dict_a_nodo(hijo_dict, nodo)
            nodo.hijos.append(hijo)
        return nodo