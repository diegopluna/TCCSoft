import sqlite3
from tkinter import messagebox

class results:
    def __init__(self, name, D, L, P, UL, Corr, E, s_mat, h_type, H, Di, h_mat, fluid, fluid_level, A, Sa, B, shell_t, head_t):
        self.name = name
        self.diam = D
        self.len = L
        self.pre = P
        self.shell_life = UL
        self.corr = Corr
        self.weld_eff = E
        self.shell_mat = s_mat
        self.head_type = h_type
        self.head_height = H
        self.end_diam = Di
        self.head_mat = h_mat
        self.fluid = fluid
        self.fluid_level = fluid_level
        self.A = A
        self.Sa = Sa
        self.B = B
        self.shell_thick = shell_t
        self.head_thick = head_t

    def load_from_nome(name):
        conn = sqlite3.connect('storage2.db')
        c = conn.cursor()
        c.execute(f"SELECT *, oid FROM results WHERE nome=\"{name}\"")
        records = c.fetchall()
        if len(records) == 1:
            record = records[0]
            return results(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11], record[12], record[13], record[14], record[15], record[16], record[17], record[18])
        conn.commit()
        conn.close()
        return None
    
    def save(self):
        conn = sqlite3.connect('storage2.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM results")
        records = c.fetchall()
        shouldInsert = True
        for record in records:
            if record[0] == self.name:
                aux = messagebox.askquestion(
                    "Erro", "Já existe um projeto com este nome.\nDeseja sobreescrever?")
                if aux == 'no':
                    shouldInsert = False
        if shouldInsert:
            c.execute("""INSERT INTO results VALUES (:name, :diameter, :shell_len, :pressure, :shell_life, :corr_t, :weld_eff, :shell_mat, :head_type, :head_height, :end_diam, :head_mat, :fluid, :fluid_level, :saddle_A, :saddle_angle, :saddle_w, :shell_thick, :head_thick) ON CONFLICT(name) 
            DO UPDATE SET 
            name=excluded.name, 
            diameter=excluded.diameter, 
            shell_len=excluded.shell_len,
            pressure= excluded.pressure,
            shell_life=excluded.shell_life, 
            corr_t=excluded.corr_t,
            weld_eff=excluded.weld_eff,
            shell_mat=excluded.shell_mat,
            head_type=excluded.head_type,
            head_height=excluded.head_height,
            end_diam=excluded.end_diam,
            head_mat=excluded.head_mat,
            fluid=excluded.fluid,
            fluid_level = excluded.fluid_level,
            saddle_A=excluded.saddle_A,
            saddle_angle=excluded.saddle_angle,
            saddle_w=excluded.saddle_w,
            shell_thick=excluded.shell_thick,
            head_thick=excluded.head_thick""",
                      {
                          "name": self.name,
                          "diameter": self.diam,
                          "shell_len": self.len,
                          "pressure": self.pre,
                          "shell_life": self.shell_life,
                          "corr_t": self.corr,
                          "weld_eff": self.weld_eff,
                          "shell_mat": self.shell_mat,
                          "head_type": self.head_type,
                          "head_height": self.head_height,
                          "end_diam": self.end_diam,
                          "head_mat": self.head_mat,
                          "fluid": self.fluid,
                          "fluid_level": self.fluid_level,
                          "saddle_A" : self.A,
                          "saddle_angle":self.Sa,
                          "saddle_w": self.B,
                          "shell_thick": self.shell_thick,
                          "head_thick": self.head_thick,
                      }
                      )
        conn.commit()
        conn.close()