from tkinter import *
from GUI import *
import sqlite3


def res_db_wdw():
    res_db = GUI(window_type.res_db, "Histórico de Resultados")

    res_frame = res_db.create_LabelFrame(
        'Histórico de Projetos', 0, columnspanint=12, padyint=10, padxint=10)

    res_frame.create_Label('Nome do Vaso', 0, 0)

    res_frame.create_Label('Diâmetro Interno', 0, 1)

    res_frame.create_Label('Pressão de Projeto', 0, 2)

    res_frame.create_Label('Eficiência de Junta', 0, 3)

    res_frame.create_Label('Tipo de Casco', 0, 4)

    res_frame.create_Label('Material do Casco', 0, 5)

    res_frame.create_Label('Tipo de Tampo', 0, 6)

    res_frame.create_Label('Material do Tampo', 0, 7)

    res_frame.create_Label('Ângulo de Cone', 0, 8)

    res_frame.create_Label('Espessura mínima do Casco', 0, 9)

    res_frame.create_Label('Espessura mínima do Tampo', 0, 10)

    res_frame.create_Label('ID', 0, 11)

    i = 1
    res_list = []
    conn = sqlite3.connect('storage.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM results")
    records = c.fetchall()
    conn.commit()
    conn.close()

    for results in records:
        for j in range(len(results)):
            res = res_frame.create_Label(results[j], i, j)
            res_list.append(res)
        i += 1

    res_db.create_Label("ID:", 10, 0)

    identry = res_db.create_Entry(10, 1)

    res_db.create_Button('Remover Vaso', lambda: delete_res(
        identry, res_frame, res_list), 10, 2, ipadxint=100, padyint=10)

    res_db.create_Button("Gerar PDF",
                         lambda: pdf_res(identry), 10, 3, ipadxint=100, padyint=10)
