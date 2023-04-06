import tkinter as tk
import tkinter.ttk as ttk
from GUI2 import *
from enum import Enum
from mat_window import *
from fluid_window import *



if __name__ == '__main__':

    root = GUI(WindowType.main, "PV_DPL", mat_window=mat_window, fluid_window=fluid_window)

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

    shell_material_label = input_frame.create_Label(
        "Tipo de Material do Casco:", 5, 0, stickystr='W')
    
    shell_material_combobox = input_frame.create_Combobox(
        "Escolha uma opção", 5, 1, postcommandf=lambda: update_cblist(shell_material_combobox))
    
    head = IntVar()
    head_type_label = input_frame.create_Label(
        "Tipo de tampo:", 6, 0, stickystr='W')
    head_type_1 = input_frame.create_RadioButton("Elipsóidal 2:1", head,
                                                 1, lambda: show_head_height(head_height_entry, False, end_diam_entry, False), 6, 1, stickystr='W')
    head_type_2 = input_frame.create_RadioButton("Toro Esférico", head,
                                                 2, lambda: show_head_height(head_height_entry, False, end_diam_entry, False), 7, 1, stickystr='W')
    head_type_3 = input_frame.create_RadioButton("Hemisférico", head,
                                                 3, lambda: show_head_height(head_height_entry, False, end_diam_entry, False), 8, 1, stickystr='W')
    head_type_4 = input_frame.create_RadioButton("Cônico", head,
                                                 4, lambda: show_head_height(head_height_entry, True, end_diam_entry, False), 9, 1, stickystr='W')
    # head_type_5 = input_frame.create_RadioButton("Toro Cônico", head,
    #                                              5, lambda: show_head_height(head_height_label, head_height_entry, True, end_diam_label, end_diam_entry, True), 10, 1, stickystr='W')

    head_height_label = input_frame.create_Label(
        "Altura do tampo(mm):", 11, 0, stickystr='W')
    head_height_entry = input_frame.create_Entry(11, 1, stickystr='W')
    
    end_diam_label = input_frame.create_Label(
        "Diâmetro final do tampo(mm):", 12, 0, stickystr='W')
    end_diam_entry = input_frame.create_Entry(12, 1, stickystr='W')

    head_material_label = input_frame.create_Label(
        "Tipo de material do tampo:", 13, 0, stickystr='W')
    
    head_material_combobox = input_frame.create_Combobox(
        "Escolha uma opção", 13, 1, postcommandf=lambda: update_cblist(head_material_combobox))
    
    fluid_label = input_frame.create_Label(
        "Fluido:", 14, 0, stickystr='W')
    fluid_combobox = input_frame.create_Combobox(
        "Escolha uma opção", 14, 1, postcommandf=lambda: update_cblist2(fluid_combobox))
    
    fluid_level_label = input_frame.create_Label(
        "Nível do fluido no vaso(%):", 15, 0, stickystr='W')
    fluid_level_entry = input_frame.create_Spinbox(
        0, 100, 15, 1, stickystr='W')
    
    

    root.window.mainloop()