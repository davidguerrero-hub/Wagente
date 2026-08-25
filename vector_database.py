from langchain_text_splitters import RecursiveCharacterTextSplitter
from embedding_model import Embedding_model
import chromadb
import json

class Vectordb_manager():

    def __init__(self, arg_size: int = 1000, arg_overlap: int = 300, arg_model: str = "sentence-transformers/all-MiniLM-L6-v2", k: int = 5):
        self.embbeding_model = Embedding_model(arg_model)
        self.k = k
        self.batch_size = 8
        self.vectordb_path = "./documents/vectordb/"
        self.clientdb = chromadb.PersistentClient(path=self.vectordb_path)
        self.collection_name = "collection"
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = arg_size, 
            chunk_overlap = arg_overlap, 
            separators = ["\n\n", ". ", ",", "\n", " ", ""],                # Saltos jerarquicos en el splitter
            keep_separator="end")


    def convert(self):
        unified = self.get_text()
        chunks = self.split(unified)
        self.create_vectordb(chunks)
        return True


    def get_text(self, jsonl_path: str = "documents/document.jsonl"):       # Obtiene el path de document.jsonl
        content: str = ""
        with open(jsonl_path, "r", encoding="utf-8") as jsonl:
            for page in jsonl:
                content += (json.loads(page))["text"]
        return content


    def split(self, text: str):
        chunks = self.splitter.split_text(text)
        return chunks
    

    def create_vectordb(self, chunks): 
        try:                                                                # Si no existe la collection
            self.clientdb.delete_collection(self.collection_name)
            print("[!] Collection deleted, creating new one")
        except Exception:
            print("[!] Collection inexistent, creating new one")
        collection = self.clientdb.get_or_create_collection(name=self.collection_name)
        id_array = []
        print("[_] Adding data to ChromaDB...")
        for i in range(len(chunks)):
            id_array.append("id_" + str(i))
        embedding_array = self.embbeding_model.encode("list", chunks)
        collection.add(ids=id_array, embeddings=embedding_array, documents=chunks)
        return True


    def retrive(self, query: str):
        embedding = self.collection_name.encode("str", query)
        try:
            collection = self.clientdb.get_collection(self.collection_name)
        except Exception:
            print("[#] Error <Vector_database>: collection inexistent")
            return ""
        results = collection.query(query_embeddings=[embedding], n_results=self.k)
        return results