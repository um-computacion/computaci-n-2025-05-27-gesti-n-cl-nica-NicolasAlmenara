class Especialidad:
    def __init__(self, tipo: str, dias: list[str]):
        self.__tipo = tipo
        self.__dias = [dia.lower() for dia in dias]
    
    def obtener_especialidad(self) -> str:
        return self.__tipo
    
    def verificar_dia(self, dia: str) -> bool:
        for d in self.__dias:
            if d.lower() == dia.lower():
                return True
        return False
    
    def __str__(self) -> str: 
        dias_str = ",".join(self.__dias)
        return f"{self.__tipo} (Dias: {dias_str})"