import math
from tkinter import *
from GUI import *
from tkinter import messagebox
from create_pdf import create_pdf
from res import *


def calculate(pre, weld_eff, diam, shell_mat, head_mat, head, head_height, root, proj_name, list_of_res, saddle_A, saddle_angle, shell_length,fluid_dens,fluid_level,end_diam,saddle_width):

    clearGrid(list_of_res)

    data_in = [["Característica", "Valor", "Unidade", ]]
    if not check_str_field(proj_name, "Nome do projeto"):
        return

    if not check_float_field(diam, "Diâmetro Interno"):
        return
    data_in.append(["Diâmetro Interno", f"{diam.get()}", "mm", ])
    if not check_float_field(pre, "Pressão de projeto"):
        return
    data_in.append(["Pressão de Projeto", f"{pre.get()}", "MPa", ])
    if not check_float_field(weld_eff, "Eficiência de junta"):
        return
    data_in.append(["Eficiência de Junta", f"{diam.get()}", "-", ])
    if not check_mat_field(shell_mat, "Material do casco"):
        return
    data_in.append(["Material do casco", shell_mat.get(), "-", ])
    if not check_float_field(saddle_A, "Distância entre suportes"):
        return
    data_in.append(["Distância entre suportes", f"{saddle_A.get()}", "mm"])
    if not check_radio_field(saddle_angle, "Ângulo do suporte", 120, 150):
        return
    data_in.append(["Ângulo do Suporte", f"{saddle_angle.get()}", "Graus"])
    if not check_float_field(shell_length, "Comprimento do casco"):
        return
    data_in.append(["Comprimento do casco", f"{shell_length.get()}", "mm"])
    if not check_radio_field(head, "Tipo de tampo", 1, 5):
        return
    if head.get() == 1:
        data_in.append(["Tipo de tampo", "Elipsóidal 2:1", "-", ])
        data_in.append(
            ["Altura do tampo", f"{int(diam.get())/4}", "mm", ])
    elif head.get() == 2:
        data_in.append(["Tipo de tampo", "Toro Esférico", "-", ])
        data_in.append(
            ["Altura do tampo", f"{int(diam.get())/3.8}", "mm", ])
    elif head.get() == 3:
        data_in.append(["Tipo de tampo", "Hemisférico", "-", ])
        data_in.append(
            ["Altura do tampo", f"{int(diam.get())/2}", "mm", ])
    elif head.get() == 4:
        data_in.append(["Tipo de tampo", "Cônico", "-", ])
    else:
        data_in.append(["Tipo de tampo", "Toro Cônico", "-", ])
        if not check_float_field(end_diam,"Diâmetro final do tampo"):
            return
        data_in.append(["Diâmetro final do tampo", f"{end_diam.get()}", "mm", ])
    if head.get() > 3:
        if not check_float_field(head_height, "Altura do tampo"):
            return
        data_in.append(
            ["Altura do tampo", f"{head_height.get()}", "mm", ])
    if not check_mat_field(head_mat, "Material do tampo"):
        return
    data_in.append(["Material do tampo", head_mat.get(), "-", ])
    if not check_float_field(fluid_dens,"Densidade do fluido"):
        return
    data_in.append(["Densidade do Fluido",f"{fluid_dens.get()}","kg/mm3"])
    if not check_float_field(fluid_level,"Nivel do fluido"):
        return
    data_in.append(["Nivel do Fluido",f"{fluid_level.get()}%","-"])
    data_out = [["Característica", "Valor", "Unidade", ]]
    if not check_float_field(saddle_width,"Largura do suporte"):
        return
    data_in.append(["Largura do Suporte",f"{saddle_width.get()}","mm"])

    frame_res = root.create_LabelFrame(
        "Resultados", 0, 2, 2, padxint=10, padyint=10, rowspanint=15)

    list_of_res.append(frame_res)

    # Puxando os dados dos campos

    P = float(pre.get())
    WE = float(weld_eff.get())
    D = float(diam.get())
    S = get_valor(shell_mat)
    S1 = get_valor(head_mat)
    La = float(saddle_A.get())
    Sa = float(saddle_angle.get())

    Ls = float(shell_length.get())
    head_type = head.get()
    if head_type == 4:
        Hint = head_height.get()
    elif head_type==5:
        Hint = head_height.get()
    if La > Ls:
        messagebox.showinfo(
            "Erro", "A distância entre suportes tem que ser menor que o comprimento do casco")
        return

    A = (Ls - La)/2
    # Calculando raio e raio de coroa
    R = D/2
    L = 0.9*D

    if A > R/2:
        messagebox.showinfo(
            "Erro", "A distância entre suportes excede os limites da norma")
    if Sa == 120:
        K2=0.880
        K3=0.0132
        K4=0.401
    else:
        K2=0.485
        K3=0.0079
        K4=0.297
    # Calculo espessura do casco e tampo
    if P <= 0.385*S*WE:
        circunf_thick = (P*R)/(S*WE - 0.6*P)
    else:
        messagebox.showinfo(
            "Erro", "O valor da pressão de projeto excede aos limites da norma ASME.\nConsidere trocar de material")
        return
    if P <= 1.25*S*WE:
        long_thick = (P*R)/(2*S*WE + 0.4*P)
    else:
        messagebox.showinfo(
            "Erro", "O valor da pressão de projeto excede aos limites da norma ASME.\nConsidere trocar de material")
        return
    shell_thick = max(circunf_thick, long_thick)

    OD = D + 2*shell_thick
    OR = OD/2

    if head_type == 1:
        Hint=D/4
        head_thick = (P*D)/(2*S1*WE - 0.2*P)
        V_head_int = (math.pi * pow(D,3))/12
        V_head_out = (math.pi * pow(D+2*head_thick,3))/12
        Salt=((P*D/head_thick)+0.2*P)/(2*WE)
    elif head_type == 2:
        Hint=D/3.8
        head_thick = (0.885*P*L)/(S1*WE-0.1*P)
        V_head_int = 0.1694 * pow(D,3)
        V_head_out = 0.1694 * pow(D+2*head_thick,3)
        Salt=((0.885*P*L/head_thick)+0.1*P)/(WE)
    elif head_type == 3:
        Hint=R
        head_thick = (P*L)/(2*S1*WE-0.2*P)
        V_head_int = (4*math.pi * pow(R,3))/3
        V_head_out = (4*math.pi * pow(R+head_thick,3))/3
        Salt=((P*L/head_thick)+0.2*P)/(2*WE)
    elif head_type == 4:
        alpha=math.tan(Hint/R)
        head_thick = (P*D)/(2*math.cos(alpha)*(S1*WE-0.6*P))
        V_head_int = 2*(math.pi *R*R*Hint)/3
        V_head_out = 2*(math.pi *pow(R+head_thick,2)*(Hint+head_thick))/3
        Salt=((P*D/(2*math.cos(alpha)*head_thick))+0.6*P)/WE
    elif head_type == 5:
        Dh=end_diam.get()
        Rh=Dh/2
        alpha=math.tan(Hint/(R-Rh))
        Di = L*2*math.cos(alpha)
        head_thick = (P*Di)/(2*math.cos(alpha)*(S*WE-0.6*P))
        V_head_int = 2*(math.pi*Hint/3)*(R*R + R*Rh + Rh*Rh)
        V_head_out = 2*(math.pi*(Hint+head_thick)/3)*(pow(R+head_thick,2) + (R+head_thick)*Rh + Rh*Rh)
        Salt=((P*Di/(2*math.cos(alpha)*head_thick))+0.6*P)/WE


    #Calculo suportes


    fluid_lvl=float(fluid_level.get())/100
    fluid_density=float(fluid_dens.get())

    V_shell_int= math.pi*R*R*Ls #mm3
    V_shell_out= math.pi*OR*OR*Ls
    V_shell_mat= V_shell_out - V_shell_int
    Vint= V_head_int + V_shell_int #mm3
    V_head_mat = V_head_out - V_head_int
    V_mat = V_shell_mat + V_head_mat
    Mat_weight = V_mat * 7.8E-6
    Fluid_weight = Vint * fluid_lvl * fluid_density
    Total_weight = Mat_weight + Fluid_weight
    Q =Total_weight/2
    b=float(saddle_width.get())
    S2=((K2*Q)/(R*shell_thick))*((Ls-2*A)/(L + Hint*4/3))
    if S2 > 0.8*S:
        messagebox.showinfo("Erro","Tensão do suporte excede os limites impostos")
        return
    if Ls >= 8*R:
        S3=-(Q/(4*shell_thick*(b+10*shell_thick)))-((3*K3*Q)/(2*pow(shell_thick,2)))
    else:
        S3=-(Q/(4*shell_thick*(b+10*shell_thick)))-((12*K3*Q*R)/(Ls*pow(shell_thick,2)))
    
    if S3 > 1.5*S:
        messagebox.showinfo("Erro","Tensão do suporte excede os limites impostos")
        return
    
    S4=(K4*Q)/(R*head_thick)
    S4 += Salt

    if S4 > 1.25*S1:
        messagebox.showinfo("Erro","Tensão do suporte excede os limites impostos")
        return

    ## Calculo Aberturas
    if D <= 1520:
        Da=D/2
        if Da > 510:
            Da=510
    else:
        Da=D/3
        if Da > 1020:
            Da=1020



    #############################################

    data_out.append(["Espessura mínima do casco",
                    f"{shell_thick:.2f}", "mm", ])

    shell_thick_label = frame_res.create_Label(
        "Espessura do casco:", 1, 3, stickystr='W')
    list_of_res.append(shell_thick_label)

    shell_thick_res = frame_res.create_Label(
        f'{shell_thick:.2f} mm', 1, 4, stickystr='W')
    list_of_res.append(shell_thick_res)

    saddle_dist_label= frame_res.create_Label("Distância casco-suporte:",3,3,stickystr='W')
    list_of_res.append(saddle_dist_label)
    saddle_dist = frame_res.create_Label(f'{A:.2f} mm',3,4,stickystr='W')
    list_of_res.append(saddle_dist)

    data_out.append(["Espessura mínima do tampo",
                    f"{head_thick:.2f}", "mm", ])
    head_thick_label = frame_res.create_Label(
        "Espessura do tampo:", 2, 3, stickystr='W')
    list_of_res.append(head_thick_label)

    head_thick_res = frame_res.create_Label(
        f'{head_thick:.2f} mm', 2, 4, stickystr='W')
    list_of_res.append(head_thick_res)

    name = proj_name.get()
    pdf_button = root.create_Button("Gerar PDF", lambda: create_pdf(
        name, data_in, data_out), 20, 2, 2, ipadxint=100, padyint=10, padxint=10)
    list_of_res.append(pdf_button)

    shell_name = "Cilíndrico"
    if head_type == 1:
        head_name = "Elipsóidal 2:1"
        x = results(name, D, P, WE, shell_name, shell_mat.get(
        ), head_name, head_mat.get(), None, head_thick, shell_thick)
    elif head_type == 2:
        head_name = "Toro Esférico"
        x = results(name, D, P, WE, shell_name, shell_mat.get(
        ), head_name, head_mat.get(), None, head_thick, shell_thick)
    elif head_type == 3:
        head_name = "Hemisférico"
        x = results(name, D, P, WE, shell_name, shell_mat.get(
        ), head_name, head_mat.get(), None, head_thick, shell_thick)
    elif head_type == 4:
        head_name = "Cônico"
        x = results(name, D, P, WE, shell_name, shell_mat.get(
        ), head_name, head_mat.get(), head_height.get(), head_thick, shell_thick)
    else:
        head_name = "Toro Cônico"
        x = results(name, D, P, WE, shell_name, shell_mat.get(
        ), head_name, head_mat.get(), head_height.get(), head_thick, shell_thick)

    x.save()
