"""Repositorio JSON para sesiones de seguimiento."""

from __future__ import annotations

import json
from pathlib import Path

from app.exceptions import DuplicateEntityError
from app.exceptions import EntityNotFoundError
from app.exceptions import PersistenceError
from app.interfaces.sesion_repository import SesionRepository
from app.models.sesion_seguimiento import SesionSeguimiento


class JsonSesionRepository(SesionRepository):
    """Persistencia de sesiones en archivo JSON."""

    def __init__(self, file_path: str) -> None:
        self._file_path = Path(file_path)
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def create(self, sesion: SesionSeguimiento) -> SesionSeguimiento:
        sesiones = self.list_all()
        if any(item.sesion_id == sesion.sesion_id for item in sesiones):
            raise DuplicateEntityError(
                f"La sesion '{sesion.sesion_id}' ya existe."
            )
        sesiones.append(sesion)
        self._save_all(sesiones)
        return sesion

    def list_all(self) -> list[SesionSeguimiento]:
        data = self._load_raw_data()
        return [SesionSeguimiento.from_dict(item) for item in data]

    def get_by_id(self, sesion_id: str) -> SesionSeguimiento:
        for sesion in self.list_all():
            if sesion.sesion_id == sesion_id:
                return sesion
        raise EntityNotFoundError(f"No existe la sesion '{sesion_id}'.")

    def update(self, sesion: SesionSeguimiento) -> SesionSeguimiento:
        sesiones = self.list_all()
        for index, actual in enumerate(sesiones):
            if actual.sesion_id == sesion.sesion_id:
                sesiones[index] = sesion
                self._save_all(sesiones)
                return sesion
        raise EntityNotFoundError(f"No existe la sesion '{sesion.sesion_id}'.")

    def delete(self, sesion_id: str) -> None:
        sesiones = self.list_all()
        nuevas_sesiones = [
            sesion for sesion in sesiones if sesion.sesion_id != sesion_id
        ]
        if len(nuevas_sesiones) == len(sesiones):
            raise EntityNotFoundError(f"No existe la sesion '{sesion_id}'.")
        self._save_all(nuevas_sesiones)

    def _load_raw_data(self) -> list[dict[str, object]]:
        if not self._file_path.exists():
            return []
        try:
            contenido = self._file_path.read_text(encoding="utf-8").strip()
            if not contenido:
                return []
            data = json.loads(contenido)
        except json.JSONDecodeError as exc:
            raise PersistenceError(
                "El archivo JSON de sesiones esta corrupto."
            ) from exc
        if not isinstance(data, list):
            raise PersistenceError(
                "El archivo JSON de sesiones debe contener una lista."
            )
        return data

    def _save_all(self, sesiones: list[SesionSeguimiento]) -> None:
        payload = [sesion.to_dict() for sesion in sesiones]
        self._file_path.write_text(
            json.dumps(payload, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )
