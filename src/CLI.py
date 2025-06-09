from src.models.clinica import Clinica
from src.models.paciente import Paciente
from src.models.medico import Medico
from src.models.especialidad import Especialidad
from src.models.excepciones import (
    PacienteNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    RecetaInvalidaException
)
from datetime import datetime

class CLI:
    def __init__(self):
        self.__clinica = Clinica()

    def iniciar(self):
        while True:
            print("\n--- Menú Clínica ---")
            print("1) Agregar paciente")
            print("2) Agregar médico")
            print("3) Agendar turno")
            print("4) Agregar especialidad a médico")
            print("5) Emitir receta")
            print("6) Ver historia clínica")
            print("7) Ver todos los turnos")
            print("8) Ver todos los pacientes")
            print("9) Ver todos los médicos")
            print("0) Salir")

            opcion = input("Seleccione una opción: ")

            try:
                if opcion == "1":
                    self.agregar_paciente()
                elif opcion == "2":
                    self.agregar_medico()
                elif opcion == "3":
                    self.agendar_turno()
                elif opcion == "4":
                    self.agregar_especialidad()
                elif opcion == "5":
                    self.emitir_receta()
                elif opcion == "6":
                    self.ver_historia_clinica()
                elif opcion == "7":
                    self.ver_todos_los_turnos()
                elif opcion == "8":
                    self.ver_todos_los_pacientes()
                elif opcion == "9":
                    self.ver_todos_los_medicos()
                elif opcion == "0":
                    print("Saliendo del sistema.")
                    break
                else:
                    print("Opción inválida.")
            except (
                PacienteNoEncontradoException,
                MedicoNoDisponibleException,
                TurnoOcupadoException,
                RecetaInvalidaException,
                ValueError
            ) as e:
                print(f"⚠️  Error: {e}")

    def agregar_paciente(self):
        nombre = input("Nombre completo: ")
        dni = input("DNI: ")
        fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ")
        paciente = Paciente(nombre, dni, fecha_nacimiento)
        self.__clinica.agregar_paciente(paciente)
        print("Paciente agregado correctamente.")

    def agregar_medico(self):
        nombre = input("Nombre del médico: ")
        matricula = input("Matrícula: ")
        medico = Medico(nombre, matricula)
        self.__clinica.agregar_medico(medico)
        print("Médico agregado correctamente.")

    def agregar_especialidad(self):
        matricula = input("Matrícula del médico: ")
        tipo = input("Especialidad: ")
        dias = input("Días de atención (separados por coma): ").split(",")
        especialidad = Especialidad(tipo, dias)
        medico = self.__clinica.obtener_medico_por_matricula(matricula)
        medico.agregar_especialidad(especialidad)
        print("Especialidad agregada correctamente.")

    def agendar_turno(self):
        dni = input("DNI del paciente: ")
        matricula = input("Matrícula del médico: ")
        especialidad = input("Especialidad: ")
        fecha_str = input("Fecha y hora del turno (dd/mm/aaaa HH:MM): ")
        fecha_hora = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
        self.__clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)
        print("Turno agendado correctamente.")

    def emitir_receta(self):
        dni = input("DNI del paciente: ")
        matricula = input("Matrícula del médico: ")
        medicamentos = input("Medicamentos (separados por coma): ").split(",")
        self.__clinica.emitir_receta(dni, matricula, medicamentos)
        print("Receta emitida correctamente.")

    def ver_historia_clinica(self):
        dni = input("DNI del paciente: ")
        historia = self.__clinica.obtener_historia_clinica(dni)
        print(historia)

    def ver_todos_los_turnos(self):
        turnos = self.__clinica.obtener_turnos()
        if not turnos:
            print("No hay turnos registrados.")
        else:
            for turno in turnos:
                print(turno)

    def ver_todos_los_pacientes(self):
        pacientes = self.__clinica.obtener_pacientes()
        if not pacientes:
            print("No hay pacientes registrados.")
        else:
            for paciente in pacientes:
                print(paciente)

    def ver_todos_los_medicos(self):
        medicos = self.__clinica.obtener_medicos()
        if not medicos:
            print("No hay médicos registrados.")
        else:
            for medico in medicos:
                print(medico)

if __name__ == "__main__":
    cli = CLI()
    cli.iniciar()
