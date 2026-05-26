"""Pruebas unitarias para el CRUD de sesiones."""

from __future__ import annotations

import json

import pytest

from app.controllers.sesion_controller import SesionController
from app.exceptions import CuestionarioRequeridoError
from app.exceptions import EntityNotFoundError
from app.exceptions import HorarioFueraDeRangoError
from app.exceptions import PersistenceError
from app.exceptions import SesionDuplicadaError
from app.exceptions import ValidationError
from app.models.sesion_seguimiento import SesionSeguimiento
from app.repositories.json_sesion_repository import JsonSesionRepository
from app.services.sesion_service import SesionService


@pytest.fixture
def repository(tmp_path: pytest.TempPathFactory) -> JsonSesionRepository:
    """Entrega un repositorio temporal para las pruebas."""
    return JsonSesionRepository(str(tmp_path / "sesiones.json"))


@pytest.fixture
def service(repository: JsonSesionRepository) -> SesionService:
    """Entrega un servicio configurado para pruebas."""
    return SesionService(repository)


@pytest.fixture
def controller(service: SesionService) -> SesionController:
    """Entrega un controlador configurado para pruebas."""
    return SesionController(service)


def build_sesion(**overrides: object) -> SesionSeguimiento:
    """Construye una sesion valida para pruebas."""
    data: dict[str, object] = {
        "sesion_id": "SES-001",
        "estudiante_codigo": "EST-100",
        "fecha": "2026-05-25",
        "hora": "10:00",
        "motivo": "Seguimiento emocional",
        "profesional": "Psicologa Ana",
        "tiene_cuestionario": True,
        "observaciones": "Sin novedades",
    }
    data.update(overrides)
    return SesionSeguimiento.from_dict(data)


def test_modelo_crear_sesion_valida() -> None:
    sesion = build_sesion()
    assert sesion.sesion_id == "SES-001"


def test_modelo_rechaza_fecha_invalida() -> None:
    with pytest.raises(ValidationError) as exc_info:
        build_sesion(fecha="25-05-2026")
    assert "YYYY-MM-DD" in str(exc_info.value)


def test_servicio_crear_sesion_persiste_en_json(
    service: SesionService,
) -> None:
    sesion = build_sesion()
    creada = service.crear_sesion(sesion)
    assert creada.sesion_id == "SES-001"
    assert len(service.listar_sesiones()) == 1


def test_servicio_rechaza_sesion_sin_cuestionario(
    service: SesionService,
) -> None:
    sesion = build_sesion(tiene_cuestionario=False)
    with pytest.raises(CuestionarioRequeridoError):
        service.crear_sesion(sesion)


def test_servicio_rechaza_horario_fuera_de_rango(
    service: SesionService,
) -> None:
    sesion = build_sesion(hora="19:00")
    with pytest.raises(HorarioFueraDeRangoError):
        service.crear_sesion(sesion)


def test_servicio_rechaza_sesion_duplicada_mismo_dia(
    service: SesionService,
) -> None:
    service.crear_sesion(build_sesion())
    duplicada = build_sesion(
        sesion_id="SES-002",
        hora="11:00",
    )
    with pytest.raises(SesionDuplicadaError):
        service.crear_sesion(duplicada)


def test_servicio_actualiza_sesion_existente(
    service: SesionService,
) -> None:
    service.crear_sesion(build_sesion())
    actualizada = build_sesion(motivo="Seguimiento academico")
    resultado = service.actualizar_sesion("SES-001", actualizada)
    assert resultado.motivo == "Seguimiento academico"


def test_servicio_elimina_sesion_existente(
    service: SesionService,
) -> None:
    service.crear_sesion(build_sesion())
    service.eliminar_sesion("SES-001")
    assert service.listar_sesiones() == []


def test_repositorio_levanta_error_si_no_existe(
    repository: JsonSesionRepository,
) -> None:
    with pytest.raises(EntityNotFoundError):
        repository.get_by_id("NO-EXISTE")


def test_repositorio_detecta_json_corrupto(tmp_path: pytest.TempPathFactory) -> None:
    json_path = tmp_path / "corrupto.json"
    json_path.write_text("{no es json}", encoding="utf-8")
    repository = JsonSesionRepository(str(json_path))
    with pytest.raises(PersistenceError):
        repository.list_all()


def test_controlador_crea_sesion_y_retorna_mensaje(
    controller: SesionController,
) -> None:
    ok, mensaje = controller.crear(build_sesion().to_dict())
    assert ok is True
    assert mensaje == "Sesion creada correctamente."


def test_controlador_lista_sesiones(
    controller: SesionController,
) -> None:
    controller.crear(build_sesion().to_dict())
    ok, resultado = controller.listar()
    assert ok is True
    assert isinstance(resultado, list)
    assert resultado[0]["sesion_id"] == "SES-001"


def test_controlador_retorna_error_de_negocio(
    controller: SesionController,
) -> None:
    payload = build_sesion(tiene_cuestionario=False).to_dict()
    ok, mensaje = controller.crear(payload)
    assert ok is False
    assert "cuestionario" in mensaje.lower()


def test_persistencia_json_guarda_estructura_esperada(
    repository: JsonSesionRepository,
) -> None:
    repository.create(build_sesion())
    contenido = repository._file_path.read_text(encoding="utf-8")
    data = json.loads(contenido)
    assert data[0]["estudiante_codigo"] == "EST-100"
