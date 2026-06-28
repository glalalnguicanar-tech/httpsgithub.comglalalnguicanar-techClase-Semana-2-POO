from modelos.cliente import Cliente
from modelos.producto import Producto
from Servicios.restaurante import Restaurante


def main() -> None:
    restaurante = Restaurante()

    cliente1 = Cliente(
        nombre="Ana",
        apellido="González",
        telefono="555-1234",
        direccion="Calle Falsa 123",
        correo_electronico="ana.gonzalez@example.com",
    )
    cliente2 = Cliente(
        nombre="Luis",
        apellido="Pérez",
        telefono="555-5678",
        direccion="Avenida Siempre Viva 456",
        correo_electronico="luis.perez@example.com",
    )

    producto1 = Producto(
        nombre="Pizza Margarita",
        precio=8.50,
        categoria="Comida",
        stock=10,
        disponible=True,
    )
    producto2 = Producto(
        nombre="Refresco",
        precio=2.00,
        categoria="Bebida",
        stock=25,
        disponible=True,
    )

    restaurante.agregar_cliente(cliente1)
    restaurante.agregar_cliente(cliente2)
    restaurante.agregar_producto(producto1)
    restaurante.agregar_producto(producto2)

    print("Clientes registrados:")
    for cliente in restaurante.listar_clientes():
        print(cliente)

    print("\nProductos registrados:")
    for producto in restaurante.listar_productos():
        print(producto)


if __name__ == "__main__":
    main()
