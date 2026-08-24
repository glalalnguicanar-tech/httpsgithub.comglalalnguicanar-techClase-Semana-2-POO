from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante


BASE_DIR = Path(__file__).resolve().parent


def pedir_texto(mensaje: str) -> str:
	while True:
		valor = input(mensaje).strip()
		if valor:
			return valor
		print("El valor no puede estar vacío.")


def pedir_entero(mensaje: str, minimo: int | None = None) -> int:
	while True:
		try:
			valor = int(input(mensaje))
			if minimo is not None and valor < minimo:
				print(f"Ingrese un valor mayor o igual que {minimo}.")
				continue
			return valor
		except ValueError:
			print("Ingrese un número entero válido.")


def pedir_precio(mensaje: str) -> float:
	while True:
		try:
			return float(input(mensaje))
		except ValueError:
			print("Ingrese un valor numérico válido.")


def guardar_productos(restaurante: Restaurante, archivos: ArchivoServicio) -> None:
	archivos.guardar_productos(restaurante.listar_productos())


def guardar_usuarios(restaurante: Restaurante, archivos: ArchivoServicio) -> None:
	archivos.guardar_usuarios(restaurante.listar_usuarios())


def registrar_producto(restaurante: Restaurante, archivos: ArchivoServicio) -> None:
	try:
		producto = Producto(
			codigo=pedir_texto("Código: "),
			nombre=pedir_texto("Nombre: "),
			categoria=pedir_texto("Categoría: "),
			precio=pedir_precio("Precio: "),
			stock=pedir_entero("Stock: ", 0),
		)
		restaurante.registrar_producto(producto)
		guardar_productos(restaurante, archivos)
		print("Producto registrado y guardado correctamente.")
	except (ValueError, PermissionError) as error:
		print(f"Error: {error}")


def registrar_usuario(restaurante: Restaurante, archivos: ArchivoServicio) -> None:
	try:
		usuario = Usuario(
			identificacion=pedir_texto("Identificación: "),
			nombre=pedir_texto("Nombre: "),
			correo=pedir_texto("Correo: "),
		)
		restaurante.registrar_usuario(usuario)
		guardar_usuarios(restaurante, archivos)
		print("Usuario registrado y guardado correctamente.")
	except (ValueError, PermissionError) as error:
		print(f"Error: {error}")


def listar_productos(restaurante: Restaurante) -> None:
	productos = restaurante.listar_productos()
	if not productos:
		print("No hay productos registrados.")
		return
	for producto in productos:
		print(producto)


def listar_usuarios(restaurante: Restaurante) -> None:
	usuarios = restaurante.listar_usuarios()
	if not usuarios:
		print("No hay usuarios registrados.")
		return
	for usuario in usuarios:
		print(usuario)


def actualizar_producto(restaurante: Restaurante, archivos: ArchivoServicio) -> None:
	codigo = pedir_texto("Código del producto: ")
	nombre = input("Nuevo nombre (vacío conserva): ").strip() or None
	categoria = input("Nueva categoría (vacío conserva): ").strip() or None
	precio_texto = input("Nuevo precio (vacío conserva): ").strip()
	stock_texto = input("Nuevo stock (vacío conserva): ").strip()
	try:
		precio = float(precio_texto) if precio_texto else None
		stock = int(stock_texto) if stock_texto else None
		if restaurante.actualizar_producto(codigo, nombre, categoria, precio, stock):
			guardar_productos(restaurante, archivos)
			print("Producto actualizado y guardado correctamente.")
		else:
			print("No se encontró el producto.")
	except ValueError as error:
		print(f"Error: {error}")


def eliminar_producto(restaurante: Restaurante, archivos: ArchivoServicio) -> None:
	codigo = pedir_texto("Código del producto: ")
	if restaurante.eliminar_producto(codigo):
		guardar_productos(restaurante, archivos)
		print("Producto eliminado y cambios guardados.")
	else:
		print("No se encontró el producto.")


def vender_producto(restaurante: Restaurante, archivos: ArchivoServicio) -> None:
	codigo = pedir_texto("Código del producto: ")
	identificacion = pedir_texto("Identificación del usuario: ")
	cantidad = pedir_entero("Cantidad: ")
	producto = restaurante.buscar_producto(codigo)
	stock_anterior = producto.stock if producto is not None else None
	if restaurante.vender_producto(codigo, identificacion, cantidad):
		archivos.guardar_productos(restaurante.listar_productos())
		archivos.guardar_ventas(restaurante.listar_ventas())
		print(f"Venta registrada correctamente. Stock disponible: {producto.stock}")
	else:
		print("Venta rechazada: verifique usuario, producto, cantidad y stock.")
		if producto is not None and producto.stock != stock_anterior:
			print("La operación no se guardó porque el stock cambió inesperadamente.")


def consultar_ventas(restaurante: Restaurante) -> None:
	identificacion = pedir_texto("Identificación del usuario: ")
	ventas = restaurante.consultar_ventas_usuario(identificacion)
	if not ventas:
		print("El usuario no tiene ventas registradas.")
		return
	for venta in ventas:
		producto = restaurante.buscar_producto(venta.producto_codigo)
		nombre = producto.nombre if producto is not None else "Producto no disponible"
		print(f"Producto: {venta.producto_codigo} - {nombre} | Cantidad: {venta.cantidad}")


def cargar_datos(restaurante: Restaurante, archivos: ArchivoServicio) -> None:
	try:
		restaurante.cargar_datos(
			archivos.cargar_productos(),
			archivos.cargar_usuarios(),
			archivos.cargar_ventas(),
		)
		print("Datos cargados correctamente.")
	except (FileNotFoundError, json.JSONDecodeError, PermissionError, ValueError) as error:
		print(f"No se pudieron cargar todos los datos: {error}")
		print("El programa iniciará con colecciones vacías.")


def ejecutar_menu(restaurante: Restaurante, archivos: ArchivoServicio) -> None:
	acciones: dict[str, Callable[[], None]] = {
		"1": lambda: registrar_producto(restaurante, archivos),
		"2": lambda: registrar_usuario(restaurante, archivos),
		"3": lambda: listar_productos(restaurante),
		"4": lambda: listar_usuarios(restaurante),
		"5": lambda: actualizar_producto(restaurante, archivos),
		"6": lambda: eliminar_producto(restaurante, archivos),
		"7": lambda: vender_producto(restaurante, archivos),
		"8": lambda: consultar_ventas(restaurante),
		"9": lambda: print("Categorías: " + ", ".join(sorted(restaurante.mostrar_categorias()))),
	}
	while True:
		print("\n=== RESTAURANTE ===")
		print("1. Registrar producto")
		print("2. Registrar usuario")
		print("3. Listar productos")
		print("4. Listar usuarios")
		print("5. Actualizar producto")
		print("6. Eliminar producto")
		print("7. Vender producto")
		print("8. Consultar ventas por usuario")
		print("9. Mostrar categorías")
		print("0. Salir")
		opcion = input("Seleccione una opción: ").strip()
		if opcion == "0":
			print("Hasta pronto.")
			return
		accion = acciones.get(opcion)
		if accion is None:
			print("Opción inválida.")
			continue
		try:
			accion()
		except PermissionError as error:
			print(f"Error de permisos: {error}")


def main() -> None:
	restaurante = Restaurante()
	archivos = ArchivoServicio(BASE_DIR / "datos")
	cargar_datos(restaurante, archivos)
	ejecutar_menu(restaurante, archivos)


if __name__ == "__main__":
	main()
