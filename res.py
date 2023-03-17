import sqlite3
from tkinter import messagebox


class results:
    def __init__(self, name, diam, pre, weld_eff, shell_type, shell_mat, head_type=None, head_mat=None, cone_angle=None, shell_thick=None, head_thick=None):
        self.name = name
        self.diam = diam
        self.pre = pre
        self.weld_eff = weld_eff
        self.shell_type = shell_type
        self.shell_mat = shell_mat
        self.head_mat = head_mat
        self.head_type = head_type
        self.cone_angle = cone_angle
        self.shell_thick = shell_thick
        self.head_thick = head_thick

    def load_from_nome(name):
        conn = sqlite3.connect('storage.db')
        c = conn.cursor()
        c.execute(f"SELECT *, oid FROM results WHERE nome=\"{name}\"")
        records = c.fetchall()
        if len(records) == 1:
            record = records[0]
            return results(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10])
        conn.commit()
        conn.close()
        return None

    def save(self):
        conn = sqlite3.connect('storage.db')
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
            c.execute("""INSERT INTO results VALUES (:name, :diameter, :pressure, :weld_eff, :shell_type, :shell_mat,:head_type, :head_mat, :cone_angle, :shell_thick, :head_thick) ON CONFLICT(name) 
            DO UPDATE SET 
            name=excluded.name, 
            diameter=excluded.diameter, 
            pressure= excluded.pressure, 
            weld_eff=excluded.weld_eff, 
            shell_type=excluded.shell_type, 
            shell_mat=excluded.shell_mat,
            head_mat=excluded.head_mat,
            head_type=excluded.head_type,
            cone_angle=excluded.cone_angle,
            shell_thick=excluded.shell_thick,
            head_thick=excluded.head_thick""",
                      {
                          "name": self.name,
                          "diameter": self.diam,
                          "pressure": self.pre,
                          "weld_eff": self.weld_eff,
                          "shell_type": self.shell_type,
                          "shell_mat": self.shell_mat,
                          "head_mat": self.head_mat,
                          "head_type": self.head_type,
                          "cone_angle": self.cone_angle,
                          "shell_thick": self.shell_thick,
                          "head_thick": self.head_thick,
                      }
                      )
        conn.commit()
        conn.close()
