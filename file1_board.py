import tkinter as tk
import random

class Brush:
    def __init__(self, color="black", size=3):
        self.color = color
        self.size = size

    def draw(self, canvas, x1, y1, x2, y2):
        canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.size, capstyle=tk.ROUND)

class SprayBrush(Brush):
    def draw(self, canvas, x1, y1, x2, y2):
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

class DrawingApp:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, bg="white", width=600, height=400)
        self.canvas.pack()
        self.brushes = {
            "Pencil": Brush(color="black", size=3),
            "Spray": SprayBrush(color="black", size=3)
        }
        self.current_brush = self.brushes["Pencil"]
        self.last_x = None
        self.last_y = None

        btn_frame = tk.Frame(master)
        btn_frame.pack()
        for name in self.brushes:
            tk.Button(btn_frame, text=name, command=lambda n=name: self.select_brush(n)).pack(side=tk.LEFT)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def select_brush(self, name):
        self.current_brush = self.brushes[name]

    def on_press(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.current_brush.draw(self.canvas, self.last_x, self.last_y, event.x, event.y)
            self.last_x = event.x
            self.last_y = event.y

    def on_release(self, event):
        self.last_x = None
        self.last_y = None

root = tk.Tk()
root.title("Multiple Brushes (pencil , spray)")
app = DrawingApp(root)
root.mainloop()
