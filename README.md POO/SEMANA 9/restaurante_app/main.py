from __future__ import annotations

from typing import Callable

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante import Restaurante


def pedir_texto(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El valor no puede estar vacío.")


def pedir_precio(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Ingrese un valor numérico válido para el precio.")


def mostrar_menu(restaurante: Restaurante) -> None:
    print("\n========================================")
    print("        SISTEMA DE RESTAURANTE")
    print("========================================")
    for opcion in restaurante.opciones_menu:
        print(opcion)
    print("----------------------------------------")


def registrar_producto_desde_consola(restaurante: Restaurante) -> None:
    try:
        codigo = pedir_texto("Código del producto: ")
        nombre = pedir_texto("Nombre del producto: ")
        categoria = pedir_texto("Categoría del producto: ")
        precio = pedir_precio("Precio del producto: ")
        producto = Producto(codigo=codigo, nombre=nombre, categoria=categoria, precio=precio)
        restaurante.registrar_producto(producto)
        print("Producto registrado correctamente.")
    except ValueError as error:
        print(f"Error: {error}")


def buscar_producto_desde_consola(restaurante: Restaurante) -> None:
    codigo = pedir_texto("Ingrese el código del producto a buscar: ")
    producto = restaurante.buscar_producto(codigo)
    if producto is None:
        print("No se encontró un producto con ese código.")
    else:
        print(producto)


def actualizar_producto_desde_consola(restaurante: Restaurante) -> None:
    codigo = pedir_texto("Ingrese el código del producto a actualizar: ")
    nombre = input("Nuevo nombre (deje en blanco para conservarlo): ").strip()
    categoria = input("Nueva categoría (deje en blanco para conservarla): ").strip()
    precio_texto = input("Nuevo precio (deje en blanco para conservarlo): ").strip()

    precio: float | None = None
    if precio_texto:
        try:
            precio = float(precio_texto)
        except ValueError:
            print("Precio inválido. La actualización no se realizó.")
            return

    actualizado = restaurante.actualizar_producto(
        codigo=codigo,
        nombre=nombre or None,
        categoria=categoria or None,
        precio=precio,
    )

    if actualizado:
        print("Producto actualizado correctamente.")
    else:
        print("No se encontró un producto con ese código.")


def eliminar_producto_desde_consola(restaurante: Restaurante) -> None:
    codigo = pedir_texto("Ingrese el código del producto a eliminar: ")
    eliminado = restaurante.eliminar_producto(codigo)
    if eliminado:
        print("Producto eliminado correctamente.")
    else:
        print("No se encontró un producto con ese código.")


def listar_productos_desde_consola(restaurante: Restaurante) -> None:
    productos = restaurante.listar_productos()
    if not productos:
        print("No hay productos registrados.")
        return

    for producto in productos:
        print(producto)


def registrar_usuario_desde_consola(restaurante: Restaurante) -> None:
    try:
        identificacion = pedir_texto("Identificación del usuario: ")
        nombre = pedir_texto("Nombre del usuario: ")
        correo = pedir_texto("Correo del usuario: ")
        usuario = Usuario(
            identificacion=identificacion,
            nombre=nombre,
            correo=correo,
        )
        restaurante.registrar_usuario(usuario)
        print("Usuario registrado correctamente.")
    except ValueError as error:
        print(f"Error: {error}")


def listar_usuarios_desde_consola(restaurante: Restaurante) -> None:
    usuarios = restaurante.listar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return

    for usuario in usuarios:
        print(usuario)


def mostrar_categorias_desde_consola(restaurante: Restaurante) -> None:
    categorias = restaurante.mostrar_categorias()
    if not categorias:
        print("No hay categorías registradas.")
        return

    print("Categorías registradas:")
    for categoria in sorted(categorias):
        print(f"- {categoria}")


def main() -> None:
    restaurante = Restaurante()
    acciones: dict[str, Callable[[], None]] = {
        "1": lambda: registrar_producto_desde_consola(restaurante),
        "2": lambda: buscar_producto_desde_consola(restaurante),
        "3": lambda: actualizar_producto_desde_consola(restaurante),
        "4": lambda: eliminar_producto_desde_consola(restaurante),
        "5": lambda: listar_productos_desde_consola(restaurante),
        "6": lambda: registrar_usuario_desde_consola(restaurante),
        "7": lambda: listar_usuarios_desde_consola(restaurante),
        "8": lambda: mostrar_categorias_desde_consola(restaurante),
    }

    while True:
        mostrar_menu(restaurante)
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "9":
            print("Gracias por usar el sistema.")
            break

        accion = acciones.get(opcion)
        if accion is None:
            print("Opción no válida. Intente nuevamente.")
            continue

        accion()


if __name__ == "__main__":
    main()
