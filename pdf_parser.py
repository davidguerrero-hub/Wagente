from pypdf import PdfReader

reader = PdfReader("W3_ROC_Data.pdf")

print("Número de páginas:", len(reader.pages))

pagina = reader.pages[2]

texto = pagina.extract_text(extraction_mode="layout")

print(texto)