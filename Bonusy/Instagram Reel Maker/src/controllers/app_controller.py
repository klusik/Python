"""Controller wiring between Tkinter widgets and export services."""

from pathlib import Path
from typing import List
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox

from src.models.project_settings import AudioSettings, ExportSettings, FrameSettings
from src.services.export_service import ExportService
from src.services.ffmpeg_service import FFmpegService
from src.services.music_service import MusicService
from src.ui.main_window import MainWindow
from src.utils.threading_utils import BackgroundTaskRunner


class AppController:
    """Coordinate UI actions, application state, and export workflow."""

    def __init__(
        self,
        root_window: tk.Tk,
        main_window: MainWindow,
        export_service: ExportService,
        music_service: MusicService,
        ffmpeg_service: FFmpegService,
    ) -> None:
        """Store dependencies and bind all UI commands."""
        self.root_window = root_window
        self.main_window = main_window
        self.export_service = export_service
        self.music_service = music_service
        self.ffmpeg_service = ffmpeg_service
        self.background_task_runner = BackgroundTaskRunner()
        self.image_paths: List[Path] = []
        self.current_music_path: Path | None = None

        self._bind_commands()
        self._refresh_status_with_encoder()

    def _bind_commands(self) -> None:
        """Connect widgets to controller methods."""
        self.main_window.add_images_button.configure(command=self.add_images)
        self.main_window.remove_selected_button.configure(command=self.remove_selected_images)
        self.main_window.move_up_button.configure(command=self.move_selected_up)
        self.main_window.move_down_button.configure(command=self.move_selected_down)
        self.main_window.reverse_button.configure(command=self.reverse_image_order)
        self.main_window.pick_frame_color_button.configure(command=self.pick_frame_color)
        self.main_window.load_music_button.configure(command=self.load_music)
        self.main_window.preview_music_button.configure(command=self.preview_music_segment)
        self.main_window.stop_preview_button.configure(command=self.stop_music_preview)
        self.main_window.browse_output_button.configure(command=self.choose_output_path)
        self.main_window.export_button.configure(command=self.start_export)

    def _refresh_status_with_encoder(self) -> None:
        """Display the currently preferred encoder in the status line."""
        preferred_encoder = self.ffmpeg_service.get_preferred_video_encoder(prefer_gpu_encoding=True)
        self.set_status(f"Ready. Preferred encoder: {preferred_encoder}")

    def set_status(self, status_text: str) -> None:
        """Update the status label in a Tk-safe way."""
        self.root_window.after(0, lambda: self.main_window.status_label.configure(text=status_text))

    def reverse_image_order(self) -> None:
        """Reverse the order of loaded images."""
        self.image_paths.reverse()
        self.main_window.image_listbox.delete(0, tk.END)
        for image_path in self.image_paths:
            self.main_window.image_listbox.insert(tk.END, image_path.name)
        self.main_window.image_listbox.selection_clear(0, tk.END)
        self._refresh_photo_count()
        self.set_status("Image order reversed.")

    def add_images(self) -> None:
        """Open a file picker and append selected photos to the project list."""
        selected_file_paths = filedialog.askopenfilenames(
            title="Select photos",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.webp"), ("All files", "*.*")],
        )
        if not selected_file_paths:
            return

        for selected_file_path in selected_file_paths:
            image_path = Path(selected_file_path)
            self.image_paths.append(image_path)
            self.main_window.image_listbox.insert(tk.END, image_path.name)
        self._refresh_photo_count()
        self.set_status(f"Loaded {len(selected_file_paths)} photos.")

    def remove_selected_images(self) -> None:
        """Remove all currently selected images from the list."""
        selected_indices = list(self.main_window.image_listbox.curselection())
        if not selected_indices:
            return

        for selected_index in reversed(selected_indices):
            del self.image_paths[selected_index]
            self.main_window.image_listbox.delete(selected_index)
        self._refresh_photo_count()
        self.set_status("Selected photos removed.")

    def move_selected_up(self) -> None:
        """Move one selected photo upward in the ordering."""
        selected_indices = list(self.main_window.image_listbox.curselection())
        if len(selected_indices) != 1:
            return
        selected_index = selected_indices[0]
        if selected_index <= 0:
            return
        self._swap_image_positions(selected_index, selected_index - 1)

    def move_selected_down(self) -> None:
        """Move one selected photo downward in the ordering."""
        selected_indices = list(self.main_window.image_listbox.curselection())
        if len(selected_indices) != 1:
            return
        selected_index = selected_indices[0]
        if selected_index >= len(self.image_paths) - 1:
            return
        self._swap_image_positions(selected_index, selected_index + 1)

    def _swap_image_positions(self, first_index: int, second_index: int) -> None:
        """Swap two image positions and refresh the listbox text."""
        self.image_paths[first_index], self.image_paths[second_index] = (
            self.image_paths[second_index],
            self.image_paths[first_index],
        )
        first_name = self.image_paths[first_index].name
        second_name = self.image_paths[second_index].name
        self.main_window.image_listbox.delete(first_index)
        self.main_window.image_listbox.insert(first_index, first_name)
        self.main_window.image_listbox.delete(second_index)
        self.main_window.image_listbox.insert(second_index, second_name)
        self.main_window.image_listbox.selection_clear(0, tk.END)
        self.main_window.image_listbox.selection_set(second_index)
        self.set_status("Photo order updated.")

    def _refresh_photo_count(self) -> None:
        """Update the visible photo count label."""
        self.main_window.photo_count_label.configure(text=f"{len(self.image_paths)} photos loaded")

    def pick_frame_color(self) -> None:
        """Open a color picker and store the selected hex color."""
        selected_color = colorchooser.askcolor(title="Choose frame color")
        if not selected_color or not selected_color[1]:
            return
        self.main_window.frame_color_entry.delete(0, tk.END)
        self.main_window.frame_color_entry.insert(0, selected_color[1])

    def load_music(self) -> None:
        """Select a music file and update timeline sliders from its duration."""
        selected_file_path = filedialog.askopenfilename(
            title="Select music",
            filetypes=[("Audio", "*.mp3 *.wav *.m4a *.aac *.flac *.ogg"), ("All files", "*.*")],
        )
        if not selected_file_path:
            return

        self.current_music_path = Path(selected_file_path)
        duration_seconds = self.music_service.get_audio_duration_seconds(self.current_music_path)
        self.main_window.music_path_entry.delete(0, tk.END)
        self.main_window.music_path_entry.insert(0, str(self.current_music_path))
        self.main_window.clip_in_scale.configure(to=max(1.0, duration_seconds))
        self.main_window.clip_out_scale.configure(to=max(1.0, duration_seconds))
        self.main_window.clip_out_scale.set(duration_seconds)
        self.main_window.music_info_label.configure(
            text=f"Loaded music: {self.current_music_path.name} ({duration_seconds:.2f} s)"
        )
        self.set_status("Music loaded.")

    def preview_music_segment(self) -> None:
        """Preview the selected music segment."""
        if not self.current_music_path:
            messagebox.showwarning("No music", "Load a music file first.")
            return
        clip_in_seconds = float(self.main_window.clip_in_scale.get())
        clip_out_seconds = float(self.main_window.clip_out_scale.get())
        if clip_out_seconds <= clip_in_seconds:
            messagebox.showwarning("Invalid segment", "Clip OUT must be greater than Clip IN.")
            return
        try:
            self.music_service.play_preview_segment(self.current_music_path, clip_in_seconds, clip_out_seconds)
            self.set_status("Preview playing.")
        except Exception as exception:
            messagebox.showerror("Preview failed", str(exception))
            self.set_status(f"Preview failed: {exception}")

    def stop_music_preview(self) -> None:
        """Stop any currently playing music preview."""
        self.music_service.stop_preview()
        self.set_status("Preview stopped.")

    def choose_output_path(self) -> None:
        """Select the target MP4 output path."""
        selected_output_path = filedialog.asksaveasfilename(
            title="Choose output MP4",
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4")],
            initialfile="instagram_reel.mp4",
        )
        if not selected_output_path:
            return
        self.main_window.output_path_entry.delete(0, tk.END)
        self.main_window.output_path_entry.insert(0, selected_output_path)

    def collect_frame_settings(self) -> FrameSettings:
        """Read current frame settings from the UI."""
        return FrameSettings(
            enabled=bool(self.main_window.frame_enabled_variable.get()),
            color_hex=self.main_window.frame_color_entry.get().strip() or "#FFFFFF",
            thickness_pixels=int(self.main_window.frame_thickness_scale.get()),
            margin_pixels=int(self.main_window.frame_margin_scale.get()),
            corner_style=self.main_window.frame_shape_combobox.get().strip() or "rounded",
            corner_radius_pixels=int(self.main_window.corner_radius_scale.get()),
        )

    def collect_audio_settings(self) -> AudioSettings:
        """Read current music mode and segment settings from the UI."""
        selected_audio_mode = self.main_window.audio_mode_variable.get()
        clip_in_seconds = float(self.main_window.clip_in_scale.get())
        clip_out_seconds = float(self.main_window.clip_out_scale.get())
        if selected_audio_mode == "manual" and self.current_music_path and clip_out_seconds <= clip_in_seconds:
            computed_clip_out_seconds = clip_in_seconds + self._estimate_manual_video_duration_seconds()
        else:
            computed_clip_out_seconds = clip_out_seconds

        return AudioSettings(
            music_path=self.current_music_path,
            use_full_track=(selected_audio_mode == "full_track"),
            use_selected_segment=(selected_audio_mode == "segment"),
            manual_timing=(selected_audio_mode == "manual"),
            clip_in_seconds=clip_in_seconds,
            clip_out_seconds=computed_clip_out_seconds,
        )

    def collect_export_settings(self) -> ExportSettings:
        """Read export settings from the UI and validate simple numeric fields."""
        output_path_text = self.main_window.output_path_entry.get().strip()
        output_width_pixels = int(self.main_window.output_width_entry.get().strip())
        output_height_pixels = int(self.main_window.output_height_entry.get().strip())
        return ExportSettings(
            photos_per_screen=int(self.main_window.photos_per_screen_scale.get()),
            screen_duration_seconds=float(self.main_window.screen_duration_scale.get()),
            frames_per_second=int(self.main_window.frames_per_second_scale.get()),
            output_width_pixels=output_width_pixels,
            output_height_pixels=output_height_pixels,
            prefer_gpu_encoding=bool(self.main_window.prefer_gpu_variable.get()),
            output_path=Path(output_path_text) if output_path_text else None,
        )

    def _estimate_manual_video_duration_seconds(self) -> float:
        """Estimate total video duration for manual timing mode."""
        if not self.image_paths:
            return 0.0
        photos_per_screen = max(1, int(self.main_window.photos_per_screen_scale.get()))
        screen_count = (len(self.image_paths) + photos_per_screen - 1) // photos_per_screen
        return screen_count * float(self.main_window.screen_duration_scale.get())

    def start_export(self) -> None:
        """Validate inputs and start export work on a background thread."""
        if not self.image_paths:
            messagebox.showwarning("No photos", "Add at least one photo before exporting.")
            return

        try:
            frame_settings = self.collect_frame_settings()
            audio_settings = self.collect_audio_settings()
            export_settings = self.collect_export_settings()
        except Exception as exception:
            messagebox.showerror("Invalid settings", str(exception))
            return

        if export_settings.output_path is None:
            messagebox.showwarning("Missing output", "Choose an output MP4 file first.")
            return

        self.main_window.export_button.configure(state="disabled")
        self.set_status("Export started...")

        def export_worker() -> None:
            """Run export steps in the background and report the result."""
            try:
                final_output_path = self.export_service.export_reel(
                    image_paths=list(self.image_paths),
                    frame_settings=frame_settings,
                    audio_settings=audio_settings,
                    export_settings=export_settings,
                    status_callback=self.set_status,
                )
                self.root_window.after(
                    0,
                    lambda: messagebox.showinfo("Export complete", f"Video created:\n{final_output_path}"),
                )
            except Exception as exception:
                self.root_window.after(
                    0,
                    lambda: messagebox.showerror("Export failed", str(exception)),
                )
                self.set_status(f"Export failed: {exception}")
            finally:
                self.root_window.after(0, lambda: self.main_window.export_button.configure(state="normal"))

        self.background_task_runner.run(export_worker)
