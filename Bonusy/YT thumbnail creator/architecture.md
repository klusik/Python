# Architecture

## Purpose

This project is a small desktop utility that lets a user load a background image, place two lines of text over it, preview the result, and export the rendered image to PNG and JPG.

Even though the application is small, the structure already follows a useful separation of concerns:

- application startup is isolated in `app.py`
- static defaults are isolated in `thumbnail_maker/config.py`
- user interface and event coordination are isolated in `thumbnail_maker/gui.py`
- image rendering is isolated in `thumbnail_maker/renderer.py`

That split matters because desktop GUI code tends to become tangled very quickly if window code, configuration, and rendering are mixed into a single file.

## High-level execution flow

1. Python starts `app.py`.
2. `app.py` imports `ThumbnailMakerApp` and creates the application instance.
3. `ThumbnailMakerApp.__init__()` creates the Tkinter root window, initializes all Tk state variables, creates the renderer service, and builds the visible UI.
4. `ThumbnailMakerApp.run()` starts Tkinter's event loop.
5. The user selects a background image, edits text, or moves sliders.
6. GUI callbacks schedule a delayed preview refresh.
7. The delayed refresh calls `ThumbnailRenderer.render()`.
8. The renderer opens the source image with Pillow, adds the readability overlay, draws the stroked title and subtitle, and returns the finished image.
9. The GUI turns the rendered image into a Tk-compatible `PhotoImage` and displays it on the preview canvas.
10. When the user exports, the already rendered image is written to PNG and JPG by `ThumbnailRenderer.save_both_formats()`.

## Module-by-module design

### `app.py`

`app.py` is deliberately minimal.

Its job is not to contain application logic. Its job is to define the executable boundary of the program.

This gives several benefits:

- the application can be imported without automatically launching a window
- packaging tools such as PyInstaller can target a clear entry point
- future tests can import the GUI class directly
- startup logic remains obvious and low-risk

The file effectively acts as a bootstrap layer.

### `thumbnail_maker/config.py`

This module is the single source of truth for default values and shared constants.

Examples include:

- application title
- default font sizes
- default text positions
- default overlay tuning
- supported file picker extensions
- preview refresh throttle interval

This is a configuration registry pattern in a lightweight form. The project does not use a formal settings class because the application is still small, but the module serves the same practical role.

Why this is useful:

- UI code stays focused on layout and events
- renderer code stays focused on image composition
- changing defaults does not require searching through multiple files
- the codebase gets an obvious place for future tunables

### `thumbnail_maker/gui.py`

This module contains `ThumbnailMakerApp`, which acts as the main controller of the application.

The class is responsible for:

- creating and configuring the Tk root window
- constructing the left control panel and right preview panel
- holding Tkinter variables that mirror the current editor state
- handling file dialogs and message boxes
- scheduling preview refreshes
- delegating rendering to the renderer service
- converting Pillow images into Tkinter preview images

What it is **not** responsible for:

- low-level pixel rendering
- choosing font files beyond delegating to the renderer
- direct image export details beyond invoking the renderer service

This file loosely follows a controller or composition-root style.

#### Internal state design

The GUI keeps several kinds of state:

1. Persistent UI settings
   - title text
   - subtitle text
   - horizontal and vertical ratios
   - font sizes
   - output base name

2. Session state
   - selected background image path
   - last rendered full-size image
   - preview image reference needed by Tkinter

3. Scheduling state
   - pending `after()` job identifier for delayed preview refresh

This separation is not formalized into separate classes yet, but the variable naming makes the role of each state group clear.

#### Why `StringVar`, `IntVar`, and `DoubleVar` are used

Tkinter variable objects create a bridge between widgets and program state.

Benefits:

- the entry or slider stays synchronized with Python state automatically
- callbacks can observe state changes via `trace_add()`
- values can be read without querying widgets directly

This is effectively a simple observer mechanism built into Tkinter.

#### Preview throttling strategy

The GUI intentionally does not render on every slider movement event.

Instead it uses this approach:

- cancel any existing pending preview refresh
- schedule a new refresh using `root.after(...)`
- only the most recent user action actually triggers rendering

This is a debounce-style update strategy.

Why it matters:

- image rendering can be relatively expensive compared to widget updates
- dragging a slider can generate many events per second
- without throttling, the UI would feel laggy or waste CPU time

This is one of the most important design choices in the application.

#### Why the preview image is stored on `self`

Tkinter image handling has a common pitfall: if the `PhotoImage` object is not strongly referenced, it may be garbage collected and disappear from the canvas.

The application avoids that by storing the preview image wrapper as `self.preview_photo_image`.

This is not an optimization. It is a correctness requirement of Tkinter image lifetime behavior.

### `thumbnail_maker/renderer.py`

This module contains `ThumbnailRenderer`, which acts as a rendering service.

The GUI does not draw pixels directly. Instead it calls this service with plain Python values.

That separation is useful because it keeps rendering deterministic and independent from the window toolkit.

The renderer performs four main tasks:

1. load the background image
2. create and apply the bottom readability overlay
3. compute title and subtitle positions
4. draw outlined text and save exported files

#### Cross-platform font lookup

The renderer stores a list of candidate bold font paths across Linux, Windows, and macOS.

This is a pragmatic portability strategy:

- try common locations in priority order
- use the first readable font found
- fall back to Pillow's default font if needed

It is not a formal font discovery subsystem, but it is appropriate for a compact desktop app.

#### Overlay rendering pipeline

The readability overlay is created as a transparent RGBA image, drawn separately, and then alpha-composited over the source image.

Why this is a good choice:

- the source image stays logically untouched during overlay creation
- the overlay behavior is easy to inspect and reason about
- the gradient can be tuned without changing text rendering code

#### Text position calculation

Text is centered around a ratio-based horizontal anchor.

The renderer does not assume fixed text width. Instead it measures the actual text via `textbbox()` and computes the final position from the measured width.

That ensures that long and short titles stay visually centered around the requested anchor point.

#### Manual text stroke implementation

The outline is produced by drawing the same text repeatedly around the target position and then drawing the fill text once on top.

Why this exists:

- it makes the stroke logic explicit
- it behaves consistently across environments
- it produces the thick YouTube-style text treatment this app wants

The circular distance check avoids drawing the full square around the glyphs, which would create a rougher-looking border.

## Data flow

### Input data

The application works with a very small data model:

- `background_path: str`
- `title_text: str`
- `subtitle_text: str`
- title font size and subtitle font size
- title position ratios and subtitle position ratios
- overlay tuning values from config

### Runtime data transformations

1. The GUI gathers state from Tk variables.
2. The GUI passes those values to `ThumbnailRenderer.render()`.
3. The renderer returns a Pillow `Image` object.
4. The GUI copies and downsizes that image for the preview canvas.
5. On export, the full-size rendered image is saved to disk.

The important design detail is that preview display uses a derived copy, while export uses the full rendered image.

That preserves quality during file generation.

## Error handling model

The application currently uses pragmatic local exception handling.

Examples:

- preview rendering errors show a message box
- save failures show a message box
- missing image selection produces a warning instead of a crash

This is appropriate for a small desktop utility. The GUI is the user-facing boundary, so it is reasonable for errors to be converted into dialogs at that boundary.

A larger version of the project might add:

- structured logging
- more precise exception classes
- validation before rendering
- font availability diagnostics

## Naming strategy

The code now favors descriptive variable names over compact names.

Examples:

- `background_image_path` instead of a shorter path variable
- `title_horizontal_ratio_var` instead of abbreviated coordinate naming
- `pending_preview_refresh_job_id` instead of a short scheduling name
- `drawing_context` instead of a single-letter drawing variable

This improves maintainability in GUI code especially, because widget code already carries a lot of contextual complexity.

## Extension points

The current structure supports several future improvements without major rewrites.

### Easy additions

- color pickers for title or subtitle
- stroke width controls
- overlay tuning controls in the GUI
- text alignment options
- separate output size presets
- drag-and-drop image loading
- automatic output naming from the input file name
- command-line batch rendering mode

### Refactors that would scale well

If the project grows, the next clean architectural steps would be:

1. Create a dedicated `ThumbnailSettings` dataclass
   - group all rendering parameters into one object
   - reduce long method signatures

2. Create a dedicated preview controller
   - isolate scheduling and canvas updates from widget construction

3. Create a file service
   - separate dialogs and output path rules from the main GUI class

4. Add logging
   - improve diagnostics during packaging and user support

## Current design strengths

- very small and understandable dependency surface
- clear separation between GUI and rendering logic
- centralized defaults
- practical cross-platform font fallback
- preview throttling avoids unnecessary rendering load
- export path handling is straightforward

## Current technical limitations

- no formal settings object yet
- no automated tests
- no explicit input validation beyond basic dialog flow
- no advanced typography features such as line wrapping or per-line alignment
- no persistent user preferences
- `ttk.Scale` does not strictly enforce the declared precision step

## Summary

This is a compact but sensibly structured desktop application.

Its main architectural idea is simple and correct: the GUI coordinates user actions, the renderer owns image composition, and shared defaults live in configuration.

For a project of this size, that is the right level of structure. It is small enough to stay easy to edit, but already separated enough that future changes will not immediately turn it into a single tangled file.
