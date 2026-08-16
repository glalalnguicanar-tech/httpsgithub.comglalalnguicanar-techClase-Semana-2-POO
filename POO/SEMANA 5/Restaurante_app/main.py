"""
Punto de entrada para el sistema de restaurante.

Presenta un menú interactivo que permite registrar/listar/buscar
productos y clientes usando la clase `Restaurante` en `servicios`.
"""

from modelos.cliente import Cliente
from modelos.producto import Producto
from servicios.restaurante import Restaurante


def mostrar_menu() -> None:
    print("=" * 40)
    print("        SISTEMA DE RESTAURANTE")
    print("=" * 40)
    print("1. Registrar producto")
    print("2. Listar productos")
    print("3. Buscar producto")
    print("-" * 40)
    print("4. Registrar cliente")
    print("5. Listar clientes")
    print("6. Buscar cliente")
    print("-" * 40)
    print("7. Salir")


def solicitar_producto() -> Producto:
    # Solicita datos al usuario y construye un Producto
    nombre = input("Nombre del producto: ").strip()
    categoria = input("Categoría: ").strip()
    while True:
        try:
            precio = float(input("Precio: ").strip())
            break
        except ValueError:
            print("Precio inválido. Ingrese un número.")
    disponible_input = input("Disponible (s/n): ").strip().lower()
    disponible = disponible_input.startswith("s")
    return Producto(nombre=nombre, categoria=categoria, precio=precio, disponible=disponible)


def solicitar_cliente() -> Cliente:
    # Solicita datos al usuario y construye un Cliente
    nombre = input("Nombre del cliente: ").strip()
    correo = input("Correo electrónico: ").strip()
    id_cliente = input("ID del cliente: ").strip()
    return Cliente(nombre=nombre, correo=correo, id_cliente=id_cliente)


def main() -> None:
    restaurante = Restaurante()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            try:
                producto = solicitar_producto()
                restaurante.registrar_producto(producto)
                print("Producto registrado correctamente.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "2":
            productos = restaurante.listar_productos()
            if productos:
                for p in productos:
                    print(p.mostrar_informacion())
            else:
                print("No hay productos registrados.")

        elif opcion == "3":
            nombre_buscar = input("Nombre del producto a buscar: ").strip()
            encontrado = restaurante.buscar_producto(nombre_buscar)
            if encontrado:
                print(encontrado.mostrar_informacion())
            else:
                print("Producto no encontrado.")

        elif opcion == "4":
            cliente = solicitar_cliente()
            restaurante.registrar_cliente(cliente)
            print("Cliente registrado correctamente.")

        elif opcion == "5":
            clientes = restaurante.listar_clientes()
            if clientes:
                for c in clientes:
                    print(f"ID: {c.id_cliente} | Nombre: {c.nombre} | Correo: {c.correo}")
            else:
                print("No hay clientes registrados.")

        elif opcion == "6":
            id_buscar = input("ID del cliente a buscar: ").strip()
            cliente = restaurante.buscar_cliente(id_buscar)
            if cliente:
                print(f"ID: {cliente.id_cliente} | Nombre: {cliente.nombre} | Correo: {cliente.correo}")
            else:
                print("Cliente no encontrado.")

        elif opcion == "7":
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
