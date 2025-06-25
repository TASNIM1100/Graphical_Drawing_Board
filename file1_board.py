import tkinter as tk
from abc import ABC, abstractmethod
import random

# Simple abstract brush base class
class Brush(ABC):
    def __init__(self, color="black", size=3):
        self.color = color
        self.size = size

    @abstractmethod
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        pass

# Pencil brush draws simple lines
class PencilBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.size, capstyle=tk.ROUND)

# Spray brush for spray paint effect
class SprayBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        steps = int(max(abs(x2-x1), abs(y2-y1)))
        for i in range(steps):
            t = i / steps if steps else 0
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            for _ in range(self.size * 2):
                dx = random.randint(-self.size*2, self.size*2)
                dy = random.randint(-self.size*2, self.size*2)
                if dx*dx + dy*dy < (self.size*2) ** 2:
                    canvas.create_oval(x+dx, y+dy, x+dx+1, y+dy+1, fill=self.color, outline="")

# Calligraphy brush draws two lines for effect
class CalligraphyBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.size*2, capstyle=tk.BUTT)
        canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.size, capstyle=tk.BUTT)

# Pattern brush draws rectangles on the path
class PatternBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        steps = int(max(abs(x2-x1), abs(y2-y1)))
        for i in range(steps):
            t = i / steps if steps else 0
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            if i % 5 == 0:
                canvas.create_rectangle(x-self.size, y-self.size, x+self.size, y+self.size, fill=self.color, outline="")

# Eraser brush (always "white")
class EraserBrush(Brush):
    def __init__(self, size=10):
        super().__init__(color="white", size=size)
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        canvas.create_line(x1, y1, x2, y2, fill="white", width=self.size, capstyle=tk.ROUND)

# Drawing Application
class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, bg="white", width=600, height=400)
        self.canvas.pack()
        self.color = tk.StringVar(value="black")
        self.size = tk.IntVar(value=3)
        # Store brush classes, not objects
        self.brushes = {
            "Pencil": PencilBrush,
            "Spray": SprayBrush,
            "Calligraphy": CalligraphyBrush,
            "Pattern": PatternBrush,
            "Eraser": EraserBrush
        }
        self.current_brush_name = tk.StringVar(value="Pencil")
        self.current_brush = self.brushes["Pencil"](color=self.color.get(), size=self.size.get())
        self.last_x = None
        self.last_y = None

        control = tk.Frame(master)
        control.pack()
        # Brush select
        tk.Label(control, text="Brush:").pack(side=tk.LEFT)
        for name in self.brushes:
            tk.Radiobutton(control, text=name, variable=self.current_brush_name, value=name, command=self.update_brush).pack(side=tk.LEFT)
        # Size select
        tk.Label(control, text="Size:").pack(side=tk.LEFT)
        tk.Scale(control, from_=1, to=15, orient=tk.HORIZONTAL, variable=self.size, command=lambda e: self.update_brush()).pack(side=tk.LEFT)
        # Color select
        tk.Label(control, text="Color:").pack(side=tk.LEFT)
        for c in ["black", "red", "blue", "green", "orange"]:
            tk.Radiobutton(control, text=c.capitalize(), variable=self.color, value=c, command=self.update_brush).pack(side=tk.LEFT)
        # Clear button
        tk.Button(control, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.update_brush()

    def update_brush(self):
        brush_name = self.current_brush_name.get()
        size = self.size.get()
        if brush_name == "Eraser":
            self.current_brush = EraserBrush(size=size)
        else:
            self.current_brush = self.brushes[brush_name](color=self.color.get(), size=size)

    def on_press(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.current_brush.draw_stroke(self.canvas, self.last_x, self.last_y, event.x, event.y)
            self.last_x = event.x
            self.last_y = event.y

    def on_release(self, event):
        self.last_x = None
        self.last_y = None

    def clear_canvas(self):
        self.canvas.delete("all")

root = tk.Tk()
root.title("with comment")
app = DrawingApp(root)
root.mainloop()
