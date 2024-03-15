import tkinter as tk
from tkinter import ttk, font
from conexion_core_y_ventana import secciones_to_horario
from core import caracterizar_y_verificar, DFF
from cursos import Cursosos
from conexion_core_y_ventana import listbox_to_cursos


class Horarioro:
    def __init__(self):
        self.parent = tk.Tk()        
        self.parent.title("Anakin-ator")
        self.parent.minsize(1030, 328)
        self.parent.maxsize(1030, 328)
        
        self.posicion_horarioro = None
        self.valores_listbox = []

        self.cursos = {}
        self.num_cruces = tk.IntVar(value=0)
        self.con_tt = tk.BooleanVar(value=False)
        self.con_tp = tk.BooleanVar(value=False)
        self.condiciones = [0, False, False]
    
        self.lista_horarios = []
        self.i_horario = tk.IntVar(value=0)
        
        self.create_frames()
    
    def create_frames(self):
        self.fr_condiciones = tk.Frame(self.parent)
        self.fr_condiciones.grid(row=0, column=0)

        self.fr_condiciones_1 = tk.Frame(self.fr_condiciones)
        self.fr_condiciones_1.grid(row=3, column=0)

        self.fr_condiciones_2 = tk.Frame(self.fr_condiciones)
        self.fr_condiciones_2.grid(row=6, column=0)

        self.fr_horario = tk.Frame(self.parent)
        self.fr_horario.grid(row=0, column=1)

        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.fr_horario, columns=("","LU","MA","MI","JU","VI","SA"), show="headings", height=15)
        self.tree.grid(row=0, column=0)
        hours = ["07-08", "08-09", "09-10", "10-11", "11-12", "12-13", "13-14", "14-15",
                 "15-16", "16-17", "17-18", "18-19", "19-20", "20-21", "21-22"]
        for row, hour in enumerate(hours):
            self.tree.insert("", "end", text=hour, values=(hour))
            self.tree.rowconfigure(row, minsize=25, weight=100)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="center")  # Ancho de cada columna en píxeles
        self.tree.column("", width=40)

        self.btn_get_cursos = tk.Button(self.fr_condiciones, text="Editar Cursos", command=self.elegir_cursos, width=15)
        self.btn_get_cursos.grid(row=0, column=0)
        
        self.checkbutton_1 = tk.Checkbutton(self.fr_condiciones, text="Incluir cruces Teoria/Teoria", variable=self.con_tt, anchor="w", justify=tk.LEFT)
        self.checkbutton_1.grid(row=1, column=0)
        self.checkbutton_1.config(command=self.generar_horarios)

        self.checkbutton_2 = tk.Checkbutton(self.fr_condiciones, text="Incluir cruces Teoria/Practica", variable=self.con_tp, anchor="w", justify=tk.LEFT)
        self.checkbutton_2.grid(row=2, column=0)
        self.checkbutton_2.config(command=self.generar_horarios)

        self.btn_mas = tk.Button(self.fr_condiciones_1, text="+", command=lambda: self.actualizar_num_cruces(1))
        self.btn_mas.grid(row=0, column=1)

        self.descripcion_num_cruces = tk.Label(self.fr_condiciones_1, text="Numero de cruces:", font=("Arial",10), width=15, justify=tk.RIGHT)
        self.descripcion_num_cruces.grid(row=1, column=0)
        self.str_num_cruces = tk.Label(self.fr_condiciones_1, text=self.num_cruces.get(), font=("Arial",20), width=2, justify=tk.CENTER)
        self.str_num_cruces.grid(row=1, column=1)

        self.btn_menos = tk.Button(self.fr_condiciones_1, text="-", command=lambda: self.actualizar_num_cruces(-1))
        self.btn_menos.grid(row=2, column=1)

        self.descripcion_horario = tk.Label(self.fr_condiciones, text="Horario actual / Horarios totales", font=("Arial",10), width=25, justify=tk.CENTER)
        self.descripcion_horario.grid(row=4, column=0)

        self.str_i_horario = tk.Label(self.fr_condiciones, text=f'{self.i_horario.get()} / {len(self.lista_horarios)}', font=("Arial",20), width=10, justify=tk.CENTER)
        self.str_i_horario.grid(row=5, column=0)

        self.btn_anterior = tk.Button(self.fr_condiciones_2, text="Anterior", command=lambda: self.actualizar_i_horario(-1))
        self.btn_anterior.grid(row=0, column=0)        

        self.btn_siguiente = tk.Button(self.fr_condiciones_2, text="Siguiente", command=lambda: self.actualizar_i_horario(1))
        self.btn_siguiente.grid(row=0, column=1)

        self.btn_siguiente = tk.Button(self.fr_condiciones, text="Generar Horarios", width=15, command=lambda: self.actualizar_num_cruces(0))
        self.btn_siguiente.grid(row=7, column=0)
        
        self.descripcion_i_horario = tk.Label(self.fr_condiciones, text=" ", font=("Arial",9), width=30, justify=tk.CENTER)
        self.descripcion_i_horario.grid(row=8, column=0)
        

    def elegir_cursos(self):
        self.posicion_horarioro = self.parent.geometry().split("+")[1:3]
        self.parent.withdraw()
        cursosos = Cursosos(self)
        cursosos.mostrar(self.posicion_horarioro, self.valores_listbox)


    def mostrar(self, posicion, valores_listbox):
        self.valores_listbox = valores_listbox
        self.cursos = listbox_to_cursos(valores_listbox) if len(valores_listbox) else {}
        self.con_tt.set(False)
        self.con_tp.set(False)
        self.lista_horarios = []
        self.num_cruces.set(0)
        self.str_num_cruces.config(text=0)
        self.i_horario.set(0)
        self.str_i_horario.config(text="0 / 0")
        self.parent.deiconify()
        self.parent.geometry(f"+{posicion[0]}+{posicion[1]}") if posicion else None
        self.descripcion_i_horario.config(text=' ')        
        self.parent.mainloop()


    def actualizar_num_cruces(self, cambio):
        nuevo_valor = max(0, min(10, self.num_cruces.get() + cambio)) if cambio != 0 else 0
        self.num_cruces.set(nuevo_valor)
        self.str_num_cruces.config(text=nuevo_valor)
        self.generar_horarios()


    def generar_horarios(self):
        self.condiciones = [self.num_cruces.get(), self.con_tt.get(), self.con_tp.get()]
        self.lista_horarios = []
        self.i_horario.set(0)
        self.lista_horarios = caracterizar_y_verificar(DFF, self.cursos, self.condiciones)
        self.actualizar_i_horario(1)


    def actualizar_i_horario(self, cambio):
        nuevo_valor = max(1, min(len(self.lista_horarios), self.i_horario.get() + cambio)) if cambio != 0 else 0
        nuevo_valor = nuevo_valor if len(self.lista_horarios) else 0
        self.i_horario.set(nuevo_valor)
        self.str_i_horario.config(text=f'{nuevo_valor} / {len(self.lista_horarios)}')
        self.cargar_horario() if cambio else None


    def cargar_horario(self):        
        hours = ["07-08", "08-09", "09-10", "10-11", "11-12", "12-13", "13-14", "14-15",
                 "15-16", "16-17", "17-18", "18-19", "19-20", "20-21", "21-22"]
        if self.i_horario.get() == 0:
            for row, hour in enumerate(hours):
                self.tree.item(self.tree.get_children()[row], values=tuple([hour]))
            self.descripcion_i_horario.config(text='')
            return
        frase = ''
        for cso in self.cursos.keys():
            frase += ' '+cso
        frase += '\n     '
        for hor in self.lista_horarios[self.i_horario.get()-1]:
            frase += ' '+hor +'         '
        self.descripcion_i_horario.config(text=frase, justify='left')
        horario = secciones_to_horario(DFF, self.cursos.keys(), self.lista_horarios[self.i_horario.get()-1])
        for hora, actividades in horario.items():
            cargas = [carga for carga in actividades.values()]
            cargas.insert(0, hora)
            self.tree.item(self.tree.get_children()[hours.index(hora)], values=tuple(cargas))
        for i, col in enumerate(self.tree["columns"]):
            if i != 0:
                self.tree.column(col, 
                                 width=font.Font().measure(
                                        max([self.tree.set(item, col) for item in self.tree.get_children("")], 
                                             key=len)
                                    ) + 15
                                )
        self.tree.column("", width=40)



if __name__ == "__main__":
    app = Horarioro()    
    app.mostrar(None, [])
