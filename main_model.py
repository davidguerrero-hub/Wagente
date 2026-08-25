from openai import OpenAI
from openai import RateLimitError           # Exception para cambio de modelo
from dotenv import load_dotenv
import os

class Main_agent():

    def __init__(self):    
        load_dotenv()
        self.KEY = os.getenv("GOOGLE_API_KEY")
        self.URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
        self.MODELS = [
            {"name": "gemini-3.1-flash-lite", "active": True},
            {"name": "gemini-2.5-flash", "active": True},
            {"name": "gemini-3.5-flash", "active": True},
            {"name": "gemini-3-flash-preview", "active": True},
            {"name": "gemini-2.5-flash-lite", "active": True},
            {"name": "gemini-2.0-flash", "active": True}]
        self.current_model = 0
        self.llm = OpenAI(base_url=self.URL, api_key=self.KEY)


    def chat(self, message: str, history: str):
        try:
            total = history + [{"role": "user", "content": message}]
            response = self.llm.chat.completions.create(model=self.MODELS[self.current_model]["name"], messages=total)#, tools=tool_list)

            while (response.choices[0].finish_reason == "tool_calls"):
                peticion_tool = response.choices[0].message
                retorno = tool_manager(peticion_tool)
                total.append({"role": "assistant", "tool_calls": peticion_tool.tool_calls})
                total.extend(retorno)
                response = openai.chat.completions.create(model=MODELS[modelo_actual]["nombre"], messages=(total), tools=tool_for_api)
            total.append({"role": "assistant", "content": response.choices[0].message.content})

            return [response.choices[0].message.content, total]
        except RateLimitError:
            flag = self.change_model()
            return


    def change_model(self):
        self.MODELS[self.current_model]["active"] = False
        print("[_] Changing model from \"" + self.MODELS[self.current_model]["name"] + "\"...")
        var = 0
        while (var < len(self.MODELS)):
            if (self.MODELS[var]["active"] == True):
                self.current_model = var
                print("[!] Model changed to \"" + self.MODELS[self.current_model]["name"] + "\"\n")
                return True
            var += 1
        print("[#] Error: Registered models aren´t able to be used")
