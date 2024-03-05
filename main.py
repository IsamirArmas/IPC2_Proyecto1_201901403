import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from graphviz import Digraph
import xml.etree.ElementTree as ET
import tkinter.messagebox as messagebox
from tkinter import Scrollbar

# Definición de la clase Azulejo
class Azulejo:
    def __init__(self, fila, columna, color):
        self.fila = fila
        self.columna = columna
        self.color = color
        self.volteado = False  # Indica si el azulejo está volteado o no
        self.siguiente = None  # Referencia al azulejo siguiente en la lista enlazada
# Definición de la clase NodoAzulejo, que se utilizará para formar la lista enlazada de azulejos en un piso
class NodoAzulejo:
    def __init__(self, azulejo):
        self.azulejo = azulejo
        self.siguiente = None
# Definición de la clase Piso
class Piso:
    def __init__(self, nombre, R, C, F, S, patrones):
        self.nombre = nombre
        self.R = R
        self.C = C
        self.F = F
        self.S = S
        self.patrones = patrones
# Definición de la clase NodoPiso, que se utilizará para formar la lista enlazada de pisos en el tablero
class NodoPiso:
    def __init__(self, piso):
        self.piso = piso
        self.siguiente = None
        self.primer_nodo_azulejo = None  # Primer nodo de la lista enlazada de azulejos
# Definición de la clase Tablero
class Tablero:
    def __init__(self):
        self.primer_nodo_piso = None

    def agregar_piso(self, piso):
        nuevo_nodo_piso = NodoPiso(piso)
        if not self.primer_nodo_piso or piso.nombre < self.primer_nodo_piso.piso.nombre:
            nuevo_nodo_piso.siguiente = self.primer_nodo_piso
            self.primer_nodo_piso = nuevo_nodo_piso
        else:
            nodo_actual = self.primer_nodo_piso
            while nodo_actual.siguiente and piso.nombre > nodo_actual.siguiente.piso.nombre:
                nodo_actual = nodo_actual.siguiente
            nuevo_nodo_piso.siguiente = nodo_actual.siguiente
            nodo_actual.siguiente = nuevo_nodo_piso

    def cargar_desde_xml(self, archivo):
        try:
            tree = ET.parse(archivo)
            root = tree.getroot()
            for piso_elem in root.findall('.//piso'):
                piso_nombre = piso_elem.attrib.get('nombre', '')
                R = int(piso_elem.find('R').text)
                C = int(piso_elem.find('C').text)
                F = int(piso_elem.find('F').text)
                S = int(piso_elem.find('S').text)
                patrones = []
                for patron_elem in piso_elem.findall('.//patron'):
                    codigo = patron_elem.attrib.get('codigo', '')
                    patron = patron_elem.text.strip()
                    patrones.append((codigo, patron))

                # Verifica que el número de patrones sea exactamente 2
                if len(patrones) != 2:
                    raise ValueError("Cada piso debe tener exactamente 2 patrones.")
                piso_obj = Piso(piso_nombre, R, C, F, S, patrones)
                self.agregar_piso(piso_obj)

        except ET.ParseError as e:
            messagebox.showerror("Error de XML", f"Error al analizar el archivo XML: {str(e)}")
        except ValueError as e:
            messagebox.showerror("Error en datos", str(e))

    def iterar_nodos_pisos(self):
        nodo_piso_actual = self.primer_nodo_piso
        while nodo_piso_actual:
            yield nodo_piso_actual
            nodo_piso_actual = nodo_piso_actual.siguiente

    def mostrar_tableros(self):
        root = tk.Tk()
        root.title("Tableros Inicial y Final")
        # Crea el frame principal
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Agrega la scrollbar vertical
        scrollbar = Scrollbar(main_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Crea el canvas
        canvas = tk.Canvas(main_frame, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Configura la scrollbar para que funcione con el canvas
        scrollbar.config(command=canvas.yview)
        # Crea un nuevo frame dentro del canvas
        self.frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.frame, anchor="nw")
        # Obtener los nombres de los pisos y ordenarlos alfabéticamente
        nombres_pisos = sorted([nodo.piso.nombre for nodo in self.iterar_nodos_pisos()])
        lb_tableros = tk.Listbox(self.frame, selectmode=tk.SINGLE)
        lb_tableros.pack(pady=5)

        for nombre_piso in nombres_pisos:
            lb_tableros.insert(tk.END, nombre_piso)

        tk.Label(self.frame, text="Selecciona un piso:", font=('Helvetica', 12), bg='lightblue').pack(pady=5)

        def actualizar_patron(event):
            selected_tablero_index = lb_tableros.curselection()
            if selected_tablero_index:
                selected_tablero_index = selected_tablero_index[0]
                selected_tablero = lb_tableros.get(selected_tablero_index)
                nodo_piso_actual = self.primer_nodo_piso
                for _ in range(selected_tablero_index):
                    nodo_piso_actual = nodo_piso_actual.siguiente

                self.mostrar_patron(nodo_piso_actual.piso)

                btn_regresar = tk.Button(self.frame, text="Seleccionar otro tablero", command=self.regresar_seleccion_tablero)
                btn_regresar.pack(side=tk.BOTTOM, pady=10)

        lb_tableros.bind("<<ListboxSelect>>", actualizar_patron)
        btn_regresar = tk.Button(root, text="Regresar al Menú", command=root.destroy)
        btn_regresar.pack(side=tk.LEFT, padx=10, pady=10)
        btn_generar_datos = tk.Button(root, text="Generar Datos en Consola", command=self.generar_datos_en_consola)
        btn_generar_datos.pack(side=tk.LEFT, padx=10, pady=10)

        root.mainloop()

    def regresar_seleccion_tablero(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.mostrar_tableros()

    def mostrar_patron(self, piso):
        for widget in self.frame.winfo_children():
            widget.destroy()
        patron_inicial = piso.patrones[0][1]
        patron_final = piso.patrones[1][1]

        self.mostrar_tablero("Tablero Inicial", piso.R, piso.C, patron_inicial)
        tk.Label(self.frame, text=f"Patron {piso.patrones[0][0]}: {patron_inicial}", font=('Helvetica', 12)).pack(pady=5)
        self.mostrar_tablero("Tablero Final", piso.R, piso.C, patron_final)
        tk.Label(self.frame, text=f"Patron {piso.patrones[1][0]}: {patron_final}", font=('Helvetica', 12)).pack(pady=5)


    def mostrar_tablero(self, titulo, R, C, patron):
        tablero_frame = tk.Frame(self.frame)
        tablero_frame.pack()
        tk.Label(tablero_frame, text=titulo, font=('Helvetica', 12)).grid(row=0, columnspan=C)
        pat_index = 0
        for i in range(R):
            for j in range(C):
                color = 'white' if patron[pat_index] == 'B' else 'black'
                pat_index = (pat_index + 1) % len(patron)
                tk.Label(tablero_frame, text='', width=2, height=1, bg=color).grid(row=i + 1, column=j)

    def generar_datos_en_consola(self):
        nodo_piso_actual = self.primer_nodo_piso
        while nodo_piso_actual:
            piso_obj = nodo_piso_actual.piso
            print(f"Piso: {piso_obj.nombre}")
            print(f"R: {piso_obj.R}, C: {piso_obj.C}, F: {piso_obj.F}, S: {piso_obj.S}")
            nodo_piso_actual = nodo_piso_actual.siguiente
        print("Datos generados en la consola.")
        self.generar_grafo()
        
        
    def generar_grafo(self):
        dot = Digraph(comment='Tableros de Azulejos', format='png')  # Puedes cambiar el formato a otro que prefieras (pdf, svg, etc.)
        nodo_piso_actual = self.primer_nodo_piso
        while nodo_piso_actual:
            piso_obj = nodo_piso_actual.piso
            dot.node(f"{piso_obj.nombre}", label=f"{piso_obj.nombre}\nR: {piso_obj.R}, C: {piso_obj.C}\nF: {piso_obj.F}, S: {piso_obj.S}", shape='box', style='rounded', fontname='Helvetica', fontsize='10')
            # Agrega nodos para cada patrón
            for codigo, patron in piso_obj.patrones:
                dot.node(f"{piso_obj.nombre}_{codigo}", label=f"{codigo}\n{patron}", shape='box', fontname='Courier', fontsize='10', color='white' if 'B' in patron else 'black')
                # Conecta el piso con el patrón correspondiente
                dot.edge(f"{piso_obj.nombre}", f"{piso_obj.nombre}_{codigo}")
            nodo_piso_actual = nodo_piso_actual.siguiente
        dot.render('reporte', cleanup=True, view=True)  # El archivo se guardará como 'reporte.png'
        return dot

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.tablero = Tablero()
        self.menu()

    def configurar_ventana(self):
        self.root.title("Optimización de Cambio de Azulejos")
        self.root.geometry('800x800') # Ajusta el tamaño de la ventana según tus necesidades
        self.root.configure(bg='#f0f0f0')

    def menu(self):
        marco_menu = tk.Frame(self.root, bg='#51CDC5')
        marco_menu.pack(pady=5)
        tk.Label(marco_menu, text="Bienvenido a mi Proyecto 1", font=('Helvetica', 16), bg='#f0f0f0').grid(row=0, column=0, pady=5)
        btn_caratula = ttk.Button(marco_menu, text="Carátula", command=self.mostrar_caratula)
        btn_caratula.grid(row=1, column=0, pady=5)
        btn_leer_archivo = ttk.Button(marco_menu, text="Leer archivo XML", command=self.leer_archivo_mostrar_tableros)
        btn_leer_archivo.grid(row=2, column=0, pady=5)
        btn_salir = ttk.Button(marco_menu, text="Salir", command=self.root.destroy)
        btn_salir.grid(row=3, column=0, pady=5)

    def leer_archivo_mostrar_tableros(self):
        filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if filename:
            self.tablero.cargar_desde_xml(filename)
            self.tablero.mostrar_tableros()

    def mostrar_caratula(self):
        caratula_root = tk.Toplevel(self.root)
        caratula_root.title("Carátula")
        caratula_root.geometry("400x400")
        tk.Label(caratula_root, text="Isamir Alessandro Armas Cano", font=('Helvetica', 20)).pack(pady=20)
        tk.Label(caratula_root, text="201901403", font=('Helvetica', 20)).pack(pady=20)
        tk.Label(caratula_root, text="Proyecto 1 lab IPC 2", font=('Helvetica', 20)).pack(pady=20)
        btn_regresar_caratula = tk.Button(caratula_root, text="Regresar al Menú", command=caratula_root.destroy)
        btn_regresar_caratula.pack(side=tk.BOTTOM, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
