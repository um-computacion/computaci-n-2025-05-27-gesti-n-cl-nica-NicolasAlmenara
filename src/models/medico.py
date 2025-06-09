from src.models.especialidad import Especialidad
class Medico:
    def __init__(self, nombre: str, matricula: str):
        self.__nombre = nombre
        self.__matricula = matricula
        self.__especialidades : list[Especialidad] = []

    def agregar_especialidad(self, especialidad: Especialidad):
        # Verificar si ya existe una especialidad con el mismo nombre
        for esp_existente in self.__especialidades:
            if esp_existente.obtener_especialidad() == especialidad.obtener_especialidad():
                raise ValueError("La especialidad ya está registrada para este médico.")
        self.__especialidades.append(especialidad)

    def obtener_matricula(self) -> str:
        return self.__matricula
    
    def obtener_especialidad_para_dia(self, dia: str) -> str | None:
        for especialidad in self.__especialidades:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_especialidad()
        return None  # ← BIEN: está fuera del for
        
    def __str__(self):
        especialidades_str = ",".join(str(especialidad) for especialidad in self.__especialidades)
        return f"Nombre: { self.__nombre}, Matricula: {self.__matricula}, Especialidades: {especialidades_str}"




    
