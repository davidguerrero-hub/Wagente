from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import pymupdf
import json
import re

class Parser():

    def convert(self):
        paths = self.get_files()
        array_doc = []
        for p in paths:
            array_doc.append(self.separate(p))
        for doc in array_doc:
            self.curate(doc)
        self.create_jsonl(array_doc)
        return True


    def get_files(self, dir: str = "documents"):
        array = []
        path = Path(dir)
        files = path.glob("*.pdf")
        for f in files:
            array.append(str(f))
        return array


    def separate(self, path: str, page_init: int = 0):
        number_page: int = page_init                # 0 ya que la portada no cuenta
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
                array.append({"text": column, "metadata": {"page": number_page, "file": path}})
                number_page += 1
        return array                                # [{..., {..., ...}}, ...]


    def curate(self, array):
        for page in array:
            page["text"] = self.__num_page(page["text"])
            page["text"] = self.__hyphen(page["text"])


    def create_jsonl(self, array: list):
        with open("documents/document.jsonl", "w", encoding="utf-8") as file:
            for i in array:
                for j in i:
                    file.write(json.dumps(j, ensure_ascii=False) + "\n")


    def __num_page(self, text: str):
        text = re.sub(r'(\n)(\d+)(\n+)(\s*)$', '\n', text)      # (\d+) 1 o mas digitos, (\s*) 0 o mas espacios
        return text

    def __hyphen(self, text: str):
        text = re.sub(r'(\w+)(-)(\n)(\w*)', r'\1\4', text)     # (\w+) 1 o mas texto, (r'\1\4) primer y cuarto bloque '
        return text