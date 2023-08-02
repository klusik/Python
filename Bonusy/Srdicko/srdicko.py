"""
    Srdíčko pro Haničku
"""

import tkinter as tk

class Heart:
    def __init__(self):
        self.create_heart()

    def create_heart(self):
        window = tk.Tk()

        # Create a PhotoImage object and load the image using the 'file' parameter
        heart_picture = tk.PhotoImage(file='heart.png')

        # Create a label with the heart image
        self.heart_label = tk.Label(window, image=heart_picture)
        self.heart_label.pack()

        # Bind the click event to a callback function
        self.heart_label.bind('<Button-1>', self.show_hanicka_label)

        # Initialize the Hanička label, but don't show it initially
        self.hanicka_label = tk.Label(window, text="Rudolfína", font=("Helvetica", 80), bg="red", fg="white")
        self.hanicka_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.hanicka_label.lower()  # Hide the label initially

        window.mainloop()

    def show_hanicka_label(self, event):
        # This function is called when the heart label is clicked
        self.hanicka_label.lift()  # Bring the Hanička label to the front, making it visible

if __name__ == "__main__":
    """ 
    Main app 
    """

    srdiiicko = Heart()

