from GUI2 import *
from mat_window import *
from fluid_window import *
from calc2 import *


if __name__ == '__main__':

    root = GUI(WindowType.main, "PV_DPL", mat_window=mat_window, fluid_window=fluid_window)

    input_frame = root.create_LabelFrame(
        "Dados de Entrada", padxint=10, padyint=10,rowint=0,columnint=0)

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

    vessel_life_label = input_frame.create_Label("Vida útil(anos):", 4, 0,stickystr='W')
    vessel_life_entry = input_frame.create_Entry(4,1,stickystr='W')

    corrosion_label = input_frame.create_Label("*Sobreespessura de corrosão(mm):",5,0,stickystr='W')
    corrosion_entry = input_frame.create_Entry(5,1,stickystr='W')

    weld_efficiency_label = input_frame.create_Label(
        "Eficiência de Junta:", 6, 0, stickystr='W')
    weld_efficiency_input = input_frame.create_Entry(6, 1, stickystr='W')

    shell_material_label = input_frame.create_Label(
        "Tipo de Material do Casco:", 7, 0, stickystr='W')
    
    shell_material_combobox = input_frame.create_Combobox(
        "Escolha uma opção", 7, 1, postcommandf=lambda: update_cblist(shell_material_combobox))
    
    head = IntVar()
    head_type_label = input_frame.create_Label(
        "Tipo de tampo:", 8, 0, stickystr='W')
    head_type_1 = input_frame.create_RadioButton("Elipsóidal 2:1", head,
                                                 1, lambda: show_head_height(head_height_entry, False, end_diam_entry, False), 8, 1, stickystr='W')
    head_type_2 = input_frame.create_RadioButton("Toro Esférico", head,
                                                 2, lambda: show_head_height(head_height_entry, False, end_diam_entry, False), 9, 1, stickystr='W')
    head_type_3 = input_frame.create_RadioButton("Hemisférico", head,
                                                 3, lambda: show_head_height(head_height_entry, False, end_diam_entry, False), 10, 1, stickystr='W')
    head_type_4 = input_frame.create_RadioButton("Cônico", head,
                                                 4, lambda: show_head_height(head_height_entry, True, end_diam_entry, False), 11, 1, stickystr='W')
    head_type_5 = input_frame.create_RadioButton("Toro Cônico", head,
                                                 5, lambda: show_head_height(head_height_entry, True, end_diam_entry, True), 12, 1, stickystr='W')

    head_height_label = input_frame.create_Label(
        "Altura do tampo(mm):", 13, 0, stickystr='W')
    head_height_entry = input_frame.create_Entry(13, 1, stickystr='W')
    
    end_diam_label = input_frame.create_Label(
        "Diâmetro final do tampo(mm):", 14, 0, stickystr='W')
    end_diam_entry = input_frame.create_Entry(14, 1, stickystr='W')

    head_material_label = input_frame.create_Label(
        "Tipo de material do tampo:", 15, 0, stickystr='W')
    
    head_material_combobox = input_frame.create_Combobox(
        "Escolha uma opção", 15, 1, postcommandf=lambda: update_cblist(head_material_combobox))
    
    fluid_label = input_frame.create_Label(
        "Fluido:", 16, 0, stickystr='W')
    fluid_combobox = input_frame.create_Combobox(
        "Escolha uma opção", 16, 1, postcommandf=lambda: update_cblist2(fluid_combobox))
    
    fluid_level_label = input_frame.create_Label(
        "Nível do fluido no vaso(%):", 17, 0, stickystr='W')
    fluid_level_entry = input_frame.create_Spinbox(
        0, 100, 17, 1, stickystr='W')
    
    saddle_A_label = input_frame.create_Label(
        "Distância (A) do suporte(mm):", 18, 0, stickystr='W')
    saddle_A_input = input_frame.create_Entry(18, 1, stickystr='W')
    
    saddle_angle = IntVar()
    saddle_angle_label = input_frame.create_Label(
        "Ângulo do suporte:", 19, 0, stickystr='W')
    saddle_angle_120 = input_frame.create_RadioButton(
        "120°", saddle_angle, 120, None, 19, 1, stickystr="W")
    saddle_angle_150 = input_frame.create_RadioButton(
        "150°", saddle_angle, 150, None, 20, 1, stickystr="W")
    

    opt_label = root.create_Label("*Opcional, se deixado em branco será considerado:\n 0.127mm por ano de vida útil para fluidos básicos,\n 6mm ao longo da vida para fluidos agressivos.",rowint=1,columnint=0,stickystr='W')

    calc_button = root.create_Button("Calcular",rowint=2,columnspanint=2,ipadxint=100,padyint=10, commandf= lambda: calculate(root, list_of_res,proj_name_input, diam_input, length_input, pressure_input,vessel_life_entry, corrosion_entry, weld_efficiency_input, shell_material_combobox, head, head_height_entry, end_diam_entry, head_material_combobox, fluid_combobox, fluid_level_entry))

    list_of_res = []

    root.window.mainloop()