import pymupdf
# from hugging_face import hugging_hub

class Parser():
    def __init__(self, document_path: str = "data/W3_ROC_Data.pdf"):
        self.document = pymupdf.open(document_path)

    def curate(self):
        content: str = ""
        for page in self.document:
            blocks = page.get_text("blocks")
            columns = ["", ""]
            for block in blocks:
                x0, y0, x1, y1, texto, *_ = block       # Asignacion de indices de un array
                if (x0 < 320):
                    columns[0] += texto + "\n"
                else:
                    columns[1] += texto + "\n"
            content += columns[0] + columns[1]
        return content

