from sentence_transformers import SentenceTransformer

class Embedding_model():

    def __init__(self, arg_model: str):
        self.model = self.set_model(arg_model)


    def set_model(self, arg_model: str):
        self.model_name = arg_model
        print("[_] Loading embedding model...")
        return SentenceTransformer(self.model_name)


    def encode(self, arg_type: str, text_or_list):           # Bendito python no soporta overloading
        if (arg_type == "list"):
            return (self.model.encode(text_or_list,
                                      batch_size=self.batch_size, 
                                      show_progress_bar=True).tolist())
        if (arg_type == "str"):
            return (self.model.encode(text_or_list, show_progress_bar=True))
        else:
            print("[#] Error <embedding>: arg_type doesn´t expected")
            return ""