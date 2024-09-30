''' Desafío 1: Sistema de Gestión de Productos
Objetivo: Desarrollar un sistema para manejar productos en un inventario.

Requisitos:
    *Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
    *Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
    *Implementar operaciones CRUD para gestionar productos del inventario.
    *Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
    *Persistir los datos en archivo JSON.
'''

import mysql.connector
from mysql.connector import Error
from decouple import config
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
    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.port = config('DB_PORT')
    
    def connect(self): 
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password, 
                port=self.port
            )
            if connection.is_connected(): 
                return connection            
        
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

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
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Verificar si el producto ya existe
                    cursor.execute('SELECT id FROM productos WHERE id = %s', (producto.id,))
                    if cursor.fetchone():
                        print(f'Error: ya existe producto con ID {producto.id}')
                        return
                    
                    # Verificación de valores
                    print(f"Producto ID: {producto.id}")
                    print(f"Nombre: {producto.nombre}")
                    print(f"Categoría: {producto.categoria}")
                    print(f"Precio: {producto.precio}")
                    print(f"Stock: {producto.stock}")

                    # Inserción en la tabla productos
                    query_productos = '''INSERT INTO productos (id, nombre, categoria, precio, stock) 
                     VALUES (%s, %s, %s, %s, %s)'''
                    cursor.execute(query_productos, (producto.id, producto.nombre, producto.categoria, producto.precio, producto.stock))

                    if isinstance(producto, ProductoOriginal):
                        query_original = '''INSERT INTO ProductoOriginal (id, estado)
                                            VALUES (%s, %s)'''
                        cursor.execute(query_original, (producto.id, producto.estado))
                    elif isinstance(producto, ProductoNoOriginal):
                        query_no_original = '''INSERT INTO ProductoNoOriginal (id, origen)
                                            VALUES (%s, %s)'''
                        cursor.execute(query_no_original, (producto.id, producto.origen))


                # Confirmar los cambios
                connection.commit()
                print(f'Producto {producto.id} se ha guardado correctamente')

        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')
            if connection:
                connection.rollback()
        finally:
            if connection and connection.is_connected():
                connection.close()



    def leer_producto(self, id):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM productos WHERE id = %s', (id,))
                    producto_data = cursor.fetchone()

                    if producto_data:
                        cursor.execute('SELECT estado FROM ProductoOriginal WHERE id = %s', (id,))
                        estado = cursor.fetchone()
                    
                        if estado:
                            producto_data['estado'] = estado['estado']
                            producto = ProductoOriginal(**producto_data)
                        else:
                            cursor.execute('SELECT origen FROM ProductoNoOriginal WHERE id = %s', (id,))
                            origen = cursor.fetchone()
                            if origen:
                                producto_data['origen'] = origen['origen']
                                producto = ProductoNoOriginal(**producto_data)
                            else:
                                producto = Producto(**producto_data)
                        return producto
                    else:
                        print(f'No se encontró el producto con el ID {id}.')
                        return None
        except Error as e:
            print(f'Error al leer el producto: {e}')
        finally:
            if connection and connection.is_connected():
                connection.close()

    def actualizar_producto(self, id, nuevo_precio):
        try:
            connection = self.connect()
            if connection: 
                with connection.cursor() as cursor:
                    #verificar si el id existe
                    cursor.execute('select * from productos where id = %s', (id,))
                    if not cursor.fetchone():
                        print(f'No se encontro producto con Id {id}.')
                        return
                    
                    #Actualizar precio
                    cursor.execute('UPDATE productos SET precio = %s WHERE id = %s', (nuevo_precio, id))
                    
                    if cursor.rowcount >0:
                        connection.commit()
                        print(f'Precio actualizado para el producto con id: {id}')
                    else:
                        print(f'no se encontró el producto con id: {id}')

        except Exception as e:
            print(f'Error al actualizar el producto: {e}')

        finally:
            if connection.is_connected():
                connection.close()

    def eliminar_producto(self, id):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    #verificar si el id existe
                    cursor.execute('select * from productos where id = %s', (id,))
                    if not cursor.fetchone():
                        print(f'No se encontro producto con Id {id}.')
                        return
                    
                    #Eliminar el producto
                    cursor.execute('DELETE from productooriginal where id = %s', (id,))
                    cursor.execute('DELETE from productonooriginal where id = %s', (id,))
                    cursor.execute('DELETE from productos where id = %s', (id,))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'Producto con id: {id} eliminado correctamente')
                    else:
                        print(f'No se encontro producto con id: {id}')

        except Exception as e:
            print(f'Error al actualizar el producto: {e}')

        finally:
            if connection.is_connected():
                connection.close()

    def leer_todos_los_productos(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM productos')
                    productos_data = cursor.fetchall()  # Esta variable es productos_data

                    productos = []
                    for producto_data in productos_data:  # Usar productos_data aquí
                        id = producto_data['id']

                        cursor.execute('SELECT estado from productooriginal WHERE id = %s', (id,))
                        estado = cursor.fetchone()

                        if estado:
                            producto_data['estado'] = estado['estado']
                            producto = ProductoOriginal(**producto_data)
                        else:
                            cursor.execute('SELECT origen from productonooriginal WHERE id = %s', (id,))
                            origen = cursor.fetchone()
                            if origen:  # Verificar si se encontró el origen
                                producto_data['origen'] = origen['origen']
                                producto = ProductoNoOriginal(**producto_data)
                            else:
                                producto = Producto(**producto_data)

                        productos.append(producto)

        except Exception as e:
            print(f'Error al mostrar todos los productos: {e}')

        else:
            return productos

        finally:
            if connection.is_connected():
                connection.close()
