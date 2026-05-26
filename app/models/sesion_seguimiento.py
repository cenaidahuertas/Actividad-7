"""Entidad de dominio SesionSeguimiento."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.exceptions import ValidationError


@dataclass(slots=True)
class SesionSeguimiento:
    """Representa una sesion de seguimiento psicologico."""

    sesion_id: str
    estudiante_codigo: str
    fecha: str
    hora: str
    motivo: str
    profesional: str
    tiene_cuestionario: bool
    observaciones: str = ""

    def __post_init__(self) -> None:
        self._validar_campos_requeridos()
        self._validar_fecha()
        self._validar_hora()

    def _validar_campos_requeridos(self) -> None:
        campos = {
            "sesion_id": self.sesion_id,
            "estudiante_codigo": self.estudiante_codigo,
            "motivo": self.motivo,
            "profesional": self.profesional,
        }
        for nombre, valor in campos.items():
            if not isinstance(valor, str) or not valor.strip():
                raise ValidationError(
                    f"El campo '{nombre}' es obligatorio."
                )

    def _validar_fecha(self) -> None:
        try:
            datetime.strptime(self.fecha, "%Y-%m-%d")
        except ValueError as exc:
            raise ValidationError(
                "La fecha debe tener el formato YYYY-MM-DD."
            ) from exc

    def _validar_hora(self) -> None:
        try:
            datetime.strptime(self.hora, "%H:%M")
        except ValueError as exc:
            raise ValidationError(
                "La hora debe tener el formato HH:MM."
            ) from exc

    def to_dict(self) -> dict[str, object]:
        """Convierte la entidad en un diccionario serializable."""
        return {
            "sesion_id": self.sesion_id,
            "estudiante_codigo": self.estudiante_codigo,
            "fecha": self.fecha,
            "hora": self.hora,
            "motivo": self.motivo,
            "profesional": self.profesional,
            "tiene_cuestionario": self.tiene_cuestionario,
            "observaciones": self.observaciones,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "SesionSeguimiento":
        """Crea una sesion a partir de un diccionario."""
        return cls(
            sesion_id=str(data["sesion_id"]),
            estudiante_codigo=str(data["estudiante_codigo"]),
            fecha=str(data["fecha"]),
            hora=str(data["hora"]),
            motivo=str(data["motivo"]),
            profesional=str(data["profesional"]),
            tiene_cuestionario=bool(data["tiene_cuestionario"]),
            observaciones=str(data.get("observaciones", "")),
        )
