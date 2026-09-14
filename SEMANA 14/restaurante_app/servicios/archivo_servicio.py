import json
from pathlib import Path


class ArchivoServicio:
    def leer_json(self, ruta):
        path = Path(ruta)
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return datos if isinstance(datos, list) else []

    def guardar_json(self, ruta, datos):
        path = Path(ruta)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
