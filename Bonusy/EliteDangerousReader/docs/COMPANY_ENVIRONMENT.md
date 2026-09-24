# Corporate environment notes

This project avoids Edge extension installation, but it does not bypass company security controls.

## Controls that can still affect the application

- AppLocker or Windows Defender Application Control can block Python or the executable.
- Endpoint protection can quarantine unsigned one-file executables.
- A proxy or TLS inspection system can block the target website.
- WebView2 Runtime execution can be restricted.
- Downloads may be blocked, although the reader disables its own download handling.
- JavaScript or website assets can be filtered by the corporate network.

## Recommended internal approval package

Provide IT or security reviewers with:

- this complete source repository;
- the dependency lock information in `requirements*.txt`;
- the PyInstaller specification;
- test results from `scripts\check.bat`;
- a checksum of the final executable;
- a description of the allowed domain and narrow JavaScript bridge.

## Why the app requests no browser extension permission

The application hosts a separate WebView2 control. It does not register an Edge extension, modify the company Edge profile, install a browser policy, or inject code into the normal Edge process.

## Network behavior

The app navigates to the official Elite Dangerous website. The page can request normal resources from its own infrastructure and content delivery networks. The app itself does not send telemetry, call an update service, or proxy page content.

## Deployment caution

Do not present this app as a method to evade organizational policy. Obtain approval when policy requires software review. A blocked extension page often indicates a broader endpoint-governance policy, not merely a technical limitation of Edge.
