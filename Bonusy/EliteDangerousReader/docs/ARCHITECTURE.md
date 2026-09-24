# Architecture

## Components

### Python application layer

`EliteReaderApplication` creates a pywebview window using the Windows `edgechromium` backend. pywebview hosts the installed Microsoft Edge WebView2 control.

The Python layer owns:

- startup URL validation;
- settings persistence;
- logging;
- native navigation cancellation;
- JavaScript resource injection;
- process lifecycle.

### Navigation policy

`navigation.py` accepts only:

- scheme: `https`;
- host: `elitedangerous.com` or a true subdomain;
- URLs without embedded username or password fields.

The implementation avoids substring matching. For example, `elitedangerous.com.example.org` and `notelitedangerous.com` are rejected.

Navigation is enforced in three layers:

1. WebView2 `NavigationStarting` cancellation before top-level navigation.
2. WebView2 `NewWindowRequested` handling.
3. JavaScript link interception plus a Python post-load fallback.

The native layer is best effort because it relies on pywebview's Windows backend internals. The post-load guard remains active if backend internals change.

### JavaScript bridge

`ReaderApi` exposes four methods:

- `get_settings`;
- `save_settings`;
- `reset_settings`;
- `get_app_info`.

No generic callback, reflection, file picker, shell command, arbitrary URL opener, or Python evaluator is exposed.

### Page injection

`reader_injection.js` creates:

- a Shadow DOM toolbar isolated from website CSS;
- a page-level style element containing the readability override;
- a visual element picker;
- a mutation observer that restores removed reader elements;
- normal-link and new-window guards.

The CSS selector is validated by both JavaScript syntax parsing and Python length and character constraints. CSS selectors are still powerful presentation expressions, but they do not provide native access.

### Persistence

`SettingsStore` writes JSON to the user's roaming application-data directory. WebView2 browser state uses a dedicated local application-data profile rather than pywebview's shared default profile. It uses a temporary file and atomic replacement to reduce corruption from interrupted writes.

## Data flow

```text
Toolbar control change
        |
        v
JavaScript local preview
        |
        v
window.pywebview.api.save_settings(payload)
        |
        v
Python validation
        |
        v
Atomic settings.json replacement
        |
        v
Sanitized settings returned to JavaScript
```

## Packaging

PyInstaller creates a one-file Windows executable. The packaged executable contains Python, pywebview, the WebView2 loader integration, and the injected JavaScript. It does not bundle the Microsoft Edge WebView2 Runtime itself.

The WebView2 Evergreen Runtime must be installed on the target machine.
