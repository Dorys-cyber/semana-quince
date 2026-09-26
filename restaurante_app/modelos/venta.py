from datetime import datetime

class Venta:
    def __init__(self, id_venta, usuario_id, producto_id, fecha=None, total=0.0):
        self.id = id_venta
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.total = float(total)

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "producto_id": self.producto_id,
            "fecha": self.fecha,
            "total": self.total
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["usuario_id"],
            data["producto_id"],
            data.get("fecha"),
            data.get("total", 0.0)
        )