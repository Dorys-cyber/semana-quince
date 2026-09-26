import os
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:  # <--- Revisa que coincida exactamente (mayúsculas y minúsculas)
    def __init__(self):
        self.base_dir = os.path.join(os.path.dirname(__file__), '..', 'datos')
        self.ruta_productos = os.path.join(self.base_dir, 'productos.json')
        self.ruta_usuarios = os.path.join(self.base_dir, 'usuarios.json')
        self.ruta_ventas = os.path.join(self.base_dir, 'ventas.json')

    def obtener_productos(self):
        datos = ArchivoServicio.leer_json(self.ruta_productos)
        return [Producto.from_dict(d) for d in datos]

    def obtener_usuarios(self):
        datos = ArchivoServicio.leer_json(self.ruta_usuarios)
        return [Usuario.from_dict(d) for d in datos]

    def obtener_ventas(self):
        datos = ArchivoServicio.leer_json(self.ruta_ventas)
        return [Venta.from_dict(d) for d in datos]

    def autenticar_usuario(self, username, password):
        usuarios = self.obtener_usuarios()
        for u in usuarios:
            if u.username == username and u.password == password:
                return u
        return None

    def registrar_venta(self, id_usuario, id_producto):
        if not id_usuario or not id_producto:
            return False, "Debe seleccionar un usuario y un producto válidos."

        usuarios = self.obtener_usuarios()
        productos = self.obtener_productos()

        usuario_existe = any(u.id == id_usuario for u in usuarios)
        producto = next((p for p in productos if p.id == id_producto), None)

        if not usuario_existe:
            return False, "El usuario seleccionado no existe."
        if not producto:
            return False, "El producto seleccionado no existe."

        ventas = self.obtener_ventas()
        nuevo_id = f"V{len(ventas) + 1:03d}"
        
        nueva_venta = Venta(
            id_venta=nuevo_id,
            usuario_id=id_usuario,
            producto_id=id_producto,
            total=producto.precio
        )

        ventas.append(nueva_venta)
        datos_guardar = [v.to_dict() for v in ventas]
        ArchivoServicio.guardar_json(self.ruta_ventas, datos_guardar)

        return True, f"Venta {nuevo_id} registrada con éxito por ${producto.precio:.2f}."