import tkinter as tk

def start_draw(event):
    global last_x, last_y
    last_x = event.x
    last_y = event.y

def draw(event):
    global last_x, last_y
    canvas.create_line(last_x, last_y, event.x, event.y, fill="black", width=3)
    last_x = event.x
    last_y = event.y

root = tk.Tk()
root.title("Drawing_Board")

canvas = tk.Canvas(root, bg="white", width=600, height=400)
canvas.pack()
last_x = None
last_y = None

canvas.bind("<ButtonPress-1>", start_draw)
canvas.bind("<B1-Motion>", draw)

root.mainloop()
