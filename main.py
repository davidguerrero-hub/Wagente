from pdf_parser import Parser
from vector_database import Vectordb_manager
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
KEY = os.getenv("GOOGLE_API_KEY")
URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODELS = [
    {"nombre": "gemini-3.1-flash-lite", "activo": True},
    {"nombre": "gemini-2.5-flash", "activo": True},
    {"nombre": "gemini-3.5-flash", "activo": True},
    {"nombre": "gemini-3-flash-preview", "activo": True},
    {"nombre": "gemini-2.5-flash-lite", "activo": True},
    {"nombre": "gemini-2.0-flash", "activo": True}
]

# parser = Parser()
# parser.convert()

vector = Vectordb_manager()
array = vector.convert()
print(len(array))
for i in range(15):
    print(array[i] + "\n" + "="*50)


# llm = OpenAI(base_url=URL, api_key=KEY)
# response = llm.chat.completions.create(model=MODELS[0]["nombre"], messages=[{"role": "user", 
#                                                                             "content": "Hola"}])
# print(response.choices[0].message.content)




# Extraer Documentos
# Curar datos
# Si esta en ingles, buscar un LLM traductor para implementar en el flujo
# Separarlo en chunks
# Buscar Modelo Embedding
# Llamar a Chroma
