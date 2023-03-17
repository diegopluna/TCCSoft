from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from create_pdf import create_pdf
import sqlite3
from enum import Enum


class window_type(Enum):
    main = 1
    mat_db = 2
    res_db = 3
    frame = 4


class GUI():

    def __init__(self, wdw_type, title=None, frame=None, mat_db_wdw=None, res_db_wdw=None) -> None:
        if wdw_type == window_type.main:
            self.window = Tk()
            MainMenu = Menu(self.window)
            filemenu = Menu(MainMenu, tearoff=0)
            filemenu.add_command(
                label="Editar database de materiais", command=mat_db_wdw)
            filemenu.add_command(
                label="Ver histórico de resultados", command=res_db_wdw)
            filemenu.add_separator()
            filemenu.add_command(label="Sair", command=self.window.destroy)
            MainMenu.add_cascade(label="Opções", menu=filemenu)
            self.window.config(menu=MainMenu)
        elif wdw_type == window_type.frame:
            self.window = frame
        else:
            self.window = Toplevel()
        if title is not None:
            self.window.title(title)

    def create_Label(self, textstr, rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, show=True):
        name = Label(self.window, text=textstr)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, pady=padyint)
        return name

    def create_LabelFrame(self, textstr, rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, show=True, rowspanint=None):
        name = LabelFrame(self.window, text=textstr,)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, pady=padyint, rowspan=rowspanint)
        return GUI(window_type.frame, frame=name)

    def create_Entry(self, rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, show=True):
        name = Entry(self.window)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, pady=padyint)
        return name

    def create_RadioButton(self, textstr, var, valueint, commandf=None, rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, show=True):
        name = Radiobutton(self.window, text=textstr, variable=var,
                           value=valueint, command=commandf)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, pady=padyint)
        return name

    def create_Button(self, textstr, commandf=None, rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, show=True, ipadxint=None, ipadyint=None):
        name = Button(self.window, text=textstr, command=commandf)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, pady=padyint, ipadx=ipadxint, ipady=ipadyint)
        return name

    def create_Combobox(self, textstr, rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, postcommandf=None, show=True):
        name = Combobox(self.window, postcommand=postcommandf)
        name.set(textstr)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, padyx=padyint)
        return name
    
    def destroy(self):
        self.window.destroy()
    
    def create_Spinbox(self,fromint,toint,rowint=None, columnint=None, columnspanint=None, stickystr=None, padxint=None, padyint=None, show=True):
        name = Spinbox(self.window,from_=fromint,to=toint)
        if show:
            name.grid(row=rowint, column=columnint, columnspan=columnspanint,
                      sticky=stickystr, padx=padxint, pady=padyint)
        return name



def update_cblist(material_type_combobox):
    conn = sqlite3.connect('storage.db')
    cursor1 = conn.cursor()
    cursor1.execute("SELECT mat_name FROM materials_list")
    vlist = []
    for row in cursor1.fetchall():
        vlist.append(row[0])
    material_type_combobox['values'] = vlist
    conn.commit()
    conn.close()


def submit(ten_mat1, nome_mat1, frame2, list_of_widgets):
    if check_str_field(nome_mat1, "Nome do material") and check_float_field(ten_mat1, "Tensão admissível do material"):
        conn = sqlite3.connect('storage.db')
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
            cursor1.execute("INSERT INTO materials_list VALUES (:mat_name, :adm_tension) ON CONFLICT(mat_name) DO UPDATE SET adm_tension=excluded.adm_tension",
                            {
                                'mat_name': nome_mat1.get(),
                                'adm_tension': float(ten_mat1.get())
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

        nome_mat1.delete(0, END)
        ten_mat1.delete(0, END)


def delete(id_entry, frame2, list_of_widgets):
    if check_int_field(id_entry, "O ID"):
        conn = sqlite3.connect('storage.db')
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
        id_entry.delete(0, END)


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
        field.delete(0, END)
        return False
    return True


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


def check_int_field(field, nome):
    if len(field.get()) == 0:
        messagebox.showinfo("Erro", f"{nome} está vazio")
        return False
    elif not isInt(field.get()):
        messagebox.showinfo("Erro", f"{nome} tem que ser um número")
        field.delete(0, END)
        return False
    return True


def isInt(var):
    funciona = False
    try:
        int(var)
        funciona = True
    except ValueError:
        funciona = False
    return funciona


def clearGrid(list_of_widgets):
    for widget in list_of_widgets:
        widget.destroy()


def show_head_height(head_height_label, head_height_entry, show, end_diam_label,end_diam_entry,show2=False):
    if show == True:
        head_height_label.grid(row=15, column=0, sticky='W')
        head_height_entry.grid(row=15, column=1, sticky='W')
    else:
        head_height_label.grid_forget()
        head_height_entry.grid_forget()
    if show2:
        end_diam_label.grid(row=16, column=0, sticky='W')
        end_diam_entry.grid(row=16, column=1, sticky='W')
    else:
        end_diam_label.grid_forget()
        end_diam_entry.grid_forget()


def delete_res(id_entry, frame, list):
    if check_int_field(id_entry, "O ID"):
        conn = sqlite3.connect('storage.db')
        c = conn.cursor()
        c.execute("DELETE from results WHERE oid= :id_entry", {
            'id_entry': id_entry.get()
        })
        c.execute("SELECT *, oid FROM results")
        records = c.fetchall()
        i = 1
        clearGrid(list)
        for results in records:
            for j in range(len(results)):
                e = frame.create_Label(results[j], i, j+2)
                list.append(e)
            i += 1
        conn.commit()
        conn.close()
        id_entry.delete(0, END)


def pdf_res(id_entry):
    print_config = [[],
                    ["Diâmetro do Casco", "mm"],
                    ["Pressão de Projeto", "MPa"],
                    ["Eficiência de Junta", "-"],
                    ["Tipo de Casco", "-"],
                    ["Material do Casco", "-"],
                    ["Tipo de Tampo", "-"],
                    ["Material do Tampo", "-"],
                    ["Ângulo de Cone", "Graus"],
                    ["Espessura mínima do tampo", "mm"],
                    ["Espessura mínima do casco", "mm"]
                    ]
    if check_int_field(id_entry, "O ID"):
        data_in = [["Característica", "Valor", "Unidade", ]]
        data_out = [["Característica", "Valor", "Unidade", ]]
        conn = sqlite3.connect('storage.db')
        c = conn.cursor()
        c.execute("SELECT * from results WHERE oid= :id_entry", {
            'id_entry': id_entry.get()
        })
        records = c.fetchall()
        conn.commit()
        conn.close()
        name = records[0][0]
        for i in range(1, 8):
            carac = print_config[i][0]
            parameter = records[0][i]
            if parameter == None:
                parameter = "-"
            else:
                if isfloat(parameter):
                    parameter = str(parameter)
            unit = print_config[i][1]
            data_in.append([carac, parameter, unit])
        for i in range(9, 11):
            carac = print_config[i][0]
            parameter = records[0][i]
            if parameter == None:
                parameter = "-"
            else:
                if isfloat(parameter):
                    parameter = str(parameter)
            unit = print_config[i][1]
            data_out.append([carac, parameter, unit])
        create_pdf(name, data_in, data_out)


def get_valor(nome):
    conn = sqlite3.connect('storage.db')
    cursor1 = conn.cursor()
    cursor1.execute(
        f"SELECT adm_tension FROM materials_list WHERE mat_name='{nome.get()}'")
    ret = cursor1.fetchall()
    conn.commit()
    conn.close()
    if len(ret) != 1:
        return None
    return ret[0][0]


def check_radio_field(field, nome, min, max):
    if field.get() < min or field.get() > max:
        messagebox.showinfo("Erro", f"{nome} está vazio")
        return False
    return True


def check_mat_field(field, nome):
    if get_valor(field) == None:
        messagebox.showinfo("Erro", f"{nome} está vazio")
        return False
    return True
