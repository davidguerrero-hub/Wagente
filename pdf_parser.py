import pymupdf
import huggingface_hub
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

class Parser():
    def __init__(self, document_path: str = "data/W3_ROC_Data.pdf", arg_size: int = 1000, arg_overlap: int = 300):
        self.document = pymupdf.open(document_path)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = arg_size, 
            chunk_overlap = arg_overlap, 
            separators = ["\n\n", ". ", ",", "\n", " ", ""], 
            keep_separator="end")
        

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
            columns[0] = self.__num_page(columns[0])
            print(columns[0] + "-"*30) if columns[0] else print("nada")
            # print(columns[1] + "-"*30) if columns[1] else print("nada")
            # print(repr(columns[0][-10:])) if columns[0] else print("nada")
            content += columns[0] + columns[1]
        return content

    def split(self, text: str):
        chunks = self.splitter.split_text(text)
        return chunks

    def __num_page(self, text: str):
        text = re.sub(r'(\n)(\d+)(\n+)(\s*)$', '\n', text)      # (\d+) 1 o mas digitos, (\s*) 0 o mas espacios
        return text

    def __hyphen(self, text: str):
        text = re.sub(r'(\w+)(-)(\n)(\w+)$', '\1\4', text)
        return text
    
    # Implementar hyphen
    # Probar hyphen
    # Meterlo en jsonl