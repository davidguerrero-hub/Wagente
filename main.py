from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
# Langchain se encargara de buscar GOOGLE_API_KEY en .env

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
respuesta = llm.invoke("Q es RAG?")
print(respuesta.content)

# Extraer Documentos
# Curar datos
# Si esta en ingles, buscar un LLM traductor para implementar en el flujo
# Separarlo en chunks
# Buscar Modelo Embedding
# Llamar a Chroma
