# Sistema de Bingo - Programacion Orientada a Objetos

## Descripcion

Este proyecto implementa un juego de Bingo en Python con una arquitectura orientada a objetos y principios SOLID.
El sistema permite configurar la partida con una palabra de 5 letras, un rango maximo de numeros, jugadores con cartones normales o dobles y ejecutar la partida desde la consola.

## Caracteristicas

- Juego de Bingo interactivo por consola
- Carton normal y carton doble construido por composicion
- Extraccion aleatoria de numeros sin repeticion
- Validacion de bingo por multiples patrones
- Inyeccion de dependencias y diseño basado en interfaces
- Manejo de errores de dominio con excepciones especificas
- Presentacion separada para consola

## Requisitos

- Python 3.11 o superior

## Ejecucion

1. Abre la terminal en la carpeta del proyecto.
2. Ejecuta:

```bash
python main.py
```

3. Sigue las instrucciones en pantalla para:
- Ingresar la palabra del juego (5 letras, sin repetir)
- Definir el numero maximo (entre 50 y 90, multiplo de 5)
- Seleccionar el modo de verificacion (filas, columnas, diagonal, etc.)
- Registrar jugadores y elegir carton normal o doble
- Iniciar la partida

## Estructura del proyecto

- `main.py`: punto de entrada, composition root y menú interactivo.
- `juego.py`: orquesta la partida, recorre turnos, extrae numeros y valida ganador.
- `bombo.py`: implementa `IBombo`, valida configuracion y gestiona extracciones sin repeticion.
- `carton.py`: representa un carton de bingo y su estado de marcado.
- `carton_doble.py`: compone dos cartones simples para el modo doble.
- `jugador.py`: administra los cartones de un jugador y marca numeros.
- `generador_carton.py`: genera tarjetas 5x5 validas con casilla central libre.
- `verificador_patron.py`: implementa verificadores de patrones de bingo.
- `verificador_bingo.py`: coordina la verificacion de bingo usando multiples patrones.
- `validador_victoria.py`: determina el ganador entre los jugadores.
- `presentador_resultados.py`: muestra el progreso, errores y resultado final en consola.
- `gestor_jugaadores.py`: administra la coleccion de jugadores.
- `interfaces.py`: define contratos e interfaces para el diseño del sistema.
- `exceptions.py`: errores de dominio usados por el proyecto.

## Diseno y principios aplicados

- SOLID:
  - Single Responsibility Principle (SRP): cada modulo mantiene una responsabilidad clara.
  - Open/Closed Principle (OCP): los validadores y patrones pueden extenderse sin modificar el flujo principal.
  - Liskov Substitution Principle (LSP): `CartonDoble` ahora se apoya en composicion y conserva el contrato de carton marcado y verificable.
  - Interface Segregation Principle (ISP): se usan interfaces pequeñas como `IMarcable`, `IVerificable`, `IGeneradorCarton`, etc.
  - Dependency Inversion Principle (DIP): el `Juego` depende de contratos (`IBombo`, `IGestorJugadores`, `IValidadorVictoria`, `IPresentadorResultados`) en vez de implementaciones concretas.

- Arquitectura:
  - `main.py` actua como Composition Root, ensamblando componentes y decidiendo que implementaciones usar.
  - La presentacion se separa de la logica de negocio en `presentador_resultados.py`.
  - La generacion de cartones y la verificacion de patrones estan desacopladas.
  - Las excepciones de dominio estan centralizadas en `exceptions.py`.

## Flujo de juego

1. `main.py` solicita configuracion al usuario.
2. Se crea un `Juego` con sus dependencias inyectadas.
3. Se registran jugadores con `Carton` o `CartonDoble`.
4. `Juego.jugar()` recorre turnos, extrae numeros del `Bombo` y marca en los cartones.
5. Al final de cada turno, `ValidadorVictoria` verifica si algún jugador ganó.
6. `PresentadorResultados` muestra el resultado final y el historial.

## Ejemplo de uso

- Inicia el juego con `python main.py`
- Ingresa la palabra `BINGO`
- Ingresa el numero maximo `75`
- Selecciona modo `filas_columnas`
- Agrega jugadores y elige cartones normales o dobles
- Inicia la partida y observa cómo se extraen números y se anuncia el ganador

## Autores

- Jose Angel Mejia Medina
- Henrry Román Puerres Tipas

