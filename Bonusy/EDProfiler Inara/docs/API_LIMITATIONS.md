# Inara API Read-Scope Limitations

## What the application can download

The application uses the official `getCommanderProfile` API event. According to
Inara's documentation, that event returns basic commander information, including
identity, ranks, preferences, a main-ship summary and squadron information.

## What the application cannot download

The API documentation contains write events such as `setCommanderInventory`,
`setCommanderShip`, `setCommanderCredits` and many others. These events exist so
journal-reading applications can upload data to Inara.

Their existence does not imply that the same datasets can be downloaded. There
are no corresponding official read events for the commander's complete:

- engineering-material inventory;
- Odyssey inventory;
- fleet and loadouts;
- stored modules;
- cargo;
- credits and assets;
- engineer state;
- mission state;
- statistics;
- flight history.

Therefore, an Inara API key cannot be used as a replacement for Frontier's
companion API or for a correctly reconstructed local journal state.

## Why the exported JSON includes `api_scope`

The output deliberately records the limitation in machine-readable form. This
prevents downstream consumers, including an AI assistant, from assuming that an
absent material or ship means the commander does not own it.

## Authoritative references

- Inara API developer guide:
  https://inara.cz/elite/inara-api-devguide/
- Inara API documentation:
  https://inara.cz/elite/inara-api-docs/
- Inara API overview:
  https://inara.cz/elite/inara-api/
