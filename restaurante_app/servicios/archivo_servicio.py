import json
import os

class ArchivoServicio:
    @staticmethod
    def leer_json(ruta_archivo):
        if not os.path.exists(ruta_archivo):
            return []
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except Exception:
            return []

    @staticmethod
    def guardar_json(ruta_archivo, datos):
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)