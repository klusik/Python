# User guide

## Purpose

Elite Dangerous Reader displays the live official Elite Dangerous website in a dedicated desktop window. It changes presentation locally after the page loads. The website remains online and interactive.

## Starting the application

From source:

```bat
scripts\run.bat
```

Packaged:

```text
EliteDangerousReader.exe
```

The update notes index is the fixed Home destination.

## Changing the background

1. Open the floating reader panel.
2. Select **Background color**.
3. Press **Apply and save**.
4. When no visible change occurs, use **Pick area**.
5. Click the large black background surrounding or containing the article.

The application removes that element's CSS background image when the corresponding option is enabled. Disable the option when the page uses an image that should remain visible.

## Text color

Leave the text color empty to preserve the website's original typography. Enter a six-digit color such as `#eeeeee` to override it.

The **Apply optional text color to child elements** option is intentionally aggressive. It can improve article readability, but it can also recolor links, buttons, and icons below the selected element.

## Font controls

- Font scale adjusts the selected element relative to the website's existing size.
- Line height adjusts vertical spacing inside the selected element.

Selecting a content container instead of `body` usually produces better typography changes.

## Navigation

The application accepts only HTTPS pages on `elitedangerous.com` and its subdomains. External links are blocked rather than opened in another browser. This is intentional because the application is single-purpose.

Website assets can still load from content delivery networks. The restriction applies to top-level pages, not every image, stylesheet, font, or script request.

## Resetting settings

Use **Reset defaults** in the reader panel or launch:

```bat
EliteDangerousReader.exe --reset-settings
```

If the settings file becomes invalid, it is moved to `settings.json.invalid` and defaults are restored.

## Common problems

### The page does not open

Check whether the company firewall, proxy, DNS filter, or TLS inspection permits the official site. WebView2 normally uses Windows networking and proxy configuration.

### A company security product blocks the executable

The executable is locally built and unsigned. SmartScreen, AppLocker, WDAC, endpoint protection, or allow-listing policy can block it. Running the Python source may also be restricted. Company IT must approve the executable or repository in that environment.

### The background returns after navigating

The website can render pages as a single-page application. The injected style is monitored and restored when removed. If the website changed its DOM structure, use **Pick area** again.

### Login or external account pages do not work

They are outside the approved domain and are blocked by design. This reader targets public website content such as update notes.
