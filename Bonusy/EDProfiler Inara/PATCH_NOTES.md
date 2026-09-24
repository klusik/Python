# Patch Notes

## 1.0.0 — 17 July 2026

Initial release.

### Added

- Object-oriented Tkinter desktop application.
- Personal Inara API key input with masked display.
- Registered Inara application-name input.
- Optional commander-name and Frontier-ID inputs.
- Official `getCommanderProfile` API request support.
- Strict request validation and structured API error reporting.
- Local request throttling to one request every 30 seconds.
- Background network execution so the GUI does not freeze.
- JSON export with raw response, normalized profile data, request metadata and an explicit API-scope statement.
- Non-secret settings persistence.
- API keys are never written to disk by the application.
- Rotating application log.
- Standard-library-only implementation.
- Automated unit tests.
- Reproducible deployment builder and Windows `deploy.bat` entry point.
- Full documentation for setup, Inara application registration, security and API limitations.
