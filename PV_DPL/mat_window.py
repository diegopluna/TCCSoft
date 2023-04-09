from tkinter import *
from GUI2 import *

conn = sqlite3.connect('storage2.db')
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS materials_list (
  mat_name text PRIMARY KEY,
  adm_tension float,
  mat_den float
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS fluids_list (
  fluid_name text PRIMARY KEY,
  fluid_type bool,
  fluid_den float
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS results (
name text PRIMARY KEY,
diameter float,
shell_len float,
pressure float,
shell_life int,
corr_t    float,
weld_eff float,
shell_mat text,
head_type text,
head_height float,
end_diam float,
head_mat text,
fluid    text,
fluid_level float,
saddle_A float,
saddle_angle int,
saddle_w float,
shell_thick float,
head_thick float
)
""")
conn.commit()
conn.close()


def mat_window():
    mat_window = GUI(WindowType.mat_window, "Database de Materiais")

    mat_frame = mat_window.create_LabelFrame(
        "Lista de Materiais", rowint=1, columnint=2, padxint=10, padyint=10, rowspanint=15)

    mat_window.create_Label("Database de Materiais", rowint=0, columnspanint=4)
    mat_window.create_Label("Nome do material:", 1, 0, stickystr='W')

    mat_name_entry = mat_window.create_Entry(1, 1, stickystr='W')

    mat_window.create_Label(
        "Tensão Admissível do Material(MPa):", 2, 0, stickystr='W')
    
    mat_ten_entry = mat_window.create_Entry(2, 1, stickystr='W')

    mat_window.create_Label(
        "Densidade do Material(kg/mm3):", 3, 0, stickystr='W')
    
    mat_den_entry = mat_window.create_Entry(3, 1, stickystr='W')

    mat_window.create_Button("Adicionar Material", commandf=lambda: submit_mat(
        mat_ten_entry, mat_name_entry, mat_frame, list_of_widgets, mat_den_entry), rowint=4, columnspanint=2, ipadxint=100, padyint=10)
    
    mat_window.create_Button("Remover material", lambda: delete_mat(
        id_entry, mat_frame, list_of_widgets), 6, columnspanint=2, ipadxint=100, padyint=10)
    
    mat_frame.create_Label("Nome", 1, 2, stickystr='W')
    mat_frame.create_Label("Tensão Admissível(MPa)", 1, 3, stickystr='W')
    mat_frame.create_Label("Densidade(kg/mm3)", 1, 4, stickystr='W')
    mat_frame.create_Label("ID", 1, 5, stickystr='W')

    mat_window.create_Label("ID: ", 5, 0, stickystr='W')
    id_entry = mat_window.create_Entry(5, 1, stickystr='W')

    i = 2
    list_of_widgets = []

    conn = sqlite3.connect('storage2.db')
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