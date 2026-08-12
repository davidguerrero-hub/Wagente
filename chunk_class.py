class Chunk():
    def __init__(self, id: int, content: str):
        self.__id = id
        self.__content = content

    # Setters y Getters

    def get_id(self):
        return self.__id

    def get_content(self):
        return self.__content

    def set_id(self, id: int):
        self.__id = id
        return True

    def set_content(self, content: str):
        self.__content = content
        return True
    