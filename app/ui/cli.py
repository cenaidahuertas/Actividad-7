"""Interfaz de consola para el CRUD de sesiones."""

from __future__ import annotations

from app.controllers.sesion_controller import SesionController
from app.ui import mensajes


class SesionCLI:
    """Vista CLI para gestionar sesiones de seguimiento."""

    def __init__(self, controller: SesionController) -> None:
        self._controller = controller

    def run(self) -> None:
        """Inicia el menu principal."""
        while True:
            print(mensajes.MENU_PRINCIPAL)
            opcion = input(mensajes.PROMPT_OPCION).strip()
            if opcion == "1":
                self._crear_sesion()
            elif opcion == "2":
                self._listar_sesiones()
            elif opcion == "3":
                self._actualizar_sesion()
            elif opcion == "4":
                self._eliminar_sesion()
            elif opcion == "5":
                print("Hasta luego.")
                break
            else:
                print("Opcion invalida. Intente nuevamente.")

    def _crear_sesion(self) -> None:
        payload = self._capturar_datos(include_id=True)
        ok, mensaje = self._controller.crear(payload)
        print(mensaje)

    def _listar_sesiones(self) -> None:
        ok, resultado = self._controller.listar()
        if not ok:
            print(resultado)
            return
        sesiones = resultado
        if not sesiones:
            print("No hay sesiones registradas.")
            return
        for sesion in sesiones:
            print(sesion)

    def _actualizar_sesion(self) -> None:
        sesion_id = input(mensajes.PROMPT_ID).strip()
        payload = self._capturar_datos(include_id=False)
        payload["sesion_id"] = sesion_id
        ok, mensaje = self._controller.actualizar(sesion_id, payload)
        print(mensaje)

    def _eliminar_sesion(self) -> None:
        sesion_id = input(mensajes.PROMPT_ID).strip()
        confirmacion = input(mensajes.PROMPT_ELIMINAR).strip().lower()
        if confirmacion != "si":
            print("Operacion cancelada.")
            return
        ok, mensaje = self._controller.eliminar(sesion_id)
        print(mensaje)

    def _capturar_datos(self, include_id: bool) -> dict[str, object]:
        payload: dict[str, object] = {}
        if include_id:
            payload["sesion_id"] = input(mensajes.PROMPT_ID).strip()
        cuestionario = input(mensajes.PROMPT_CUESTIONARIO).strip().lower()
        payload.update({
            "estudiante_codigo": input(mensajes.PROMPT_CODIGO).strip(),
            "fecha": input(mensajes.PROMPT_FECHA).strip(),
            "hora": input(mensajes.PROMPT_HORA).strip(),
            "motivo": input(mensajes.PROMPT_MOTIVO).strip(),
            "profesional": input(mensajes.PROMPT_PROFESIONAL).strip(),
            "tiene_cuestionario": cuestionario == "si",
            "observaciones": input(mensajes.PROMPT_OBSERVACIONES).strip(),
        })
        return payload
