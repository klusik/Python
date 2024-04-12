import tkinter as tk
import pyautogui
import threading
import time
import random


class MouseMoverApp:
    def __init__(self, root):
        """
        Initializes the Mouse Mover application with a GUI for setting the inactivity interval and movement pixels.
        Sets up a background thread to monitor mouse activity and move the mouse cursor after a period of inactivity.

        :param root: The Tkinter root window where the app will be attached.
        """
        self.update_button = None
        self.pixels_entry = None
        self.interval_entry = None
        self.root = root
        self.root.title("Mouse Mover Simulator")

        # Default settings for inactivity interval (in seconds) and mouse movement (in pixels).
        self.inactivity_interval = 30
        self.move_pixels = 10

        # Initialize the GUI components.
        self.setup_gui()

        # Start a background thread to monitor mouse inactivity and trigger movement.
        self.monitor_thread = threading.Thread(target=self.monitor_mouse_activity, daemon=True)
        self.monitor_thread.start()

    def setup_gui(self):
        """
        Sets up the graphical user interface for the application.
        It includes text entry fields for setting the inactivity interval and the number of pixels to move.
        An 'Update Settings' button allows applying the entered configurations.
        """
        tk.Label(self.root, text="Inactivity Interval (Seconds):").pack()
        self.interval_entry = tk.Entry(self.root)
        self.interval_entry.pack()
        self.interval_entry.insert(0, str(self.inactivity_interval))

        tk.Label(self.root, text="Pixels to Move:").pack()
        self.pixels_entry = tk.Entry(self.root)
        self.pixels_entry.pack()
        self.pixels_entry.insert(0, str(self.move_pixels))

        self.update_button = tk.Button(self.root, text="Update Settings", command=self.update_settings)
        self.update_button.pack()

    def update_settings(self):
        """
        Updates the application settings based on user input.
        Reads the inactivity interval and movement pixels from the text entry fields
        and updates the corresponding attributes.
        """
        self.inactivity_interval = int(self.interval_entry.get())
        self.move_pixels = int(self.pixels_entry.get())

    def monitor_mouse_activity(self):
        """
        Monitors mouse activity in a loop. If the mouse position does not change for the configured interval,
        triggers a mouse movement. This function runs in a background thread.
        """
        last_position = pyautogui.position()
        while True:
            current_position = pyautogui.position()
            if current_position == last_position:
                time.sleep(self.inactivity_interval)
                current_position = pyautogui.position()
                if current_position == last_position:
                    self.move_mouse()
            else:
                last_position = current_position
                time.sleep(1)

    def move_mouse(self):
        """
        Moves the mouse cursor by a random number of pixels in a random direction.
        The number of pixels moved is determined by the 'move_pixels' setting.
        """
        current_position = pyautogui.position()
        move_x = random.choice([-1, 1]) * self.move_pixels
        move_y = random.choice([-1, 1]) * self.move_pixels
        pyautogui.moveTo(current_position.x + move_x, current_position.y + move_y)


if __name__ == "__main__":
    root = tk.Tk()
    app = MouseMoverApp(root)
    root.mainloop()
