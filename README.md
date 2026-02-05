# airbnb-search 🏠

Search Airbnb listings from the command line. No API key required.

## Installation

```bash
pip install airbnb-search
```

## Usage

### Command Line

```bash
# Basic search
airbnb-search "Steamboat Springs, CO"

# With dates and filters
airbnb-search "Winter Park, CO" --checkin 2026-02-27 --checkout 2026-03-01 --max-price 400

# JSON output
airbnb-search "Denver, CO" --format json
```

### Python API

```python
from airbnb_search import search_airbnb, parse_listings

# Search
data = search_airbnb(
    query="Steamboat Springs, CO",
    checkin="2026-02-27",
    checkout="2026-03-01",
    max_price=500
)

# Parse results
result = parse_listings(data)

for listing in result['listings']:
    print(f"{listing['name']} - {listing['total_price']}")
    print(f"  {listing['url']}")
```

## Features

- 🔍 Search by location, dates, price range, and bedrooms
- 💰 Get actual total prices (not per-night)
- ⭐ See ratings, reviews, and superhost status
- 🔗 Direct links to listings
- 📊 Table or JSON output
- 🚀 No API key required

## Options

| Flag | Description |
|------|-------------|
| `--checkin`, `-i` | Check-in date (YYYY-MM-DD) |
| `--checkout`, `-o` | Check-out date (YYYY-MM-DD) |
| `--min-price` | Minimum price |
| `--max-price` | Maximum price |
| `--min-bedrooms` | Minimum bedrooms |
| `--limit` | Max results (default: 50) |
| `--format`, `-f` | Output format: table or json |

## License

MIT

---

Made with 🌿 by [Olaf](https://olafs-world.vercel.app)
