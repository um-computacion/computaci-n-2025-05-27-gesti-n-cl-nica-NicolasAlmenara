from src.models.paciente import Paciente
from src.models.turno import Turno
from src.models.receta import Receta

class HistoriaClinica:
    def __init__(self, paciente: Paciente):
        self.__paciente = paciente
        self.__turnos = []
        self.__recetas = []
    
    def agregar_turno(self, turno: Turno):
        self.__turnos.append(turno)
    
    def agregar_receta(self, receta: Receta):
        self.__recetas.append(receta)
    
    def obtener_turnos(self) -> list[Turno]:
        return list(self.__turnos)
    
    def obtener_recetas(self) -> list[Receta]:
        return list(self.__recetas)
    
    def __str__(self) -> str:
        if self.__turnos:
            turnos_str = "\n".join(str(turno) for turno in self.__turnos)
        else:
            turnos_str = "no hay turnos registrados"
        if self.__recetas:
            recetas_str = "\n".join(str(receta) for receta in self.__recetas)
        else:
            recetas_str = "no hay recetas registradas"
        return f"Historia clinica de {self.__paciente}: turnos:\n{turnos_str}\n, Recetas:\n{recetas_str}"
    

