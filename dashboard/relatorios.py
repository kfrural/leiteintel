from fpdf import FPDF

def gerar_pdf_resumo(texto, caminho):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, texto)
    pdf.output(caminho)
