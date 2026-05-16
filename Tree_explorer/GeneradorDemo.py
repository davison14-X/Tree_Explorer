"""
generador_demo.py
Genera una estructura JSON de prueba con 100+ nodos
para demostrar el sistema sin necesidad de una carpeta real.
"""

import json
import random
from datetime import datetime, timedelta


# ── Datos de ejemplo realistas ───────────────────────────────
NOMBRES_CARPETAS = [
    "src", "tests", "docs", "assets", "images", "videos", "audio",
    "downloads", "backup", "config", "lib", "utils", "models",
    "controllers", "views", "static", "templates", "scripts",
    "reports", "data", "logs", "cache", "temp", "uploads", "public",
]

NOMBRES_ARCHIVOS = [
    ("main", "py"), ("app", "py"), ("index", "html"), ("style", "css"),
    ("script", "js"), ("README", "md"), ("requirements", "txt"),
    ("config", "json"), ("database", "sql"), ("report", "pdf"),
    ("logo", "png"), ("banner", "jpg"), ("video_intro", "mp4"),
    ("music", "mp3"), ("data", "csv"), ("notas", "txt"),
    ("presentacion", "pptx"), ("factura", "pdf"), ("foto_viaje", "jpg"),
    ("backup", "zip"), ("setup", "py"), ("Dockerfile", ""),
    ("docker-compose", "yml"), ("schema", "json"), ("test_main", "py"),
    ("utils", "py"), ("helpers", "py"), ("constants", "py"),
    ("middleware", "py"), ("routes", "py"), ("models", "py"),
    ("views", "py"), ("serializers", "py"), ("admin", "py"),
    ("migrations", "sql"), ("seed", "sql"), ("analysis", "ipynb"),
    ("chart", "png"), ("diagram", "svg"), ("wireframe", "fig"),
]

EXTENSIONES_SIZES = {
    "py":   (500,   50_000),
    "js":   (1_000, 200_000),
    "html": (2_000, 80_000),
    "css":  (1_000, 60_000),
    "md":   (500,   20_000),
    "txt":  (100,   10_000),
    "json": (200,   50_000),
    "sql":  (1_000, 500_000),
    "pdf":  (50_000, 5_000_000),
    "png":  (10_000, 2_000_000),
    "jpg":  (50_000, 8_000_000),
    "mp4":  (5_000_000, 500_000_000),
    "mp3":  (2_000_000, 50_000_000),
    "csv":  (1_000, 10_000_000),
    "pptx": (100_000, 20_000_000),
    "zip":  (50_000, 200_000_000),
    "yml":  (100,   5_000),
    "":     (0, 1_000),
    "ipynb": (10_000, 500_000),
    "svg":  (5_000, 100_000),
}


def _fecha_aleatoria() -> str:
    dias = random.randint(0, 365 * 2)
    fecha = datetime(2024, 1, 1) + timedelta(days=dias, seconds=random.randint(0, 86400))
    return fecha.isoformat()


def _tamaño_aleatorio(ext: str) -> int:
    rango = EXTENSIONES_SIZES.get(ext, (1_000, 500_000))
    return random.randint(*rango)


def _crear_archivo(nombre: str, ext: str, ruta_padre: str) -> dict:
    nombre_completo = f"{nombre}.{ext}" if ext else nombre
    ruta = f"{ruta_padre}/{nombre_completo}"
    return {
        "nombre": nombre_completo,
        "tipo": "archivo",
        "tamaño": _tamaño_aleatorio(ext),
        "fecha_modificacion": _fecha_aleatoria(),
        "ruta": ruta,
        "extension": ext,
        "hijos": []
    }


def _crear_carpeta(nombre: str, ruta_padre: str, hijos: list) -> dict:
    ruta = f"{ruta_padre}/{nombre}"
    tamaño_total = sum(h["tamaño"] for h in hijos)
    return {
        "nombre": nombre,
        "tipo": "carpeta",
        "tamaño": tamaño_total,
        "fecha_modificacion": _fecha_aleatoria(),
        "ruta": ruta,
        "extension": "",
        "hijos": hijos
    }


def generar_estructura(nodos_objetivo: int = 120) -> dict:
    """
    Genera una estructura de árbol N-ario realista con al menos
    nodos_objetivo nodos, usando datos ficticios pero coherentes.
    """
    random.seed(42)  # Semilla fija para reproducibilidad

    ruta_raiz = "/proyecto_demo"
    archivos_usados = list(NOMBRES_ARCHIVOS)
    random.shuffle(archivos_usados)
    idx_archivo = [0]  # Índice mutable

    def siguiente_archivo():
        if idx_archivo[0] >= len(archivos_usados):
            idx_archivo[0] = 0
        entry = archivos_usados[idx_archivo[0]]
        idx_archivo[0] += 1
        return entry

    def generar_subcarpeta(nombre: str, ruta_padre: str, num_archivos: int,
                           nivel: int = 0, max_nivel: int = 3) -> dict:
        hijos = []
        ruta_actual = f"{ruta_padre}/{nombre}"

        # Agregar archivos directos
        for _ in range(num_archivos):
            n, ext = siguiente_archivo()
            hijos.append(_crear_archivo(n, ext, ruta_actual))

        # Agregar subcarpetas (si no llegamos al nivel máximo)
        if nivel < max_nivel and random.random() > 0.3:
            num_sub = random.randint(1, 3)
            nombres_sub = random.sample(NOMBRES_CARPETAS, min(num_sub, len(NOMBRES_CARPETAS)))
            for nombre_sub in nombres_sub:
                num_arch_sub = random.randint(2, 6)
                sub = generar_subcarpeta(nombre_sub, ruta_actual, num_arch_sub,
                                         nivel + 1, max_nivel)
                hijos.append(sub)

        return _crear_carpeta(nombre, ruta_padre, hijos)

    # Construir estructura raíz con carpetas principales
    carpetas_raiz = [
        ("src",       10, 2),
        ("docs",       5, 1),
        ("tests",      8, 2),
        ("assets",     5, 2),
        ("data",       6, 1),
        ("config",     4, 0),
        ("scripts",    5, 1),
        ("reports",    4, 1),
        ("logs",       4, 0),
    ]

    hijos_raiz = []

    # Archivos en la raíz
    for nombre, ext in [
        ("README", "md"), ("requirements", "txt"), ("Dockerfile", ""),
        ("docker-compose", "yml"), ("setup", "py"), (".gitignore", ""),
        ("CHANGELOG", "md"), ("LICENSE", "txt"), ("Makefile", ""),
        ("pyproject", "toml"), (".env", ""), ("pytest", "ini"),
    ]:
        hijos_raiz.append(_crear_archivo(nombre, ext, ruta_raiz))

    for nombre_carpeta, num_archivos, max_nivel in carpetas_raiz:
        carpeta = generar_subcarpeta(nombre_carpeta, ruta_raiz, num_archivos,
                                     nivel=0, max_nivel=max_nivel)
        hijos_raiz.append(carpeta)

    raiz = {
        "nombre": "proyecto_demo",
        "tipo": "carpeta",
        "tamaño": sum(h["tamaño"] for h in hijos_raiz),
        "fecha_modificacion": _fecha_aleatoria(),
        "ruta": ruta_raiz,
        "extension": "",
        "hijos": hijos_raiz
    }

    return raiz


def contar_nodos(nodo: dict) -> int:
    """Cuenta nodos recursivamente en el dict JSON."""
    return 1 + sum(contar_nodos(h) for h in nodo.get("hijos", []))


def guardar_demo(ruta_salida: str = "demo_100nodos.json"):
    """Genera y guarda el JSON de demostración."""
    print("  ⏳ Generando estructura de demo con 100+ nodos...")
    estructura = generar_estructura(120)
    total = contar_nodos(estructura)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(estructura, f, indent=2, ensure_ascii=False)

    carpetas = _contar_tipo(estructura, "carpeta")
    archivos = _contar_tipo(estructura, "archivo")

    print(f"  ✅ Demo generada: {ruta_salida}")
    print(f"     Total nodos : {total}")
    print(f"     Carpetas    : {carpetas}")
    print(f"     Archivos    : {archivos}")
    return ruta_salida


def _contar_tipo(nodo: dict, tipo: str) -> int:
    count = 1 if nodo["tipo"] == tipo else 0
    return count + sum(_contar_tipo(h, tipo) for h in nodo.get("hijos", []))


if __name__ == "__main__":
    guardar_demo()