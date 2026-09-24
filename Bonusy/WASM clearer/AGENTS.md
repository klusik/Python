# Repository Guidelines

## Product intent

This is a small, dependable Windows utility for clearing selected Microsoft Flight Simulator WASM caches. Keep it understandable, conservative, and easy to run with a normal Python installation.

## Engineering principles

- Prefer the Python standard library. Add a dependency only when it solves a real problem that cannot be handled clearly in the existing stack.
- Do not add `from __future__ import annotations`. The supported Python version already provides the typing syntax used here.
- Preserve the boundaries documented in `ARCHITECTURE.md`: discovery finds eligible targets, cleanup owns inspection and deletion policy, models carry data, and the GUI owns presentation and user interaction.
- Keep functions small and explicit. Extend the existing responsibility owner instead of adding parallel helpers or duplicated policy.
- Treat deletion as a hostile boundary. Canonicalize and validate paths, reject ambiguous targets, avoid reparse points, preserve known state folders, and continue safely when one target fails.
- Keep destructive actions transparent. Show the selected scope and an inspection-based estimate before changing the filesystem.
- Do not broaden cleanup eligibility or weaken safety checks merely to make a case pass.
- Keep the interface responsive by running filesystem scans, cleanup planning, and deletion outside the Tkinter UI thread.
- Prefer focused tests for filesystem policy and pure formatting logic. Tests must use temporary directories and must never touch actual simulator data.

## Verification

Run from the repository root:

```powershell
python -m unittest discover -s tests -v
python -m compileall -q WASM_clear.pyw src tests
```

For interface changes, also launch `WASM_clear.pyw` and manually verify selection, cancellation, confirmation, resizing, and cleanup-result reporting.
