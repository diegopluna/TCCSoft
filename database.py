import sqlite3

conn = sqlite3.connect('storage.db')
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS materials_list (
  mat_name text PRIMARY KEY,
  adm_tension float,
  mat_den float,
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS fluids_list (
  fluid_name text PRIMARY KEY,
  fluid_type bool,
  fluid_den float,
)
""")

conn.commit()
conn.close()