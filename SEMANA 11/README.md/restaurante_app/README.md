# Restaurante App - Semana 11

Aplicación de consola desarrollada como evolución de Semana 10. Mantiene las colecciones de productos y usuarios e incorpora ventas relacionadas entre ambos objetos.

## Estructura

- `modelos/`: `Producto`, `Usuario` y `Venta`.
- `servicios/restaurante.py`: colecciones, búsquedas, validaciones y reglas de negocio.
- `servicios/archivo_servicio.py`: lectura y escritura JSON en `datos/`.
- `main.py`: menú e interacción por consola.
- `datos/`: `productos.json`, `usuarios.json` y `ventas.json`.

## Operaciones

Se pueden registrar y listar productos y usuarios, vender productos y consultar las ventas filtradas por identificación de usuario. Una venta exige usuario y producto existentes, cantidad positiva y stock suficiente; al confirmarse, reduce el stock.

## Persistencia

Después de registrar productos o usuarios se guarda su colección. Después de una venta se guardan `productos.json` y `ventas.json`. Los tres archivos se cargan al iniciar mediante `json.load()` y se convierten nuevamente en objetos.

## Ejecución

Desde la carpeta `restaurante_app`:

```text
py main.py
```

En el menú, registre un usuario y un producto con stock, venda una cantidad válida y consulte sus ventas. Al reiniciar, los datos se recuperan desde los archivos JSON.