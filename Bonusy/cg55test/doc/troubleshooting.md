# Troubleshooting

## The App Opens but Downloads Fail

Install dependencies first:

```bash
pip install -r requirements.txt
```

If the error mentions merging, conversion, or FFmpeg, install FFmpeg and make sure it is available on your system `PATH`.

## `_tkinter` Is Missing

The selected Python installation does not include Tkinter. The app cannot create a Tkinter window without this native Python module.

For Homebrew Python on macOS, install the matching Tk package:

```bash
brew install python-tk@3.14
```

If there is no matching package for your Python version, install Python from python.org or use another Python distribution that includes Tcl/Tk support.

## Some Videos Work and Others Do Not

The application tries several `yt-dlp` format strategies, but availability depends on the specific video, region, age restrictions, live status, and YouTube changes. Updating `yt-dlp` usually fixes many extraction problems:

```bash
pip install --upgrade yt-dlp
```

## Audio-Only MP3 Mode Fails

MP3 conversion requires FFmpeg. Without FFmpeg, use normal video mode or update the app to prefer raw audio output.

## Packaged App Cannot Download

The deploy scripts bundle FFmpeg and FFprobe when those commands are available on the build machine. If they are missing during packaging, the app still builds, but some merging and MP3 conversion paths can fail on target machines.
