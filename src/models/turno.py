from datetime import datetime
from src.models.paciente import Paciente
from src.models.medico import Medico
class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime, especialidad: str ):
        self.__paciente = paciente
        self.__medico = medico
        self.__fecha_hora = fecha_hora
        self.__especialidad = especialidad
    def obtener_medico(self) -> Medico:
        return self.__medico
    def obtener_fecha_hora(self) -> datetime:
        return self.__fecha_hora
    
    def __str__(self) -> str:
        return f"paciente: {self.__paciente}, Medico {self.__medico}, fecha y hora {self.__fecha_hora}, Especialidad: {self.__especialidad}"