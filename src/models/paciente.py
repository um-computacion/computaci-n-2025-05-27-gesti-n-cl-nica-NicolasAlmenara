class Paciente:
    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):
        self.__dni = dni
        self.__nombre = nombre
        self.__fecha_nacimiento = fecha_nacimiento

    def obtener_dni(self):
        return self.__dni
    
    def __str__(self):
        return f"{self.__nombre}, DNI: {self.__dni}, fecha de nacimiento: {self.__fecha_nacimiento}"
    