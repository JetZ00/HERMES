
import json
from pathlib import Path


def guardar_json(datos, nombre_archivo):
    carpeta = Path("results")
    carpeta.mkdir(exist_ok=True)

    ruta_archivo = carpeta / f"{nombre_archivo}.json"

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
