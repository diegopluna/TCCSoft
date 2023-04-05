import math


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

##Tampo toroconico Não usar por enquanto
### def toroconical_head():
####     Di = 

#Suportes
def head_weight(h_type,D,head_t,fluid_den, fluid_level, mat_den, H):
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



def calculate(P,S,L,E,D,h_type,Sh,H,Dh):
    R = D/2
    try:
        circun_stress = circunferencial_stress(P,S,E,R)
    except ValueError:
        return ##Alerta tkinter
    
    try:
        long_stress = longitudinal_stress(P,S,E,R)
    except ValueError:
        return ## Alerta tkinter
    

    #Rever norma sobre corrosão
    shell_t = max(circun_stress,long_stress) + 6 # Pegando o maximo e adicionando a sobreespessura de corrosão

    if h_type == 1:
        head_t = elipsoidal_head(P,D,Sh,E)
    elif h_type == 2:
        head_t = torospherical_head(P,D,Sh,E)
    elif h_type == 3:
        head_t = hemispheric_head(P,R,Sh,E)
    elif h_type == 4:
        try:
            head_t = conical_head(H,D,P,Sh,E)
        except ValueError:
            return ## Alerta tkinter
    # elif h_type == 5: Não usando tampo toro conico por enquanto

    total_w = shell_weight(R, L, shell_t, mat_den, fluid_den, fluid_level) + head_weight(h_type,D,head_t,fluid_den,fluid_level,mat_den,H)  # Criar DB para fluídos

    Q = total_w/2


    print(shell_t) # Apagar depois, somente checando valor





calculate(10,82.7,1,1000)