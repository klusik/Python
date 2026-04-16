"""Tkinter main window and widget layout for the reel builder."""

import tkinter as tk
from tkinter import ttk


class MainWindow:
    """Create and expose the main widgets used by the controller."""

    def __init__(self, root_window: tk.Tk) -> None:
        """Build the complete main window layout."""
        self.root_window = root_window
        self._build_styles()
        self._build_layout()

    def _build_styles(self) -> None:
        """Configure a few ttk styles for a cleaner desktop appearance."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Muted.TLabel", foreground="#4B5563")

    def _build_layout(self) -> None:
        """Create the full widget tree."""
        self.root_window.columnconfigure(0, weight=1)
        self.root_window.rowconfigure(0, weight=1)

        self.main_frame = ttk.Frame(self.root_window, padding=14)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=2)
        self.main_frame.columnconfigure(1, weight=3)
        self.main_frame.rowconfigure(1, weight=1)

        self.header_label = ttk.Label(self.main_frame, text="Instagram Reel Builder", style="Title.TLabel")
        self.header_label.grid(row=0, column=0, sticky="w")

        self.subtitle_label = ttk.Label(
            self.main_frame,
            text="Stack multiple wide photos into vertical Reel screens and export to MP4.",
            style="Muted.TLabel",
        )
        self.subtitle_label.grid(row=0, column=1, sticky="e")

        self.left_panel = ttk.Frame(self.main_frame, padding=(0, 12, 10, 0))
        self.left_panel.grid(row=1, column=0, sticky="nsew")
        self.left_panel.columnconfigure(0, weight=1)
        self.left_panel.rowconfigure(1, weight=1)

        self.right_panel = ttk.Frame(self.main_frame, padding=(10, 12, 0, 0))
        self.right_panel.grid(row=1, column=1, sticky="nsew")
        self.right_panel.columnconfigure(0, weight=1)

        self._build_file_panel()
        self._build_settings_panel()
        self._build_status_panel()

    def _build_file_panel(self) -> None:
        """Create the image list controls."""
        image_section = ttk.LabelFrame(self.left_panel, text="Photos", padding=10)
        image_section.grid(row=0, column=0, sticky="nsew")
        image_section.columnconfigure(0, weight=1)
        image_section.rowconfigure(1, weight=1)

        button_row_top = ttk.Frame(image_section)
        button_row_top.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        self.add_images_button = ttk.Button(button_row_top, text="Add photos")
        self.add_images_button.grid(row=0, column=0, padx=(0, 6))
        self.remove_selected_button = ttk.Button(button_row_top, text="Remove selected")
        self.remove_selected_button.grid(row=0, column=1, padx=(0, 6))

        button_row_bottom = ttk.Frame(image_section)
        button_row_bottom.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        self.move_up_button = ttk.Button(button_row_bottom, text="Move up")
        self.move_up_button.grid(row=0, column=0, padx=(0, 6))
        self.move_down_button = ttk.Button(button_row_bottom, text="Move down")
        self.move_down_button.grid(row=0, column=1, padx=(0, 6))
        self.reverse_button = ttk.Button(button_row_bottom, text="Reverse order")
        self.reverse_button.grid(row=0, column=2)

        list_frame = ttk.Frame(image_section)
        list_frame.grid(row=2, column=0, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.image_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED, height=18)
        self.image_listbox.grid(row=0, column=0, sticky="nsew")
        self.image_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.image_listbox.yview)
        self.image_scrollbar.grid(row=0, column=1, sticky="ns")
        self.image_listbox.configure(yscrollcommand=self.image_scrollbar.set)

        self.photo_count_label = ttk.Label(image_section, text="0 photos loaded", style="Muted.TLabel")
        self.photo_count_label.grid(row=3, column=0, sticky="w", pady=(8, 0))

    def _build_settings_panel(self) -> None:
        """Create all export and audio controls."""
        self.settings_notebook = ttk.Notebook(self.right_panel)
        self.settings_notebook.grid(row=0, column=0, sticky="nsew")

        self.layout_tab = ttk.Frame(self.settings_notebook, padding=12)
        self.audio_tab = ttk.Frame(self.settings_notebook, padding=12)
        self.export_tab = ttk.Frame(self.settings_notebook, padding=12)
        self.settings_notebook.add(self.layout_tab, text="Layout")
        self.settings_notebook.add(self.audio_tab, text="Music")
        self.settings_notebook.add(self.export_tab, text="Export")

        for tab_frame in [self.layout_tab, self.audio_tab, self.export_tab]:
            tab_frame.columnconfigure(1, weight=1)

        self._build_layout_tab()
        self._build_audio_tab()
        self._build_export_tab()

    def _build_layout_tab(self) -> None:
        """Build the layout settings tab."""
        ttk.Label(self.layout_tab, text="Photos per screen").grid(row=0, column=0, sticky="w")
        self.photos_per_screen_scale = tk.Scale(
            self.layout_tab,
            from_=1,
            to=6,
            orient="horizontal",
            resolution=1,
        )
        self.photos_per_screen_scale.set(3)
        self.photos_per_screen_scale.grid(row=0, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(self.layout_tab, text="Screen duration (manual mode)").grid(row=1, column=0, sticky="w")
        self.screen_duration_scale = tk.Scale(
            self.layout_tab,
            from_=0.2,
            to=10.0,
            orient="horizontal",
            resolution=0.1,
        )
        self.screen_duration_scale.set(1.0)
        self.screen_duration_scale.grid(row=1, column=1, sticky="ew", pady=(0, 8))

        self.frame_enabled_variable = tk.BooleanVar(value=True)
        self.frame_enabled_checkbutton = ttk.Checkbutton(
            self.layout_tab,
            text="Enable photo frame",
            variable=self.frame_enabled_variable,
        )
        self.frame_enabled_checkbutton.grid(row=2, column=0, sticky="w")

        ttk.Label(self.layout_tab, text="Frame thickness").grid(row=3, column=0, sticky="w")
        self.frame_thickness_scale = tk.Scale(
            self.layout_tab,
            from_=0,
            to=40,
            orient="horizontal",
            resolution=1,
        )
        self.frame_thickness_scale.set(12)
        self.frame_thickness_scale.grid(row=3, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(self.layout_tab, text="Frame margin").grid(row=4, column=0, sticky="w")
        self.frame_margin_scale = tk.Scale(
            self.layout_tab,
            from_=0,
            to=40,
            orient="horizontal",
            resolution=1,
        )
        self.frame_margin_scale.set(5)
        self.frame_margin_scale.grid(row=4, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(self.layout_tab, text="Frame color").grid(row=5, column=0, sticky="w")
        frame_color_row = ttk.Frame(self.layout_tab)
        frame_color_row.grid(row=5, column=1, sticky="ew", pady=(0, 8))
        frame_color_row.columnconfigure(0, weight=1)
        self.frame_color_entry = ttk.Entry(frame_color_row)
        self.frame_color_entry.insert(0, "#FFFFFF")
        self.frame_color_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.pick_frame_color_button = ttk.Button(frame_color_row, text="Pick")
        self.pick_frame_color_button.grid(row=0, column=1)

        ttk.Label(self.layout_tab, text="Frame shape").grid(row=6, column=0, sticky="w")
        self.frame_shape_combobox = ttk.Combobox(self.layout_tab, state="readonly", values=["rounded", "rectangular"])
        self.frame_shape_combobox.set("rounded")
        self.frame_shape_combobox.grid(row=6, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(self.layout_tab, text="Corner radius").grid(row=7, column=0, sticky="w")
        self.corner_radius_scale = tk.Scale(
            self.layout_tab,
            from_=0,
            to=80,
            orient="horizontal",
            resolution=1,
        )
        self.corner_radius_scale.set(28)
        self.corner_radius_scale.grid(row=7, column=1, sticky="ew")

    def _build_audio_tab(self) -> None:
        """Build the music settings tab."""
        music_row = ttk.Frame(self.audio_tab)
        music_row.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        music_row.columnconfigure(0, weight=1)
        self.music_path_entry = ttk.Entry(music_row)
        self.music_path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.load_music_button = ttk.Button(music_row, text="Load music")
        self.load_music_button.grid(row=0, column=1)

        self.audio_mode_variable = tk.StringVar(value="manual")
        self.use_full_track_radiobutton = ttk.Radiobutton(
            self.audio_tab,
            text="Use whole song and stretch timing to fill it",
            value="full_track",
            variable=self.audio_mode_variable,
        )
        self.use_full_track_radiobutton.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.use_selected_segment_radiobutton = ttk.Radiobutton(
            self.audio_tab,
            text="Use selected song segment",
            value="segment",
            variable=self.audio_mode_variable,
        )
        self.use_selected_segment_radiobutton.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.use_manual_timing_radiobutton = ttk.Radiobutton(
            self.audio_tab,
            text="Manual timing, optional music starts at selected IN point",
            value="manual",
            variable=self.audio_mode_variable,
        )
        self.use_manual_timing_radiobutton.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 10))

        ttk.Label(self.audio_tab, text="Clip IN (seconds)").grid(row=4, column=0, sticky="w")
        self.clip_in_scale = tk.Scale(self.audio_tab, from_=0, to=300, orient="horizontal", resolution=0.1)
        self.clip_in_scale.grid(row=4, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(self.audio_tab, text="Clip OUT (seconds)").grid(row=5, column=0, sticky="w")
        self.clip_out_scale = tk.Scale(self.audio_tab, from_=0, to=300, orient="horizontal", resolution=0.1)
        self.clip_out_scale.grid(row=5, column=1, sticky="ew", pady=(0, 10))

        preview_row = ttk.Frame(self.audio_tab)
        preview_row.grid(row=6, column=0, columnspan=2, sticky="w")
        self.preview_music_button = ttk.Button(preview_row, text="Preview segment")
        self.preview_music_button.grid(row=0, column=0, padx=(0, 6))
        self.stop_preview_button = ttk.Button(preview_row, text="Stop")
        self.stop_preview_button.grid(row=0, column=1)

        self.music_info_label = ttk.Label(self.audio_tab, text="No music loaded", style="Muted.TLabel")
        self.music_info_label.grid(row=7, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def _build_export_tab(self) -> None:
        """Build the export settings tab."""
        ttk.Label(self.export_tab, text="Output width").grid(row=0, column=0, sticky="w")
        self.output_width_entry = ttk.Entry(self.export_tab)
        self.output_width_entry.insert(0, "1080")
        self.output_width_entry.grid(row=0, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(self.export_tab, text="Output height").grid(row=1, column=0, sticky="w")
        self.output_height_entry = ttk.Entry(self.export_tab)
        self.output_height_entry.insert(0, "1920")
        self.output_height_entry.grid(row=1, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(self.export_tab, text="Frames per second").grid(row=2, column=0, sticky="w")
        self.frames_per_second_scale = tk.Scale(
            self.export_tab,
            from_=24,
            to=60,
            orient="horizontal",
            resolution=1,
        )
        self.frames_per_second_scale.set(30)
        self.frames_per_second_scale.grid(row=2, column=1, sticky="ew", pady=(0, 8))

        self.prefer_gpu_variable = tk.BooleanVar(value=True)
        self.prefer_gpu_checkbutton = ttk.Checkbutton(
            self.export_tab,
            text="Prefer NVIDIA GPU encoding when FFmpeg supports it",
            variable=self.prefer_gpu_variable,
        )
        self.prefer_gpu_checkbutton.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 12))

        output_row = ttk.Frame(self.export_tab)
        output_row.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        output_row.columnconfigure(0, weight=1)
        self.output_path_entry = ttk.Entry(output_row)
        self.output_path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.browse_output_button = ttk.Button(output_row, text="Browse output")
        self.browse_output_button.grid(row=0, column=1)

        self.export_button = ttk.Button(self.export_tab, text="Export MP4")
        self.export_button.grid(row=5, column=0, columnspan=2, sticky="ew")

    def _build_status_panel(self) -> None:
        """Create the bottom status widgets."""
        status_frame = ttk.LabelFrame(self.right_panel, text="Status", padding=10)
        status_frame.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        status_frame.columnconfigure(0, weight=1)

        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.grid(row=0, column=0, sticky="w")
