import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from enum import Enum
import sqlite3

class WindowType(Enum):
    main = 1
    mat_window = 2
    fluid_window = 3
    res_window = 4
    frame = 5




class GUI():

    def __init__(
            self, window_type, title = None, 
            frame = None, mat_window = None,
            fluid_window = None, 
            ) -> None:

        if window_type == WindowType.main:
            self.window = tk.Tk()
            MainMenu = tk.Menu(self.window)
            filemenu = tk.Menu(MainMenu, tearoff=0)
            filemenu.add_command(
                label="Editar database de materiais",
                command=mat_window
            )
            filemenu.add_command(
                label="Editar database de fluidos",
                command=fluid_window
            )
            # filemenu.add_command(
            #     label="Ver histórico de resultados",
            #     command=res_window
            # )
            filemenu.add_separator()
            filemenu.add_command(
                label="Sair",
                command=self.window.destroy
            )
            MainMenu.add_cascade(label="Opções", menu=filemenu)
            self.window.config(menu=MainMenu)
        elif window_type == WindowType.frame:
            self.window = frame
        else:
            self.window = tk.Toplevel()
        if title is not None:
            self.window.title(title)
    
    def create_LabelFrame(self, textstr, rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, show=True, rowspanint=None):
        name = tk.LabelFrame(self.window, text=textstr,)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, pady=padyint, rowspan=rowspanint)
        return GUI(WindowType.frame, frame=name)
    
    def create_Label(self, textstr, rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, show=True):
        name = ttk.Label(self.window, text=textstr)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, pady=padyint)
        return name
    
    def create_Entry(self, rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, show=True, state = "normal"):
        name = ttk.Entry(self.window)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, pady=padyint)
        name.config(state=state)
        return name
    
    def create_Button(self, textstr, commandf=None, rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, show=True, ipadxint=None, ipadyint=None):
        name = ttk.Button(self.window, text=textstr, command=commandf)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, pady=padyint, ipadx=ipadxint, ipady=ipadyint)
        return name
    
    def create_RadioButton(self, textstr, var, valueint, commandf=None, rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, show=True):
        name = ttk.Radiobutton(self.window, text=textstr, variable=var,
                           value=valueint, command=commandf)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, pady=padyint)
        return name
    
    def create_Combobox(self, textstr, rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, postcommandf=None, show=True):
        name = ttk.Combobox(self.window, postcommand=postcommandf)
        name.set(textstr)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, padyx=padyint)
        return name
    
    def create_Spinbox(self,fromint,toint,rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, show=True):
        name = ttk.Spinbox(self.window,from_=fromint,to=toint)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, pady=padyint)
        return name





def isInt(var):
    funciona = False
    try:
        int(var)
        funciona = True
    except ValueError:
        funciona = False
    return funciona

def isfloat(var):
    funciona = False
    if var != None:
        try:
            float(var)
            funciona = True
        except ValueError:
            funciona = False
        return funciona
    return funciona

def check_str_field(field, nome):
    if len(field.get()) == 0:
        messagebox.showinfo("Erro", f"{nome} está vazio")
        return False
    return True

def check_float_field(field, nome):
    if len(field.get()) == 0:
        messagebox.showinfo("Erro", f"{nome} está vazio")
        return False
    elif not isfloat(field.get()):
        messagebox.showinfo("Erro", f"{nome} tem que ser um número")
        field.delete(0, tk.END)
        return False
    return True

def check_int_field(field, nome):
    if len(field.get()) == 0:
        messagebox.showinfo("Erro", f"{nome} está vazio")
        return False
    elif not isInt(field.get()):
        messagebox.showinfo("Erro", f"{nome} tem que ser um número")
        field.delete(0, tk.END)
        return False
    return True

def clearGrid(list_of_widgets):
    for widget in list_of_widgets:
        widget.destroy()


def submit_mat(ten_mat1, nome_mat1, frame2, list_of_widgets, den_mat1):
    if check_str_field(nome_mat1, "Nome do material") and check_float_field(ten_mat1, "Tensão admissível do material") and check_float_field(den_mat1, "Densidade do material"):
        conn = sqlite3.connect('storage2.db')
        cursor1 = conn.cursor()
        cursor1.execute("SELECT *, oid FROM materials_list")
        records = cursor1.fetchall()
        shouldInsert = True
        for record in records:
            if record[0] == nome_mat1.get():
                aux = messagebox.askquestion(
                    "Erro", "Já existe um material com este nome.\nDeseja sobreescrever?")
                if aux == 'no':
                    shouldInsert = False
        if shouldInsert:
            cursor1.execute("INSERT INTO materials_list VALUES (:mat_name, :adm_tension, :mat_den) ON CONFLICT(mat_name) DO UPDATE SET adm_tension=excluded.adm_tension, mat_den=excluded.mat_den",
                            {
                                'mat_name': nome_mat1.get(),
                                'adm_tension': float(ten_mat1.get()),
                                'mat_den': float(den_mat1.get())
                            }
                            )
        cursor1.execute("SELECT *, oid FROM materials_list")
        records = cursor1.fetchall()
        i = 2
        for listamateriais in records:
            for j in range(len(listamateriais)):
                e = frame2.create_Label(listamateriais[j], i, j+2)
                list_of_widgets.append(e)
            i += 1
        conn.commit()
        conn.close()

        nome_mat1.delete(0, tk.END)
        ten_mat1.delete(0, tk.END)
        den_mat1.delete(0, tk.END)

def delete_mat(id_entry, frame2, list_of_widgets):
    if check_int_field(id_entry, "O ID"):
        conn = sqlite3.connect('storage2.db')
        cursor1 = conn.cursor()
        cursor1.execute("DELETE from materials_list WHERE oid= :id_entry", {
            'id_entry': id_entry.get()
        })
        cursor1.execute("SELECT *, oid FROM materials_list")
        records = cursor1.fetchall()
        i = 2
        clearGrid(list_of_widgets)
        for listamateriais in records:
            for j in range(len(listamateriais)):
                e = frame2.create_Label(listamateriais[j], i, j+2)
                list_of_widgets.append(e)
            i += 1
        conn.commit()
        conn.close()
        id_entry.delete(0, tk.END)

def submit_fluid(den_fluid1, nome_fluid1, frame2, list_of_widgets, type_fluid1):
    if check_str_field(nome_fluid1, "Nome do fluido") and check_float_field(den_fluid1, "Densidade do fluido"):
        conn = sqlite3.connect('storage2.db')
        cursor1 = conn.cursor()
        cursor1.execute("SELECT *, oid FROM fluids_list")
        records = cursor1.fetchall()
        shouldInsert = True
        for record in records:
            if record[0] == nome_fluid1.get():
                aux = messagebox.askquestion(
                    "Erro", "Já existe um fluid com este nome.\nDeseja sobreescrever?")
                if aux == 'no':
                    shouldInsert = False
        if shouldInsert:
            cursor1.execute("INSERT INTO fluids_list VALUES (:fluid_name, :fluid_type, :fluid_den) ON CONFLICT(fluid_name) DO UPDATE SET fluid_type=excluded.fluid_type, fluid_den=excluded.fluid_den",
                            {
                                'fluid_name': nome_fluid1.get(),
                                'fluid_type': type_fluid1.get(),
                                'fluid_den': float(den_fluid1.get())
                            }
                            )
        cursor1.execute("SELECT *, oid FROM fluids_list")
        records = cursor1.fetchall()
        i = 2
        for listafluidos in records:
            for j in range(len(listafluidos)):
                if j == 1:
                    if listafluidos[j] == False:
                        e = frame2.create_Label("Básico", i, j+2)
                    else:
                        e = frame2.create_Label("Agressivo", i, j+2)
                else:
                    e = frame2.create_Label(listafluidos[j], i, j+2)
                list_of_widgets.append(e)
            i += 1
        conn.commit()
        conn.close()

        nome_fluid1.delete(0, tk.END)
        den_fluid1.delete(0, tk.END)

def delete_fluid(id_entry, frame2, list_of_widgets):
    if check_int_field(id_entry, "O ID"):
        conn = sqlite3.connect('storage2.db')
        cursor1 = conn.cursor()
        cursor1.execute("DELETE from fluids_list WHERE oid= :id_entry", {
            'id_entry': id_entry.get()
        })
        cursor1.execute("SELECT *, oid FROM fluids_list")
        records = cursor1.fetchall()
        i = 2
        clearGrid(list_of_widgets)
        for listafluidos in records:
            for j in range(len(listafluidos)):
                if j == 1:
                    if listafluidos[j] == False:
                        e = frame2.create_Label("Básico", i, j+2)
                    else:
                        e = frame2.create_Label("Agressivo", i, j+2)
                else:
                    e = frame2.create_Label(listafluidos[j], i, j+2)
                list_of_widgets.append(e)
            i += 1
        conn.commit()
        conn.close()
        id_entry.delete(0, tk.END)

def update_cblist(material_type_combobox):
    conn = sqlite3.connect('storage2.db')
    cursor1 = conn.cursor()
    cursor1.execute("SELECT mat_name FROM materials_list")
    vlist = []
    for row in cursor1.fetchall():
        vlist.append(row[0])
    material_type_combobox['values'] = vlist
    conn.commit()
    conn.close()

def update_cblist2(fluid_type_combobox):
    conn = sqlite3.connect('storage2.db')
    cursor1 = conn.cursor()
    cursor1.execute("SELECT fluid_name FROM fluids_list")
    vlist = []
    for row in cursor1.fetchall():
        vlist.append(row[0])
    fluid_type_combobox['values'] = vlist
    conn.commit()
    conn.close()

def show_head_height(head_height_entry, show,end_diam_entry,show2=False):
    if show == True:
        head_height_entry.config(state="normal")
    else:
        head_height_entry.config(state="disabled")
    if show2:
        end_diam_entry.config(state="normal")
    else:
        end_diam_entry.config(state="disabled")
    