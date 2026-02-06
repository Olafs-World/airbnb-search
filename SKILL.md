---
name: airbnb-search
description: Search Airbnb listings from the command line. Use when you need to find vacation rentals, check prices, or help with travel planning. Supports location search, date filtering, price limits, guest counts, and room types. No API key required.
---

# Airbnb Search

Search Airbnb listings via CLI. No browser automation, no API key.

## Installation

```bash
uvx airbnb-search "Denver, CO"  # one-off
uv tool install airbnb-search   # persistent
```

## Usage

```bash
# Basic search
airbnb-search "Steamboat Springs, CO"

# With dates and filters
airbnb-search "Winter Park, CO" \
  --checkin 2026-03-15 \
  --checkout 2026-03-17 \
  --max-price 400 \
  --min-bedrooms 2

# JSON output for parsing
airbnb-search "Aspen, CO" --format json
```

## Options

| Flag | Description |
|------|-------------|
| `--checkin` | Check-in date (YYYY-MM-DD) |
| `--checkout` | Check-out date (YYYY-MM-DD) |
| `--max-price` | Maximum total price |
| `--min-price` | Minimum total price |
| `--min-bedrooms` | Minimum bedrooms |
| `--min-bathrooms` | Minimum bathrooms |
| `--guests` | Number of guests |
| `--room-type` | entire_home, private_room, shared_room |
| `--superhost` | Only superhosts |
| `--format` | Output format: pretty (default), json, csv |
| `--limit` | Max results to return |

## Python API

```python
from airbnb_search import search_airbnb

results = search_airbnb(
    location="Denver, CO",
    checkin="2026-03-01",
    checkout="2026-03-03",
    max_price=300
)

for listing in results["listings"]:
    print(f"{listing['name']}: ${listing['total_price']}")
    print(f"  {listing['url']}")
```

## Links

- PyPI: https://pypi.org/project/airbnb-search/
- GitHub: https://github.com/Olafs-World/airbnb-search
