import os
import tkinter as tk
from tkinter import filedialog

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("One-Letter Word Fixer")

        # File selection frame
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.file_path_var = tk.StringVar()

        # Text field for file path
        self.file_entry = tk.Entry(self.frame, textvariable=self.file_path_var, width=50)
        self.file_entry.pack(side=tk.LEFT, padx=5)

        # "..." button for file dialog
        self.browse_button = tk.Button(self.frame, text="...", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT, padx=5)

        # Process button
        self.process_button = tk.Button(root, text="Process File", command=self.process_file)
        self.process_button.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("TeX files", "*.tex"), ("All files", "*.*")])
        if file_path:
            self.file_path_var.set(file_path)

    def process_file(self):
        file_path = self.file_path_var.get()
        if not os.path.isfile(file_path):
            self.show_error("Invalid file path")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            processed_lines = [self.fix_line(line) for line in lines]

            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(processed_lines)

            self.show_message("File processed successfully!")
        except Exception as e:
            self.show_error(f"Error processing file: {e}")

    def fix_line(self, line):
        words = line.split()
        for i in range(len(words) - 1):
            if len(words[i]) == 1 and words[i].isalpha() and words[i + 1].isalnum():
                words[i] = words[i] + "~" + words[i + 1]
                words.pop(i + 1)
        return " ".join(words) + "\n"

    def show_error(self, message):
        tk.messagebox.showerror("Error", message)

    def show_message(self, message):
        tk.messagebox.showinfo("Info", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
