class Chunk():
    def __init__(self, id: int, content: str, page: int):
        self.__id = id
        self.__content = content
        self.__page = page

    # Setters y Getters

    def get_id(self):
        return self.__id
    
    def set_id(self, id: int):
            self.__id = id
            return True

    def get_content(self):
        return self.__content

    def set_content(self, content: str):
        self.__content = content
        return True

    def get_page(self):
        return self.__page
        
    def set_page(self, page: int):
        self.__page = page
        return True
