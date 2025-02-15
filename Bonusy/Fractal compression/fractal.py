import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import struct
import time
import concurrent.futures
import threading


class FractalCompressor:
    # Block parameters
    RANGE_SIZE = 8  # Range block: 8x8 pixels
    DOMAIN_SIZE = 16  # Domain block: 16x16 pixels (should be 2x RANGE_SIZE)
    DOMAIN_STEP = 4  # Step size for sliding the domain window

    @staticmethod
    def apply_transform(block, t):
        """
        Apply one of 8 isometries to a block.
        t = 0: identity
        t = 1: rotate 90°
        t = 2: rotate 180°
        t = 3: rotate 270°
        t = 4: horizontal flip
        t = 5: vertical flip
        t = 6: transpose (flip over main diagonal)
        t = 7: anti-diagonal flip (rotate 90° then vertical flip)
        """
        if t == 0:
            return block
        elif t == 1:
            return np.rot90(block, 1)
        elif t == 2:
            return np.rot90(block, 2)
        elif t == 3:
            return np.rot90(block, 3)
        elif t == 4:
            return np.fliplr(block)
        elif t == 5:
            return np.flipud(block)
        elif t == 6:
            return np.transpose(block)
        elif t == 7:
            return np.flipud(np.rot90(block, 1))
        else:
            return block

    @staticmethod
    def downsample(block):
        """
        Downsample a (2*RANGE_SIZE x 2*RANGE_SIZE) domain block to (RANGE_SIZE x RANGE_SIZE)
        by averaging each 2x2 non-overlapping group.
        """
        R = FractalCompressor.RANGE_SIZE
        return block.reshape(R, 2, R, 2).mean(axis=(1, 3))

    @staticmethod
    def encode(image, progress_callback=None):
        """
        Fractal encode the image.
        The image is first converted to grayscale. Then the image is divided
        into non-overlapping range blocks (8x8). For each range block the algorithm
        searches over overlapping 16x16 domain blocks (stepped by DOMAIN_STEP),
        downsampling each domain block to 8x8, and trying 8 isometric transformations.
        For each candidate it computes the optimal linear mapping (contrast s and offset o).
        The best transform is stored.

        The function accepts an optional progress_callback(completed, total)
        which is called after processing each range block.
        """
        # Convert to grayscale if needed
        if image.mode != 'L':
            image = image.convert('L')
        arr = np.array(image, dtype=np.float64)
        height, width = arr.shape
        R = FractalCompressor.RANGE_SIZE
        D = FractalCompressor.DOMAIN_SIZE
        step = FractalCompressor.DOMAIN_STEP

        # Prepare tasks for each range block (row-major order)
        tasks = []
        order = 0
        for ry in range(0, height - R + 1, R):
            for rx in range(0, width - R + 1, R):
                tasks.append((order, rx, ry))
                order += 1
        total_tasks = len(tasks)
        results = []

        # Worker function: process one range block and find the best matching transform.
        def worker(task):
            order, rx, ry = task
            range_block = arr[ry:ry + R, rx:rx + R]
            best_error = float('inf')
            best_params = None
            for dy in range(0, height - D + 1, step):
                for dx in range(0, width - D + 1, step):
                    domain_block = arr[dy:dy + D, dx:dx + D]
                    ds_block = FractalCompressor.downsample(domain_block)
                    for t in range(8):
                        transformed = FractalCompressor.apply_transform(ds_block, t)
                        D_flat = transformed.flatten()
                        R_flat = range_block.flatten()
                        meanD = np.mean(D_flat)
                        meanR = np.mean(R_flat)
                        varD = np.sum((D_flat - meanD) ** 2)
                        if varD < 1e-6:
                            s = 0.0
                        else:
                            s = np.sum((D_flat - meanD) * (R_flat - meanR)) / varD
                        o = meanR - s * meanD
                        error = np.sum((s * D_flat + o - R_flat) ** 2)
                        if error < best_error:
                            best_error = error
                            best_params = (dx, dy, t, s, o)
            return (order, best_params)

        start_time = time.time()
        # Use ThreadPoolExecutor to process range blocks in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(worker, task): task for task in tasks}
            completed = 0
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                results.append(res)
                completed += 1
                if progress_callback:
                    progress_callback(completed, total_tasks)
        # Sort results back into row-major order
        results.sort(key=lambda x: x[0])
        transforms = [r[1] for r in results]
        elapsed = time.time() - start_time
        print(f"Fractal encoding completed in {elapsed:.2f} seconds.")

        # Pack header and transform data into binary format.
        header = b'FRAC'
        header += struct.pack('>HHBBB', width, height, R, D, step)
        n_transforms = len(transforms)
        header += struct.pack('>I', n_transforms)
        body = bytearray()
        for params in transforms:
            dx, dy, t, s, o = params
            body.extend(struct.pack('>HHBff', dx, dy, t, s, o))
        return header + body

    @staticmethod
    def decode(data, iterations=20):
        """
        Fractal decode the compressed data.
        Starting from a constant gray image, the stored transforms are applied
        iteratively (default 20 iterations) to reconstruct the image.
        """
        if not data.startswith(b'FRAC'):
            raise ValueError("Not a valid fractal compressed file")
        offset = 4
        width, height, R, D, step = struct.unpack('>HHBBB', data[offset:offset + 7])
        offset += 7
        n_transforms = struct.unpack('>I', data[offset:offset + 4])[0]
        offset += 4
        num_range_x = width // R
        num_range_y = height // R
        if n_transforms != num_range_x * num_range_y:
            raise ValueError("Mismatch in number of transforms")
        transforms = []
        record_size = 2 + 2 + 1 + 4 + 4
        for i in range(n_transforms):
            record = data[offset:offset + record_size]
            dx, dy, t, s, o = struct.unpack('>HHBff', record)
            transforms.append((dx, dy, t, s, o))
            offset += record_size

        current = np.full((height, width), 128.0, dtype=np.float64)
        new_img = current.copy()
        for it in range(iterations):
            block_index = 0
            for ry in range(0, height - R + 1, R):
                for rx in range(0, width - R + 1, R):
                    dx, dy, t, s, o = transforms[block_index]
                    block_index += 1
                    domain_block = current[dy:dy + D, dx:dx + D]
                    ds_block = domain_block.reshape(R, 2, R, 2).mean(axis=(1, 3))
                    transformed = FractalCompressor.apply_transform(ds_block, t)
                    new_block = s * transformed + o
                    new_img[ry:ry + R, rx:rx + R] = new_block
            current = new_img.copy()
        current = np.clip(current, 0, 255).astype(np.uint8)
        return Image.fromarray(current)


class FractalConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fractal Converter")
        self.geometry("600x450")

        # Label to display the image
        self.image_label = tk.Label(self)
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # Button frame
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        btn_open_image = tk.Button(btn_frame, text="Open Image File", command=self.open_image)
        btn_open_image.grid(row=0, column=0, padx=5)

        btn_save_frac = tk.Button(btn_frame, text="Save as .frac", command=self.save_frac)
        btn_save_frac.grid(row=0, column=1, padx=5)

        btn_open_frac = tk.Button(btn_frame, text="Open .frac File", command=self.open_frac)
        btn_open_frac.grid(row=0, column=2, padx=5)

        btn_save_jpg = tk.Button(btn_frame, text="Save as JPG", command=self.save_jpg)
        btn_save_jpg.grid(row=0, column=3, padx=5)

        # Progress bar for encoding
        self.progressbar = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progressbar.pack(pady=5)
        self.progressbar['maximum'] = 100

        self.current_image = None  # Currently loaded PIL image
        self.current_frac_data = None  # Latest fractal data

    def open_image(self):
        """Open a common image file and display it."""
        filetypes = [("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        filename = filedialog.askopenfilename(title="Select an Image File", filetypes=filetypes)
        if filename:
            try:
                img = Image.open(filename)
                self.current_image = img
                self.display_image(img)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image:\n{e}")

    def save_frac(self):
        """Encode the current image with fractal compression and save as a .frac file.
           Shows a progress bar while encoding in a background thread.
        """
        if self.current_image is None:
            messagebox.showinfo("Info", "No image loaded to save.")
            return
        if not messagebox.askokcancel("Warning",
                                      "Fractal encoding is computationally intensive and may take a while. Proceed?"):
            return

        filename = filedialog.asksaveasfilename(
            title="Save as .frac",
            defaultextension=".frac",
            filetypes=[("Frac Files", "*.frac")]
        )
        if not filename:
            return

        # Reset progress bar
        self.progressbar['value'] = 0

        # Define a progress callback that safely updates the progress bar in the main thread.
        def progress_callback(completed, total):
            percent = (completed / total) * 100
            self.after(0, lambda: self.progressbar.config(value=percent))

        def encode_thread():
            try:
                frac_data = FractalCompressor.encode(self.current_image, progress_callback)
                with open(filename, "wb") as f:
                    f.write(frac_data)
                self.after(0, lambda: messagebox.showinfo("Success", "File saved as .frac successfully."))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", f"Failed to save .frac file:\n{e}"))
            finally:
                # Reset progress bar after completion
                self.after(0, lambda: self.progressbar.config(value=0))

        # Run the encoding in a separate thread so the UI remains responsive.
        threading.Thread(target=encode_thread, daemon=True).start()

    def open_frac(self):
        """Open a .frac file, decode it, and display the resulting image."""
        filename = filedialog.askopenfilename(
            title="Open .frac File",
            filetypes=[("Frac Files", "*.frac")]
        )
        if filename:
            try:
                with open(filename, "rb") as f:
                    data = f.read()
                self.current_frac_data = data
                # Decoding (20 iterations by default)
                img = FractalCompressor.decode(data, iterations=20)
                self.current_image = img
                self.display_image(img)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open .frac file:\n{e}")

    def save_jpg(self):
        """Save the currently displayed image as a JPG file."""
        if self.current_image is None:
            messagebox.showinfo("Info", "No image loaded to save.")
            return
        filename = filedialog.asksaveasfilename(
            title="Save as JPG",
            defaultextension=".jpg",
            filetypes=[("JPEG Files", "*.jpg;*.jpeg")]
        )
        if filename:
            try:
                rgb_image = self.current_image.convert("RGB")
                rgb_image.save(filename, "JPEG")
                messagebox.showinfo("Success", "File saved as JPG successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save JPG file:\n{e}")

    def display_image(self, img):
        """Display the PIL image in the GUI."""
        max_width, max_height = 600, 400
        img_for_display = img.copy()
        img_width, img_height = img_for_display.size
        if img_width > max_width or img_height > max_height:
            img_for_display.thumbnail((max_width, max_height))
        photo = ImageTk.PhotoImage(img_for_display)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference


if __name__ == "__main__":
    app = FractalConverterApp()
    app.mainloop()
