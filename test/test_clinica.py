import unittest
from datetime import datetime
from src.models.paciente import Paciente
from src.models.medico import Medico
from src.models.especialidad import Especialidad
from src.models.clinica import Clinica
from src.models.turno import Turno
from src.models.receta import Receta
from src.models.historiaclinica import HistoriaClinica
from src.models.excepciones import (
    PacienteNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    RecetaInvalidaException
)

class TestClinica(unittest.TestCase):
    def setUp(self):
        self.clinica = Clinica()
        self.paciente = Paciente("Juan Pérez", "12345678", "12/12/2000")
        self.medico = Medico("Dr. García", "M001")
        self.especialidad = Especialidad("Pediatría", ["lunes", "miércoles"])
        self.medico.agregar_especialidad(self.especialidad)
        self.fecha_turno = datetime(2025, 6, 9, 10, 0)  # lunes

    def test_agregar_paciente(self):
        self.clinica.agregar_paciente(self.paciente)
        self.assertEqual(len(self.clinica.obtener_pacientes()), 1)

    def test_agregar_paciente_duplicado(self):
        self.clinica.agregar_paciente(self.paciente)
        with self.assertRaises(ValueError):
            self.clinica.agregar_paciente(self.paciente)

    def test_agregar_medico(self):
        self.clinica.agregar_medico(self.medico)
        self.assertEqual(len(self.clinica.obtener_medicos()), 1)

    def test_agregar_medico_duplicado(self):
        self.clinica.agregar_medico(self.medico)
        with self.assertRaises(ValueError):
            self.clinica.agregar_medico(self.medico)

    def test_especialidad_dia_valido(self):
        self.assertTrue(self.especialidad.verificar_dia("lunes"))
        self.assertFalse(self.especialidad.verificar_dia("viernes"))

    def test_agregar_especialidad_duplicada(self):
        with self.assertRaises(ValueError):
            self.medico.agregar_especialidad(Especialidad("Pediatría", ["viernes"]))

    def test_agendar_turno(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        self.clinica.agendar_turno("12345678", "M001", "Pediatría", self.fecha_turno)
        self.assertEqual(len(self.clinica.obtener_turnos()), 1)

    def test_turno_duplicado(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        self.clinica.agendar_turno("12345678", "M001", "Pediatría", self.fecha_turno)
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("12345678", "M001", "Pediatría", self.fecha_turno)

    def test_turno_medico_inexistente(self):
        self.clinica.agregar_paciente(self.paciente)
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "INEXISTENTE", "Pediatría", self.fecha_turno)

    def test_turno_paciente_inexistente(self):
        self.clinica.agregar_medico(self.medico)
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno("99999999", "M001", "Pediatría", self.fecha_turno)

    def test_turno_especialidad_incorrecta(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "M001", "Cardiología", self.fecha_turno)

    def test_turno_dia_incorrecto(self):
        fecha_martes = datetime(2025, 6, 10, 10, 0)
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "M001", "Pediatría", fecha_martes)

    def test_emitir_receta_exitosa(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        self.clinica.emitir_receta("12345678", "M001", ["Ibuprofeno"])
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.obtener_recetas()), 1)

    def test_emitir_receta_sin_medicamentos(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("12345678", "M001", [])

    def test_emitir_receta_medico_inexistente(self):
        self.clinica.agregar_paciente(self.paciente)
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.emitir_receta("12345678", "INEXISTENTE", ["Paracetamol"])

    def test_emitir_receta_paciente_inexistente(self):
        self.clinica.agregar_medico(self.medico)
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.emitir_receta("99999999", "M001", ["Paracetamol"])

    def test_historia_clinica_existente(self):
        self.clinica.agregar_paciente(self.paciente)
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertIsInstance(historia, HistoriaClinica)

    def test_historia_clinica_inexistente(self):
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.obtener_historia_clinica("99999999")

