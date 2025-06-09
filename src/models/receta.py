from src.models.paciente import Paciente
from src.models.medico import Medico
from datetime import datetime
class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: list[str]):
        self.__paciente = paciente
        self.__medico = medico
        self.__medicamentos = medicamentos
        self.__fecha = datetime.now()
    def __str__(self) -> str:
        fecha_str = self.__fecha.strftime("%d/%m/%Y")
        medicamentos_str = ",".join(self.__medicamentos)
        return f"Receta: paciente: {self.__paciente}, medico {self.__medico}, fecha {fecha_str}, medicamentos: {medicamentos_str}"



