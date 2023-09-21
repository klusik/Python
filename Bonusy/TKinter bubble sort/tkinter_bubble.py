import random
import tkinter as tk


def bubble_sort(array):
    """
    Sort an array using the bubble sort algorithm.

    Args:
    - array (list): the array to be sorted.
    """

    array_length = len(array)
    for index in range(array_length):
        for inner_index in range(array_length - index - 1):
            if array[inner_index] > array[inner_index + 1]:
                array[inner_index], array[inner_index + 1] = array[inner_index + 1], array[inner_index]


def visualize_bubble_sort(initial_array):
    """
    Visualize the bubble sort algorithm applied to an array.

    Args:
    - initial_array (list): the initial array to be sorted.
    """

    def draw_bars(array):
        """
        Draw the bars on the canvas to visualize the array.

        Args:
        - array (list): the array to be visualized.
        """

        canvas.delete("all")
        bar_width = canvas_width / len(array)
        maximum_value = max(array)
        for index, number in enumerate(array):
            x0 = index * bar_width
            y0 = canvas_height - number*(canvas_height*0.9)/maximum_value
            x1 = (index + 1) * bar_width
            y1 = canvas_height
            canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
            canvas.create_text((x0 + x1) / 2, y0 - 10, text=str(number), font=("Arial", 16))
        canvas.update()

    def bubble_sort_visualized(array):
        """
        Sort and visualize the array using the bubble sort algorithm.

        Args:
        - array (list): the array to be sorted and visualized.
        """

        array_length = len(array)
        for index in range(array_length):
            for inner_index in range(array_length - index - 1):
                if array[inner_index] > array[inner_index + 1]:
                    array[inner_index], array[inner_index + 1] = array[inner_index + 1], array[inner_index]
                    draw_bars(array)
                    root.update_idletasks()

    root = tk.Tk()
    root.title("Bubble Sort Visualization")
    canvas_width = 1600
    canvas_height = 900
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack()

    array = initial_array.copy()
    draw_bars(array)

    sort_button = tk.Button(root, text="Sort", command=lambda: bubble_sort_visualized(array))
    sort_button.pack()

    root.mainloop()


if __name__ == "__main__":
    array = [random.randint(1, 100) for _ in range(40)]
    visualize_bubble_sort(array)
