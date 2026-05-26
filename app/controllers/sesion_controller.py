"""Controlador MVC para sesiones de seguimiento."""

from __future__ import annotations

from app.exceptions import AppError
from app.models.sesion_seguimiento import SesionSeguimiento
from app.services.sesion_service import SesionService


class SesionController:
    """Traduce entradas crudas de la UI a acciones del servicio."""

    def __init__(self, service: SesionService) -> None:
        self._service = service

    def crear(self, data: dict[str, object]) -> tuple[bool, str]:
        """Crea una sesion a partir de datos crudos."""
        try:
            sesion = SesionSeguimiento.from_dict(data)
            self._service.crear_sesion(sesion)
        except AppError as exc:
            return False, str(exc)
        return True, "Sesion creada correctamente."

    def listar(self) -> tuple[bool, list[dict[str, object]] | str]:
        """Lista todas las sesiones registradas."""
        try:
            sesiones = self._service.listar_sesiones()
        except AppError as exc:
            return False, str(exc)
        return True, [sesion.to_dict() for sesion in sesiones]

    def actualizar(
        self, sesion_id: str, data: dict[str, object]
    ) -> tuple[bool, str]:
        """Actualiza una sesion existente."""
        try:
            sesion = SesionSeguimiento.from_dict(data)
            self._service.actualizar_sesion(sesion_id, sesion)
        except AppError as exc:
            return False, str(exc)
        return True, "Sesion actualizada correctamente."

    def eliminar(self, sesion_id: str) -> tuple[bool, str]:
        """Elimina una sesion existente."""
        try:
            self._service.eliminar_sesion(sesion_id)
        except AppError as exc:
            return False, str(exc)
        return True, "Sesion eliminada correctamente."
