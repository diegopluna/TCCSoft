from tkinter import *
import sqlite3
from GUI import *

conn = sqlite3.connect('storage.db')
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS materials_list (
  mat_name text PRIMARY KEY,
  adm_tension float
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS results (
name text PRIMARY KEY,
diameter float,
pressure float,
weld_eff float,
shell_type text,
shell_mat text,
head_type text,
head_mat text,
cone_angle float,
shell_thick float,
head_thick float
)
""")
conn.commit()
conn.close()


def mat_db_wdw():
    mat_db = GUI(window_type.mat_db,"Database de Materiais")

    mat_frame = mat_db.create_LabelFrame(
        "Lista de Materiais", rowint=1, columnint=2, padxint=10, padyint=10, rowspanint=15)

    mat_db.create_Label("Database de Materiais", rowint=0, columnspanint=4)

    mat_db.create_Label("Nome do material:", 1, 0, stickystr='W')

    mat_name_entry = mat_db.create_Entry(1, 1, stickystr='W')

    mat_db.create_Label(
        "Tensão Admissível do Material(MPa):", 2, 0, stickystr='W')

    mat_ten_entry = mat_db.create_Entry(2, 1, stickystr='W')

    mat_db.create_Button("Adicionar Material", commandf=lambda: submit(
        mat_ten_entry, mat_name_entry, mat_frame, list_of_widgets), rowint=3, columnspanint=2, ipadxint=100, padyint=10)

    mat_db.create_Button("Remover material", lambda: delete(
        id_entry, mat_frame, list_of_widgets), 5, columnspanint=2, ipadxint=100, padyint=10)

    mat_frame.create_Label("Nome", 1, 2, stickystr='W')

    mat_frame.create_Label("Valor(MPa)", 1, 3, stickystr='W')

    mat_frame.create_Label("ID", 1, 4, stickystr='W')

    mat_db.create_Label("ID: ", 4, 0, stickystr='W')

    id_entry = mat_db.create_Entry(4, 1, stickystr='W')

    i = 2
    list_of_widgets = []

    conn = sqlite3.connect('storage.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM materials_list")
    records = c.fetchall()
    conn.commit()
    conn.close()

    for materials in records:
        for j in range(len(materials)):
            e = mat_frame.create_Label(materials[j], i, j+2)
            list_of_widgets.append(e)
        i += 1
