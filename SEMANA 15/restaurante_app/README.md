# Restaurante App - Semana 15

Aplicación de escritorio para gestionar usuarios, productos y ventas de un restaurante con Tkinter. Esta semana conserva la arquitectura de las semanas anteriores y agrega una operación de venta enfocada en el manejo básico de eventos.

## Flujo de eventos

En la pestaña **Ventas**, el usuario selecciona un usuario y un producto en controles `ttk.Combobox`. Al pulsar **Registrar venta**, el botón usa `command=self.registrar_venta` para ejecutar el callback. El callback obtiene las selecciones, delega la validación y el registro a `RestauranteServicio`, y luego actualiza la tabla y muestra el resultado.

```text
acción del usuario -> command= -> callback -> RestauranteServicio -> ventas.json -> tabla y mensaje
```

La interfaz no abre ni modifica archivos JSON directamente. `ArchivoServicio` concentra la lectura y escritura, mientras que `RestauranteServicio` valida usuarios, productos y ventas.

## Estructura

```text
restaurante_app/
├── assets/
│   ├── restaurante_logo.svg
│   └── ventas_icon.svg
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── login_view.py
│   └── main_view.py
└── main.py
```

## Funcionalidades

- Inicio de sesión y cierre de sesión.
- Consulta de usuarios.
- Registro, consulta, actualización y eliminación de productos.
- Selección de usuario y producto mediante `ttk.Combobox`.
- Registro y consulta visual de ventas mediante `ttk.Treeview`.
- Persistencia de ventas en `datos/ventas.json`.
- Identidad visual con recursos de `assets/`.

## Ejecución

Desde `SEMANA 15/restaurante_app`:

```bash
py main.py
```

Credenciales iniciales: `admin` / `1234`.
