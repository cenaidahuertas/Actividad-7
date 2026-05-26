"""Excepciones de dominio de la aplicacion."""


class AppError(Exception):
    """Excepcion base de la aplicacion."""


class ValidationError(AppError):
    """Error de validacion de datos."""


class PersistenceError(AppError):
    """Error general de persistencia."""


class EntityNotFoundError(PersistenceError):
    """La entidad solicitada no existe."""


class DuplicateEntityError(PersistenceError):
    """La entidad ya existe en la persistencia."""


class BusinessRuleError(AppError):
    """Error de regla de negocio."""


class HorarioFueraDeRangoError(BusinessRuleError):
    """La sesion no cumple el horario permitido."""


class SesionDuplicadaError(BusinessRuleError):
    """Ya existe una sesion para el mismo estudiante y fecha."""


class CuestionarioRequeridoError(BusinessRuleError):
    """El estudiante no tiene cuestionarios asociados."""
