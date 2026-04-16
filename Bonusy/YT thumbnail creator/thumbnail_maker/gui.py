"""Tkinter user interface for building simple YouTube thumbnail text overlays.

The GUI class in this module plays the role of a composition root. It wires the
Tkinter widgets, owns the state variables that reflect the current editor
settings, and delegates image generation to the renderer service.

Design pattern note:
This module loosely follows a controller-style arrangement. The Tkinter window is
stateful, but all pixel manipulation is delegated to ``ThumbnailRenderer``.
That separation keeps rendering rules outside the widget code.
"""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk

from . import config
from .renderer import ThumbnailRenderer


class ThumbnailMakerApp:
    """Desktop app that previews and exports text overlays on top of an image."""

    def __init__(self) -> None:
        """Create the main window, state variables, and widgets.

        The constructor only prepares the window and binds the UI. It does not
        immediately render anything because the user has not selected a source
        image yet.
        """
        self.root = tk.Tk()
        self.root.title(config.APP_TITLE)
        self.root.geometry("1420x860")
        self.root.minsize(1200, 760)

        # The renderer is a dedicated service object. The GUI gathers settings
        # and forwards them to the renderer, which keeps rendering logic out of
        # the event handler layer.
        self.renderer = ThumbnailRenderer()

        # The selected background image path is stored as plain text because it
        # is easy to pass to dialogs, labels, and the renderer.
        self.background_image_path: str = ""

        # The most recent full-size rendered image. This is reused for export so
        # the application does not need to render a second time after preview in
        # the common success path.
        self.rendered_thumbnail_image: Image.Image | None = None

        # Tkinter requires the PhotoImage object to stay strongly referenced.
        # If it is not stored on the instance, the preview may disappear because
        # the image wrapper gets garbage collected.
        self.preview_photo_image: ImageTk.PhotoImage | None = None

        # Delayed preview refresh job id returned by Tkinter's after(). This is
        # the core of the preview throttling strategy.
        self.pending_preview_refresh_job_id: str | None = None

        # Tkinter variable objects keep the UI and the internal state connected.
        # When an entry or slider changes, the matching variable changes too.
        self.title_text_var = tk.StringVar(value="11 HOUR FLIGHT")
        self.subtitle_text_var = tk.StringVar(
            value=f"HONG KONG {config.DEFAULT_PLANE_ICON} PRAGUE"
        )
        self.title_horizontal_ratio_var = tk.DoubleVar(
            value=config.DEFAULT_TITLE_HORIZONTAL_RATIO
        )
        self.subtitle_horizontal_ratio_var = tk.DoubleVar(
            value=config.DEFAULT_SUBTITLE_HORIZONTAL_RATIO
        )
        self.title_vertical_ratio_var = tk.DoubleVar(
            value=config.DEFAULT_TITLE_VERTICAL_RATIO
        )
        self.subtitle_vertical_ratio_var = tk.DoubleVar(
            value=config.DEFAULT_SUBTITLE_VERTICAL_RATIO
        )
        self.title_font_size_var = tk.IntVar(value=config.DEFAULT_TITLE_SIZE)
        self.subtitle_font_size_var = tk.IntVar(value=config.DEFAULT_SUBTITLE_SIZE)
        self.output_base_name_var = tk.StringVar(value=config.DEFAULT_EXPORT_BASENAME)

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

        controls_panel = ttk.Frame(self.root, padding=12)
        controls_panel.grid(row=0, column=0, sticky="ns")

        preview_panel = ttk.Frame(self.root, padding=12)
        preview_panel.grid(row=0, column=1, sticky="nsew")
        preview_panel.columnconfigure(0, weight=1)
        preview_panel.rowconfigure(1, weight=1)

        self._build_controls_panel(controls_panel)
        self._build_preview_panel(preview_panel)

    def _build_controls_panel(self, parent_frame: ttk.Frame) -> None:
        """Build the editor controls shown on the left side."""
        background_section = ttk.LabelFrame(parent_frame, text="Background", padding=10)
        background_section.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        background_section.columnconfigure(0, weight=1)

        ttk.Button(
            background_section,
            text="Browse image...",
            command=self._browse_background_image,
        ).grid(row=0, column=0, sticky="ew")

        self.background_label = ttk.Label(
            background_section,
            text="No image selected",
            wraplength=300,
        )
        self.background_label.grid(row=1, column=0, sticky="w", pady=(8, 0))

        text_section = ttk.LabelFrame(parent_frame, text="Text", padding=10)
        text_section.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        text_section.columnconfigure(0, weight=1)

        ttk.Label(text_section, text="Top title").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(text_section, textvariable=self.title_text_var, width=34)
        self.title_entry.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(text_section, text="Bottom subtitle").grid(row=2, column=0, sticky="w")
        self.subtitle_entry = ttk.Entry(
            text_section,
            textvariable=self.subtitle_text_var,
            width=34,
        )
        self.subtitle_entry.grid(row=3, column=0, sticky="ew")

        sliders_section = ttk.LabelFrame(parent_frame, text="Position and size", padding=10)
        sliders_section.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        sliders_section.columnconfigure(0, weight=1)

        self._add_slider(
            parent_frame=sliders_section,
            row_index=0,
            label_text="Title horizontal position",
            variable=self.title_horizontal_ratio_var,
            minimum_value=0.10,
            maximum_value=0.90,
            resolution=0.01,
        )
        self._add_slider(
            parent_frame=sliders_section,
            row_index=2,
            label_text="Title vertical position",
            variable=self.title_vertical_ratio_var,
            minimum_value=0.00,
            maximum_value=0.50,
            resolution=0.01,
        )
        self._add_slider(
            parent_frame=sliders_section,
            row_index=4,
            label_text="Subtitle horizontal position",
            variable=self.subtitle_horizontal_ratio_var,
            minimum_value=0.10,
            maximum_value=0.90,
            resolution=0.01,
        )
        self._add_slider(
            parent_frame=sliders_section,
            row_index=6,
            label_text="Subtitle vertical position",
            variable=self.subtitle_vertical_ratio_var,
            minimum_value=0.35,
            maximum_value=0.95,
            resolution=0.01,
        )
        self._add_slider(
            parent_frame=sliders_section,
            row_index=8,
            label_text="Title size",
            variable=self.title_font_size_var,
            minimum_value=28,
            maximum_value=180,
            resolution=1,
        )
        self._add_slider(
            parent_frame=sliders_section,
            row_index=10,
            label_text="Subtitle size",
            variable=self.subtitle_font_size_var,
            minimum_value=22,
            maximum_value=160,
            resolution=1,
        )

        export_section = ttk.LabelFrame(parent_frame, text="Export", padding=10)
        export_section.grid(row=3, column=0, sticky="ew")
        export_section.columnconfigure(0, weight=1)

        ttk.Label(export_section, text="Output base name").grid(row=0, column=0, sticky="w")
        ttk.Entry(export_section, textvariable=self.output_base_name_var, width=34).grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 8),
        )

        button_row = ttk.Frame(export_section)
        button_row.grid(row=2, column=0, sticky="ew")
        button_row.columnconfigure(0, weight=1)
        button_row.columnconfigure(1, weight=1)

        ttk.Button(button_row, text="Preview", command=self._refresh_preview).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 4),
        )
        ttk.Button(button_row, text="Generate PNG + JPG", command=self._generate_files).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(4, 0),
        )

    def _build_preview_panel(self, parent_frame: ttk.Frame) -> None:
        """Build the preview canvas area on the right side."""
        ttk.Label(parent_frame, text="Preview", font=("TkDefaultFont", 12, "bold")).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 8),
        )

        self.preview_canvas = tk.Canvas(
            parent_frame,
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
        parent_frame: ttk.LabelFrame,
        row_index: int,
        label_text: str,
        variable: tk.DoubleVar | tk.IntVar,
        minimum_value: float,
        maximum_value: float,
        resolution: float,
    ) -> None:
        """Add a labeled slider and initialize it with the current variable value.

        The slider change callback does not render immediately. Instead it calls
        ``_schedule_preview_refresh`` so repeated slider motion produces one
        consolidated redraw.
        """
        ttk.Label(parent_frame, text=label_text).grid(row=row_index, column=0, sticky="w")

        slider_widget = ttk.Scale(
            parent_frame,
            variable=variable,
            from_=minimum_value,
            to=maximum_value,
            orient="horizontal",
            command=lambda current_slider_value: self._on_slider_value_changed(
                current_slider_value
            ),
        )
        slider_widget.grid(row=row_index + 1, column=0, sticky="ew", pady=(2, 6))

        # The explicit configure call makes the initial thumb position line up
        # with the current Tkinter variable value.
        slider_widget.configure(value=variable.get())

        # ttk.Scale does not enforce the concept of "resolution" the same way as
        # the classic Tk Scale widget. The argument is still accepted here so the
        # method signature documents the intended precision and remains extensible
        # if the UI later switches to a widget with explicit step support.
        _unused_resolution = resolution

    def _on_slider_value_changed(self, current_slider_value: str) -> None:
        """Handle slider movement.

        The slider value itself is already written into the linked Tk variable by
        Tkinter. This method exists to make the callback name descriptive and to
        keep the scheduling logic out of the lambda expression.
        """
        _unused_slider_value = current_slider_value
        self._schedule_preview_refresh()

    def _bind_live_preview_updates(self) -> None:
        """Refresh the preview whenever text inputs change.

        ``trace_add`` effectively creates a small observer-style relationship
        between Tk variables and the preview update scheduling logic.
        """
        self.title_text_var.trace_add(
            "write",
            lambda variable_name, variable_index, operation_mode: self._on_text_input_changed(
                variable_name,
                variable_index,
                operation_mode,
            ),
        )
        self.subtitle_text_var.trace_add(
            "write",
            lambda variable_name, variable_index, operation_mode: self._on_text_input_changed(
                variable_name,
                variable_index,
                operation_mode,
            ),
        )
        self.output_base_name_var.trace_add(
            "write",
            lambda variable_name, variable_index, operation_mode: self._on_output_name_changed(
                variable_name,
                variable_index,
                operation_mode,
            ),
        )

    def _on_text_input_changed(
        self,
        variable_name: str,
        variable_index: str,
        operation_mode: str,
    ) -> None:
        """Schedule a preview refresh after entry field text changes."""
        _unused_variable_name = variable_name
        _unused_variable_index = variable_index
        _unused_operation_mode = operation_mode
        self._schedule_preview_refresh()

    def _on_output_name_changed(
        self,
        variable_name: str,
        variable_index: str,
        operation_mode: str,
    ) -> None:
        """Handle output name updates.

        The output name does not affect preview pixels, so no redraw is needed.
        This callback is still kept as a named method because it documents that
        the variable is intentionally observed but intentionally ignored for
        preview rendering.
        """
        _unused_variable_name = variable_name
        _unused_variable_index = variable_index
        _unused_operation_mode = operation_mode

    def _schedule_preview_refresh(self) -> None:
        """Delay preview rendering so rapid UI changes do not trigger constant redraws."""
        if self.pending_preview_refresh_job_id is not None:
            self.root.after_cancel(self.pending_preview_refresh_job_id)

        self.pending_preview_refresh_job_id = self.root.after(
            config.PREVIEW_REFRESH_DELAY_MS,
            self._refresh_preview,
        )

    def _browse_background_image(self) -> None:
        """Open a file picker and load the selected background image."""
        selected_background_image_path = filedialog.askopenfilename(
            title="Choose background image",
            filetypes=config.SUPPORTED_IMAGE_TYPES,
        )
        if not selected_background_image_path:
            return

        self.background_image_path = selected_background_image_path
        self.background_label.configure(text=Path(selected_background_image_path).name)

        # Render immediately after a new image is chosen so the user gets fast feedback.
        self._refresh_preview()

    def _refresh_preview(self) -> None:
        """Render a fresh preview into the right-side canvas."""
        if self.pending_preview_refresh_job_id is not None:
            self.root.after_cancel(self.pending_preview_refresh_job_id)
            self.pending_preview_refresh_job_id = None

        if not self.background_image_path:
            return

        try:
            self.rendered_thumbnail_image = self.renderer.render(
                background_path=self.background_image_path,
                title_text=self.title_text_var.get(),
                subtitle_text=self.subtitle_text_var.get(),
                title_size=int(self.title_font_size_var.get()),
                subtitle_size=int(self.subtitle_font_size_var.get()),
                title_horizontal_ratio=float(self.title_horizontal_ratio_var.get()),
                subtitle_horizontal_ratio=float(self.subtitle_horizontal_ratio_var.get()),
                title_vertical_ratio=float(self.title_vertical_ratio_var.get()),
                subtitle_vertical_ratio=float(self.subtitle_vertical_ratio_var.get()),
            )
        except Exception as error:
            messagebox.showerror("Preview error", str(error))
            return

        preview_image = self.rendered_thumbnail_image.copy()
        preview_image.thumbnail(config.CANVAS_PREVIEW_MAX_SIZE, Image.LANCZOS)
        self.preview_photo_image = ImageTk.PhotoImage(preview_image)

        self.preview_canvas.delete("all")
        canvas_width = self.preview_canvas.winfo_width() or config.CANVAS_PREVIEW_MAX_SIZE[0]
        canvas_height = self.preview_canvas.winfo_height() or config.CANVAS_PREVIEW_MAX_SIZE[1]
        self.preview_canvas.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=self.preview_photo_image,
        )

    def _generate_files(self) -> None:
        """Export the current thumbnail as both PNG and JPG."""
        if not self.background_image_path:
            messagebox.showwarning("Missing image", "Choose a background image first.")
            return

        self._refresh_preview()
        if self.rendered_thumbnail_image is None:
            messagebox.showerror("Generation error", "Could not render the thumbnail preview.")
            return

        selected_export_directory = filedialog.askdirectory(title="Choose export folder")
        if not selected_export_directory:
            return

        output_base_name = self.output_base_name_var.get().strip() or config.DEFAULT_EXPORT_BASENAME
        output_base_path = str(Path(selected_export_directory) / output_base_name)

        try:
            png_path, jpg_path = self.renderer.save_both_formats(
                self.rendered_thumbnail_image,
                output_base_path,
            )
        except Exception as error:
            messagebox.showerror("Save error", str(error))
            return

        messagebox.showinfo(
            "Done",
            "Generated files:\n"
            f"PNG: {png_path}\n"
            f"JPG: {jpg_path}",
        )
