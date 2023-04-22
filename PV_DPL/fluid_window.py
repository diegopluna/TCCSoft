from tkinter import *
from GUI2 import *

def fluid_window():
    fluid_window = GUI(WindowType.fluid_window, "Database de fluidos")

    fluid_frame = fluid_window.create_LabelFrame(
        "Lista de Fluidos", rowint=1, columnint=2, padxint=10, padyint=10, rowspanint=15)
    
    fluid_window.create_Label("Database de Fluidos", rowint=0, columnspanint=4)

    fluid_window.create_Label("Nome do fluido:", 1, 0, stickystr='W')
    fluid_name_entry = fluid_window.create_Entry(1, 1, stickystr='W')

    fluid_type = tk.BooleanVar()
    fluid_window.create_Label("Tipo de fluido:", 2, 0, stickystr='W')
    fluid_type_1 = fluid_window.create_RadioButton("Básico",fluid_type,False,rowint=2,columnint=1)
    fluid_type_2 = fluid_window.create_RadioButton("Agressivo",fluid_type,True,rowint=3,columnint=1)

    fluid_window.create_Label("Densidade do fluido(kg/m3):", 4, 0, stickystr='W')
    fluid_den_entry = fluid_window.create_Entry(4, 1, stickystr='W')

    fluid_window.create_Button("Adicionar Material", commandf=lambda: submit_fluid(fluid_den_entry,fluid_name_entry,fluid_frame,list_of_widgets,fluid_type), rowint=5, columnspanint=2, ipadxint=100, padyint=10)

    fluid_window.create_Button("Remover material", lambda: delete_fluid(
        id_entry, fluid_frame, list_of_widgets), 7, columnspanint=2, ipadxint=100, padyint=10)
    
    fluid_frame.create_Label("Nome", 1, 2, stickystr='W')
    fluid_frame.create_Label("Tipo de fluido", 1, 3, stickystr='W')
    fluid_frame.create_Label("Densidade(kg/m3)", 1, 4, stickystr='W')
    fluid_frame.create_Label("ID", 1, 5, stickystr='W')

    fluid_window.create_Label("ID: ", 6, 0, stickystr='W')
    id_entry = fluid_window.create_Entry(6, 1, stickystr='W')

    i = 2
    list_of_widgets = []

    conn = sqlite3.connect('storage2.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM fluids_list")
    records = c.fetchall()
    conn.commit()
    conn.close()

    for fluids in records:
        for j in range(len(fluids)):
            if j == 1:
                if fluids[j] == False:
                    e = fluid_frame.create_Label("Básico", i, j+2)
                else:
                    e = fluid_frame.create_Label("Agressivo", i, j+2)
            else:
                e = fluid_frame.create_Label(fluids[j], i, j+2)
            list_of_widgets.append(e)
        i += 1