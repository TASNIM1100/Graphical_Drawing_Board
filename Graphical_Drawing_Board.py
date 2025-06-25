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

    # p_ METHOD
    def brush_type(self):
        return "Generic Brush"

# Brush Implementations

class PencilBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.size, capstyle=tk.ROUND)
    def brush_type(self):
        return "Pencil"

class SprayBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        steps = int(max(abs(x2-x1), abs(y2-y1)))
        for i in range(steps):
            t = i / steps
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            for _ in range(self.size * 2):
                dx = random.randint(-self.size*2, self.size*2)
                dy = random.randint(-self.size*2, self.size*2)
                if dx*dx + dy*dy < (self.size*2) ** 2:
                    canvas.create_oval(x+dx, y+dy, x+dx+1, y+dy+1, fill=self.color, outline="")
    def brush_type(self):
        return "Spray"

class CalligraphyBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.size*2, capstyle=tk.BUTT)
        canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.size, capstyle=tk.BUTT)
    def brush_type(self):
        return "Calligraphy"

class PatternBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        steps = int(max(abs(x2-x1), abs(y2-y1)))
        for i in range(steps):
            t = i / steps
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            size = self.size
            if i % 5 == 0:
                canvas.create_rectangle(x-size, y-size, x+size, y+size, fill=self.color, outline="")
    def brush_type(self):
        return "Pattern"

class StarBrush(Brush):
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        steps = int(max(abs(x2-x1), abs(y2-y1)))
        for i in range(steps):
            t = i / steps
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            if i % 10 == 0:
                self.draw_star(canvas, x, y, self.size)
    def draw_star(self, canvas, x, y, size):
        points = []
        for i in range(5):
            angle = i * 144 * 3.14 / 180
            px = x + size * 2 * 0.5 * (1 + 0.5 * random.random()) * (1 if i % 2 == 0 else 0.5) * random.choice([-1, 1])
            py = y + size * 2 * 0.5 * (1 + 0.5 * random.random()) * (1 if i % 2 == 1 else 0.5) * random.choice([-1, 1])
            points.append(px)
            points.append(py)
        canvas.create_polygon(points, fill=self.color, outline="black")
    def brush_type(self):
        return "Star"

class EraserBrush(Brush):
    def __init__(self, size=10):
        # Eraser uses white color by default
        super().__init__(color="white", size=size)
    def draw_stroke(self, canvas, x1, y1, x2, y2):
        # Draw a white line (eraser effect)
        canvas.create_line(x1, y1, x2, y2, fill="white", width=self.size, capstyle=tk.ROUND)
    def brush_type(self):
        return "Eraser"

# Drawing App 

class DrawingApp:
    def __init__(self, master):
        self.master = master
        master.title(" Graphical Drawing Board _(final)")

        self.canvas = tk.Canvas(master, bg="white", width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Brush options
        self.brushes = {
            "Pencil": PencilBrush(),
            "Spray": SprayBrush(),
            "Calligraphy": CalligraphyBrush(),
            "Pattern": PatternBrush(),
            "Star": StarBrush(),
            "Eraser": EraserBrush()
        }
        self.current_brush_name = tk.StringVar(value="Pencil")
        self.size = tk.IntVar(value=3)

        # Color options
        self.colors = {
            "Black": "black",
            "Red": "red",
            "Blue": "blue",
            "Green": "green",
            "Orange": "orange"
        }
        self.color_name = tk.StringVar(value="Black")

        # This part for UI Controls
        control_frame = tk.Frame(master)
        control_frame.pack(fill=tk.X)

        tk.Label(control_frame, text="Brush:").pack(side=tk.LEFT)
        for name in self.brushes:
            tk.Radiobutton(
                control_frame,
                text=name,
                variable=self.current_brush_name,
                value=name,
                command=self.update_brush).pack(side=tk.LEFT)

        tk.Label(control_frame, text="Size:").pack(side=tk.LEFT)
        tk.Scale(
            control_frame,
            from_=1,
            to=15,
            orient=tk.HORIZONTAL,
            variable=self.size,
            command=lambda e: self.update_brush()
        ).pack(side=tk.LEFT)

        tk.Label(control_frame, text="Color:").pack(side=tk.LEFT)
        for cname in self.colors:
            tk.Radiobutton(
                control_frame,
                text=cname,
                variable=self.color_name,
                value=cname,
                command=self.update_brush,
                indicatoron=0,
                background=self.colors[cname],
                width=7
            ).pack(side=tk.LEFT, padx=1)

        tk.Button(control_frame, text="Clear", command=self.clear_canvas).pack(side=tk.RIGHT)

        # Show Brush Type
        self.brush_type_label = tk.Label(master, text="")
        self.brush_type_label.pack()

        self.last_x = None
        self.last_y = None

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.update_brush()

    def update_brush(self):
        brush_name = self.current_brush_name.get()
        size = self.size.get()
        if brush_name == "Eraser":
            # Eraser always uses white color (background)
            self.current_brush = EraserBrush(size=size)
        else:
            color = self.colors[self.color_name.get()]
            brush_class = self.brushes[brush_name].__class__
            self.current_brush = brush_class(color=color, size=size)
        #  Show current brush type
        self.brush_type_label.config(text="Current Brush Type: " + self.current_brush.brush_type())

    def on_press(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.current_brush.draw_stroke(self.canvas, self.last_x, self.last_y, event.x, event.y)
            self.last_x, self.last_y = event.x, event.y

    def on_release(self, event):
        self.last_x = None
        self.last_y = None

    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
