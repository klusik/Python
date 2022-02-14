#tkinter
import Tkinter as tk
import ttk

class App(tk.Tk):
    def __init__ (self):
        tk.Tk.__init__(self)

        self.title("Tkinter Tab Widgets")
        self.minsize(600,400)

        tabControl = ttk.Notebook(self)
        
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text = "Tab 1")

        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text = "Tab 1")

        tabControl.pack(expan = 1, fill = "both")

app = App()
app.mainloop()

                       
