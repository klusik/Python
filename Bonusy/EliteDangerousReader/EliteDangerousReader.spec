# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification for the Windows one-file executable."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_all

project_root = Path(SPECPATH)
src_root = project_root / "src"
webview_datas, webview_binaries, webview_hiddenimports = collect_all("webview")

application_datas = [
    (
        str(src_root / "elite_reader" / "assets" / "reader_injection.js"),
        "elite_reader/assets",
    ),
]

analysis = Analysis(
    [str(project_root / "run_elite_reader.py")],
    pathex=[str(src_root)],
    binaries=webview_binaries,
    datas=webview_datas + application_datas,
    hiddenimports=webview_hiddenimports + ["webview.platforms.edgechromium"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "PyQt5",
        "PyQt6",
        "PySide2",
        "PySide6",
        "cefpython3",
    ],
    noarchive=False,
    optimize=1,
)

python_archive = PYZ(analysis.pure)

executable = EXE(
    python_archive,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
    [],
    name="EliteDangerousReader",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / "assets" / "elite_reader.ico"),
)
