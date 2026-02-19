"""
Interactive picture comparer and sorter (Tkinter).

Features
- Load a folder containing images (jpg, jpeg, png, bmp, gif, webp, tif, tiff).
- Shows two pictures side by side in square fields.
- Click the better picture (left or right) to sort images with minimal comparisons.
- After sorting, creates an output folder named "_compare" inside the selected folder
  (or "_compare_2", "_compare_3", ... if it already exists).
- Copies images into the output folder and renames them as 0001.ext, 0002.ext, ...
  where 0001 is the top ranked image.

Notes
- Requires Pillow for JPEG support: pip install pillow
- No console output. All feedback via UI dialogs.
"""

from __future__ import annotations

import os
import shutil
import tkinter as tk
from dataclasses import dataclass, field
from tkinter import filedialog, messagebox
from typing import Callable, Dict, List, Optional, Tuple

try:
    from PIL import Image, ImageTk
except Exception:  # pragma: no cover
    Image = None
    ImageTk = None


@dataclass(frozen=True)
class Picture:
    """Represents a single picture on disk.

    Attributes:
        path: Absolute file path to the image.
        filename: Base filename of the image (including extension).
    """

    path: str
    filename: str = field(init=False)

    def __post_init__(self) -> None:
        """Derive filename from the path."""
        object.__setattr__(self, "filename", os.path.basename(self.path))


@dataclass
class Score:
    """Tracks basic comparison statistics for a picture.

    This is not used as the primary sorting mechanism (we build a total order),
    but it provides a "score-like" metric that aligns with the user's clicks.

    Attributes:
        wins: How many times the picture was chosen as better.
        losses: How many times the picture was not chosen.
        comparisons: Total times the picture was involved in a comparison.
    """

    wins: int = 0
    losses: int = 0
    comparisons: int = 0

    def register_win(self) -> None:
        """Record that the picture won a comparison."""
        self.wins += 1
        self.comparisons += 1

    def register_loss(self) -> None:
        """Record that the picture lost a comparison."""
        self.losses += 1
        self.comparisons += 1


class Tools:
    """Utility helpers used across the application."""

    IMAGE_EXTENSIONS: Tuple[str, ...] = (
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".gif",
        ".webp",
        ".tif",
        ".tiff",
    )

    @staticmethod
    def require_pillow() -> bool:
        """Verify Pillow availability and show a GUI error if missing.

        Returns:
            True if Pillow is available, otherwise False.
        """
        if Image is None or ImageTk is None:
            messagebox.showerror(
                "Missing dependency",
                "This app requires Pillow for image loading.\n\nInstall it with:\n  pip install pillow",
            )
            return False
        return True

    @staticmethod
    def list_pictures_in_folder(folder_path: str) -> List[Picture]:
        """List image files in a folder and return them as Picture objects.

        Args:
            folder_path: Folder containing images.

        Returns:
            A list of Picture objects sorted by filename (case-insensitive).
        """
        entries: List[str] = []
        for name in os.listdir(folder_path):
            full_path = os.path.join(folder_path, name)
            if not os.path.isfile(full_path):
                continue
            if Tools.is_supported_image_file(name):
                entries.append(full_path)

        entries.sort(key=lambda p: os.path.basename(p).lower())
        return [Picture(path=os.path.abspath(path)) for path in entries]

    @staticmethod
    def is_supported_image_file(filename: str) -> bool:
        """Check whether a filename matches supported image extensions.

        Args:
            filename: Filename to test.

        Returns:
            True if supported, otherwise False.
        """
        lower_name = filename.lower()
        return any(lower_name.endswith(ext) for ext in Tools.IMAGE_EXTENSIONS)

    @staticmethod
    def ensure_unique_output_folder(base_folder: str, desired_name: str = "_compare") -> str:
        """Create a unique output folder inside base_folder.

        If base_folder/_compare already exists, creates _compare_2, _compare_3, etc.

        Args:
            base_folder: The parent folder.
            desired_name: The preferred output folder name.

        Returns:
            Absolute path of the created folder.
        """
        candidate = os.path.join(base_folder, desired_name)
        if not os.path.exists(candidate):
            os.makedirs(candidate, exist_ok=True)
            return os.path.abspath(candidate)

        suffix = 2
        while True:
            candidate = os.path.join(base_folder, f"{desired_name}_{suffix}")
            if not os.path.exists(candidate):
                os.makedirs(candidate, exist_ok=True)
                return os.path.abspath(candidate)
            suffix += 1

    @staticmethod
    def compute_name_width(count: int) -> int:
        """Compute filename numeric width for leading zeros.

        Uses at least 4 digits (0001), and more if needed.

        Args:
            count: Total number of pictures.

        Returns:
            Width for numeric part.
        """
        if count <= 0:
            return 4
        return max(4, len(str(count)))

    @staticmethod
    def copy_and_rename_ordered_pictures(
        ordered_pictures: List[Picture], output_folder: str
    ) -> None:
        """Copy pictures into output_folder and rename them as 0001.ext, 0002.ext, ...

        Args:
            ordered_pictures: Pictures in final sorted order (best first).
            output_folder: Destination folder (must exist).
        """
        width = Tools.compute_name_width(len(ordered_pictures))
        for index, picture in enumerate(ordered_pictures, start=1):
            _, ext = os.path.splitext(picture.filename)
            new_name = f"{index:0{width}d}{ext.lower()}"
            destination_path = os.path.join(output_folder, new_name)
            shutil.copy2(picture.path, destination_path)

    @staticmethod
    def fit_image_to_square(image: "Image.Image", side_pixels: int) -> "Image.Image":
        """Resize an image to fit inside a square, preserving aspect ratio.

        Args:
            image: Pillow Image instance.
            side_pixels: Side of the square target area.

        Returns:
            A resized Pillow Image that fits within side_pixels x side_pixels.
        """
        if side_pixels <= 1:
            side_pixels = 1
        working = image.copy()
        working.thumbnail((side_pixels, side_pixels), Image.Resampling.LANCZOS)
        return working


class InteractiveSorter:
    """Performs an interactive merge sort driven by user comparisons.

    This sorter builds a total ordering with approximately O(n log n) comparisons.

    Design
    - We create merge tasks for sublists.
    - At each step, we need the user to choose which of two "front" items is better.
    - The chosen item is appended to the merged result.
    - Once a merge completes, it becomes an input to the next merge up the tree.

    This yields a deterministic sorting flow that does not require comparing every pair.
    """

    def __init__(self, pictures: List[Picture], score_map: Dict[str, Score]) -> None:
        """Initialize the interactive sorter.

        Args:
            pictures: The pictures to sort.
            score_map: Mapping picture.path -> Score for statistics.
        """
        self._pictures = pictures[:]
        self._score_map = score_map

        self._runs: List[List[Picture]] = [[p] for p in self._pictures]
        self._current_left: Optional[List[Picture]] = None
        self._current_right: Optional[List[Picture]] = None
        self._left_index: int = 0
        self._right_index: int = 0
        self._merged: List[Picture] = []

        self._completed: bool = False
        self._total_upper_bound: int = self._estimate_upper_bound_comparisons(self._runs)
        self._comparisons_done: int = 0

        self._advance_to_next_merge_if_needed()

    def is_completed(self) -> bool:
        """Return whether sorting is finished."""
        return self._completed

    def get_current_pair(self) -> Optional[Tuple[Picture, Picture]]:
        """Get the current comparison pair.

        Returns:
            (left_picture, right_picture) if a comparison is needed, otherwise None.
        """
        if self._completed or self._current_left is None or self._current_right is None:
            return None

        if self._left_index >= len(self._current_left) or self._right_index >= len(self._current_right):
            return None

        return (self._current_left[self._left_index], self._current_right[self._right_index])

    def choose_left(self) -> None:
        """Register that the left picture is preferred for the current comparison."""
        pair = self.get_current_pair()
        if pair is None:
            return
        left_picture, right_picture = pair
        self._register_result(winner=left_picture, loser=right_picture)
        self._merged.append(left_picture)
        self._left_index += 1
        self._comparisons_done += 1
        self._finalize_merge_if_finished()

    def choose_right(self) -> None:
        """Register that the right picture is preferred for the current comparison."""
        pair = self.get_current_pair()
        if pair is None:
            return
        left_picture, right_picture = pair
        self._register_result(winner=right_picture, loser=left_picture)
        self._merged.append(right_picture)
        self._right_index += 1
        self._comparisons_done += 1
        self._finalize_merge_if_finished()

    def get_progress_text(self) -> str:
        """Return a user-facing progress string.

        We show comparisons_done and an upper bound estimate that is known upfront.

        Returns:
            Progress string suitable for a small status label.
        """
        remaining_upper = max(0, self._total_upper_bound - self._comparisons_done)
        return f"Comparisons: {self._comparisons_done} / <= {self._total_upper_bound}   Remaining: <= {remaining_upper}"

    def get_sorted_result_if_done(self) -> Optional[List[Picture]]:
        """Return the final sorted list if completed.

        Returns:
            Sorted list (best first) if done, else None.
        """
        if not self._completed:
            return None
        if not self._runs:
            return []
        return self._runs[0][:]

    def _register_result(self, winner: Picture, loser: Picture) -> None:
        """Update Score statistics for a winner/loser outcome.

        Args:
            winner: Chosen as better.
            loser: Not chosen.
        """
        self._score_map[winner.path].register_win()
        self._score_map[loser.path].register_loss()

    def _finalize_merge_if_finished(self) -> None:
        """If the current merge is finished, push merged run back into the run list."""
        if self._current_left is None or self._current_right is None:
            return

        left_done = self._left_index >= len(self._current_left)
        right_done = self._right_index >= len(self._current_right)

        if left_done and right_done:
            self._runs.append(self._merged)
            self._clear_current_merge()
            self._advance_to_next_merge_if_needed()
            return

        if left_done:
            self._merged.extend(self._current_right[self._right_index :])
            self._runs.append(self._merged)
            self._clear_current_merge()
            self._advance_to_next_merge_if_needed()
            return

        if right_done:
            self._merged.extend(self._current_left[self._left_index :])
            self._runs.append(self._merged)
            self._clear_current_merge()
            self._advance_to_next_merge_if_needed()
            return

    def _clear_current_merge(self) -> None:
        """Reset current merge state."""
        self._current_left = None
        self._current_right = None
        self._left_index = 0
        self._right_index = 0
        self._merged = []

    def _advance_to_next_merge_if_needed(self) -> None:
        """Start the next merge task, or mark completion if only one run remains."""
        if len(self._pictures) <= 1:
            self._runs = [self._pictures[:]]
            self._completed = True
            return

        while True:
            if self._current_left is not None and self._current_right is not None:
                return

            if len(self._runs) == 1:
                self._completed = True
                return

            if len(self._runs) >= 2:
                left_run = self._runs.pop(0)
                right_run = self._runs.pop(0)
                self._current_left = left_run
                self._current_right = right_run
                self._left_index = 0
                self._right_index = 0
                self._merged = []
                return

            self._completed = True
            return

    @staticmethod
    def _estimate_upper_bound_comparisons(initial_runs: List[List[Picture]]) -> int:
        """Estimate an upper bound on comparisons for merge sorting these runs.

        For each merge of size a and b, worst-case comparisons is (a + b - 1).
        This depends only on sizes, not on user decisions.

        Args:
            initial_runs: List of singleton runs (or any run partition).

        Returns:
            Upper bound comparison count.
        """
        sizes = [len(run) for run in initial_runs]
        upper_bound = 0
        queue = sizes[:]
        while len(queue) > 1:
            left = queue.pop(0)
            right = queue.pop(0)
            upper_bound += (left + right - 1)
            queue.append(left + right)
        return upper_bound


class App(tk.Tk):
    """Main Tkinter application.

    UI
    - "Load folder" button
    - Two square image fields (left, right)
    - Status line with comparison progress

    Interaction
    - Click left or right image to pick the preferred one
    - Sorting proceeds until completion, then output folder is created automatically
    """

    def __init__(self) -> None:
        """Initialize the application window and widgets."""
        super().__init__()

        self.title("Picture Compare")
        self.minsize(900, 650)

        self._folder_path: Optional[str] = None
        self._pictures: List[Picture] = []
        self._score_map: Dict[str, Score] = {}
        self._sorter: Optional[InteractiveSorter] = None

        self._left_photo: Optional["ImageTk.PhotoImage"] = None
        self._right_photo: Optional["ImageTk.PhotoImage"] = None
        self._left_picture: Optional[Picture] = None
        self._right_picture: Optional[Picture] = None

        self._image_side: int = 420
        self._image_cache: Dict[Tuple[str, int], "ImageTk.PhotoImage"] = {}

        self._build_ui()
        self._bind_events()

    def _build_ui(self) -> None:
        """Create and place all widgets."""
        self._top_bar = tk.Frame(self)
        self._top_bar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self._load_button = tk.Button(self._top_bar, text="Load folder", command=self._on_load_folder)
        self._load_button.pack(side=tk.LEFT)

        self._status_label = tk.Label(self._top_bar, text="Load a folder to start.", anchor="w")
        self._status_label.pack(side=tk.LEFT, padx=12, fill=tk.X, expand=True)

        self._content = tk.Frame(self)
        self._content.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._left_frame = tk.Frame(self._content, bd=1, relief=tk.SOLID)
        self._right_frame = tk.Frame(self._content, bd=1, relief=tk.SOLID)
        self._left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self._right_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self._content.grid_rowconfigure(0, weight=1)
        self._content.grid_columnconfigure(0, weight=1)
        self._content.grid_columnconfigure(1, weight=1)

        self._left_canvas = tk.Canvas(self._left_frame, highlightthickness=0)
        self._right_canvas = tk.Canvas(self._right_frame, highlightthickness=0)
        self._left_canvas.pack(fill=tk.BOTH, expand=True)
        self._right_canvas.pack(fill=tk.BOTH, expand=True)

        self._bottom_bar = tk.Frame(self)
        self._bottom_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))

        self._progress_label = tk.Label(self._bottom_bar, text="", anchor="w")
        self._progress_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _bind_events(self) -> None:
        """Bind UI events for resizing and clicking."""
        self.bind("<Configure>", self._on_window_resize)
        self._left_canvas.bind("<Button-1>", self._on_choose_left)
        self._right_canvas.bind("<Button-1>", self._on_choose_right)

    def _on_load_folder(self) -> None:
        """Handle folder selection and initialize the comparison workflow."""
        if not Tools.require_pillow():
            return

        selected = filedialog.askdirectory(title="Select folder with images")
        if not selected:
            return

        pictures = Tools.list_pictures_in_folder(selected)
        if len(pictures) < 2:
            messagebox.showwarning(
                "Not enough images",
                "Please select a folder with at least 2 supported images (jpg, jpeg, png, ...).",
            )
            return

        self._folder_path = os.path.abspath(selected)
        self._pictures = pictures
        self._score_map = {p.path: Score() for p in self._pictures}
        self._image_cache.clear()

        self._sorter = InteractiveSorter(self._pictures, self._score_map)
        self._status_label.config(text=f"Folder: {self._folder_path}")
        self._advance_and_render()

    def _on_window_resize(self, event: tk.Event) -> None:
        """Recompute square image side on window resize and rerender current pair.

        Args:
            event: Tkinter resize event.
        """
        _ = event
        self._recompute_image_side()
        self._render_current_pair()

    def _recompute_image_side(self) -> None:
        """Compute the square side length based on available UI space."""
        content_width = max(1, self._content.winfo_width())
        content_height = max(1, self._content.winfo_height())

        per_panel_width = max(1, (content_width - 16) // 2)
        side = min(per_panel_width, content_height)
        side = max(200, side)

        if side != self._image_side:
            self._image_side = side
            self._image_cache.clear()

    def _advance_and_render(self) -> None:
        """Advance to the next needed comparison and render it, or finish and export."""
        if self._sorter is None:
            return

        if self._sorter.is_completed():
            ordered = self._sorter.get_sorted_result_if_done()
            if ordered is None:
                return
            self._finalize_export(ordered)
            return

        pair = self._sorter.get_current_pair()
        if pair is None:
            self._finalize_export(self._sorter.get_sorted_result_if_done() or [])
            return

        left_picture, right_picture = pair
        self._left_picture = left_picture
        self._right_picture = right_picture

        self._progress_label.config(text=self._sorter.get_progress_text())
        self._render_current_pair()

    def _render_current_pair(self) -> None:
        """Render the current left and right pictures into their square canvases."""
        if self._left_picture is None or self._right_picture is None:
            self._clear_canvases()
            return

        self._draw_picture_on_canvas(self._left_canvas, self._left_picture, is_left=True)
        self._draw_picture_on_canvas(self._right_canvas, self._right_picture, is_left=False)

    def _clear_canvases(self) -> None:
        """Clear both image canvases."""
        self._left_canvas.delete("all")
        self._right_canvas.delete("all")

    def _draw_picture_on_canvas(self, canvas: tk.Canvas, picture: Picture, is_left: bool) -> None:
        """Draw a picture centered in a square canvas, preserving aspect ratio.

        Args:
            canvas: Target Tkinter Canvas.
            picture: Picture to display.
            is_left: Whether this is the left side (used only to keep references).
        """
        canvas.delete("all")

        canvas_width = max(1, canvas.winfo_width())
        canvas_height = max(1, canvas.winfo_height())
        side = min(canvas_width, canvas_height, self._image_side)

        photo_image = self._get_cached_photo(picture, side)
        if photo_image is None:
            canvas.create_text(
                canvas_width // 2,
                canvas_height // 2,
                text=f"Failed to load:\n{picture.filename}",
                anchor="center",
            )
            return

        x_center = canvas_width // 2
        y_center = canvas_height // 2
        canvas.create_image(x_center, y_center, image=photo_image, anchor="center")

        if is_left:
            self._left_photo = photo_image
        else:
            self._right_photo = photo_image

    def _get_cached_photo(self, picture: Picture, side: int) -> Optional["ImageTk.PhotoImage"]:
        """Get a resized PhotoImage for a picture and square side, using an in-memory cache.

        Args:
            picture: Image descriptor.
            side: Target square side in pixels.

        Returns:
            A Tk-compatible PhotoImage or None if loading fails.
        """
        cache_key = (picture.path, side)
        cached = self._image_cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            with Image.open(picture.path) as img:
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGB")
                fitted = Tools.fit_image_to_square(img, side)
                photo = ImageTk.PhotoImage(fitted)
                self._image_cache[cache_key] = photo
                return photo
        except Exception:
            return None

    def _on_choose_left(self, event: tk.Event) -> None:
        """Handle user choosing the left picture.

        Args:
            event: Mouse click event.
        """
        _ = event
        if self._sorter is None:
            return
        self._sorter.choose_left()
        self._advance_and_render()

    def _on_choose_right(self, event: tk.Event) -> None:
        """Handle user choosing the right picture.

        Args:
            event: Mouse click event.
        """
        _ = event
        if self._sorter is None:
            return
        self._sorter.choose_right()
        self._advance_and_render()

    def _finalize_export(self, ordered: List[Picture]) -> None:
        """Create the output folder and copy/rename pictures as requested.

        This runs automatically once comparisons are complete.

        Args:
            ordered: Pictures sorted best-first.
        """
        if self._folder_path is None:
            return

        if not ordered:
            messagebox.showerror("Export failed", "No ordered pictures were produced.")
            self._reset_session_state()
            return

        try:
            output_folder = Tools.ensure_unique_output_folder(self._folder_path, "_compare")
            Tools.copy_and_rename_ordered_pictures(ordered, output_folder)
            messagebox.showinfo(
                "Done",
                f"Created ordered output folder:\n{output_folder}",
            )
        except Exception as exc:
            messagebox.showerror("Export failed", f"Could not create output:\n{exc}")

        self._reset_session_state()

    def _reset_session_state(self) -> None:
        """Reset session state so the user can load another folder or quit."""
        self._pictures = []
        self._score_map = {}
        self._sorter = None
        self._left_picture = None
        self._right_picture = None
        self._left_photo = None
        self._right_photo = None
        self._image_cache.clear()

        self._progress_label.config(text="")
        self._status_label.config(text="Load a folder to start.")
        self._clear_canvases()


def main() -> None:
    """Entry point for running the application."""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()