# Static Gallery Structure

This gallery system is fully static. No PHP, database, or server-side rendering is required.

## Run it locally

Because the app loads JSON with `fetch()`, serve the folder through a small local web server instead of opening `index.html` directly as a file.

Example:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Add a new gallery

1. Create a folder in `/galleries`, for example `/galleries/my-trip`.
2. Put your image files into that folder.
3. Add a `gallery.json` file in that folder.
4. Register the gallery in `/galleries/index.json`.

## Gallery manifest format

```json
{
  "title": "My Trip",
  "description": "Short description.",
  "cover": "./galleries/my-trip/cover.jpg",
  "tags": ["travel", "city"],
  "images": [
    {
      "src": "./galleries/my-trip/photo-1.jpg",
      "title": "Photo title",
      "caption": "Photo description",
      "alt": "Accessible alt text"
    }
  ]
}
```
