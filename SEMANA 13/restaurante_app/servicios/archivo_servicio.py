import json
from pathlib import Path


class ArchivoServicio:
	def leer_json(self, ruta):
		with Path(ruta).open("r", encoding="utf-8") as archivo:
			return json.load(archivo)
