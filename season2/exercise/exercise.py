from __future__ import annotations
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    """
    Interface Shape declara operações que todas as formas concretas
    devem implementar.
    """
    
    @abstractmethod
    def draw(self) -> str:
        pass
    
    @abstractmethod
    def calculate_area(self) -> float:
        pass


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    def draw(self) -> str:
        return "Desenhando um círculo"
    
    def calculate_area(self) -> float:
        return math.pi * (self.radius ** 2)
    
    def __str__(self) -> str:
        return f"Circle com raio {self.radius}"


class Square(Shape):
    def __init__(self, side_length: float):
        self.side_length = side_length
    
    def draw(self) -> str:
        return "Desenhando um quadrado"
    
    def calculate_area(self) -> float:
        return self.side_length ** 2
    
    def __str__(self) -> str:
        return f"Square com lado {self.side_length}"


# Criador (Creator)
class ShapeCreator(ABC):
    """
    A classe ShapeCreator declara o método fábrica que deve retornar
    um objeto da classe Shape. As subclasses de ShapeCreator geralmente
    fornecem a implementação desse método.
    """
    
    @abstractmethod
    def factory_method(self) -> Shape:
        """
        Subclasses devem implementar este método para criar uma Shape específica.
        """
        pass
    
    def draw_and_describe(self) -> str:
        """
        Lógica de negócio que utiliza o objeto Shape criado pelo factory_method.
        """
        shape = self.factory_method()
        
        result = (f"ShapeCreator: {shape}\n"
                  f"Método draw: {shape.draw()}\n"
                  f"Área calculada: {shape.calculate_area():.2f}")
        
        return result


class CircleCreator(ShapeCreator):
    def __init__(self, radius: float):
        self.radius = radius
    
    def factory_method(self) -> Shape:
        return Circle(self.radius)


class SquareCreator(ShapeCreator):
    def __init__(self, side_length: float):
        self.side_length = side_length
    
    def factory_method(self) -> Shape:
        return Square(self.side_length)


def client_code(creator: ShapeCreator) -> None:
    """
    O código cliente trabalha com uma instância de um criador concreto,
    embora através da sua interface base. Enquanto o cliente continuar
    trabalhando com o criador via interface base, você pode passar
    qualquer subclasse do criador.
    """
    print(f"Cliente: Não sei qual classe do criador estou usando, mas funciona.\n"
          f"{creator.draw_and_describe()}")


if __name__ == "__main__":
    print("Aplicação: Iniciada com CircleCreator.")
    client_code(CircleCreator(5.0))
    print("\n")
    
    print("Aplicação: Iniciada com SquareCreator.")
    client_code(SquareCreator(4.0))