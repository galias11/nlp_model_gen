# nlp_model_gen changelog

## Version 0.1.5:

- Initial release version.

## Version 0.1.6:

#### New features

- TF-0035: Control de la configuración del modulo de procesamiento de palabras.
- TF-0044: Prevenir que la edición de nombre haga que se pierda relación con su directorio de modelo.
- TF-0053: Implementación funcional del administrador de tareas
- TF-0054: Obtener el estado de una tarea
- TF-0055: Obtener los listados de tareas activas y completadas del task manager.
- TF-0062: Abortar una tarea desde el task manager.

#### Tasks / Improvements

- TF-0045: Eliminar archivos del prototipo del repositorio
- TF-0051: Task manager: Implementación del diagrama de clases.
- TF-0050: Cambiar atributo de identificación de los modelos.

#### Bugs fixed

- TFI-0002: No se puede crear un modelo a pesar de que no hay ninguno con ese nombre.
- TFI-0005: No se puede borrar un modelo durante la misma sesión de su creación.
- TFI-0004: Color no válido para el logger en plataforma Windows

## Version 0.1.7:

#### New features

- TF-0046: Procesar los resultados del análisis del tokenizer a nivel oración.
- TF-0043: Crear y guardar ejemplos de entrenamiento.
- TF-0064: Obtener la lista de ejemplo por modelo y estado.
- TF-0065: Actualizar el controlador de entrenamiento cuando se crea un nuevo modelo.
- TF-0038: Aprobar o desaprobar un ejemplo de entrenamiento.
- TF-0066: Actualizar el controlador de entrenamiento cuando se elimina un modelo.
- TF-0039: Aplicar los ejemplos de entrenamiento aprobados para un modelo.

#### Tasks / Improvements

- TF-0067: Agregar logs a las operaciones que realiza el modulo de entrenamiento.
- TF-0052: System controller: Implementación del diagrama de clases.
- TF-0049: Implementación de la estructura del modulo de entrenamiento.

#### Bugs fixed

- TFI-0004: Color no válido para el logger en plataforma Windows.

## Version 0.1.8:

#### New features

- TF-0057: Mover funcionalidad de análisis de texto al modulo de aplicación.
- TF-0058: Aplicar los ejemplos de entrenamiento desde el módulo de administración.

#### Tasks / Improvements

- TF-0056: Implementar modelo de clases del modulo de aplicación.
- TF-0068: Agregar los métodos para el control de los ejemplos de entrenamiento al admin module.

#### Bugs fixed

- TFI-0007: Se pierde el color del log principal cuando se aplican textos insertados con otros colores.
- TFI-0006: Se pueden aprobar / desaprobar ejemplos previamente aprobados / desaprobados.

## Version 0.1.9:

#### New features

- TF-0047: Permitir el procesamiento concurrente de archivos.

#### Tasks / Improvements

- TF-0060: Integrar modulo de aplicación con el controlador de sistema.
- TF-0059: Integrar modulo de administración con el controlador de sistema.
- TF-0048: Implementar y aplicar modulo de manejo de errores

#### Bugs fixed

- TFI-0008: El elemento token_text esta devolviendo la oración completa en lugar del token.
- TFI-0009: Implementar funcionalidades faltantes en el controlador de sistema

## Version 0.1.10:

#### New features

- TF-0075: Agregar excepciones para el analizador.
- TF-0076: Habilitar / Deshabilitar excepciones para el analizador.
- TF-0074: Aplicar excepciones al analizador al momento de analizar los tokens de un texto.
- TF-0078: Consultar las excepciones al analizador para un modelo particular.

#### Tasks / Improvements

- TF-0077: Agregar logs a funcionalidades de manejo de excepciones del analizador

#### Bugs fixed

- TFI-0010: Funcionalidad de descartar un ejemplo de entrenamiento ausente en system controller.

## Version 0.1.11:

#### Hotfix

- TF-0079: Hotfix: Model creation process