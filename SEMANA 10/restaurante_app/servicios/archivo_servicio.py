from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from modelos.producto import Producto


class ArchivoServicio:
    """Servicio responsable de cargar y guardar productos en un archivo JSON."""

    def __init__(self, ruta_archivo: str | Path) -> None:
        """
        Inicializa el servicio de archivo.

        Args:
            ruta_archivo: Ruta al archivo JSON de productos.
        """
        self.ruta_archivo = Path(ruta_archivo)
        # Crear el directorio si no existe
        self.ruta_archivo.parent.mkdir(parents=True, exist_ok=True)

    def cargar_productos(self) -> list[Producto]:
        """
        Carga los productos desde el archivo JSON.

        Retorna:
            Lista de objetos Producto cargados desde el archivo.

        Excepciones:
            - FileNotFoundError: Si el archivo no existe (primer inicio).
            - json.JSONDecodeError: Si el contenido no es JSON válido.
            - PermissionError: Si no hay permisos para leer el archivo.
            - ValueError: Si un registro tiene datos inválidos.
        """
        productos: list[Producto] = []

        # Si el archivo no existe, retornar lista vacía (primer inicio)
        if not self.ruta_archivo.exists():
            return productos

        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            # Validar que sea una lista
            if not isinstance(datos, list):
                raise ValueError("El archivo JSON debe contener una lista de productos.")

            # Reconstruir cada producto desde su diccionario
            for indice, registro in enumerate(datos):
                try:
                    producto = Producto.from_dict(registro)
                    productos.append(producto)
                except ValueError as e:
                    print(f"Advertencia: No se pudo cargar el registro {indice}: {e}")
                    continue

        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"El archivo JSON no tiene un formato válido: {e.msg}",
                e.doc,
                e.pos,
            )
        except PermissionError:
            raise PermissionError(
                f"No hay permisos para leer el archivo: {self.ruta_archivo}"
            )

        return productos

    def guardar_productos(self, productos: list[Producto]) -> bool:
        """
        Guarda la lista de productos en el archivo JSON.

        Args:
            productos: Lista de objetos Producto a guardar.

        Retorna:
            True si el guardado fue exitoso.

        Excepciones:
            - PermissionError: Si no hay permisos para escribir el archivo.
            - ValueError: Si hay un error al convertir productos a diccionarios.
        """
        try:
            # Convertir productos a diccionarios
            datos: list[dict[str, Any]] = [producto.to_dict() for producto in productos]

            # Guardar en archivo con codificación UTF-8
            with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)

            return True

        except PermissionError:
            raise PermissionError(
                f"No hay permisos para escribir en el archivo: {self.ruta_archivo}"
            )
        except (ValueError, TypeError) as e:
            raise ValueError(f"Error al guardar productos: {e}")
