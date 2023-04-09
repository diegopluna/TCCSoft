from tkinter import *
from GUI2 import *
import sqlite3

def res_window():
    res_db = GUI(WindowType.res_window, "Histórico de Resultados")

    res_frame = res_db.create_LabelFrame(
        'Histórico de Projetos', 0, columnspanint=12, padyint=10, padxint=10)

    res_frame.create_Label('Nome do Vaso', 0, 0)

    res_frame.create_Label('ID', 0, 11)

    i = 1
    res_list = []
    conn = sqlite3.connect('storage2.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM results")
    records = c.fetchall()
    conn.commit()
    conn.close()

    for results in records:
        res = res_frame.create_Label(results[0],i,0)
        id = res_frame.create_Label(results[19],i,1)
        res_list.append(res)
        res_list.append(id)
        i += 1

    res_db.create_Label("ID:", 10, 0)

    identry = res_db.create_Entry(10, 1)

    res_db.create_Button('Remover Vaso', lambda: delete_res(
        identry, res_frame, res_list), 10, 2, ipadxint=100, padyint=10)

    res_db.create_Button("Gerar PDF",
                         lambda: pdf_res(identry), 10, 3, ipadxint=100, padyint=10)
