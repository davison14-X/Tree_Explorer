# Tree Explorer — Analizador de Archivos

Proyecto desarrollado en Python para explorar y analizar la estructura de archivos y directorios del sistema operativo o Importacion desde un archivo (.JSON). Utiliza un **árbol N-ario** como estructura de datos principal e implementa los algoritmos **DFS** y **BFS** para recorridos y búsquedas.

> Desarrollado para DPAS 3 — Politécnico Colombiano Jaime Isaza Cadavid
> Davison Jaramillo Gonzalez
> Jose Luis Grajales Cuervo

---

## ¿Qué hace?

El programa permite cargar cualquier carpeta del sistema y representarla como un árbol jerárquico. En el cuel el usuario puede:

- Visualizar la estructura de carpetas y archivos con recorrido DFS (profundidad) o BFS (por niveles)
- Buscar archivos por nombre, extensión, tamaño o combinación de filtros
- Ver estadísticas y reportes del directorio analizado
- Detectar archivos duplicados (por nombre o por hash MD5)
- Exportar e importar la estructura del árbol en formato JSON
- Medir el rendimiento de los algoritmos con benchmarks reales

---

## Estructura del proyecto

```
Tree_Explorer/
├── Main.py               # Punto de entrada y menú interactivo
├── NodoArchivo.py        # Clase que representa cada nodo del árbol (archivo -> Hoja o carpeta -> Padre)
├── ArbolArchivos.py      # Árbol N-ario con implementación de DFS y BFS
├── BuscadorArchivos.py   # Motor de búsqueda con múltiples filtros
├── Analizador.py         # Estadísticas, reportes y detección de duplicados
├── Exportador.py         # Exportación e importación a/desde JSON
├── Benchmark.py          # Pruebas de rendimiento DFS vs BFS
├── GeneradorDemo.py      # Generador de estructura demo con 100+ nodos
└── demo_100nodos.json    # Demo precargada para pruebas
```

---

## Tecnologías

- **Lenguaje:** Python 3
- **Librerías:** Solo librerías estándar (`os`, `sys`, `collections`, `time`, `statistics`, `hashlib`)
- **Entorno:** Terminal / Consola

---

## Instalación y uso

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/davison14-X/Tree_Explorer.git
   cd Tree_Explorer/Tree_explorer
   ```

2. Ejecutar el programa:
   ```bash
   python Main.py
   ```

No se requiere instalar dependencias externas.

---

## Menú principal

```
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
```

> **Tip:** Usa la opción `D` para cargar una demo de 100+ nodos y probar todas las funciones sin necesidad de apuntar a una carpeta real.

---

## Conceptos aplicados

- Árbol N-ario como estructura de datos principal
- Recorrido en profundidad (DFS) y por niveles (BFS)
- Hashing MD5 para detección de duplicados
- Serialización de árboles a JSON
- Medición estadística de rendimiento (min, max, promedio, mediana)
