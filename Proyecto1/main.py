import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from graphviz import Digraph

class Azulejo:
    def __init__(self, fila, columna, color):
        self.fila = fila
        self.columna = columna
        self.color = color
        self.volteado = False  # Indica si el azulejo está volteado o no
        self.siguiente = None  # Referencia al azulejo siguiente en la lista enlazada

class Tablero:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.inicio = None  # Nodo inicial de la lista enlazada

    def agregar_azulejo(self, fila, columna, color):
        nuevo_azulejo = Azulejo(fila, columna, color)
        if not self.inicio:
            self.inicio = nuevo_azulejo
        else:
            actual = self.inicio
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_azulejo

    def mostrar_tablero(self):
        print("# Aquí implementa la lógica para mostrar el tablero en Tkinter")
        

    def cargar_desde_xml(self, archivo):
        print("# Implementa la lógica para cargar los datos desde el archivo XML")

    def generar_grafo(self):
        # Implementa la lógica para generar un gráfico con Graphviz
        dot = Digraph(comment='Tablero de Azulejos')
        # Agrega nodos y conexiones al grafo
        return dot

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.tablero = Tablero(filas=0, columnas=0)
        self.menu()

    def configurar_ventana(self):
        self.root.title("Optimización de Cambio de Azulejos")
        self.root.geometry("600x600")  # Ajusta el tamaño de la ventana según tus necesidades
        self.root.configure(bg='#f0f0f0')

    def menu(self):
        # Marco para organizar mejor los elementos
        marco_menu = tk.Frame(self.root, bg='#44FAEF')
        marco_menu.pack(pady=20)

        # Etiqueta para el título
        tk.Label(marco_menu, text="Bienvenido a mi Proyecto 1", font=('Helvetica', 16), bg='#f0f0f0').grid(row=0, column=0, pady=10)

        # Botones
        btn_caratula = ttk.Button(marco_menu, text="Carátula", command=self.mostrar_caratula)
        btn_caratula.grid(row=1, column=0, pady=5)

        btn_leer_archivo = ttk.Button(marco_menu, text="Leer archivo XML", command=self.leer_archivo)
        btn_leer_archivo.grid(row=2, column=0, pady=5)

        btn_salir = ttk.Button(marco_menu, text="Salir", command=self.root.destroy)
        btn_salir.grid(row=3, column=0, pady=5)

    def leer_archivo(self):
        filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if filename:
            self.tablero.cargar_desde_xml(filename)
            self.tablero.mostrar_tablero()
            grafo = self.tablero.generar_grafo()
            grafo.render('output/tablero', format='png', cleanup=True)
            img = tk.PhotoImage(file='output/tablero.png')
            tk.Label(self.root, image=img).pack()

    def mostrar_caratula(self):
        # Implementa la lógica para mostrar la carátula con tu nombre
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
