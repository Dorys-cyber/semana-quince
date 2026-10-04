import os
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
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

    # ================= MÉTODOS DE USUARIOS =================
    def registrar_usuario(self, uid, nombre, username, password, rol):
        usuarios = self.obtener_usuarios()
        if any(u.id == uid for u in usuarios):
            return False, f"El identificador {uid} ya está registrado."
        
        # Conectado correctamente con id_usuario que exige tu modelo Usuario
        nuevo_usuario = Usuario(id_usuario=uid, nombre=nombre, username=username, password=password, rol=rol)
        usuarios.append(nuevo_usuario)
        datos = [u.to_dict() for u in usuarios]
        ArchivoServicio.guardar_json(self.ruta_usuarios, datos)
        return True, "Usuario registrado exitosamente."

    def actualizar_usuario(self, uid, nombre, username, password, rol):
        usuarios = self.obtener_usuarios()
        encontrado = False
        for u in usuarios:
            if u.id == uid:
                u.nombre = nombre
                u.username = username
                if password:  
                    u.password = password
                u.rol = rol
                encontrado = True
                break
        
        if not encontrado:
            return False, f"No se encontró el usuario con ID {uid}."
        
        datos = [u.to_dict() for u in usuarios]
        ArchivoServicio.guardar_json(self.ruta_usuarios, datos)
        return True, "Usuario actualizado exitosamente."

    def eliminar_usuario(self, uid):
        usuarios = self.obtener_usuarios()
        nuevos_usuarios = [u for u in usuarios if u.id != uid]
        
        if len(nuevos_usuarios) == len(usuarios):
            return False, f"No se encontró el usuario con ID {uid}."
        
        datos = [u.to_dict() for u in nuevos_usuarios]
        ArchivoServicio.guardar_json(self.ruta_usuarios, datos)
        return True, "Usuario eliminado exitosamente."

    # ================= MÉTODOS DE PRODUCTOS =================
    def buscar_producto_por_id(self, pid):
        productos = self.obtener_productos()
        for p in productos:
            if p.id == pid:
                return p
        return None

    def registrar_producto(self, pid, nombre, precio, categoria):
        productos = self.obtener_productos()
        if any(p.id == pid for p in productos):
            return False, f"El código de producto {pid} ya existe."
        
        # Conectado correctamente con id_producto que exige tu modelo Producto
        nuevo_producto = Producto(id_producto=pid, nombre=nombre, precio=precio, categoria=categoria)
        productos.append(nuevo_producto)
        datos = [p.to_dict() for p in productos]
        ArchivoServicio.guardar_json(self.ruta_productos, datos)
        return True, "Producto registrado exitosamente."

    def actualizar_producto(self, pid, nombre, precio, categoria):
        productos = self.obtener_productos()
        encontrado = False
        for p in productos:
            if p.id == pid:
                p.nombre = nombre
                p.precio = precio
                p.categoria = categoria
                encontrado = True
                break
        
        if not encontrado:
            return False, f"No se encontró el producto con código {pid}."
        
        datos = [p.to_dict() for p in productos]
        ArchivoServicio.guardar_json(self.ruta_productos, datos)
        return True, "Producto actualizado exitosamente."

    def eliminar_producto(self, pid):
        productos = self.obtener_productos()
        nuevos_productos = [p for p in productos if p.id != pid]
        
        if len(nuevos_productos) == len(productos):
            return False, f"No se encontró el producto con código {pid}."
        
        datos = [p.to_dict() for p in nuevos_productos]
        ArchivoServicio.guardar_json(self.ruta_productos, datos)
        return True, "Producto eliminado exitosamente."

    # ================= MÉTODOS DE VENTAS =================
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