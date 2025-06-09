from src.models.paciente import Paciente
from src.models.medico import Medico
from src.models.turno import Turno
from src.models.historiaclinica import HistoriaClinica
from src.models.receta import Receta
from src.models.excepciones import (
    PacienteNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    RecetaInvalidaException
)

from datetime import datetime
class Clinica:
    def __init__(self):
        self.__pacientes: dict[str, Paciente] = {}
        self.__medicos: dict[str, Medico] = {}
        self.__turnos: list[Turno] = []
        self.__historias_clinicas: dict[str, HistoriaClinica] = {}

    def agregar_paciente(self, paciente: Paciente):
        dni = paciente.obtener_dni()
        if dni in self.__pacientes:
            raise ValueError("El paciente ya está registrado.")
        self.__pacientes[dni] = paciente
        self.__historias_clinicas[dni] = HistoriaClinica(paciente)

    def agregar_medico(self, medico: Medico):
        matricula = medico.obtener_matricula()
        if matricula in self.__medicos:
            raise ValueError("El médico ya está registrado.")
        self.__medicos[matricula] = medico

    def obtener_pacientes(self) -> list[Paciente]:
        return list(self.__pacientes.values())

    def obtener_medicos(self) -> list[Medico]:
        return list(self.__medicos.values())

    def obtener_medico_por_matricula(self, matricula: str) -> Medico:
        if matricula not in self.__medicos:
            raise MedicoNoDisponibleException("Médico no registrado.")
        return self.__medicos[matricula]

    def obtener_turnos(self) -> list[Turno]:
        return list(self.__turnos)

    def obtener_historia_clinica(self, dni: str) -> HistoriaClinica:
        if dni not in self.__historias_clinicas:
            raise PacienteNoEncontradoException("Historia clínica no encontrada.")
        return self.__historias_clinicas[dni]

    def validar_existencia_paciente(self, dni: str):
        if dni not in self.__pacientes:
            raise PacienteNoEncontradoException("Paciente no registrado.")

    def validar_existencia_medico(self, matricula: str):
        if matricula not in self.__medicos:
            raise MedicoNoDisponibleException("Médico no registrado.")

    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime):
        for turno in self.__turnos:
            if turno.obtener_medico().obtener_matricula() == matricula and turno.obtener_fecha_hora() == fecha_hora:
                raise TurnoOcupadoException("Ya existe un turno para ese médico en esa fecha y hora.")

    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dias[fecha_hora.weekday()]

    def obtener_especialidad_disponible(self, medico: Medico, dia_semana: str) -> str:
        especialidad = medico.obtener_especialidad_para_dia(dia_semana)
        if especialidad is None:
            raise MedicoNoDisponibleException("El médico no atiende ese día.")
        return especialidad

    def validar_especialidad_en_dia(self, medico: Medico, especialidad_solicitada: str, dia_semana: str):
        especialidad_en_dia = medico.obtener_especialidad_para_dia(dia_semana)
        if especialidad_en_dia is None or especialidad_en_dia.lower() != especialidad_solicitada.lower():
            raise MedicoNoDisponibleException("El médico no atiende esa especialidad ese día.")

    def agendar_turno(self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime):
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        self.validar_turno_no_duplicado(matricula, fecha_hora)

        medico = self.__medicos[matricula]
        paciente = self.__pacientes[dni]
        dia_semana = self.obtener_dia_semana_en_espanol(fecha_hora)

        self.validar_especialidad_en_dia(medico, especialidad, dia_semana)

        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos.append(turno)
        self.__historias_clinicas[dni].agregar_turno(turno)

    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str]):
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)

        if not medicamentos:
            raise RecetaInvalidaException("La lista de medicamentos no puede estar vacía.")

        paciente = self.__pacientes[dni]
        medico = self.__medicos[matricula]

        receta = Receta(paciente, medico, medicamentos)
        self.__historias_clinicas[dni].agregar_receta(receta)

    
