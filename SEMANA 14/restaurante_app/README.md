# Restaurante App - Semana 14

Aplicación gráfica para gestionar usuarios y productos de un restaurante, desarrollada con Tkinter y organizada en módulos por responsabilidad: modelos, servicios, interfaz y punto de entrada.

## Objetivo de la semana

Se mantiene la estructura modular trabajada en semanas anteriores y se mejora la capa visual usando contenedores, formularios, tablas y controles de acción. La lógica del negocio sigue centralizada en `RestauranteServicio`, mientras que la interfaz solo coordina la interacción con el usuario.

## Estructura del proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
├── README.md
└── assets/ (opcional)
```

## Componentes y contenedores utilizados

- `tk.Frame`: contenedores para login y panel principal.
- `ttk.Notebook`: separación de secciones `Usuarios` y `Productos`.
- `tk.Entry`: captura de datos para formulario de productos.
- `ttk.Treeview`: visualización organizada de usuarios y productos.
- `tk.Button`: acciones de registro, consulta, actualización, eliminación y limpieza.

## Operaciones implementadas

- Inicio de sesión con validación por usuario y contraseña.
- Consulta de usuarios desde la interfaz principal.
- Registro de productos con validaciones.
- Consulta de producto por código.
- Actualización de nombre, categoría, precio y cantidad.
- Eliminación por código.
- Persistencia de los cambios en `datos/productos.json` mediante el servicio.

## Persistencia

Los datos se mantienen en archivos JSON, y la lectura/escritura se realiza a través de `ArchivoServicio` y `RestauranteServicio`, evitando que la vista manipule directamente los archivos.

## Ejecución

Desde la carpeta del proyecto, ejecuta:

```bash
py main.py
```

o en algunos sistemas:

```bash
python main.py
```

Se abrirá la ventana de login. Con las credenciales por defecto:

- Usuario: `admin`
- Contraseña: `1234`

Luego podrás ingresar al panel principal y gestionar productos.

## Mejoras realizadas

- Se conserva el flujo previo de login y acceso.
- La interfaz principal se organiza con secciones claras para usuarios y productos.
- Los productos cuentan con un formulario ordenado y una tabla de listado.
- Las operaciones se manejan desde la lógica del servicio y no desde botones aislados.
- La información se actualiza visualmente después de cada operación.
