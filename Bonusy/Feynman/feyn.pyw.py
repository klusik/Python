import tkinter as tk


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Feynman Diagram Drawer")

        # Create a canvas for drawing
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Grid settings
        self.grid_size = 20  # Size of the grid
        self.draw_grid()

        # Bind mouse events to methods
        self.canvas.bind("<B1-Motion>", self.draw)

    def draw_grid(self):
        # Draw grid lines
        for i in range(0, 800, self.grid_size):
            self.canvas.create_line(i, 0, i, 600, fill="light gray")
        for j in range(0, 600, self.grid_size):
            self.canvas.create_line(0, j, 800, j, fill="light gray")

    def draw(self, event):
        # Draw a small rectangle (dot) on the canvas at the mouse position
        x = event.x - (event.x % self.grid_size)
        y = event.y - (event.y % self.grid_size)
        self.canvas.create_rectangle(x, y, x + self.grid_size, y + self.grid_size, fill='black', outline='black')


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
