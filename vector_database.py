import huggingface_hub
from langchain_text_splitters import RecursiveCharacterTextSplitter

# splitter = RecursiveCharacterTextSplitter(     # Se encarga embedding_model
#             chunk_size = arg_size, 
#             chunk_overlap = arg_overlap, 
#             separators = ["\n\n", ". ", ",", "\n", " ", ""], 
#             keep_separator="end")