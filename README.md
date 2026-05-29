# Sistema de Bingo - Programación Orientada a Objetos

## Descripción

Este proyecto implementa un juego de Bingo en Python con una arquitectura orientada a objetos y principios SOLID.
El sistema permite configurar la partida con una palabra de 5 letras, un rango máximo de números, jugadores con cartones normales o dobles y ejecutar la partida desde la consola.

## Características

- Juego de Bingo interactivo por consola
- Cartón normal y cartón doble
- Extracción aleatoria de números sin repetición
- Validación de bingo por múltiples patrones
- Inyección de dependencias y diseño basado en interfaces
- Manejo de errores de dominio y presentación separada

## Requisitos

- Python 3.11 o superior

## Ejecución

1. Abre la terminal en la carpeta del proyecto.
2. Ejecuta:

```bash
python main.py
```

3. Sigue las instrucciones en pantalla para:
- Ingresar la palabra del juego (5 letras, sin repetir)
- Definir el número máximo (entre 50 y 90, múltiplo de 5)
- Seleccionar el modo de verificación (filas, columnas, diagonal, etc.)
- Registrar jugadores y elegir cartón normal o doble
- Iniciar la partida

## Estructura del proyecto

- `main.py`: punto de entrada, configuración del juego y menú interactivo.
- `juego.py`: orquesta la partida, recorre turnos, extrae números y valida ganador.
- `bombo.py`: gestiona el bombo de números aleatorios.
- `carton.py`: representa un cartón de bingo y su estado de marcado.
- `carton_doble.py`: extiende `Carton` para manejar dos grillas.
- `jugador.py`: administra los cartones de un jugador y marca números.
- `generador_carton.py`: genera tarjetas 5x5 válidas con casilla central libre.
- `verificador_patron.py`: implementa verificadores de patrones de bingo.
- `verificador_bingo.py`: coordina la verificación de bingo usando múltiples patrones.
- `validador_victoria.py`: determina el ganador entre los jugadores.
- `presentador_resultados.py`: muestra el progreso y resultado final en consola.
- `gestor_jugaadores.py`: administra la colección de jugadores.
- `interfaces.py`: define contratos e interfaces para el diseño del sistema.
- `exceptions.py`: errores de dominio usados por el proyecto.

## Diseño y principios aplicados

- SOLID:
  - Single Responsibility Principle (SRP): cada módulo tiene una responsabilidad clara.
  - Open/Closed Principle (OCP): los validadores y patrones pueden extenderse sin modificar código existente.
  - Liskov Substitution Principle (LSP): `CartonDoble` extiende `Carton` y mantiene la misma interfaz pública.
  - Interface Segregation Principle (ISP): se usan interfaces pequeñas como `IMarcable`, `IVerificable`, `IGeneradorCarton`, etc.
  - Dependency Inversion Principle (DIP): el `Juego` depende de contratos (`IBombo`, `IGestorJugadores`, `IValidadorVictoria`, `IPresentadorResultados`) en vez de implementaciones concretas.

- Arquitectura:
  - `main.py` actúa como Composition Root, ensamblando componentes y decidiendo qué implementaciones usar.
  - La presentación se separa de la lógica de negocio en `presentador_resultados.py`.
  - La generación de cartones y la verificación de patrones están desacopladas.

## Flujo de juego

1. `main.py` solicita configuración al usuario.
2. Se crea un `Juego` con sus dependencias inyectadas.
3. Se registran jugadores con `Carton` o `CartonDoble`.
4. `Juego.jugar()` recorre turnos, extrae números del `Bombo` y marca en los cartones.
5. Al final de cada turno, `ValidadorVictoria` verifica si algún jugador ganó.
6. `PresentadorResultados` muestra el resultado final y el historial.

## Ejemplo de uso

- Inicia el juego con `python main.py`
- Ingresa la palabra `BINGO`
- Ingresa el número máximo `75`
- Selecciona modo `filas_columnas`
- Agrega jugadores y elige cartones normales o dobles
- Inicia la partida y observa cómo se extraen números y se anuncia el ganador

## Autores

- Jose Angel Mejia Medina
- Henrry Román Puerres Tipas

