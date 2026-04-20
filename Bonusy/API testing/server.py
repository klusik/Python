"""
server.py

This file starts a very small HTTP server that exposes a GET-only JSON API.

The goal of this project is educational:
- keep everything in a single Python file,
- avoid external dependencies,
- show how query parameters work,
- show how routing works,
- show how a browser-based JavaScript page can talk to a Python API.

How to run:
1. Open a terminal in this folder.
2. Run: python server.py
3. When asked for a port, press Enter for the default (8484),
   or type another port number.
4. Open index.html in your browser.

The browser page will call this API using JavaScript fetch().
"""

# We use only Python standard-library modules so the project works out of the box.
# That keeps the project easy to run on any machine with Python installed.
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


# This is our in-memory "database".
# In a real application this data could come from:
# - a SQL database,
# - a NoSQL database,
# - a CSV file,
# - another external API.
# Here we keep the data inline because the learning goal is to focus on HTTP and GET requests.
# For learning purposes, a plain Python list of dictionaries is ideal,
# because it is easy to read and easy to filter.
PRODUCTS = [
    {
        "id": 1,
        "name": "TrailBlaze Backpack 24L",
        "category": "Outdoor",
        "brand": "PeakRiver",
        "price": 79.90,
        "rating": 4.7,
        "stock": 18,
        "color": "Forest Green",
        "description": "Compact hiking backpack with padded straps and rain cover.",
    },
    {
        "id": 2,
        "name": "CityTune Wireless Headphones",
        "category": "Electronics",
        "brand": "SoundMint",
        "price": 129.50,
        "rating": 4.4,
        "stock": 9,
        "color": "Black",
        "description": "Bluetooth over-ear headphones with noise reduction and long battery life.",
    },
    {
        "id": 3,
        "name": "BaristaPro Coffee Grinder",
        "category": "Kitchen",
        "brand": "HomeCraft",
        "price": 64.00,
        "rating": 4.2,
        "stock": 14,
        "color": "Silver",
        "description": "Burr grinder with multiple grind settings for espresso and filter coffee.",
    },
    {
        "id": 4,
        "name": "FlexDesk LED Monitor Lamp",
        "category": "Office",
        "brand": "BrightForm",
        "price": 42.75,
        "rating": 4.6,
        "stock": 25,
        "color": "White",
        "description": "USB-powered desk lamp with adjustable brightness and color temperature.",
    },
    {
        "id": 5,
        "name": "SprintFlow Running Shoes",
        "category": "Sports",
        "brand": "MotionCore",
        "price": 95.20,
        "rating": 4.8,
        "stock": 12,
        "color": "Blue",
        "description": "Lightweight road-running shoes with responsive foam cushioning.",
    },
    {
        "id": 6,
        "name": "Nord Glass Water Bottle",
        "category": "Lifestyle",
        "brand": "PureLoop",
        "price": 18.90,
        "rating": 4.1,
        "stock": 40,
        "color": "Clear",
        "description": "Reusable borosilicate glass bottle with silicone sleeve.",
    },
    {
        "id": 7,
        "name": "PixelNote Drawing Tablet",
        "category": "Electronics",
        "brand": "InkForge",
        "price": 149.99,
        "rating": 4.5,
        "stock": 6,
        "color": "Graphite",
        "description": "Creative pen tablet for sketching, notes, and basic photo editing.",
    },
    {
        "id": 8,
        "name": "ChefStone Frying Pan 28cm",
        "category": "Kitchen",
        "brand": "HomeCraft",
        "price": 36.40,
        "rating": 4.3,
        "stock": 22,
        "color": "Charcoal",
        "description": "Non-stick frying pan with heat-resistant handle and induction base.",
    },
    {
        "id": 9,
        "name": "Orbit Mini Projector",
        "category": "Electronics",
        "brand": "BrightForm",
        "price": 219.00,
        "rating": 4.0,
        "stock": 4,
        "color": "Gray",
        "description": "Portable projector for movies, presentations, and travel use.",
    },
    {
        "id": 10,
        "name": "Balance Cork Yoga Mat",
        "category": "Sports",
        "brand": "MotionCore",
        "price": 54.30,
        "rating": 4.9,
        "stock": 16,
        "color": "Natural",
        "description": "Eco-friendly yoga mat with cork top layer and anti-slip rubber base.",
    },
]


# These are the fields the client is allowed to sort by.
# Restricting allowed sort fields is good practice.
# Without this, a typo or unexpected field could cause confusing behavior.
# This also makes the server safer, because we do not blindly trust user input.
ALLOWED_SORT_FIELDS = {"id", "name", "category", "brand", "price", "rating", "stock", "color"}


def first_value(query_dict, key, default=""):
    """
    Helper for reading query parameters.

    parse_qs() returns values in the form:
        {"category": ["Electronics"], "page": ["2"]}

    Even though we expect one value most of the time,
    parse_qs stores it inside a list.

    This helper makes the calling code much cleaner:
    instead of query_dict.get("page", ["1"])[0]
    we can write:
        first_value(query_dict, "page", "1")
    """
    # Query string values are stored as lists, so we take the first entry.
    return query_dict.get(key, [default])[0]


def try_parse_float(value, fallback=None):
    """
    Convert text to float safely.

    If conversion fails, return the fallback value instead of crashing.
    This lets the server handle bad input more gracefully.
    """
    # A failed conversion should not crash the server.
    # Returning a fallback lets the handler continue with a sensible default.
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def try_parse_int(value, fallback=None):
    """
    Convert text to integer safely.

    Again, we return a fallback instead of throwing an exception.
    """
    # The same safety rule applies to integers.
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def product_matches(product, filters):
    """
    Return True if a product matches all requested filters.

    The front-end will send many possible query parameters.
    For example:
        /api/products?category=Electronics&min_price=50&search=tablet

    We apply those one by one.
    """
    # Pull filter values into local variables so the checks read clearly.
    search_text = filters["search"]
    category = filters["category"]
    brand = filters["brand"]
    min_price = filters["min_price"]
    max_price = filters["max_price"]
    min_rating = filters["min_rating"]
    in_stock = filters["in_stock"]

    # Text search:
    # We compare against multiple fields so users can find products by
    # name, description, brand, category, or color.
    # Search is a broad, user-friendly text check.
    # We intentionally search multiple fields so the demo feels practical.
    if search_text:
        haystack = " ".join(
            [
                product["name"],
                product["description"],
                product["brand"],
                product["category"],
                product["color"],
            ]
        ).lower()
        if search_text not in haystack:
            return False

    # Exact category match, case-insensitive.
    # These checks are exact matches, but case-insensitive.
    if category and product["category"].lower() != category:
        return False

    # Exact brand match, case-insensitive.
    if brand and product["brand"].lower() != brand:
        return False

    # Numeric filters.
    # Price range filtering is a classic GET query parameter use case.
    if min_price is not None and product["price"] < min_price:
        return False

    if max_price is not None and product["price"] > max_price:
        return False

    if min_rating is not None and product["rating"] < min_rating:
        return False

    # Boolean filter:
    # If the client asks for in_stock=true, we only keep products with stock > 0.
    # Boolean filters are often represented as text in the query string.
    # Here we interpret "true" as "only show items with stock remaining".
    if in_stock and product["stock"] <= 0:
        return False

    return True


def build_stats(products):
    """
    Build summary information about the currently filtered products.

    This is useful because APIs often return both:
    - raw records,
    - summary metadata about those records.
    """
    # When nothing matches, we return a stable empty payload.
    # That keeps the client code simple because it can still render the same shape.
    if not products:
        return {
            "count": 0,
            "average_price": 0,
            "average_rating": 0,
            "total_stock": 0,
            "cheapest_product": None,
            "most_expensive_product": None,
        }

    # These aggregations are deliberately simple so the learning path stays clear.
    total_price = sum(product["price"] for product in products)
    total_rating = sum(product["rating"] for product in products)
    total_stock = sum(product["stock"] for product in products)
    cheapest = min(products, key=lambda product: product["price"])
    most_expensive = max(products, key=lambda product: product["price"])

    return {
        "count": len(products),
        "average_price": round(total_price / len(products), 2),
        "average_rating": round(total_rating / len(products), 2),
        "total_stock": total_stock,
        "cheapest_product": {
            "id": cheapest["id"],
            "name": cheapest["name"],
            "price": cheapest["price"],
        },
        "most_expensive_product": {
            "id": most_expensive["id"],
            "name": most_expensive["name"],
            "price": most_expensive["price"],
        },
    }


class ProductApiHandler(BaseHTTPRequestHandler):
    """
    Request handler class.

    BaseHTTPRequestHandler creates one handler object per request.
    Our job is to override methods like do_GET() and decide how each URL behaves.
    """

    server_version = "LearningProductApi/1.0"

    def end_headers(self):
        """
        Add CORS headers before finishing the response headers.

        Why this matters:
        - If you open index.html directly from disk, it will usually have a "null" origin.
        - If the API is on http://localhost:8484 and the page is opened another way,
          the browser may treat that as cross-origin.

        By allowing all origins here, the browser is allowed to call the API.
        This is fine for a small local-learning project.
        """
        # CORS headers allow the HTML page to call this API from the browser.
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def log_message(self, format_text, *args):
        """
        Customize terminal logging.

        The default log format is OK, but this version is a bit easier to read.
        """
        # BaseHTTPRequestHandler logs to stderr by default.
        # This custom format makes the terminal output easier to scan.
        print(f"[HTTP] {self.address_string()} - {format_text % args}")

    def do_OPTIONS(self):
        """
        Respond to CORS preflight requests.

        Our page mainly uses GET requests, but supporting OPTIONS is still a good example.
        """
        # OPTIONS is often used by browsers as a preflight check.
        # We do not need a body here, so 204 No Content is appropriate.
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        """
        Main GET router.

        A router decides which code runs for each path.
        Example paths:
        - /
        - /api
        - /api/products
        - /api/products/3
        - /api/categories
        - /api/brands
        - /api/stats
        """
        # Parse the path once, then route based on the clean path and query string.
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        # The root path is a small self-description page in JSON form.
        # This is helpful when you test the API directly in a browser.
        if path == "/":
            self.respond_json(
                200,
                {
                    "message": "Python GET API is running.",
                    "hint": "Open index.html in your browser and point it to this server.",
                    "available_endpoints": [
                        "/api",
                        "/api/products",
                        "/api/products/<id>",
                        "/api/categories",
                        "/api/brands",
                        "/api/stats",
                    ],
                },
            )
            return

        # Each path gets its own handler so the code stays easy to read.
        if path == "/api":
            self.handle_api_info()
            return

        if path == "/api/products":
            self.handle_products_list(query)
            return

        # This route handles detail lookup, like /api/products/3.
        if path.startswith("/api/products/"):
            self.handle_single_product(path)
            return

        if path == "/api/categories":
            self.handle_categories()
            return

        if path == "/api/brands":
            self.handle_brands()
            return

        if path == "/api/stats":
            self.handle_stats(query)
            return

        # If no route matched, we return a standard 404 response.
        self.respond_json(
            404,
            {
                "error": "Not found",
                "path": path,
            },
        )

    def handle_api_info(self):
        """
        Return documentation-like information for the API.

        This teaches the idea that an API can expose self-description.
        """
        # This endpoint acts like built-in documentation for the demo API.
        self.respond_json(
            200,
            {
                "name": "Learning Product API",
                "version": "1.0",
                "method": "GET only",
                "endpoints": {
                    "/api/products": {
                        "description": "List products with filtering, sorting, and pagination.",
                        "query_parameters": {
                            "search": "Text search in name/description/category/brand/color",
                            "category": "Exact category match",
                            "brand": "Exact brand match",
                            "min_price": "Minimum price",
                            "max_price": "Maximum price",
                            "min_rating": "Minimum rating",
                            "in_stock": "true or false",
                            "sort_by": "id, name, category, brand, price, rating, stock, color",
                            "sort_dir": "asc or desc",
                            "page": "Page number, starting at 1",
                            "page_size": "Number of items per page",
                        },
                    },
                    "/api/products/<id>": "Get one product by numeric id",
                    "/api/categories": "Get unique category values",
                    "/api/brands": "Get unique brand values",
                    "/api/stats": "Get summary statistics for the filtered result set",
                },
                "examples": [
                    "/api/products",
                    "/api/products?category=Electronics",
                    "/api/products?search=coffee&sort_by=price&sort_dir=desc",
                    "/api/products?brand=HomeCraft&min_price=30&max_price=80",
                    "/api/products/3",
                    "/api/stats?category=Sports",
                ],
            },
        )

    def handle_products_list(self, query):
        """
        Return the main list endpoint.

        This endpoint demonstrates the most common GET API patterns:
        - reading query parameters,
        - filtering records,
        - sorting records,
        - paginating records,
        - returning metadata along with the data.
        """
        # Convert raw query-string text into a normalized filter dictionary.
        filters = {
            "search": first_value(query, "search", "").strip().lower(),
            "category": first_value(query, "category", "").strip().lower(),
            "brand": first_value(query, "brand", "").strip().lower(),
            "min_price": try_parse_float(first_value(query, "min_price", "")),
            "max_price": try_parse_float(first_value(query, "max_price", "")),
            "min_rating": try_parse_float(first_value(query, "min_rating", "")),
            "in_stock": first_value(query, "in_stock", "").strip().lower() == "true",
        }

        # Sorting and pagination settings also come from the URL.
        sort_by = first_value(query, "sort_by", "id").strip()
        sort_dir = first_value(query, "sort_dir", "asc").strip().lower()
        page = try_parse_int(first_value(query, "page", "1"), 1)
        page_size = try_parse_int(first_value(query, "page_size", "50"), 50)

        # Defensive defaults keep the API stable even when the client sends bad input.
        # Reject unsupported sort columns by falling back to a safe default.
        if sort_by not in ALLOWED_SORT_FIELDS:
            sort_by = "id"

        if sort_dir not in {"asc", "desc"}:
            sort_dir = "asc"

        if page is None or page < 1:
            page = 1

        # We intentionally cap the maximum page size so the client cannot request
        # an absurdly large response.
        # Page size is capped so one request cannot ask for too much data.
        if page_size is None or page_size < 1:
            page_size = 5
        page_size = min(page_size, 100)

        # Step 1: filter.
        # Filtering happens first, before sorting and paging.
        filtered_products = [product for product in PRODUCTS if product_matches(product, filters)]

        # Step 2: sort.
        reverse = sort_dir == "desc"
        # Sorting is applied to the filtered result set only.
        filtered_products.sort(key=lambda product: product[sort_by], reverse=reverse)

        # Step 3: paginate.
        total_items = len(filtered_products)
        # Pagination is just slicing a list.
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paged_products = filtered_products[start_index:end_index]

        # total_pages is calculated in a way that avoids importing math.ceil().
        total_pages = (total_items + page_size - 1) // page_size if total_items else 1

        self.respond_json(
            200,
            {
                "filters_used": {
                    "search": filters["search"],
                    "category": filters["category"],
                    "brand": filters["brand"],
                    "min_price": filters["min_price"],
                    "max_price": filters["max_price"],
                    "min_rating": filters["min_rating"],
                    "in_stock": filters["in_stock"],
                    "sort_by": sort_by,
                    "sort_dir": sort_dir,
                    "page": page,
                    "page_size": page_size,
                },
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_items": total_items,
                    "total_pages": total_pages,
                    "has_previous_page": page > 1,
                    "has_next_page": page < total_pages,
                },
                "stats_for_filtered_set": build_stats(filtered_products),
                "items": paged_products,
            },
        )

    def handle_single_product(self, path):
        """
        Return one product based on the numeric id in the URL path.

        Example:
            /api/products/7
        """
        # Split the path and take the last segment.
        # "/api/products/7" -> "7"
        # Split once from the right so only the final path segment is treated as the id.
        product_id_text = path.rsplit("/", 1)[-1]
        product_id = try_parse_int(product_id_text)

        if product_id is None:
            self.respond_json(
                400,
                {
                    "error": "Product id must be a number.",
                    "received": product_id_text,
                },
            )
            return

        # Linear search is perfectly fine for a tiny learning dataset.
        for product in PRODUCTS:
            if product["id"] == product_id:
                self.respond_json(200, product)
                return

        self.respond_json(
            404,
            {
                "error": "Product not found.",
                "requested_id": product_id,
            },
        )

    def handle_categories(self):
        """
        Return distinct category values.

        This is useful for building filter dropdowns on the client.
        """
        # A set removes duplicates; sorting makes the output stable and pleasant to read.
        categories = sorted({product["category"] for product in PRODUCTS})
        self.respond_json(
            200,
            {
                "count": len(categories),
                "items": categories,
            },
        )

    def handle_brands(self):
        """
        Return distinct brand values.
        """
        # Same pattern as categories, just with a different field.
        brands = sorted({product["brand"] for product in PRODUCTS})
        self.respond_json(
            200,
            {
                "count": len(brands),
                "items": brands,
            },
        )

    def handle_stats(self, query):
        """
        Return stats for the filtered result set.

        This endpoint reuses the same filter logic as /api/products.
        That is a good design habit: keep behavior consistent between endpoints.
        """
        # The stats endpoint uses the same filters as the list endpoint.
        # Reusing the logic keeps the API behavior consistent.
        filters = {
            "search": first_value(query, "search", "").strip().lower(),
            "category": first_value(query, "category", "").strip().lower(),
            "brand": first_value(query, "brand", "").strip().lower(),
            "min_price": try_parse_float(first_value(query, "min_price", "")),
            "max_price": try_parse_float(first_value(query, "max_price", "")),
            "min_rating": try_parse_float(first_value(query, "min_rating", "")),
            "in_stock": first_value(query, "in_stock", "").strip().lower() == "true",
        }

        filtered_products = [product for product in PRODUCTS if product_matches(product, filters)]

        self.respond_json(
            200,
            {
                "filters_used": filters,
                "stats": build_stats(filtered_products),
            },
        )

    def respond_json(self, status_code, data):
        """
        Send a JSON response to the client.

        Every JSON response needs:
        - an HTTP status code,
        - a Content-Type header,
        - the JSON body encoded as bytes.
        """
        # indent=2 makes manual browser testing easier because the output is readable.
        response_text = json.dumps(data, indent=2)
        response_bytes = response_text.encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)


def ask_port():
    """
    Ask the user which port to use.

    Requirements from the task:
    - the server should ask for a port,
    - default should be 8484.
    """
    default_port = 8484

    # We loop until the user enters a valid port.
    while True:
        user_text = input(f"Enter port to run the API on [{default_port}]: ").strip()

        # If the user just presses Enter, we use the default port.
        # Empty input means "use the default".
        if user_text == "":
            return default_port

        parsed_port = try_parse_int(user_text)

        # Valid TCP ports are in the range 1..65535.
        # A real TCP port must be in the valid range.
        if parsed_port is not None and 1 <= parsed_port <= 65535:
            return parsed_port

        print("Invalid port. Please enter a number between 1 and 65535, or press Enter for 8484.")


def main():
    """
    Program entry point.
    """
    # First we ask for configuration, then we start the server.
    port = ask_port()
    server_address = ("", port)
    httpd = ThreadingHTTPServer(server_address, ProductApiHandler)

    print()
    print(f"API server is running on http://localhost:{port}")
    print("You can test it with these URLs:")
    print(f"  http://localhost:{port}/api")
    print(f"  http://localhost:{port}/api/products")
    print(f"  http://localhost:{port}/api/products?category=Electronics")
    print(f"  http://localhost:{port}/api/products?search=coffee&sort_by=price&sort_dir=desc")
    print(f"  http://localhost:{port}/api/stats?category=Sports")
    print()
    print("Open index.html in your browser and use the controls there.")
    print("Press Ctrl+C in this terminal to stop the server.")
    print()

    # serve_forever() blocks until the user interrupts the program.
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    finally:
        httpd.server_close()


# This condition ensures main() runs only when the file is executed directly.
# If somebody imports this file as a module later, the server will not auto-start.
if __name__ == "__main__":
    main()
