
from tkinter import *
from GUI import *
from matdb import *
from resdb import *
from calc import *


if __name__ == '__main__':

    root = GUI(window_type.main, "Programa Vasos",
               mat_db_wdw=mat_db_wdw, res_db_wdw=res_db_wdw)

    input_frame = root.create_LabelFrame(
        "Dados de Entrada", padxint=10, padyint=10)

    proj_name_label = input_frame.create_Label(
        "Nome do Projeto:", 0, 0, stickystr='W')
    proj_name_input = input_frame.create_Entry(0, 1, stickystr='W')

    diam_label = input_frame.create_Label(
        "Diâmetro Interno(mm):", 1, 0, stickystr='W')
    diam_input = input_frame.create_Entry(1, 1, stickystr='W')

    pressure_label = input_frame.create_Label(
        "Pressão de Projeto(MPa):", 2, 0, stickystr='W')
    pressure_input = input_frame.create_Entry(2, 1, stickystr='W')

    weld_efficiency_label = input_frame.create_Label(
        "Eficiência de Junta:", 3, 0, stickystr='W')
    weld_efficiency_input = input_frame.create_Entry(3, 1, stickystr='W')

    shell_material_label = input_frame.create_Label(
        "Tipo de Material do Casco:", 4, 0, stickystr='W')
    shell_material_combobox = input_frame.create_Combobox(
        "Escolha uma opção", 4, 1, postcommandf=lambda: update_cblist(shell_material_combobox))

    head = IntVar()
    saddle_A_label = input_frame.create_Label(
        "Distância entre suportes:", 5, 0, stickystr='W')
    saddle_A_input = input_frame.create_Entry(5, 1, stickystr='W')

    saddle_angle = IntVar()
    saddle_angle_label = input_frame.create_Label(
        "Ângulo do suporte:", 6, 0, stickystr='W')
    saddle_angle_120 = input_frame.create_RadioButton(
        "120°", saddle_angle, 120, None, 6, 1)
    saddle_angle_150 = input_frame.create_RadioButton(
        "150°", saddle_angle, 150, None, 7, 1)

    length_label = input_frame.create_Label(
        "Comprimento do casco(mm):", 8, 0, stickystr='W')
    length_input = input_frame.create_Entry(8, 1, stickystr='W')

    head_type_label = input_frame.create_Label(
        "Tipo de tampo:", 9, 0, stickystr='W')
    head_type_1 = input_frame.create_RadioButton("Elipsóidal 2:1", head,
                                                 1, lambda: show_head_height(head_height_label, head_height_entry, False, end_diam_label, end_diam_entry, False), 9, 1, stickystr='W')
    head_type_2 = input_frame.create_RadioButton("Toro Esférico", head,
                                                 2, lambda: show_head_height(head_height_label, head_height_entry, False, end_diam_label, end_diam_entry, False), 10, 1, stickystr='W')
    head_type_3 = input_frame.create_RadioButton("Hemisférico", head,
                                                 3, lambda: show_head_height(head_height_label, head_height_entry, False, end_diam_label, end_diam_entry, False), 11, 1, stickystr='W')
    head_type_4 = input_frame.create_RadioButton("Cônico", head,
                                                 4, lambda: show_head_height(head_height_label, head_height_entry, True, end_diam_label, end_diam_entry, False), 12, 1, stickystr='W')
    head_type_5 = input_frame.create_RadioButton("Toro Cônico", head,
                                                 5, lambda: show_head_height(head_height_label, head_height_entry, True, end_diam_label, end_diam_entry, True), 13, 1, stickystr='W')
    head_height_label = input_frame.create_Label(
        "Altura do tampo(mm):", show=False)
    head_height_entry = input_frame.create_Entry(show=False)

    end_diam_label = input_frame.create_Label(
        "Diâmetro final do tampo(mm):", show=False)
    end_diam_entry = input_frame.create_Entry(show=False)

    head_material_label = input_frame.create_Label(
        "Tipo de material do tampo:", 14, 0)

    head_material_combobox = input_frame.create_Combobox(
        "Escolha uma opção", 14, 1, postcommandf=lambda: update_cblist(head_material_combobox))

    fluid_label = input_frame.create_Label(
        "Densidade do fluido(kg/mm3):", 17, 0, stickystr='W')
    fluid_entry = input_frame.create_Entry(17, 1, stickystr='W')

    fluid_level_label = input_frame.create_Label(
        "Nível do fluido no vaso(%):", 18, 0, stickystr='W')
    fluid_level_entry = input_frame.create_Spinbox(
        0, 100, 18, 1, stickystr='W')

    saddle_width_label = input_frame.create_Label("Largura do suporte:",19,0,stickystr='W')
    saddle_width_entry = input_frame.create_Entry(19,1,stickystr='W')

    calc_button = root.create_Button("Calcular", rowint=20, columnspanint=2, ipadxint=100, padyint=10, commandf=lambda: calculate(
        pressure_input, weld_efficiency_input, diam_input, shell_material_combobox, head_material_combobox, head, head_height_entry,
        root, proj_name_input, list_of_res, saddle_A_input, saddle_angle, length_input, fluid_entry, fluid_level_entry ,end_diam_entry,saddle_width_entry))

    list_of_res = []

    root.window.mainloop()
