# Actividad 7 - CRUD de SesionSeguimiento

Proyecto en Python que implementa un CRUD de la entidad
`SesionSeguimiento`, con persistencia en JSON, arquitectura MVC y
patrón Repository.

## Requisitos cumplidos

- CRUD completo: crear, listar, actualizar y eliminar sesiones.
- Persistencia en `data/sesiones.json`.
- Uso de MVC:
  - Modelo: `SesionSeguimiento`
  - Controlador: `SesionController`
  - Vista: `SesionCLI`
- Uso de Repository: `SesionRepository` y `JsonSesionRepository`
- Aplicación de principios SOLID.
- Pruebas unitarias con más de 10 casos.

## Estructura principal

```text
app/
├── controllers/
├── interfaces/
├── models/
├── repositories/
├── services/
└── ui/
tests/
main.py
```

## Ejecución

```bash
python main.py
```

## Pruebas

```bash
python -m pytest -v
```
