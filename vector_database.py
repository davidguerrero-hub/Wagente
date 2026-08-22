from langchain_text_splitters import RecursiveCharacterTextSplitter
import huggingface_hub
import json

class Vectordb_manager():

    def __init__(self, arg_size: int = 1000, arg_overlap: int = 300):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = arg_size, 
            chunk_overlap = arg_overlap, 
            separators = ["\n\n", ". ", ",", "\n", " ", ""], 
            keep_separator="end")


    def convert(self):
        unified = self.get_text()
        chunks = self.split(unified)
        return chunks


    def get_text(self, jsonl_path: str = "documents/document.jsonl"):
        content: str = ""
        with open("documents/document.jsonl", "r", encoding="utf-8") as jsonl:
            for page in jsonl:
                content += (json.loads(page))["text"]
        return content


    def split(self, text: str):
        chunks = self.splitter.split_text(text)
        return chunks