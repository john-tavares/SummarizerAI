class Extractor:
    def __init__(self, url:str, file_type:str, language="pt-BR")->None:
        self.url = url
        self.file_type = file_type
        self.file_extension = file_type.split('/')[-1]
        self.language = language

    def transcribe(self)->str:
        return ""