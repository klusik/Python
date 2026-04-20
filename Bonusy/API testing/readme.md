# GET API Learning Project

This project is a compact, self-contained demonstration of how a Python server can expose a **GET-only JSON API** and how a browser page written in **HTML, CSS, and JavaScript** can consume that API with `fetch()`.

The project is intentionally small, but it covers a lot of practical API ideas:

- a list endpoint that returns many items,
- a single-item endpoint that returns one record by ID,
- query-parameter filtering,
- query-parameter sorting,
- pagination,
- summary statistics,
- dropdown metadata endpoints,
- browser-side rendering of JSON data,
- direct inspection of raw responses in the UI.

The code is heavily commented on purpose. The goal is not to be minimal. The goal is to make the workflow understandable for someone learning both Python HTTP servers and browser-side API consumption.

## Project Files

Only two files are required to run the project:

- [server.py](./server.py)
- [index.html](./index.html)

Two extra documentation files are included:

- [requirements.txt](./requirements.txt)
- [readme.md](./readme.md)
- [learn.html](./learn.html)

`requirements.txt` exists even though the server uses no external packages. That is deliberate: it makes the dependency situation explicit and makes it easy to extend the project later.

## What This Project Does

The demo shows a tiny product catalog with 10 sample items. The catalog is just a Python list of dictionaries inside `server.py`, which means the data is easy to inspect and easy to reason about.

From the browser page you can:

- search products by text,
- filter by category,
- filter by brand,
- filter by price range,
- filter by minimum rating,
- filter to in-stock-only items,
- sort by several fields,
- move through pages of results,
- open one product at a time by ID,
- inspect the raw JSON response returned by the server.

This gives you a practical view of how GET APIs work in real applications.

## Why GET

This project focuses on GET requests because they are the easiest place to learn API basics.

GET is used when you want to:

- request data from a server,
- encode filter choices in the URL,
- keep the interaction stateless,
- make endpoints easy to test in a browser,
- make the request visible and shareable as a URL.

Examples:

- `http://localhost:8484/api/products`
- `http://localhost:8484/api/products?category=Electronics`
- `http://localhost:8484/api/products?search=coffee&sort_by=price&sort_dir=desc`

Those URLs are readable because the input lives in the query string instead of the request body.

## How The Workflow Works

The full workflow is:

1. Start the Python server.
2. Open `index.html` in a browser.
3. The page loads categories and brands from the server.
4. The page loads the first product page.
5. When you change a filter, the JavaScript builds a new GET URL.
6. The browser sends a new request to the Python API.
7. The server filters, sorts, and slices the data.
8. The server returns JSON.
9. The browser renders the JSON into cards, stats, and a raw preview panel.

That is the core loop. Every control in the interface feeds into that loop.

## Server Overview

`server.py` uses only the Python standard library.

Main modules:

- `http.server` for the web server,
- `urllib.parse` for reading the path and query string,
- `json` for producing JSON responses.

The server listens on a port you choose at startup. If you press Enter at the prompt, it uses the default port `8484`.

The server supports these endpoints:

- `/`
- `/api`
- `/api/products`
- `/api/products/<id>`
- `/api/categories`
- `/api/brands`
- `/api/stats`

## Endpoint Details

### `/`

This is a small JSON landing response. It is useful for checking that the server is running and for seeing the list of available endpoints.

Example response fields:

- `message`
- `hint`
- `available_endpoints`

### `/api`

This is a documentation-style endpoint. It describes the API, its version, and example URLs.

It is useful because the API effectively explains itself when you open it in the browser.

### `/api/products`

This is the main endpoint.

It supports the following query parameters:

- `search`
- `category`
- `brand`
- `min_price`
- `max_price`
- `min_rating`
- `in_stock`
- `sort_by`
- `sort_dir`
- `page`
- `page_size`

Example URLs:

```text
/api/products
/api/products?category=Electronics
/api/products?brand=HomeCraft
/api/products?min_price=30&max_price=100
/api/products?search=tablet
/api/products?search=coffee&sort_by=price&sort_dir=desc
/api/products?category=Sports&in_stock=true&page=1&page_size=4
```

The server response includes:

- `filters_used`
- `pagination`
- `stats_for_filtered_set`
- `items`

That shape is intentional. It shows a common API pattern where the server returns both data and metadata in the same response.

### `/api/products/<id>`

This returns one product object by numeric ID.

Examples:

- `/api/products/1`
- `/api/products/3`
- `/api/products/10`

This endpoint is useful for learning the difference between:

- collection endpoints, which return many records,
- resource endpoints, which return one record.

### `/api/categories`

This returns a unique list of categories found in the dataset.

The browser uses this endpoint to populate the category dropdown dynamically.

### `/api/brands`

This returns a unique list of brands found in the dataset.

The browser uses this endpoint to populate the brand dropdown dynamically.

### `/api/stats`

This returns summary statistics for the currently filtered result set.

It uses the same filter logic as `/api/products`, which is important because it keeps the behavior consistent.

Example:

- `/api/stats?category=Sports`
- `/api/stats?search=wireless`
- `/api/stats?brand=HomeCraft&min_price=20&max_price=80`

## Front-End Overview

`index.html` contains:

- HTML markup,
- CSS styling,
- JavaScript behavior.

That is done intentionally so the entire client side stays in one file.

The page includes:

- an API base URL field,
- a text search input,
- category and brand dropdowns,
- minimum and maximum price inputs,
- minimum rating selection,
- page size selection,
- sort field and sort direction selection,
- an in-stock checkbox,
- a single-product lookup input,
- buttons for loading data and moving through pages,
- a status box,
- summary stat cards,
- a product card grid,
- a raw JSON preview panel.

## JavaScript Workflow

The browser code follows a simple flow:

1. read values from the form,
2. convert those values into query parameters,
3. call `fetch()`,
4. validate the HTTP response,
5. parse the JSON,
6. render the result into the DOM,
7. show the raw JSON in a preview panel.

Important functions:

- `buildApiBase()` normalizes the server URL,
- `buildProductsUrl()` constructs the GET request URL,
- `fetchJson()` performs the request and handles HTTP errors,
- `loadMetadata()` loads dropdown choices,
- `loadProducts()` loads the paginated list,
- `loadSingleProduct()` loads one product by ID,
- `renderProducts()` converts objects into cards,
- `renderStats()` updates the stat cards,
- `renderPagination()` updates page controls,
- `initializePage()` wires everything together.

## Query Parameter Examples

These examples show what the server understands and what the browser can generate.

### Text search

```text
/api/products?search=coffee
```

### Category filter

```text
/api/products?category=Kitchen
```

### Brand filter

```text
/api/products?brand=MotionCore
```

### Price range

```text
/api/products?min_price=30&max_price=100
```

### Minimum rating

```text
/api/products?min_rating=4.5
```

### In-stock only

```text
/api/products?in_stock=true
```

### Sorting

```text
/api/products?sort_by=price&sort_dir=desc
```

### Pagination

```text
/api/products?page=2&page_size=4
```

### Combined filter

```text
/api/products?search=wireless&category=Electronics&min_rating=4&sort_by=rating&sort_dir=desc&page=1&page_size=5
```

That last example is the most realistic one. Real APIs often combine multiple filters at once.

## Data Shape

Each product in the sample dataset contains:

- `id`
- `name`
- `category`
- `brand`
- `price`
- `rating`
- `stock`
- `color`
- `description`

That variety is useful because it lets the demo show different kinds of filtering:

- exact match,
- text search,
- numeric range,
- boolean condition,
- sorting by numeric and string fields.

## Running The Project

### 1. Start the server

Open a terminal in the project folder and run:

```powershell
python server.py
```

The server will ask:

```text
Enter port to run the API on [8484]:
```

If you press Enter, it uses `8484`.

If you type another valid port, the server will use that port instead.

### 2. Open the browser page

Open `index.html` in your browser.

The page defaults to:

```text
http://localhost:8484
```

If your server is running on a different port, change the API base URL field in the page.

### 3. Try the controls

Use the controls on the left side to:

- change filters,
- change sort order,
- change page size,
- navigate between pages,
- load a single product by ID.

Watch the raw JSON preview panel to see exactly what the server returned.

## Example Learning Exercises

If you want to learn from the project instead of just running it, try these exercises:

1. Change the search text to `coffee` and inspect the URL generated by the browser.
2. Filter to `Electronics` and sort by `price` descending.
3. Set `page_size` to `4` and move through pages.
4. Load one product by ID and compare the raw JSON to the card view.
5. Open the browser devtools Network tab and inspect the request URL and response body.
6. Add a new product to the Python list and refresh the page to see the new item.

These exercises make the request/response loop concrete.

## Why The Code Uses Comments So Heavily

This is intentionally a learning project.

The comments are doing several jobs:

- explaining what each block does,
- explaining why the code exists,
- showing examples of how the API can be called,
- connecting the Python side to the browser side,
- clarifying the flow from user input to HTTP request to rendered output.

This style is not ideal for production code, but it is excellent for learning because it reduces the gap between reading the file and understanding the behavior.

## If You Want To Extend It

Natural extensions would be:

- add a POST endpoint to create a product,
- add a DELETE endpoint to remove a product,
- persist data to a JSON file,
- move the sample data into a separate module,
- add form validation messages in the browser,
- add a search debounce,
- add server-side fuzzy search,
- add a small test suite.

Those are all good follow-up steps after you understand the current GET-only version.

## Notes

- The project is safe to run locally.
- It uses no third-party Python packages.
- The API enables CORS so the browser page can call it directly.
- The dataset is small on purpose so you can see the full result set while learning.
