from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
import json

class Vectordb_manager():

    def __init__(self, arg_size: int = 1000, arg_overlap: int = 300, arg_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.batch_size = 8
        self.vectordb_path = "./documents/vectordb/"
        self.model_name = arg_model                                         # Nombre del embedding
        self.model = self.set_model(self.model_name)                        # Funcion set_model
        self.clientdb = chromadb.PersistentClient(path=self.vectordb_path)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = arg_size, 
            chunk_overlap = arg_overlap, 
            separators = ["\n\n", ". ", ",", "\n", " ", ""],                # Saltos jerarquicos en el splitter
            keep_separator="end")


    def convert(self):
        unified = self.get_text()
        chunks = self.split(unified)
        self.embedding_model(chunks)
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
    

    def embedding_model(self, chunks):                               # !MEJORA: batching (tiene su propio tqdm), metadata 
        try:                                                                # Si no existe la collection
            self.clientdb.delete_collection("collection")
            print("[!] Collection deleted, creating new one")
        except Exception:
            print("[!] Collection inexistent, creating new one")
        collection = self.clientdb.get_or_create_collection(name="collection")
        id_array = []
        print("[_] Adding data to ChromaDB...")
        for i in range(len(chunks)):
            id_array.append("id_" + str(i))
        embedding_array = (self.model.encode(chunks, 
                                             batch_size=self.batch_size, 
                                             show_progress_bar=True).tolist())
        collection.add(ids=id_array, embeddings=embedding_array, documents=chunks)
        return True


    def set_model(self, model_name: str):
        print("[_] Loading embedding model...")
        return SentenceTransformer(model_name)