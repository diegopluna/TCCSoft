import math
from GUI2 import *
from tkinter import messagebox
from create_pdf import create_pdf

# Calculo espessura do casco

##Tensão Circunferencial
def circunferencial_stress(P,S,E,R):
    if (P > 0.385*S*E):
        raise ValueError("Pressão de projeto excede 0.38 * Tensão admissível * Eficiência de Junta")
    circun_stress = (P*R)/(S*E - 0.6*P)
    if circun_stress > R/2:
        raise ValueError("Espessura excede metade do raio interno")
    return circun_stress

## Tensão longitudinal
def longitudinal_stress(P,S,E,R):
    if (P > 1.25*S*E):
        raise ValueError("Pressão de projeto excede 1.25 * Tensão admissível * Eficiência de Junta")
    long_stress = (P*R)/(2*S*E + 0.4*P)
    if long_stress > R/2:
        raise ValueError("Espessura excede metade do raio interno")
    return long_stress


# Calculo espessura dos tampos

## Tampo elipsoidal 2:1
def elipsoidal_head(P,D,S,E):
    elip_t = (P*D)/(2*S*E-0.2*P)
    return elip_t

##Tampo toro esférico; Raio da coroa igual a D do costado
def torospherical_head(P,L,S,E):
    toro_t = (0.885*P*L)/(S*E - 0.1*P)
    return toro_t

##Tampo hemisférico; Raio da coroa = R do casco
def hemispheric_head(P,L,S,E):
    hemi_t = (P*L)/(2*S*E - 0.2*P)
    return hemi_t

##Tampo cônico
def conical_head(H,D,P,S,E):
    R = D/2
    radian_alpha = math.atan(R/H)
    cos_alpha = math.cos(radian_alpha)
    alpha = (radian_alpha*180)/math.pi
    if alpha > 30:
        raise ValueError("Ângulo de cone superior a 30 graus")
    con_t = (P*D)/(2*cos_alpha(S*E - 0.6*P))
    return con_t

#Tampo toroconico
def toroconical_head(Di, D, H, P, S, E):
    Ri = Di/2
    R = D/2
    alpha = math.atan(H/(R-Ri))
    deg_alpha = (alpha*180)/math.pi
    if deg_alpha > 30:
        raise ValueError("Ângulo de cone superior a 30 graus")
    L = Di/(2*math.cos(alpha))
    toro_t = (P*L)/(S*E - 0.6*P)
    return toro_t

#Suportes
def head_weight(h_type,D, Di, head_t,fluid_den, fluid_level, mat_den, H):
    R = D/2
    
    if h_type == 1:
        inside_head_v = (math.pi * pow(D,3))/12
        outside_head_v = (math.pi * pow(D+2*head_t,3))/12
    elif h_type == 2:
        inside_head_v = 0.1694 * pow(D,3)
        outside_head_v = 0.1694 * pow(D+2*head_t,3)
    elif h_type == 3:
        inside_head_v = (4*math.pi * pow(R,3))/3
        outside_head_v = (4*math.pi * pow(R+head_t,3))/3
    elif h_type == 4:
        inside_head_v = 2*(math.pi *R*R*H)/3
        outside_head_v = 2*(math.pi *pow(R+head_t,2)*(H+head_t))/3
    elif h_type == 5:
        Ri = Di/2
        inside_head_v = 2*(math.pi*H/3)*(math.pow(R,2)+ R*Ri + math.pow(Ri,2))
        outside_head_v = 2*(math.pi*(H+head_t)/3)*(math.pow(R+head_t,2) + (R+head_t)*(Ri+head_t) + math.pow(Ri+head_t,2))
    fluid_w = fluid_den * inside_head_v * fluid_level
    mat_w = (outside_head_v - inside_head_v) * mat_den
    head_w = fluid_w + mat_w
    return head_w


def shell_weight(R, L,shell_t,mat_den,fluid_den,fluid_level):
    inside_base_area = math.pi * math.pow(R,2)
    inside_v = inside_base_area * L
    out_r = R + shell_t
    outside_base_area = math.pi * math.pow(out_r,2)
    outside_v = outside_base_area * L
    shell_v = outside_v - inside_v
    mat_w = shell_v * mat_den
    fluid_w = inside_v*fluid_den*fluid_level
    shell_w = mat_w + fluid_w
    return shell_w



def calculate(root, list_of_res, name, D, L, P, UF, Cor, E, shell_mat, h_type, H, Di, head_mat, fluid, fluid_level, A, Sa, B):

    clearGrid(list_of_res)
    data_in = [["Característica", "Valor", "Unidade", "Observação" ]]
    if not check_str_field(name, "Nome do projeto"):
        return

    if not check_float_field(D, "Diâmetro Interno"):
        return
    data_in.append(["Diâmetro Interno", f"{D.get()}", "mm", "-"])

    if not check_float_field(L, "Comprimento do casco"):
        return
    data_in.append(["Comprimento do casco", f"{L.get()}", "mm", "-"])

    if not check_float_field(P, "Pressão de projeto"):
        return
    data_in.append(["Pressão de Projeto", f"{P.get()}", "MPa", "-"])

    if not check_int_field(UF, "Vida útil do vaso"):
        return
    data_in.append(["Vida útil do vaso", f"{UF.get()}", "Anos", "-"])

    if Cor.get():
        if not check_float_field(Cor, "Sobreespessura de corrosão"):
            return
        data_in.append(["Sobreespessura de corrosão", f"{Cor.get()}", "mm", "Especificado pelo usuário"])
    else:
        data_in.append(["-","-","-","-"])
    
    if not check_float_field(E, "Eficiência de junta"):
        return
    data_in.append(["Eficiência de Junta", f"{E.get()}", "-", "-"])

    if not check_mat_field(shell_mat, "Material do casco"):
        return
    data_in.append(["Material do casco", shell_mat.get(), "-", "-" ])

    if h_type.get() == 1:
        data_in.append(["Tipo de tampo", "Elipsóidal 2:1", "-", "-"])
        data_in.append(
            ["Altura do tampo", f"{int(D.get())/4}", "mm", "-" ])
    elif h_type.get() == 2:
        data_in.append(["Tipo de tampo", "Toro Esférico", "-", "-"])
        data_in.append(
            ["Altura do tampo", f"{int(D.get())/3.8}", "mm", "-"])
    elif h_type.get() == 3:
        data_in.append(["Tipo de tampo", "Hemisférico", "-", "-"])
        data_in.append(
            ["Altura do tampo", f"{int(D.get())/2}", "mm", "-"])
    elif h_type.get() == 4:
        data_in.append(["Tipo de tampo", "Cônico", "-", "-"])
    else:
        data_in.append(["Tipo de tampo", "Toro Cônico", "-", "-"])
    
    if h_type.get() > 3:
        if not check_float_field(H, "Altura do tampo"):
            return
        data_in.append(
            ["Altura do tampo", f"{H.get()}", "mm", "-"])
        
        if h_type.get() == 5:
            if not check_float_field(Di,"Diâmetro final do tampo"):
                return
            data_in.append(["Diâmetro final do tampo", f"{Di.get()}", "mm", "-"])
    
    if not check_mat_field(head_mat, "Material do tampo"):
        return
    data_in.append(["Material do tampo", head_mat.get(), "-", "-"])

    if not check_fluid_field(fluid, "Fluido"):
        return
    data_in.append(["Fluido", fluid.get(), "-", "-"])

    if not check_float_field(fluid_level,"Nivel do fluido"):
        return
    data_in.append(["Nivel do Fluido",f"{fluid_level.get()}%","-","-"])

    if not check_float_field(A, "Distância (A) do suporte"):
        return
    data_in.append(["Distância (A) do suporte", f"{A.get()}", "mm","-"])

    data_in.append(["Ângulo do suporte", f"{Sa.get()}", "Graus", "-"])

    if not check_float_field(B, "Largura do suporte"):
        return
    data_in.append(["Largura do suporte", f"{B.get()}", "mm","-"])

    data_out = [["Característica", "Valor", "Unidade", "Observação"]]

    frame_res = root.create_LabelFrame(
        "Resultados", 0, 2, 2, padxint=10, padyint=10, rowspanint=15)
    list_of_res.append(frame_res)


    # Puxando os dados dos campos

    P = float(P.get())
    E = float(E.get())
    D = float(D.get())
    R = D/2
    S = get_mat_tension(shell_mat)
    Sh = get_mat_tension(head_mat)
    L = float(L.get())
    UL= int(UF.get())
    h_type = h_type.get()
    A = float(A.get())
    Sa = Sa.get()
    B = float(B.get())
    if h_type == 1:
        H = D/4
    elif h_type == 2:
        H = D/3.8
    elif h_type == 3:
        H = R
    elif h_type == 4:
        H = float(H.get())
    elif h_type==5:
        H = float(H.get())
        Di = float(Di.get())

    
    try:
        circun_stress = circunferencial_stress(P,S,E,R)
    except ValueError as e:
        return messagebox.showerror("Erro!",str(e))
    
    try:
        long_stress = longitudinal_stress(P,S,E,R)
    except ValueError as e:
        return messagebox.showerror("Erro!",str(e))
    
    if Cor.get():
        corr = float(Cor.get())
    else:
        if get_fluid_type(fluid) == True:
            corr = 6
        else:
            corr = 0.127*UL

    data_in[5] = (["Sobreespessura de corrosão", f"{corr}", "mm", "Usuário não especificou, dado calculado"])

    shell_t = max(circun_stress,long_stress) + corr # Pegando o maximo e adicionando a sobreespessura de corrosão

    if h_type == 1:
        head_t = elipsoidal_head(P,D,Sh,E)
    elif h_type == 2:
        head_t = torospherical_head(P,D,Sh,E)
    elif h_type == 3:
        head_t = hemispheric_head(P,R,Sh,E)
    elif h_type == 4:
        try:
            head_t = conical_head(H,D,P,Sh,E)
        except ValueError as e:
            return messagebox.showerror("Erro!",str(e))
    elif h_type == 5:
        try:
            head_t = toroconical_head(Di,D,H,P,Sh,E)
        except ValueError as e:
            return messagebox.showerror("Erro!",str(e))



    head_t += corr

    #######
    H0 = H + head_t
    Lss = L - 2*A
    Lt = L + 2*H0
    shell_mat_den = get_mat_den(shell_mat)
    head_mat_den = get_mat_den(head_mat)
    fluid_den = get_fluid_den(fluid)
    fluid_level = float(fluid_level.get())/100
    total_w = shell_weight(R, L, shell_t, shell_mat_den, fluid_den, fluid_level) + head_weight(h_type,D, Di, head_t,fluid_den,fluid_level,head_mat_den,H)
    Q = total_w/2

    if A > R/2:
        messagebox.showinfo(
            "Erro", "A distância entre suportes excede os limites da norma")
        return
    
    if Sa == 120:
        K2=0.880
        K3=0.0132
        K4=0.401
    else:
        K2=0.485
        K3=0.0079
        K4=0.297
    
    ##Tensao cisalhante
    S1 = (P*R)/(2*E*shell_t) #MPa
    S1s = 0.8 * S1
    #Tensao cisalhante no costado para A <= R/2
    S2 = (Q * K2)/(shell_t * R) 

    print(S2)
    print(S1s)
    if S2/S1s >= 1:
        messagebox.showinfo(
            "Erro", "A tensão cisalhante no costado excede a tensão cisalhante admissível")
        return
    #Tensao cisalhante nos tampos para A <= R/2
    S2h = (Q * K2)/(head_t * R)
    if S2h/S1s >= 1:
        messagebox.showinfo(
            "Erro", "A tensão cisalhante no tampo excede a tensão cisalhante admissível")
        return
    #Tensao adicional no tampo
    S3 = (Q * K4)/(head_t * R)
    if S3/(1.25*S1) >= 1:
        messagebox.showinfo(
            "Erro", "A tensão adicional no tampo excede a tensão cisalhante admissível")
        return
    
    if L >= 8*R:
        S4=-(Q/(4*shell_t*(B+10*shell_t)))-((3*K3*Q)/(2*pow(shell_t,2)))
    else:
        S4=-(Q/(4*shell_t*(B+10*shell_t)))-((12*K3*Q*R)/(L*pow(shell_t,2)))
    
    if S4 >= 1.5*S1:
        messagebox.showinfo("Erro","Tensão do suporte excede os limites impostos")
        return
    #########################
    data_out.append(["Espessura mínima do casco",
                    f"{shell_t:.3f}", "mm", "-" ])
    
    shell_thick_label = frame_res.create_Label(
        "Espessura do casco:", 1, 3, stickystr='W')
    list_of_res.append(shell_thick_label)

    shell_thick_res = frame_res.create_Label(
        f'{shell_t:.3f} mm', 1, 4, stickystr='W')
    list_of_res.append(shell_thick_res)

    data_out.append(["Espessura mínima do tampo",
                    f"{head_t:.3f}", "mm", "-"])
    head_thick_label = frame_res.create_Label(
        "Espessura do tampo:", 2, 3, stickystr='W')
    list_of_res.append(head_thick_label)

    head_thick_res = frame_res.create_Label(
        f'{head_t:.3f} mm', 2, 4, stickystr='W')
    list_of_res.append(head_thick_res)

    name = name.get()
    pdf_button = root.create_Button("Gerar PDF", lambda: create_pdf(
        name, data_in, data_out), 5, 2, 2, ipadxint=100, padyint=10, padxint=10)
    list_of_res.append(pdf_button)