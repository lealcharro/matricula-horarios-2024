import tkinter as tk
from tkinter import ttk
import sqlite3


class Cursosos:
    def __init__(self, instancia_horarioro):
        self.instancia_horarioro = instancia_horarioro
        self.parent = tk.Tk()
        self.parent.title("Franatostein")
        self.parent.minsize(1030, 328)  # Tamaño mínimo
        self.parent.maxsize(1030, 328)  # Tamaño máximo
        self.posicion_cursoso = None

        self.conn = sqlite3.connect('Generador de Horarios db malla_2018 horarios_2024_1.db')
        self.cursor = self.conn.cursor()

        self.opciones = []
        self.valores_listbox = []
        self.cursos = {}
        
        self.create_frames()
    
    def create_frames(self):
        self.fr_malla = tk.Frame(self.parent)
        self.fr_malla.grid(row=0, column=0, padx=0, pady=0)
        self.fr_malla.place(x=0, y=0)
        
        self.fr_listbox = tk.Frame(self.parent)
        self.fr_listbox.grid(row=0, column=1, padx=431, pady=0)
        self.fr_malla.place(x=0, y=0)

        self.fr_edit_listbox = tk.Frame(self.fr_listbox)
        self.fr_edit_listbox.grid(row=2, column=0)

        self.create_widgets()
    
    def create_widgets(self):     
        self.lb_descripcion_fac = tk.Label(self.fr_malla, text="Facultad:")
        self.lb_descripcion_fac.grid(row=0, column=0, padx=2, pady=1, sticky=tk.W)

        self.primer_combobox = ttk.Combobox(self.fr_malla, state='readonly', width=50)
        self.primer_combobox.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.primer_combobox.bind("<<ComboboxSelected>>", self.cargar_opciones_segundo_combobox)

        self.lb_descripcion_carrera = tk.Label(self.fr_malla, text="Carrera:")
        self.lb_descripcion_carrera.grid(row=2, column=0, padx=2, pady=1, sticky=tk.W)

        self.segundo_combobox = ttk.Combobox(self.fr_malla, state='readonly', width=50)
        self.segundo_combobox.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.segundo_combobox.bind("<<ComboboxSelected>>", self.cargar_opciones_tercer_combobox)

        self.lb_descripcion_ciclo = tk.Label(self.fr_malla, text="Ciclo:")
        self.lb_descripcion_ciclo.grid(row=4, column=0, padx=2, pady=1, sticky=tk.W)

        self.tercer_combobox = ttk.Combobox(self.fr_malla, state='readonly', width=50)
        self.tercer_combobox.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.tercer_combobox.bind("<<ComboboxSelected>>", self.cargar_opciones_cuarto_combobox)

        self.lb_descripcion_curso = tk.Label(self.fr_malla, text="Sección:")
        self.lb_descripcion_curso.grid(row=6, column=0, padx=2, pady=1, sticky=tk.W)

        self.cuarto_combobox = ttk.Combobox(self.fr_malla, state='readonly', width=50)
        self.cuarto_combobox.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.cuarto_combobox.bind("<<ComboboxSelected>>", self.cargar_opciones_quinto_combobox)

        self.lb_descripcion_seccion = tk.Label(self.fr_malla, text="Sección:")
        self.lb_descripcion_seccion.grid(row=8, column=0, padx=2, pady=1, sticky=tk.W)

        self.quinto_combobox = ttk.Combobox(self.fr_malla, state='readonly', width=50)
        self.quinto_combobox.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)

        self.btn_agregar_ciclo = tk.Button(self.fr_malla, text="Agregar Ciclo", width=12, command=self.agregar_ciclo)
        self.btn_agregar_ciclo.grid(row=5, column=1, padx=5, pady=5)

        self.btn_agregar_curso = tk.Button(self.fr_malla, text="Agregar Curso", width=12, command=self.agregar_curso)
        self.btn_agregar_curso.grid(row=7, column=1, padx=5, pady=5)

        self.btn_agregar_curso = tk.Button(self.fr_malla, text="Agregar Sección", width=12, command=self.agregar_seccion)
        self.btn_agregar_curso.grid(row=9, column=1, padx=5, pady=5)

        self.btn_guardar_seleccion = tk.Button(self.fr_malla, text="Guardar y Salir", width=12, command=self.guardar_y_salir)
        self.btn_guardar_seleccion.grid(row=10, column=0, padx=5, pady=5)

        self.lb_descripcion_fac = tk.Label(self.fr_listbox, text="Asignaturas-sección seleccionados:")
        self.lb_descripcion_fac.grid(row=0, column=0, padx=7, pady=1, sticky=tk.W)

        self.seleccionados_listbox = tk.Listbox(self.fr_listbox, selectmode=tk.MULTIPLE, width=97, height=16)
        self.seleccionados_listbox.grid(row=1, column=0, padx=10, pady=3)

        self.btn_eliminar = tk.Button(self.fr_edit_listbox, text="Eliminar seleccionados", command=self.eliminar_seleccion)
        self.btn_eliminar.grid(row=0, column=0, padx=10, pady=5)

        self.btn_eliminar_todo = tk.Button(self.fr_edit_listbox, text="Eliminar todo", command=self.eliminar_todos)
        self.btn_eliminar_todo.grid(row=0, column=1, padx=10, pady=5)

        self.cargar_opciones_primer_combobox()


    def cargar_opciones_primer_combobox(self):
        self.cursor.execute("SELECT DISTINCT facultad FROM malla_2018")
        opciones = [fila[0] for fila in self.cursor.fetchall()]
        self.primer_combobox.config(values=opciones, height=len(opciones))
        self.primer_combobox.set(opciones[0])
        self.cargar_opciones_segundo_combobox(event=None)


    def cargar_opciones_segundo_combobox(self, event):
        for combo_box in [self.segundo_combobox, self.tercer_combobox, self.cuarto_combobox, self.quinto_combobox]:
            combo_box['values'] = ()
            combo_box.set('')
        self.cursor.execute("SELECT DISTINCT carrera FROM malla_2018 WHERE facultad = ?",
                            (self.primer_combobox.get(),))
        opciones = [fila[0] for fila in self.cursor.fetchall()]
        self.segundo_combobox.config(values=opciones, height=len(opciones))


    def cargar_opciones_tercer_combobox(self, event):
        for combo_box in [self.tercer_combobox, self.cuarto_combobox, self.quinto_combobox]:
            combo_box['values'] = ()
            combo_box.set('')
        self.cursor.execute("SELECT DISTINCT ciclo FROM malla_2018 WHERE facultad = ? AND carrera = ?", 
                            (self.primer_combobox.get(), self.segundo_combobox.get(),))
        opciones = [fila[0] for fila in self.cursor.fetchall()]
        self.tercer_combobox.config(values=opciones, height=len(opciones))


    def cargar_opciones_cuarto_combobox(self, event):
        for combo_box in [self.cuarto_combobox, self.quinto_combobox]:
            combo_box['values'] = ()
            combo_box.set('')
        consulta = """
            SELECT DISTINCT codigo, nombre FROM malla_2018 
            WHERE facultad = ? 
            AND carrera = ? 
            AND ciclo = ? 
            AND codigo IN (SELECT codigo FROM horarios_2024_1)
        """
        self.cursor.execute(consulta, (self.primer_combobox.get(), self.segundo_combobox.get(), self.tercer_combobox.get()))
        opciones = [f'{op_codigo} {op_nombre}' for op_codigo, op_nombre in self.cursor.fetchall()]
        self.cuarto_combobox.config(values=opciones, height=len(opciones))


    def cargar_opciones_quinto_combobox(self, event):
        self.quinto_combobox['values'] = ()
        self.quinto_combobox.set('')
        self.cursor.execute("SELECT DISTINCT seccion FROM horarios_2024_1 WHERE codigo = ?",
                            (self.cuarto_combobox.get()[0:5],))
        opciones = [f'{fila[0]}' for fila in self.cursor.fetchall()]
        self.quinto_combobox.config(values=opciones, height=len(opciones))


    def agregar_seccion(self):
        if not self.quinto_combobox.get():
            return
        codigo, nombre = self.cuarto_combobox.get().split(' ', 1)
        seccion = self.quinto_combobox.get()
        opcion = f'{codigo} {seccion} {nombre}'
        if opcion not in self.valores_listbox:
            self.seleccionados_listbox.insert(tk.END, opcion)
            self.valores_listbox.append(opcion)


    def agregar_curso(self):
        if not self.cuarto_combobox.get():
            return
        self.cargar_opciones_quinto_combobox(event=None)
        codigo, nombre = self.cuarto_combobox.get().split(' ', 1)
        for seccion in self.quinto_combobox['values']:
            opcion = f'{codigo} {seccion} {nombre}'
            if opcion not in self.valores_listbox:
                self.seleccionados_listbox.insert(tk.END, opcion)
                self.valores_listbox.append(opcion)


    def agregar_ciclo(self):
        self.cargar_opciones_cuarto_combobox(event=None)
        for curso in self.cuarto_combobox['values']:
            self.cuarto_combobox.set(curso)
            self.cargar_opciones_quinto_combobox(event=None)
            self.agregar_curso()
        self.cuarto_combobox.set('')


    def eliminar_seleccion(self):
        seleccion = self.seleccionados_listbox.curselection()
        for index in reversed(seleccion):
            valor = self.seleccionados_listbox.get(index)
            self.seleccionados_listbox.delete(index)
            self.valores_listbox.remove(valor)


    def eliminar_todos(self):
        self.seleccionados_listbox.delete(0, tk.END)
        self.valores_listbox.clear()


    def mostrar(self, posicion, valores_listbox):
        self.parent.deiconify()
        if posicion:
            self.parent.geometry(f"+{posicion[0]}+{posicion[1]}")
        self.valores_listbox = valores_listbox
        for opcion in self.valores_listbox:
            self.seleccionados_listbox.insert(tk.END, opcion)
        self.parent.mainloop()
 
 
    def guardar_y_salir(self):
        self.parent.withdraw()
        self.posicion_cursoso = self.parent.geometry().split("+")[1:3]
        self.instancia_horarioro.mostrar(self.posicion_cursoso, self.valores_listbox)
        