class Producto:
    def __init__(self, id_producto, nombre, precio, categoria):
        self.id = id_producto
        self.nombre = nombre
        self.precio = float(precio)
        self.categoria = categoria

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["nombre"], data["precio"], data["categoria"])