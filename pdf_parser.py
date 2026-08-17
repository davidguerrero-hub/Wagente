import pymupdf
import huggingface_hub
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Parser():
    def __init__(self, document_path: str = "data/W3_ROC_Data.pdf", arg_size: int = 800, arg_overlap: int = 200):
        self.document = pymupdf.open(document_path)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = arg_size, 
            chunk_overlap = arg_overlap, 
            separators = ["\n\n", ".", ",", "\n", " ", ""], 
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
            content += columns[0] + columns[1]
        return content

    def split(self, text: str):
        chunks = self.splitter.split_text(text)
        return chunks
