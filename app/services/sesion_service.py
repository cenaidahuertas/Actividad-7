"""Servicios de negocio para sesiones de seguimiento."""

from __future__ import annotations

from app.constants import HORA_FIN_ATENCION
from app.constants import HORA_INICIO_ATENCION
from app.exceptions import CuestionarioRequeridoError
from app.exceptions import HorarioFueraDeRangoError
from app.exceptions import SesionDuplicadaError
from app.interfaces.sesion_repository import SesionRepository
from app.models.sesion_seguimiento import SesionSeguimiento


class SesionService:
    """Coordina reglas de negocio y acceso a datos."""

    def __init__(self, repository: SesionRepository) -> None:
        self._repository = repository

    def crear_sesion(self, sesion: SesionSeguimiento) -> SesionSeguimiento:
        """Valida reglas y crea una nueva sesion."""
        self._validar_reglas_de_negocio(sesion)
        return self._repository.create(sesion)

    def listar_sesiones(self) -> list[SesionSeguimiento]:
        """Retorna todas las sesiones registradas."""
        return self._repository.list_all()

    def obtener_sesion(self, sesion_id: str) -> SesionSeguimiento:
        """Busca una sesion por su identificador."""
        return self._repository.get_by_id(sesion_id)

    def actualizar_sesion(
        self, sesion_id: str, sesion_actualizada: SesionSeguimiento
    ) -> SesionSeguimiento:
        """Actualiza una sesion existente."""
        if sesion_id != sesion_actualizada.sesion_id:
            raise SesionDuplicadaError(
                "El identificador de la sesion no puede cambiar."
            )
        self._validar_reglas_de_negocio(
            sesion_actualizada, ignorar_id=sesion_id
        )
        return self._repository.update(sesion_actualizada)

    def eliminar_sesion(self, sesion_id: str) -> None:
        """Elimina una sesion por identificador."""
        self._repository.delete(sesion_id)

    def _validar_reglas_de_negocio(
        self, sesion: SesionSeguimiento, ignorar_id: str | None = None
    ) -> None:
        if not sesion.tiene_cuestionario:
            raise CuestionarioRequeridoError(
                "El estudiante debe tener al menos un cuestionario."
            )

        hora = int(sesion.hora.split(":")[0])
        if hora < HORA_INICIO_ATENCION or hora >= HORA_FIN_ATENCION:
            raise HorarioFueraDeRangoError(
                "La sesion debe agendarse entre las 08:00 y las 18:00."
            )

        sesiones = self._repository.list_all()
        for actual in sesiones:
            if actual.sesion_id == ignorar_id:
                continue
            mismo_estudiante = (
                actual.estudiante_codigo == sesion.estudiante_codigo
            )
            misma_fecha = actual.fecha == sesion.fecha
            if mismo_estudiante and misma_fecha:
                raise SesionDuplicadaError(
                    "El estudiante ya tiene una sesion ese dia."
                )
