# AGENTS.md

This file provides guidance to Codex when working with code in this
repository.

## Proyecto

Actividad academica para la materia **Lenguaje de Programacion**,
3er semestre, Ciencia de Datos.

Todo el codigo debe estar escrito en **Python 3.10+**.

## Principios obligatorios

### SOLID

- **S - Single Responsibility:** cada clase o funcion tiene una unica
  razon para cambiar.
- **O - Open/Closed:** el codigo debe estar abierto para extension y
  cerrado para modificacion. Usar herencia o composicion antes que
  cadenas largas de `if`/`elif`.
- **L - Liskov Substitution:** las subclases deben poder sustituir a su
  clase base sin romper el comportamiento.
- **I - Interface Segregation:** usar interfaces pequenas y especificas;
  no forzar dependencias innecesarias.
- **D - Dependency Inversion:** depender de abstracciones (`ABC`,
  protocolos), no de implementaciones concretas.

### Clean Code

- Usar nombres descriptivos y pronunciables, por ejemplo
  `calcular_promedio`, no `cp`.
- Mantener funciones cortas, idealmente de maximo unas 20 lineas, y con
  una sola responsabilidad.
- Evitar numeros magicos; usar constantes con nombre.
- Evitar comentarios que expliquen el que hace el codigo. Comentar solo
  el por que cuando no sea obvio.
- Aplicar DRY: no duplicar logica. Extraer funciones o clases cuando una
  misma logica aparezca mas de una vez.

### PEP 8

- Indentacion de 4 espacios.
- Lineas de maximo 79 caracteres. Docstrings y comentarios de maximo 72
  caracteres.
- Dos lineas en blanco entre clases o funciones de nivel superior; una
  linea en blanco entre metodos.
- Imports ordenados por grupos: biblioteca estandar, dependencias de
  terceros y codigo local, separados por una linea en blanco.
- Nombres en `snake_case` para variables y funciones, `PascalCase` para
  clases y `UPPER_CASE` para constantes.
- Espacios alrededor de operadores, por ejemplo `x = 1 + 2`.
- No usar espacios dentro de parentesis, por ejemplo `f(a, b)`.

### Heuristicas de Nielsen para interfaces de consola/CLI

1. **Visibilidad del estado:** mostrar siempre en que paso o estado se
   encuentra el programa.
2. **Coincidencia sistema-mundo real:** usar lenguaje del dominio, no
   jerga tecnica, en los mensajes al usuario.
3. **Control y libertad:** ofrecer opcion de cancelar o volver atras
   cuando sea posible.
4. **Consistencia:** mantener mensajes, prompts y formatos de salida
   uniformes.
5. **Prevencion de errores:** validar entradas antes de procesarlas y
   guiar al usuario con ejemplos en el prompt.
6. **Reconocimiento antes que recuerdo:** mostrar opciones disponibles;
   no obligar al usuario a memorizar comandos.
7. **Flexibilidad:** manejar entradas en mayusculas y minusculas.
8. **Diseno minimalista:** no mostrar informacion irrelevante; cada linea
   de salida debe tener proposito.
9. **Mensajes de error claros:** describir el problema en lenguaje llano
   y sugerir la solucion.
10. **Ayuda y documentacion:** incluir opcion `ayuda` o `--help` con
    instrucciones de uso.

## Comandos de desarrollo

```bash
# Ejecutar el programa principal
python main.py

# Ejecutar todos los tests
python -m pytest

# Ejecutar un test especifico
python -m pytest tests/test_<modulo>.py::NombreTest::nombre_metodo -v

# Verificar estilo PEP 8
flake8 . --max-line-length=79

# Verificar tipos estaticos
mypy . --strict

# Formatear automaticamente
black . --line-length 79
```

## Arquitectura del proyecto

```text
Actividad 7/
├── main.py                # Punto de entrada; instancia y arranca la app
├── app/
│   ├── models/            # Entidades del dominio
│   ├── services/          # Logica de negocio
│   ├── repositories/      # Acceso a datos
│   ├── interfaces/        # ABCs / Protocolos
│   └── ui/                # Capa de presentacion CLI
└── tests/                 # Espeja la estructura de app/
```

- `models/` no debe importar nada de `services/` ni de `ui/`.
- `services/` debe recibir dependencias por inyeccion, normalmente en el
  constructor. No debe instanciar repositorios directamente.
- `ui/` solo debe llamar a `services/`; no debe contener logica de
  negocio.
- Los contratos entre capas se definen en `interfaces/` usando `abc.ABC`
  o `typing.Protocol`.

## Convenciones de este proyecto

- Toda funcion publica debe llevar docstring en formato Google Style.
- Todas las firmas deben tener anotaciones de tipos.
- Las excepciones de dominio se definen en `app/exceptions.py` y heredan
  de una base comun.
- Los mensajes visibles para el usuario se centralizan en
  `app/ui/mensajes.py` como constantes.

## Instrucciones para Codex

- Antes de modificar codigo, revisar la estructura existente del proyecto
  y respetar sus patrones.
- Mantener los cambios enfocados en la tarea solicitada.
- No revertir cambios existentes del usuario.
- Usar `rg` para buscar archivos o texto cuando este disponible.
- Usar `apply_patch` para ediciones manuales.
- Al finalizar cambios de codigo, ejecutar las verificaciones relevantes
  disponibles en el proyecto. Si alguna herramienta no esta instalada o
  no puede ejecutarse, reportarlo claramente.