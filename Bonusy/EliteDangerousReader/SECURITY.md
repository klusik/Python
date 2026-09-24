# Security policy

## Scope

Elite Dangerous Reader embeds remote website content. Treat all page JavaScript and HTML as untrusted input even though top-level navigation is restricted to the official domain.

## Implemented controls

- HTTPS-only top-level navigation.
- Exact base-domain and subdomain validation.
- Native WebView2 navigation cancellation.
- New-window cancellation or same-window handling.
- Post-load navigation fallback.
- Disabled downloads and local file URLs.
- Disabled developer tools outside explicit debug mode.
- Narrow settings-only Python API.
- Strict settings field validation.
- Atomic settings persistence.
- No application telemetry.

## Known limitations

- A compromised official website can invoke the exposed settings API. It can only change validated visual settings.
- The native navigation hook depends on pywebview's Windows backend implementation. The fallback guard reduces, but does not eliminate, compatibility risk after dependency upgrades.
- Subresources are not restricted to the base domain because the official website may require content delivery networks, analytics, fonts, or media hosts.
- A compromised WebView2 runtime or operating system is outside this application's threat model.
- The executable is unsigned unless the repository owner adds organizational code signing.

## Reporting

Open a private security report in the repository hosting platform when possible. Do not include company-confidential URLs, logs, or proxy information in a public issue.
