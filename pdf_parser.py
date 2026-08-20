from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import pymupdf
import json
import re

class Parser():
    def get_files(self, dir: str = "documents"):
        array = []
        path = Path(dir)
        files = path.glob("*.pdf")
        for f in files:
            array.append(str(f))
        return array

    def convert(self):
        documets = self.get_files()
        for doc in documets:
            self.separate(doc)

    def separate(self, path: str, page_init: int = 0):
        page: int = page_init
        array = []
        document = pymupdf.open(path)
        for page in document:
            columns = ["", ""]
            blocks = page.get_text("blocks")        # Separado por \n, block siendo un objeto
            for block in blocks:
                pos_x = block[0]                    # 1, 2, 3 serian y0, x1, y1
                texto = block[4]
                if (pos_x < 320):
                    columns[0] += texto + "\n"
                else:
                    columns[1] += texto + "\n"
            for column in columns:
                array.append({"texto": column})
            content = columns[0] + columns[1]
            array.append(content)
        return array


    def curate(self):
        array = []
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
            # print(columns[0] + "="*50) if columns[0] else print("nada")
            # print(columns[1] + "="*50) if columns[1] else print("nada")
            # print(repr(columns[0]) + "="*50) if columns[0] else print("nada")
            columns[0] = self.__num_page(columns[0])
            content = columns[0] + columns[1]
            content = self.__hyphen(content)
            array.append(content)
        return array

    # def split(self, text: str):     # embedding_model
    #     chunks = self.splitter.split_text(text)
    #     return chunks

    def __num_page(self, text: str):
        text = re.sub(r'(\n)(\d+)(\n+)(\s*)$', '\n', text)      # (\d+) 1 o mas digitos, (\s*) 0 o mas espacios
        return text

    def __hyphen(self, text: str):
        text = re.sub(r'(\w+)(-)(\n)(\w*)', r'\1\4', text)     # (\w+) 1 o mas texto, (r'\1\4) primer y cuarto bloque '
        # text = re.sub(r'-\n$', "", text)
        return text
    
    # Implementar hyphen
    # Probar hyphen
    # Meterlo en jsonl

    def create_jsonl(self, array: list):
        with open("data/jsonl.", "w", encoding="utf-8") as file:
            for i in len(array):
                dic = {
                    "id": 1, 
                    "source": "data/W3_ROC_Data.pdf",
                    "page": i, 
                    "content": array[i], 
                    "extra": ""
                }
            file.write(json.dumps(dic, ensure_ascii=False) + "\n")
