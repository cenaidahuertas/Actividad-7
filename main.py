"""Punto de entrada de la aplicacion."""

from app.controllers.sesion_controller import SesionController
from app.repositories.json_sesion_repository import JsonSesionRepository
from app.services.sesion_service import SesionService
from app.ui.cli import SesionCLI


def main() -> None:
    """Configura dependencias e inicia la interfaz CLI."""
    repository = JsonSesionRepository("data/sesiones.json")
    service = SesionService(repository)
    controller = SesionController(service)
    cli = SesionCLI(controller)
    cli.run()


if __name__ == "__main__":
    main()
