from vector_database import Vectordb_manager

class Tool_manager():

    def __init__(self, model_name: str):
        self.vectordb = Vectordb_manager(arg_model=model_name)
        self.tool_list = [{"get_chunks": self.get_chunks, "descriptor": self.desc_get_chunks},
                          {}]    
    


    def get_tool_desc(self):
        array = []
        for dic in self.tool_list:
            array.append({"type": "function", "function": dic["descriptor"]})
        return array

    desc_get_chunks = {
        "name": "get_chunks",
        "description": """
            Permanently deletes the relationship between a song and an instrument. A relation represents that a song uses a particular instrument.
            Use this tool when user asks that a song does not use an instrument, or an instrument do not belong a song.
            Before calling this tool, you must obtain explicit confirmation from the user.
            """,
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "ID of song-instrument relationship, You could use list_relation"
                    }
                },
            "required": ["id"],
            "additionalProperties": False
        }
    }

    def get_chunks(self, query: str):
        ret_result = self.vectordb.retrive(query)
        content = ""
        for i in range(len(ret_result["documents"]) - 1):
            content += "<BATCH" + str(i) + ">\n"
            content += ret_result["documents"][i]
            content += "\n"
        return content