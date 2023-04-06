import tkinter as tk
import tkinter.ttk as ttk
from GUI2 import *
from enum import Enum
from mat_window import *



if __name__ == '__main__':

    root = GUI(WindowType.main, "PV_DPL", mat_window=mat_window)

    input_frame = root.create_LabelFrame(
        "Dados de Entrada", padxint=10, padyint=10)

    proj_name_label = input_frame.create_Label(
        "Nome do Projeto:", 0, 0, stickystr='W')
    proj_name_input = input_frame.create_Entry(0, 1, stickystr='W')

    diam_label = input_frame.create_Label(
        "Diâmetro Interno(mm):", 1, 0, stickystr='W')
    diam_input = input_frame.create_Entry(1, 1, stickystr='W')

    length_label = input_frame.create_Label(
        "Comprimento do casco(mm):", 2, 0, stickystr='W')
    length_input = input_frame.create_Entry(2, 1, stickystr='W')

    pressure_label = input_frame.create_Label(
        "Pressão de Projeto(MPa):", 3, 0, stickystr='W')
    pressure_input = input_frame.create_Entry(3, 1, stickystr='W')

    weld_efficiency_label = input_frame.create_Label(
        "Eficiência de Junta:", 4, 0, stickystr='W')
    weld_efficiency_input = input_frame.create_Entry(4, 1, stickystr='W')

    root.window.mainloop()