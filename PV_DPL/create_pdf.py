from pdf import PDF
from tkinter import messagebox
import os.path
import os

def create_pdf(nome, data_in, data_out, data_calc=None):

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Times", size=10)

    pdf.create_table(table_data=data_in,
                     title='Dados de Entrada', cell_width='even')
    pdf.ln()
    pdf.create_table(table_data=data_out,
                     title='Dados Calculados', cell_width='even')
    pdf.ln()
    if data_calc is not None:
        pdf.create_table(table_data=data_calc,
                        title='Folha de cálculo', cell_width='even')
        pdf.ln()
    if os.path.isfile(f"{nome}.pdf"):
        res = messagebox.askquestion(
            "Erro", "Já existe um arquivo com este nome, deseja sobreescrever?")
        if res == 'yes':
            os.remove(f"{nome}.pdf")
        else:
            return
    pdf.output(f"{nome}.pdf")
    messagebox.showinfo("Aviso", "Relatório em PDF gerado com sucesso!")

