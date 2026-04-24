# Sistema de Bingo - Programación Orientada a Objetos

## Descripción

Este proyecto implementa un sistema completo de Bingo utilizando Programación Orientada a Objetos en Python. A partir de un generador de cartones parametrizable, se construye una simulación completa que incluye jugadores, cartones, un bombo y la ejecución de la partida.

El sistema permite:
- Configurar la palabra del bingo (5 letras sin repetir)
- Definir el rango máximo de números (entre 50 y 90, múltiplo de 5)
- Simular una partida completa hasta que haya un ganador

---

## Estructura del proyecto

proyecto_bingo/
│
├── carton.py
├── carton_doble.py
├── jugador.py
├── bombo.py
├── juego.py
├── main.py
└── README.md


---

## Cómo ejecutar

1. Asegúrate de tener Python 3.11 o superior
2. Ejecuta el siguiente comando en la terminal:

```bash
python main.py
```

3. Sigue las instrucciones en consola 

---

## Diseño del sistema

El sistema está compuesto por las siguientes clases:

- Carton: representa un cartón de bingo
- CartonDoble: extiende Carton y contiene dos grillas
- Jugador: gestiona cartones y verifica si ha ganado
- Bombo: genera números aleatorios sin repetición
- Juego: coordina toda la partida

## Justificación de relaciones

### 1. Carton → CartonDoble (Herencia)

CartonDoble es un tipo de Carton, ya que comparte su comportamiento base pero lo extiende para manejar dos grillas. Se utiliza herencia para reutilizar código y especializar la lógica.

### 2. Juego → Bombo (Composición)

El bombo es parte fundamental del juego. Se crea junto con el juego y no tiene sentido sin él. Su ciclo de vida depende completamente del Juego.

### 3. Jugador → Carton (Agregación)

Los cartones existen independientemente de los jugadores. Un cartón puede ser creado antes, asignado o eliminado sin afectar su existencia. Por eso se modela como agregación.

### 4. Juego → Jugador (Asociación)

El juego no crea ni destruye jugadores, solo los registra. Los jugadores pueden existir fuera del juego, por lo que la relación es de asociación.

## Características destacadas
- Uso de herencia y polimorfismo
- Implementación sin librerías externas
- Uso de type hints
- Código organizado por clases
- Cumplimiento de convenciones PEP 8

## Autores
- Jose Angel Mejia Medina
- Henrry Román Puerres Tipas

