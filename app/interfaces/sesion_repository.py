"""Contratos para acceso a datos de sesiones."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.sesion_seguimiento import SesionSeguimiento


class SesionRepository(ABC):
    """Contrato del repositorio de sesiones."""

    @abstractmethod
    def create(self, sesion: SesionSeguimiento) -> SesionSeguimiento:
        """Guarda una nueva sesion."""

    @abstractmethod
    def list_all(self) -> list[SesionSeguimiento]:
        """Retorna todas las sesiones."""

    @abstractmethod
    def get_by_id(self, sesion_id: str) -> SesionSeguimiento:
        """Busca una sesion por su identificador."""

    @abstractmethod
    def update(self, sesion: SesionSeguimiento) -> SesionSeguimiento:
        """Actualiza una sesion existente."""

    @abstractmethod
    def delete(self, sesion_id: str) -> None:
        """Elimina una sesion por identificador."""
