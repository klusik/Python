# Inara Profile Downloader

A Windows-oriented Tkinter application that sends the official Inara API
`getCommanderProfile` event and saves the returned data into a single,
well-structured JSON file.

## Critical API limitation

The official Inara API does **not** provide a full private commander-data export.
The `getCommanderProfile` event returns only basic profile information such as:

- Inara user and commander identity;
- pilot ranks and rank progress;
- preferred allegiance and power;
- main-ship summary;
- squadron summary;
- preferred role;
- avatar and profile URLs;
- whether Inara game-data import is active.

It does **not** return:

- raw, manufactured or encoded engineering materials;
- Odyssey goods, assets, data, consumables, backpack or ship locker;
- the complete fleet or ship loadouts;
- stored modules;
- cargo;
- credits and assets;
- engineer unlock state;
- missions, statistics, permits or travel history.

This is a limitation of the read API, not of this application. The Inara API
documentation describes `getCommanderProfile` as returning *basic information*.
The API contains many events that let third-party tools **send** materials,
ships and other data to Inara, but it does not expose corresponding read events
for downloading those private datasets.

Official references:

- https://inara.cz/elite/inara-api-devguide/
- https://inara.cz/elite/inara-api-docs/
- https://inara.cz/elite/inara-api/

## Requirements

- Windows 10 or Windows 11 recommended;
- Python 3.11 or newer;
- Tkinter, normally included with the standard Windows Python installer;
- an Inara account;
- a personal Inara API key;
- an Inara-whitelisted application name.

No third-party Python packages are required.

## Inara setup

### 1. Generate a personal API key

Sign in to Inara and open the API settings page:

https://inara.cz/elite/cmdr-settings-api/

Generate or copy your personal API key. The application keeps the key only in
memory and never writes it to settings, logs or exported JSON.

### 2. Register the application name

Inara requires applications using the API to be identified and whitelisted.
The exact application name sent in requests must be accepted by Inara.

See `docs/INARA_REGISTRATION.md` for the information Inara asks developers to
provide. Enter that exact registered name in the application.

A personal API key by itself may not be sufficient when the application name
has not been whitelisted.

## Running the application

From PowerShell in the project directory:

```powershell
py -3 .\run_app.py
```

If the Python launcher is unavailable:

```powershell
python .\run_app.py
```

For a console-free Windows launch, double-click `run_app.pyw`.

## Using the application

1. Enter your personal Inara API key.
2. Enter the exact whitelisted application name.
3. Optionally enter the commander name.
   - With a personal API key, Inara can return the key owner's profile when the
     search name is omitted.
   - Supplying the exact in-game commander name makes the request more explicit.
4. Optionally enter the Frontier ID in `F123456` or `123456` form.
5. Select the output directory.
6. Click **Download profile**.

The application creates one file:

```text
output/inara_profile.json
```

Each successful download atomically replaces the previous file.

## Export structure

The output file contains:

```json
{
  "schema": {},
  "source": {},
  "request": {},
  "api_scope": {},
  "profile": {},
  "raw_api_response": {}
}
```

- `schema`: exporter name, schema version and generation timestamp;
- `source`: Inara endpoint, event name and application version;
- `request`: non-secret request metadata;
- `api_scope`: explicit list of available and unavailable data;
- `profile`: the `eventData` returned by `getCommanderProfile`;
- `raw_api_response`: the complete JSON returned by Inara.

The API key is never included.

## Settings and generated files

Non-secret settings are stored outside the repository in the user's application
data directory. On Windows this is normally:

```text
%APPDATA%\InaraProfileDownloader\settings.json
```

Logs are stored in:

```text
%LOCALAPPDATA%\InaraProfileDownloader\logs\application.log
```

The following project-local directories are generated and ignored by Git:

- `output/`
- `deploy/`
- `logs/`

## Request-rate policy

The application permits one request every 30 seconds, equivalent to no more
than two requests per minute. This follows Inara's published request-rate
guidance. There are no aggressive automatic retries.

## Deployment

Run from PowerShell:

```powershell
.\deploy.bat
```

The deployment builder:

1. removes any old `deploy` directory;
2. creates `deploy\InaraProfileDownloader`;
3. copies the runtime source and documentation;
4. excludes caches, generated output, logs, credentials, tests and the deploy
   directory itself;
5. creates `deploy\InaraProfileDownloader-1.0.0.zip`;
6. writes a SHA-256 checksum file.

The batch file detects either `py -3` or `python` and returns a clean exit code.

## Tests

Run:

```powershell
py -3 -m unittest discover -s tests -v
```

The tests do not call the live Inara API.

## Security design

- The API key is held only in memory.
- The API key is not saved with settings.
- The API key is not written into output JSON.
- The API key is not logged.
- Network traffic uses HTTPS.
- JSON output is written atomically through a temporary file.
- API error messages are presented without echoing credentials.

## Architecture

- `api_client.py`: payload construction, HTTPS request and response validation;
- `configuration.py`: non-secret settings persistence;
- `controller.py`: application workflow orchestration;
- `exporter.py`: stable JSON export;
- `gui.py`: Tkinter user interface and background worker handling;
- `models.py`: typed immutable data models;
- `rate_limiter.py`: local request throttling;
- `logging_setup.py`: rotating file logging;
- `scripts/create_deploy.py`: deterministic deployment packaging.

## License

MIT. See `LICENSE`.
