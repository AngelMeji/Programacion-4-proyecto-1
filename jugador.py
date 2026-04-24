"""
Representa un jugador del juego de bingo.

Responsabilidades:
- Gestionar uno o más cartones.
- Marcar números en sus cartones.
- Verificar si ha ganado.
- Llevar conteo de números marcados.

Relación:
- Contiene cartones que pueden existir independientemente (agregación).
"""
class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cartones: list = []
        self.numeros_marcados = 0   # Contador de números marcados en todos los cartones

    def agregar_carton(self, carton)-> None:
        """Agrega un cartón al jugador."""
        self.cartones.append(carton)
        
    def eliminar_carton(self, carton)-> None:
        """Elimina un cartón del jugador."""
        if carton in self.cartones:
            self.cartones.remove(carton)
            
    def marcar_numero(self, numero)-> None:
         """Marca un número en todos los cartones del jugador."""
         marcados = 0
         for carton in self.cartones:
            if carton.marcar_numero(numero):
                marcados += 1
         self.numeros_marcados += marcados
        
    def verificar_bingo(self)-> bool:
          """Verifica si alguno de sus cartones tiene bingo."""
          return any(carton.verificar_bingo() for carton in self.cartones)
      
    