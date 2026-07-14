from modelos.bebida import Bebida
from modelos.cliente import Cliente
from modelos.producto import Producto
from servicios.restaurante import Restaurante


def mostrar_menu() -> None:
    print("========================================")
    print("        SISTEMA DE RESTAURANTE")
    print("========================================")
    print("1. Registrar producto")
    print("2. Registrar bebida")
    print("3. Registrar cliente")
    print("----------------------------------------")
    print("4. Listar productos")
    print("5. Listar clientes")
    print("----------------------------------------")
    print("6. Salir")


def solicitar_texto(mensaje: str) -> str:
    return input(f"{mensaje}: ").strip()


def solicitar_precio(mensaje: str) -> float:
    while True:
        valor = input(f"{mensaje}: ").strip()
        try:
            precio = float(valor)
            if precio < 0:
                print("El precio no puede ser negativo. Intente nuevamente.")
                continue
            return precio
        except ValueError:
            print("Debe ingresar un número válido para el precio.")


def registrar_producto(restaurante: Restaurante) -> None:
    print("\n-- Registro de producto --")
    codigo = solicitar_texto("Ingrese el código")
    nombre = solicitar_texto("Ingrese el nombre")
    categoria = solicitar_texto("Ingrese la categoría")
    precio = solicitar_precio("Ingrese el precio")
    producto = Producto(codigo=codigo, nombre=nombre, categoria=categoria, precio=precio)

    if restaurante.registrar_producto(producto):
        print("Producto registrado correctamente.\n")
    else:
        print("Error: ya existe un producto con ese código.\n")


def registrar_bebida(restaurante: Restaurante) -> None:
    print("\n-- Registro de bebida --")
    codigo = solicitar_texto("Ingrese el código")
    nombre = solicitar_texto("Ingrese el nombre")
    categoria = solicitar_texto("Ingrese la categoría")
    precio = solicitar_precio("Ingrese el precio")
    tamano = solicitar_texto("Ingrese el tamaño")
    envase = solicitar_texto("Ingrese el tipo de envase")
    bebida = Bebida(
        codigo=codigo,
        nombre=nombre,
        categoria=categoria,
        precio=precio,
        tamano=tamano,
        envase=envase,
    )

    if restaurante.registrar_producto(bebida):
        print("Bebida registrada correctamente.\n")
    else:
        print("Error: ya existe un producto con ese código.\n")


def registrar_cliente(restaurante: Restaurante) -> None:
    print("\n-- Registro de cliente --")
    identificacion = solicitar_texto("Ingrese la identificación")
    nombre = solicitar_texto("Ingrese el nombre")
    correo = solicitar_texto("Ingrese el correo")
    cliente = Cliente(identificacion=identificacion, nombre=nombre, correo=correo)

    if restaurante.registrar_cliente(cliente):
        print("Cliente registrado correctamente.\n")
    else:
        print("Error: ya existe un cliente con esa identificación.\n")


def listar_productos(restaurante: Restaurante) -> None:
    print("\n-- Lista de productos --")
    productos = restaurante.listar_productos()
    if not productos:
        print("No hay productos registrados.\n")
        return
    for producto_info in productos:
        print(producto_info)
    print()


def listar_clientes(restaurante: Restaurante) -> None:
    print("\n-- Lista de clientes --")
    clientes = restaurante.listar_clientes()
    if not clientes:
        print("No hay clientes registrados.\n")
        return
    for cliente_info in clientes:
        print(cliente_info)
    print()


def main() -> None:
    restaurante = Restaurante()

    while True:
        mostrar_menu()
        opcion = solicitar_texto("Seleccione una opción")

        if opcion == "1":
            registrar_producto(restaurante)
        elif opcion == "2":
            registrar_bebida(restaurante)
        elif opcion == "3":
            registrar_cliente(restaurante)
        elif opcion == "4":
            listar_productos(restaurante)
        elif opcion == "5":
            listar_clientes(restaurante)
        elif opcion == "6":
            print("Saliendo del sistema. Hasta luego.")
            break
        else:
            print("Opción incorrecta. Por favor seleccione una opción válida.\n")


if __name__ == "__main__":
    main()
