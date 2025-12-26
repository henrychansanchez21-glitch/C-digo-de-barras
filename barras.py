import json
import os
import re

class Producto:
    def __init__(self, codigo_barras, nombre):
        self.codigo_barras = codigo_barras
        self.nombre = nombre
    
    def to_dict(self):
        return {
            'codigo_barras': self.codigo_barras,
            'nombre': self.nombre
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['codigo_barras'], data['nombre'])

class GaleriaProductos:
    def __init__(self, archivo_datos='productos.json'):
        self.archivo_datos = archivo_datos
        self.productos = []
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga los productos desde el archivo JSON"""
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
                    self.productos = [Producto.from_dict(item) for item in datos]
                print(f"Datos cargados: {len(self.productos)} productos en la galería.")
            except Exception as e:
                print(f"Error al cargar los datos: {e}")
                self.productos = []
        else:
            self.productos = []
    
    def guardar_datos(self):
        """Guarda los productos en el archivo JSON"""
        try:
            with open(self.archivo_datos, 'w', encoding='utf-8') as archivo:
                datos = [producto.to_dict() for producto in self.productos]
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            print("Datos guardados correctamente.")
        except Exception as e:
            print(f"Error al guardar los datos: {e}")
    
    def verificar_codigo_unico(self, codigo_barras):
        """Verifica que el código de barras no exista en la galería"""
        for producto in self.productos:
            if producto.codigo_barras == codigo_barras:
                return False
        return True
    
    def verificar_nombre_unico(self, nombre):
        """Verifica que el nombre no exista en la galería"""
        for producto in self.productos:
            if producto.nombre.lower() == nombre.lower():
                return False
        return True
    
    def agregar_producto(self, codigo_barras, nombre):
        """Agrega un nuevo producto a la galería"""
        # Validaciones
        if not codigo_barras or not nombre:
            return False, "El código de barras y el nombre son obligatorios."
        
        if not self.verificar_codigo_unico(codigo_barras):
            return False, f"El código de barras '{codigo_barras}' ya existe."
        
        if not self.verificar_nombre_unico(nombre):
            return False, f"El nombre '{nombre}' ya existe."
        
        # Agregar producto
        nuevo_producto = Producto(codigo_barras, nombre)
        self.productos.append(nuevo_producto)
        self.guardar_datos()
        return True, f"Producto '{nombre}' agregado correctamente."
    
    def buscar_por_codigo(self, codigo_barras):
        """Busca un producto por su código de barras"""
        for producto in self.productos:
            if producto.codigo_barras == codigo_barras:
                return producto
        return None
    
    def buscar_por_nombre(self, nombre):
        """Busca productos por nombre (búsqueda parcial)"""
        resultados = []
        for producto in self.productos:
            if nombre.lower() in producto.nombre.lower():
                resultados.append(producto)
        return resultados
    
    def listar_productos(self):
        """Lista todos los productos en la galería"""
        if not self.productos:
            print("No hay productos en la galería.")
            return
        
        print("\n" + "="*60)
        print("LISTA DE PRODUCTOS EN LA GALERÍA")
        print("="*60)
        for i, producto in enumerate(self.productos, 1):
            print(f"{i:3}. Código: {producto.codigo_barras:15} | Nombre: {producto.nombre}")
        print("="*60)
        print(f"Total: {len(self.productos)} productos")
    
    def eliminar_producto(self, codigo_barras):
        """Elimina un producto por su código de barras"""
        producto = self.buscar_por_codigo(codigo_barras)
        if producto:
            self.productos.remove(producto)
            self.guardar_datos()
            return True, f"Producto '{producto.nombre}' eliminado correctamente."
        else:
            return False, f"No se encontró un producto con código '{codigo_barras}'."

def mostrar_menu():
    """Muestra el menú principal del programa"""
    print("\n" + "="*60)
    print("SISTEMA DE GESTIÓN DE PRODUCTOS CON CÓDIGOS DE BARRAS")
    print("="*60)
    print("1. Agregar producto (escribir código y nombre)")
    print("2. 'Escanear' código de barras (simulación)")
    print("3. Buscar producto por nombre")
    print("4. Buscar producto por código de barras")
    print("5. Listar todos los productos")
    print("6. Eliminar producto")
    print("7. Verificar unicidad de código/nombre")
    print("8. Salir")
    print("="*60)

def simular_escaneo():
    """Simula el escaneo de un código de barras"""
    print("\n" + "-"*60)
    print("SIMULACIÓN DE ESCANEO DE CÓDIGO DE BARRAS")
    print("-"*60)
    print("Para simular el escaneo, ingrese un código de barras de 12-13 dígitos.")
    print("Ejemplo: 123456789012")
    print("O presione Enter para generar un código automáticamente.")
    print("-"*60)
    
    codigo = input("Ingrese el código de barras: ").strip()
    
    if not codigo:
        # Generar un código de barras aleatorio (simulado)
        import random
        codigo = str(random.randint(100000000000, 999999999999))
        print(f"Código generado automáticamente: {codigo}")
    
    return codigo

def validar_codigo_barras(codigo):
    """Valida el formato del código de barras"""
    # Verificar que sean solo dígitos y longitud típica de códigos EAN
    if not codigo.isdigit():
        return False, "El código de barras debe contener solo dígitos."
    
    if len(codigo) < 12 or len(codigo) > 13:
        return False, "El código de barras debe tener entre 12 y 13 dígitos."
    
    return True, "Código válido."

def main():
    galeria = GaleriaProductos()
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSeleccione una opción (1-8): ").strip()
            
            if opcion == "1":
                # Agregar producto manualmente
                print("\n" + "-"*60)
                print("AGREGAR PRODUCTO MANUALMENTE")
                print("-"*60)
                
                codigo = input("Ingrese el código de barras: ").strip()
                valido, mensaje = validar_codigo_barras(codigo)
                if not valido:
                    print(f"Error: {mensaje}")
                    continue
                
                nombre = input("Ingrese el nombre del producto: ").strip()
                if not nombre:
                    print("Error: El nombre no puede estar vacío.")
                    continue
                
                exito, mensaje = galeria.agregar_producto(codigo, nombre)
                print(f"\n{mensaje}")
            
            elif opcion == "2":
                # Simular escaneo
                print("\n" + "-"*60)
                print("AGREGAR PRODUCTO POR ESCANEO")
                print("-"*60)
                
                codigo = simular_escaneo()
                valido, mensaje = validar_codigo_barras(codigo)
                if not valido:
                    print(f"Error: {mensaje}")
                    continue
                
                # Verificar si el código ya existe
                producto_existente = galeria.buscar_por_codigo(codigo)
                if producto_existente:
                    print(f"\nEl código ya existe. Producto asociado: {producto_existente.nombre}")
                    continue
                
                # Si no existe, pedir el nombre
                nombre = input("Ingrese el nombre del producto: ").strip()
                if not nombre:
                    print("Error: El nombre no puede estar vacío.")
                    continue
                
                exito, mensaje = galeria.agregar_producto(codigo, nombre)
                print(f"\n{mensaje}")
            
            elif opcion == "3":
                # Buscar por nombre
                print("\n" + "-"*60)
                print("BUSCAR PRODUCTO POR NOMBRE")
                print("-"*60)
                
                nombre = input("Ingrese el nombre o parte del nombre: ").strip()
                if not nombre:
                    print("Error: Debe ingresar un término de búsqueda.")
                    continue
                
                resultados = galeria.buscar_por_nombre(nombre)
                if resultados:
                    print(f"\nSe encontraron {len(resultados)} resultado(s):")
                    for i, producto in enumerate(resultados, 1):
                        print(f"{i}. Código: {producto.codigo_barras} | Nombre: {producto.nombre}")
                else:
                    print(f"No se encontraron productos con '{nombre}' en el nombre.")
            
            elif opcion == "4":
                # Buscar por código
                print("\n" + "-"*60)
                print("BUSCAR PRODUCTO POR CÓDIGO DE BARRAS")
                print("-"*60)
                
                codigo = input("Ingrese el código de barras: ").strip()
                producto = galeria.buscar_por_codigo(codigo)
                
                if producto:
                    print(f"\nProducto encontrado:")
                    print(f"Código: {producto.codigo_barras}")
                    print(f"Nombre: {producto.nombre}")
                else:
                    print(f"No se encontró un producto con código '{codigo}'.")
            
            elif opcion == "5":
                # Listar todos los productos
                galeria.listar_productos()
            
            elif opcion == "6":
                # Eliminar producto
                print("\n" + "-"*60)
                print("ELIMINAR PRODUCTO")
                print("-"*60)
                
                codigo = input("Ingrese el código de barras del producto a eliminar: ").strip()
                
                # Confirmar eliminación
                confirmar = input(f"¿Está seguro de eliminar el producto con código {codigo}? (s/n): ").strip().lower()
                if confirmar == 's':
                    exito, mensaje = galeria.eliminar_producto(codigo)
                    print(mensaje)
                else:
                    print("Eliminación cancelada.")
            
            elif opcion == "7":
                # Verificar unicidad
                print("\n" + "-"*60)
                print("VERIFICAR UNICIDAD DE CÓDIGO Y NOMBRE")
                print("-"*60)
                
                codigo = input("Ingrese el código de barras a verificar: ").strip()
                nombre = input("Ingrese el nombre a verificar: ").strip()
                
                if codigo:
                    if galeria.verificar_codigo_unico(codigo):
                        print(f"✓ El código '{codigo}' está disponible.")
                    else:
                        print(f"✗ El código '{codigo}' ya existe en la galería.")
                
                if nombre:
                    if galeria.verificar_nombre_unico(nombre):
                        print(f"✓ El nombre '{nombre}' está disponible.")
                    else:
                        print(f"✗ El nombre '{nombre}' ya existe en la galería.")
            
            elif opcion == "8":
                # Salir
                print("\n¡Gracias por usar el sistema de gestión de productos!")
                break
            
            else:
                print("\nOpción no válida. Por favor, seleccione una opción del 1 al 8.")
        
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario.")
            break
        except Exception as e:
            print(f"\nError inesperado: {e}")

if __name__ == "__main__":
    main()