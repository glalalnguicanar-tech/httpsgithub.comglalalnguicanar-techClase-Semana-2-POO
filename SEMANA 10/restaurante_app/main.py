from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante


# Ruta del archivo de persistencia de productos
RUTA_PRODUCTOS = Path("datos") / "productos.json"


def pedir_texto(mensaje: str) -> str:
    """Solicita texto no vacío al usuario."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El valor no puede estar vacío.")


def pedir_precio(mensaje: str) -> float:
    """Solicita un precio válido al usuario."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Ingrese un valor numérico válido para el precio.")


def mostrar_menu(restaurante: Restaurante) -> None:
    """Muestra el menú principal del sistema."""
    print("\n========================================")
    print("        SISTEMA DE RESTAURANTE")
    print("========================================")
    for opcion in restaurante.opciones_menu:
        print(opcion)
    print("----------------------------------------")


def registrar_producto_desde_consola(
    restaurante: Restaurante, archivo_servicio: ArchivoServicio
) -> None:
    """Registra un nuevo producto desde la consola y lo persiste."""
    try:
        codigo = pedir_texto("Código del producto: ")
        nombre = pedir_texto("Nombre del producto: ")
        categoria = pedir_texto("Categoría del producto: ")
        precio = pedir_precio("Precio del producto: ")
        producto = Producto(codigo=codigo, nombre=nombre, categoria=categoria, precio=precio)
        restaurante.registrar_producto(producto)
        print("Producto registrado correctamente.")
        # Guardar en archivo después de registrar
        archivo_servicio.guardar_productos(restaurante.listar_productos())
        print("✓ Producto guardado en archivo.")
    except ValueError as error:
        print(f"Error: {error}")
    except PermissionError as error:
        print(f"Error de permisos: {error}")


def buscar_producto_desde_consola(restaurante: Restaurante) -> None:
    """Busca un producto por código."""
    codigo = pedir_texto("Ingrese el código del producto a buscar: ")
    producto = restaurante.buscar_producto(codigo)
    if producto is None:
        print("No se encontró un producto con ese código.")
    else:
        print(producto)


def actualizar_producto_desde_consola(
    restaurante: Restaurante, archivo_servicio: ArchivoServicio
) -> None:
    """Actualiza un producto existente y lo persiste."""
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

    try:
        actualizado = restaurante.actualizar_producto(
            codigo=codigo,
            nombre=nombre or None,
            categoria=categoria or None,
            precio=precio,
        )

        if actualizado:
            print("Producto actualizado correctamente.")
            # Guardar en archivo después de actualizar
            archivo_servicio.guardar_productos(restaurante.listar_productos())
            print("✓ Cambios guardados en archivo.")
        else:
            print("No se encontró un producto con ese código.")
    except ValueError as error:
        print(f"Error: {error}")
    except PermissionError as error:
        print(f"Error de permisos: {error}")


def eliminar_producto_desde_consola(
    restaurante: Restaurante, archivo_servicio: ArchivoServicio
) -> None:
    """Elimina un producto y actualiza la persistencia."""
    codigo = pedir_texto("Ingrese el código del producto a eliminar: ")
    eliminado = restaurante.eliminar_producto(codigo)
    if eliminado:
        print("Producto eliminado correctamente.")
        # Guardar en archivo después de eliminar
        archivo_servicio.guardar_productos(restaurante.listar_productos())
        print("✓ Cambios guardados en archivo.")
    else:
        print("No se encontró un producto con ese código.")


def listar_productos_desde_consola(restaurante: Restaurante) -> None:
    """Lista todos los productos registrados."""
    productos = restaurante.listar_productos()
    if not productos:
        print("No hay productos registrados.")
        return

    print("\n--- PRODUCTOS REGISTRADOS ---")
    for producto in productos:
        print(producto)
    print(f"Total de productos: {len(productos)}\n")


def registrar_usuario_desde_consola(restaurante: Restaurante) -> None:
    """Registra un nuevo usuario."""
    try:
        identificacion = pedir_texto("Identificación del usuario: ")
        nombre = pedir_texto("Nombre del usuario: ")
        correo = pedir_texto("Correo del usuario: ")
        usuario = Usuario(identificacion=identificacion, nombre=nombre, correo=correo)
        restaurante.registrar_usuario(usuario)
        print("Usuario registrado correctamente.")
    except ValueError as error:
        print(f"Error: {error}")


def listar_usuarios_desde_consola(restaurante: Restaurante) -> None:
    """Lista todos los usuarios registrados."""
    usuarios = restaurante.listar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return

    print("\n--- USUARIOS REGISTRADOS ---")
    for usuario in usuarios:
        print(usuario)
    print(f"Total de usuarios: {len(usuarios)}\n")


def mostrar_categorias_desde_consola(restaurante: Restaurante) -> None:
    """Muestra todas las categorías de productos."""
    categorias = restaurante.mostrar_categorias()
    if not categorias:
        print("No hay categorías registradas.")
        return

    print("\n--- CATEGORÍAS DE PRODUCTOS ---")
    for categoria in sorted(categorias):
        print(f"  - {categoria}")
    print()


def cargar_productos_iniciales(
    restaurante: Restaurante, archivo_servicio: ArchivoServicio
) -> None:
    """Carga los productos almacenados al iniciar la aplicación."""
    try:
        productos = archivo_servicio.cargar_productos()
        restaurante.cargar_productos_iniciales(productos)
        if productos:
            print(f"✓ Se cargaron {len(productos)} producto(s) desde el archivo.")
        else:
            print("El archivo de productos está vacío o es la primera ejecución.")
    except FileNotFoundError:
        print("Primer inicio: no existe archivo de productos. Se creará al registrar.")
    except json.JSONDecodeError as error:
        print(f"Error: El archivo JSON no es válido: {error}")
        print("Se iniciará con una colección vacía.")
    except PermissionError as error:
        print(f"Error de permisos al leer el archivo: {error}")
        print("Se iniciará con una colección vacía.")


def ejecutar_menu_principal(
    restaurante: Restaurante, archivo_servicio: ArchivoServicio
) -> None:
    """Ejecuta el bucle principal del menú."""
    opciones: dict[str, Callable[[], None]] = {
        "1": lambda: registrar_producto_desde_consola(restaurante, archivo_servicio),
        "2": lambda: buscar_producto_desde_consola(restaurante),
        "3": lambda: actualizar_producto_desde_consola(restaurante, archivo_servicio),
        "4": lambda: eliminar_producto_desde_consola(restaurante, archivo_servicio),
        "5": lambda: listar_productos_desde_consola(restaurante),
        "6": lambda: registrar_usuario_desde_consola(restaurante),
        "7": lambda: listar_usuarios_desde_consola(restaurante),
        "8": lambda: mostrar_categorias_desde_consola(restaurante),
    }

    while True:
        mostrar_menu(restaurante)
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "9":
            print("¡Gracias por usar el sistema!")
            break

        if opcion in opciones:
            opciones[opcion]()
        else:
            print("Opción inválida. Por favor, seleccione una opción del menú.")


def main() -> None:
    """Punto de entrada principal de la aplicación."""
    print("========================================")
    print("   BIENVENIDO AL SISTEMA RESTAURANTE")
    print("========================================\n")

    # Crear servicios
    restaurante = Restaurante()
    archivo_servicio = ArchivoServicio(RUTA_PRODUCTOS)

    # Cargar productos almacenados
    cargar_productos_iniciales(restaurante, archivo_servicio)

    # Ejecutar menú principal
    ejecutar_menu_principal(restaurante, archivo_servicio)


if __name__ == "__main__":
    main()
