import tkinter as tk
from abc import ABC, abstractmethod
import random

#  Here is Abstract Brush Base Class 
class Brush(ABC):
    def __init__(self, color="black", size=3):
        self.color = color
        self.size = size

    @abstractmethod
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        pass

    def brush_type(self):
        return "Generic Brush"

class PencilBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        pass 
    def brush_type(self):
        return "Pencil"

class SprayBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        pass
    def brush_type(self):
        return "Spray"

class CalligraphyBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        pass
    def brush_type(self):
        return "Calligraphy"

class PatternBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        pass
    def brush_type(self):
        return "Pattern"

class StarBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        pass
    def brush_type(self):
        return "Star"

class EraserBrush(Brush):
    def __init__(self, size=10):
        super().__init__(color="white", size=size)
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        pass
    def brush_type(self):
        return "Eraser"

# Simple tests  

def test_brush_instantiation():
    pencil = PencilBrush("red", 5)
    assert pencil.color == "red"
    assert pencil.size == 5
    assert pencil.brush_type() == "Pencil"
    print("PencilBrush works!")

    spray = SprayBrush("green", 7)
    assert spray.color == "green"
    assert spray.size == 7
    assert spray.brush_type() == "Spray"
    print("SprayBrush works!")

    calli = CalligraphyBrush("blue", 2)
    assert calli.color == "blue"
    assert calli.size == 2
    assert calli.brush_type() == "Calligraphy"
    print("CalligraphyBrush works!")

    pattern = PatternBrush("orange", 3)
    assert pattern.color == "orange"
    assert pattern.size == 3
    assert pattern.brush_type() == "Pattern"
    print("PatternBrush works!")

    star = StarBrush("black", 6)
    assert star.color == "black"
    assert star.size == 6
    assert star.brush_type() == "Star"
    print("StarBrush works!")

    eraser = EraserBrush(11)
    assert eraser.color == "white"
    assert eraser.size == 11
    assert eraser.brush_type() == "Eraser"
    print("EraserBrush works!")

def test_polymorphism():
    brushes = [
        PencilBrush("red", 1),
        SprayBrush("green", 2),
        CalligraphyBrush("blue", 3),
        PatternBrush("orange", 4),
        StarBrush("black", 5),
        EraserBrush(6)
    ]
    types = [b.brush_type() for b in brushes]
    assert types == ["Pencil", "Spray", "Calligraphy", "Pattern", "Star", "Eraser"]
    print("Polymorphism test passed!")

if __name__ == "__main__":
    test_brush_instantiation()
    test_polymorphism()
    print("All tests passed!")
