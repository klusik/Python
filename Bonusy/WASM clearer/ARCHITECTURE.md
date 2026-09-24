# MSFS WASM Cache Cleaner Architecture

## Purpose

The application finds product-level WASM cache folders for MSFS 2020 and MSFS 2024, lets the user select them, previews the cleanup, and deletes only validated cache content. It is a Windows desktop utility built entirely with the Python standard library.

## Core design principles

1. **Standard library first** — Tkinter and normal filesystem APIs keep installation simple. No framework or build step is required.
2. **Conservative discovery** — only known simulator locations and existing `WASM` roots are considered. Ambiguous folders are not exposed as cleanup targets.
3. **One cleanup policy** — preview and deletion use the same protected-name, containment, and reparse-point rules. Presentation code does not decide what is safe to delete.
4. **Validate again at mutation time** — a preview is informative, not authority. Every entry and child path is checked again immediately before deletion because the filesystem may change after inspection.
5. **Transparent destructive actions** — confirmation shows selected products, estimated bytes, files, folders, and protected items. Nothing is selected by default.
6. **Responsive interface** — filesystem discovery, preview calculation, and cleanup run on worker threads. Tkinter widgets are changed only on the UI thread through the result queue.
7. **Partial failure is contained** — one unreadable or failed target does not prevent other selected entries from being processed, and failures remain visible in the status log.

## Module boundaries

```text
WASM_clear.pyw
  -> src.gui          Tkinter presentation, selection, workflow coordination
      -> src.discovery   eligible cache-entry discovery
          -> src.detection   known simulator/install locations
      -> src.cleaner     read-only cleanup planning and validated deletion
      -> src.models      immutable data exchanged between layers
      -> src.path_utils  shared path primitives
```

- `models.py` contains immutable transport objects and no filesystem or UI behavior.
- `path_utils.py` contains reusable path normalization and Windows reparse-point checks.
- `detection.py` finds simulator installations and known user-data roots.
- `discovery.py` converts safe product folders beneath approved WASM roots into selectable entries.
- `cleaner.py` is the sole owner of protected folder names, cleanup inspection, and deletion rules.
- `gui.py` renders data and coordinates background work; it must not invent cleanup safety policy.

## Cleanup workflow

```text
scan -> user selection -> background preview -> detailed confirmation
     -> background revalidation and deletion -> result log -> rescan
```

Preview totals are estimates from the moment of inspection. Cleanup deliberately revalidates targets and may report different final counts if files change, become locked, or cannot be read.

File details are loaded on demand from the confirmation dialog so the initial preview remains bounded and responsive. The inspector reports filesystem metadata and recognizes the WebAssembly binary signature and version; it does not speculate about compiled module behavior or simulator runtime usage.

## Deliberate non-goals

- No automatic or scheduled deletion.
- No registry or configuration writes.
- No deletion of an entire approved `WASM` root.
- No traversal through symlinks, junctions, or other reparse points.
- No third-party GUI framework, installer framework, telemetry, updater, or network access.
- No speculative abstraction, plugin system, or configuration layer for this single-purpose utility.
