from laboratorio2 import ProductoOriginal, ProductoNoOriginal, GestionProductos
import json

def mostrar_menu():
    print("========== Menú de Gestión de Productos ==========")
    print("1. Agregar producto")
    print("2. Buscar producto por ID")
    print("3. Actualizar precio de producto")
    print("4. Eliminar producto por ID")
    print("5. Mostrar todos los productos")
    print("6. Salir")

def agregar_producto(gestion, tipo_producto):
    id = int(input("Ingrese el ID del producto: "))
    nombre = input("Ingrese el nombre del producto: ")
    categoria = input("Ingrese la categoría del producto: ")
    precio = float(input("Ingrese el precio del producto: "))
    stock = int(input("Ingrese el stock del producto: "))

    if tipo_producto == "original":
        estado = input("Ingrese el estado del producto: ")
        producto = ProductoOriginal(id, nombre, categoria, precio, stock, estado)
    else:
        origen = input("Ingrese el origen del producto: ")
        producto = ProductoNoOriginal(id, nombre, categoria, precio, stock, origen)

    gestion.crear_producto(producto)

def buscar_producto_por_id(gestion):
    id = int(input("Ingrese el ID del producto: "))
    producto = gestion.leer_producto(id)
    if producto:
        print(json.dumps(producto.to_dict(), indent=4))
    else:
        print(f'Producto con id {id} no encontrado')

def actualizar_precio_producto(gestion):
    id = int(input("Ingrese el ID del producto: "))
    nuevo_precio = float(input("Ingrese el nuevo precio del producto: "))
    gestion.actualizar_producto(id, nuevo_precio)

def eliminar_producto_por_id(gestion):
    id = int(input("Ingrese el ID del producto: "))
    gestion.eliminar_producto(id)

def mostrar_todos_los_productos(gestion):
    try:
        productos = gestion.leer_todos_los_productos()
        for producto in productos:
            if isinstance(producto, ProductoOriginal):
                print(f'{producto.id} {producto.nombre} {producto.estado}')
            elif isinstance(producto, ProductoNoOriginal):
                print(f'{producto.id} {producto.nombre} {producto.origen}')


    
    except Exception as e:
        print(f'Error al mostrar los productos {e}')


def main():
    gestion = GestionProductos()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            tipo_producto = input("¿El producto es original o no original? (original/no original): ").strip().lower()
            agregar_producto(gestion, tipo_producto)
        elif opcion == "2":
            buscar_producto_por_id(gestion)
        elif opcion == "3":
            actualizar_precio_producto(gestion)
        elif opcion == "4":
            eliminar_producto_por_id(gestion)
        elif opcion == "5":
            mostrar_todos_los_productos(gestion)
        elif opcion == "6":
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

if __name__ == "__main__":
    main()

