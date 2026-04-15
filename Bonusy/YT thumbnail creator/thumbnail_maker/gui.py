"""Tkinter user interface for building simple YouTube thumbnail text overlays."""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk

from . import config
from .renderer import ThumbnailRenderer


class ThumbnailMakerApp:
    """Desktop app that previews and exports text overlays on top of an image."""

    def __init__(self) -> None:
        """Create the main window, state variables, and widgets."""
        self.root = tk.Tk()
        self.root.title(config.APP_TITLE)
        self.root.geometry("1420x860")
        self.root.minsize(1200, 760)

        self.renderer = ThumbnailRenderer()
        self.background_path: str = ""
        self.rendered_image: Image.Image | None = None
        self.preview_photo: ImageTk.PhotoImage | None = None

        # Delayed preview refresh job id returned by Tkinter's after().
        # This keeps preview generation from running on every tiny slider move.
        self.pending_preview_job: str | None = None

        self.title_text_var = tk.StringVar(value="11 HOUR FLIGHT")
        self.subtitle_text_var = tk.StringVar(value=f"HONG KONG {config.DEFAULT_PLANE_ICON} PRAGUE")
        self.title_x_var = tk.DoubleVar(value=config.DEFAULT_TITLE_X_RATIO)
        self.subtitle_x_var = tk.DoubleVar(value=config.DEFAULT_SUBTITLE_X_RATIO)
        self.title_y_var = tk.DoubleVar(value=config.DEFAULT_TITLE_Y_RATIO)
        self.subtitle_y_var = tk.DoubleVar(value=config.DEFAULT_SUBTITLE_Y_RATIO)
        self.title_size_var = tk.IntVar(value=config.DEFAULT_TITLE_SIZE)
        self.subtitle_size_var = tk.IntVar(value=config.DEFAULT_SUBTITLE_SIZE)
        self.output_name_var = tk.StringVar(value=config.DEFAULT_EXPORT_BASENAME)

        self._build_layout()
        self._bind_live_preview_updates()

    def run(self) -> None:
        """Start the Tkinter event loop."""
        self.root.mainloop()

    def _build_layout(self) -> None:
        """Construct the left control panel and right preview panel."""
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        controls_frame = ttk.Frame(self.root, padding=12)
        controls_frame.grid(row=0, column=0, sticky="ns")

        preview_frame = ttk.Frame(self.root, padding=12)
        preview_frame.grid(row=0, column=1, sticky="nsew")
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)

        self._build_controls_panel(controls_frame)
        self._build_preview_panel(preview_frame)

    def _build_controls_panel(self, parent: ttk.Frame) -> None:
        """Build the editor controls shown on the left side."""
        image_section = ttk.LabelFrame(parent, text="Background", padding=10)
        image_section.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        image_section.columnconfigure(0, weight=1)

        ttk.Button(image_section, text="Browse image...", command=self._browse_background_image).grid(
            row=0, column=0, sticky="ew"
        )

        self.background_label = ttk.Label(image_section, text="No image selected", wraplength=300)
        self.background_label.grid(row=1, column=0, sticky="w", pady=(8, 0))

        text_section = ttk.LabelFrame(parent, text="Text", padding=10)
        text_section.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        text_section.columnconfigure(0, weight=1)

        ttk.Label(text_section, text="Top title").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(text_section, textvariable=self.title_text_var, width=34)
        self.title_entry.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(text_section, text="Bottom subtitle").grid(row=2, column=0, sticky="w")
        self.subtitle_entry = ttk.Entry(text_section, textvariable=self.subtitle_text_var, width=34)
        self.subtitle_entry.grid(row=3, column=0, sticky="ew")

        sliders_section = ttk.LabelFrame(parent, text="Position and size", padding=10)
        sliders_section.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        sliders_section.columnconfigure(0, weight=1)

        self._add_slider(
            parent=sliders_section,
            row_index=0,
            label_text="Title horizontal position",
            variable=self.title_x_var,
            from_value=0.10,
            to_value=0.90,
            resolution=0.01,
        )
        self._add_slider(
            parent=sliders_section,
            row_index=2,
            label_text="Title vertical position",
            variable=self.title_y_var,
            from_value=0.00,
            to_value=0.50,
            resolution=0.01,
        )
        self._add_slider(
            parent=sliders_section,
            row_index=4,
            label_text="Subtitle horizontal position",
            variable=self.subtitle_x_var,
            from_value=0.10,
            to_value=0.90,
            resolution=0.01,
        )
        self._add_slider(
            parent=sliders_section,
            row_index=6,
            label_text="Subtitle vertical position",
            variable=self.subtitle_y_var,
            from_value=0.35,
            to_value=0.95,
            resolution=0.01,
        )
        self._add_slider(
            parent=sliders_section,
            row_index=8,
            label_text="Title size",
            variable=self.title_size_var,
            from_value=28,
            to_value=180,
            resolution=1,
        )
        self._add_slider(
            parent=sliders_section,
            row_index=10,
            label_text="Subtitle size",
            variable=self.subtitle_size_var,
            from_value=22,
            to_value=160,
            resolution=1,
        )

        export_section = ttk.LabelFrame(parent, text="Export", padding=10)
        export_section.grid(row=3, column=0, sticky="ew")
        export_section.columnconfigure(0, weight=1)

        ttk.Label(export_section, text="Output base name").grid(row=0, column=0, sticky="w")
        ttk.Entry(export_section, textvariable=self.output_name_var, width=34).grid(
            row=1, column=0, sticky="ew", pady=(0, 8)
        )

        button_row = ttk.Frame(export_section)
        button_row.grid(row=2, column=0, sticky="ew")
        button_row.columnconfigure(0, weight=1)
        button_row.columnconfigure(1, weight=1)

        ttk.Button(button_row, text="Preview", command=self._refresh_preview).grid(
            row=0, column=0, sticky="ew", padx=(0, 4)
        )
        ttk.Button(button_row, text="Generate PNG + JPG", command=self._generate_files).grid(
            row=0, column=1, sticky="ew", padx=(4, 0)
        )

    def _build_preview_panel(self, parent: ttk.Frame) -> None:
        """Build the preview canvas area on the right side."""
        ttk.Label(parent, text="Preview", font=("TkDefaultFont", 12, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )

        self.preview_canvas = tk.Canvas(
            parent,
            background="#1e1e1e",
            highlightthickness=1,
            highlightbackground="#4a4a4a",
        )
        self.preview_canvas.grid(row=1, column=0, sticky="nsew")

        self.preview_canvas.create_text(
            180,
            120,
            text="Select a background image to see the preview",
            fill="#d0d0d0",
            font=("TkDefaultFont", 12),
            tags="placeholder",
        )

    def _add_slider(
        self,
        parent: ttk.LabelFrame,
        row_index: int,
        label_text: str,
        variable: tk.DoubleVar | tk.IntVar,
        from_value: float,
        to_value: float,
        resolution: float,
    ) -> None:
        """Add a labeled slider and current value label."""
        ttk.Label(parent, text=label_text).grid(row=row_index, column=0, sticky="w")
        scale = ttk.Scale(
            parent,
            variable=variable,
            from_=from_value,
            to=to_value,
            orient="horizontal",
            command=lambda _value: self._schedule_preview_refresh(),
        )
        scale.grid(row=row_index + 1, column=0, sticky="ew", pady=(2, 6))

        if isinstance(variable, tk.IntVar):
            scale.configure(value=variable.get())
        else:
            scale.configure(value=variable.get())

    def _bind_live_preview_updates(self) -> None:
        """Refresh the preview whenever text inputs change."""
        self.title_text_var.trace_add("write", lambda *_args: self._schedule_preview_refresh())
        self.subtitle_text_var.trace_add("write", lambda *_args: self._schedule_preview_refresh())
        self.output_name_var.trace_add("write", lambda *_args: None)

    def _schedule_preview_refresh(self) -> None:
        """Delay preview rendering so rapid UI changes do not trigger constant redraws."""
        if self.pending_preview_job is not None:
            self.root.after_cancel(self.pending_preview_job)

        self.pending_preview_job = self.root.after(
            config.PREVIEW_REFRESH_DELAY_MS,
            self._refresh_preview,
        )

    def _browse_background_image(self) -> None:
        """Open a file picker and load the selected background image."""
        selected_path = filedialog.askopenfilename(
            title="Choose background image",
            filetypes=config.SUPPORTED_IMAGE_TYPES,
        )
        if not selected_path:
            return

        self.background_path = selected_path
        self.background_label.configure(text=Path(selected_path).name)

        # Render immediately after a new image is chosen so the user gets fast feedback.
        self._refresh_preview()

    def _refresh_preview(self) -> None:
        """Render a fresh preview into the right-side canvas."""
        if self.pending_preview_job is not None:
            self.root.after_cancel(self.pending_preview_job)
            self.pending_preview_job = None

        if not self.background_path:
            return

        try:
            self.rendered_image = self.renderer.render(
                background_path=self.background_path,
                title_text=self.title_text_var.get(),
                subtitle_text=self.subtitle_text_var.get(),
                title_size=int(self.title_size_var.get()),
                subtitle_size=int(self.subtitle_size_var.get()),
                title_x_ratio=float(self.title_x_var.get()),
                subtitle_x_ratio=float(self.subtitle_x_var.get()),
                title_y_ratio=float(self.title_y_var.get()),
                subtitle_y_ratio=float(self.subtitle_y_var.get()),
            )
        except Exception as error:
            messagebox.showerror("Preview error", str(error))
            return

        preview_image = self.rendered_image.copy()
        preview_image.thumbnail(config.CANVAS_PREVIEW_MAX_SIZE, Image.LANCZOS)
        self.preview_photo = ImageTk.PhotoImage(preview_image)

        self.preview_canvas.delete("all")
        canvas_width = self.preview_canvas.winfo_width() or config.CANVAS_PREVIEW_MAX_SIZE[0]
        canvas_height = self.preview_canvas.winfo_height() or config.CANVAS_PREVIEW_MAX_SIZE[1]
        self.preview_canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.preview_photo)

    def _generate_files(self) -> None:
        """Export the current thumbnail as both PNG and JPG."""
        if not self.background_path:
            messagebox.showwarning("Missing image", "Choose a background image first.")
            return

        self._refresh_preview()
        if self.rendered_image is None:
            messagebox.showerror("Generation error", "Could not render the thumbnail preview.")
            return

        selected_directory = filedialog.askdirectory(title="Choose export folder")
        if not selected_directory:
            return

        output_name = self.output_name_var.get().strip() or config.DEFAULT_EXPORT_BASENAME
        output_base_path = str(Path(selected_directory) / output_name)

        try:
            png_path, jpg_path = self.renderer.save_both_formats(self.rendered_image, output_base_path)
        except Exception as error:
            messagebox.showerror("Save error", str(error))
            return

        messagebox.showinfo(
            "Done",
            "Generated files:\n"
            f"PNG: {png_path}\n"
            f"JPG: {jpg_path}",
        )
