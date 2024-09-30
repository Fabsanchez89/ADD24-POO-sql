''' Desafío 1: Sistema de Gestión de Productos
Objetivo: Desarrollar un sistema para manejar productos en un inventario.

Requisitos:
    *Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
    *Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
    *Implementar operaciones CRUD para gestionar productos del inventario.
    *Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
    *Persistir los datos en archivo JSON.
'''
import json

class Producto:
    def __init__(self, id, nombre, categoria, precio, stock):
        self.__id = self.validar_id(id)
        self.__nombre = nombre
        self.__categoria = categoria
        self.__precio = self.validar_precio(precio)
        self.__stock = self.validar_stock(stock)

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre.capitalize()
    
    @property
    def categoria(self):
        return self.__categoria.capitalize()
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def stock(self):
        return self.__stock

    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)
    
    @stock.setter
    def stock(self, nuevo_stock):
        self.__stock = self.validar_stock(nuevo_stock)

    def validar_id(self, id):
        if not isinstance(id, int):
            raise ValueError("El ID debe ser un número entero")
        return id

    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num < 0:
                raise ValueError("El precio debe ser un número positivo")
            return precio_num
        except ValueError:
            raise ValueError("El precio debe ser un número válido")

    def validar_stock(self, stock):
        try:
            stock_num = int(stock)
            if stock_num < 0:
                raise ValueError("El stock no puede ser negativo")
            return stock_num
        except ValueError:
            raise ValueError("El stock debe ser numérico")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock
        }

    def __str__(self):
        return f"{self.nombre} {self.categoria}"
    
class ProductoOriginal(Producto):
    def __init__(self, id, nombre, categoria, precio, stock, estado):
        super().__init__(id, nombre, categoria, precio, stock)
        self.__estado = estado

    @property
    def estado(self):
        return self.__estado
    
    def to_dict(self):
        data = super().to_dict()
        data['estado'] = self.estado
        return data
    
    def __str__(self):
        return f'{super().__str__()} - Estado: {self.estado}'
 
class ProductoNoOriginal(Producto):
    def __init__(self, id, nombre, categoria, precio, stock, origen):
        super().__init__(id, nombre, categoria, precio, stock)
        self.__origen = origen

    @property
    def origen(self):
        return self.__origen

    def to_dict(self):
        data = super().to_dict()
        data["origen"] = self.origen
        return data
    
    def __str__(self):
        return f"{super().__str__()} - Origen: {self.origen}"
    
class GestionProductos:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_producto(self, producto):
        try:
            datos = self.leer_datos()
            id = producto.id
            if str(id) not in datos.keys():
                datos[id] = producto.to_dict()
                self.guardar_datos(datos)
                print('Guardado exitoso')
            else:
                print(f'Producto con id {id} ya existe')
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')

    def leer_producto(self, id):
        datos = self.leer_datos()
        return datos.get(str(id), None)

    def actualizar_producto(self, id, nuevo_precio):
        datos = self.leer_datos()
        if str(id) in datos:
            datos[str(id)]['precio'] = nuevo_precio
            self.guardar_datos(datos)
            print('Actualización exitosa')
        else:
            print(f'Producto con id {id} no encontrado')

    def eliminar_producto(self, id):
        datos = self.leer_datos()
        if str(id) in datos:
            del datos[str(id)]
            self.guardar_datos(datos)
            print('Eliminación exitosa')
        else:
            print(f'Producto con id {id} no encontrado')




            

        