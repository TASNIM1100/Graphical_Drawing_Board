import tkinter as tk

class Brush:
    def __init__(self, color="black", size=3):
        self.color = color
        self.size = size

    def draw(self, canvas, x1, y1, x2, y2):
        canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.size, capstyle=tk.ROUND)

class DrawingApp:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, bg="white", width=600, height=400)
        self.canvas.pack()
        self.brush = Brush(color="black", size=3)
        self.last_x = None
        self.last_y = None
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.brush.draw(self.canvas, self.last_x, self.last_y, event.x, event.y)
            self.last_x = event.x
            self.last_y = event.y

    def on_release(self, event):
        self.last_x = None
        self.last_y = None

root = tk.Tk()
root.title(" OOP One Brush")
app = DrawingApp(root)
root.mainloop()
