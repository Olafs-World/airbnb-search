#!/usr/bin/env python3
"""Search Airbnb listings from the command line. No API key required.

Usage:
    uv run --with requests scripts/airbnb-search.py "Steamboat Springs, CO" --checkin 2025-03-01 --checkout 2025-03-03
    python scripts/airbnb-search.py "Denver, CO" --checkin 2025-06-01 --checkout 2025-06-05 --json
"""

import argparse
import json
import sys

import requests

API_KEY = "d306zoyjsyarp7ifhu67rjxn52tv0t20"
API_URL = "https://www.airbnb.com/api/v3/ExploreSearch"


def search_airbnb(
    query,
    checkin=None,
    checkout=None,
    min_price=None,
    max_price=None,
    min_bedrooms=None,
    items_per_page=50,
    currency="USD",
):
    """Search Airbnb and return raw API results."""
    headers = {"x-airbnb-api-key": API_KEY}

    request_params = {
        "metadataOnly": False,
        "version": "1.7.9",
        "itemsPerGrid": items_per_page,
        "tabId": "home_tab",
        "refinementPaths": ["/homes"],
        "source": "structured_search_input_header",
        "searchType": "filter_change",
        "query": query,
        "cdnCacheSafe": False,
        "simpleSearchTreatment": "simple_search_only",
    }

    if checkin:
        request_params["checkin"] = checkin
    if checkout:
        request_params["checkout"] = checkout
    if min_price:
        request_params["priceMin"] = min_price
    if max_price:
        request_params["priceMax"] = max_price
    if min_bedrooms:
        request_params["minBedrooms"] = min_bedrooms

    variables = {"request": request_params}
    extensions = {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "13aa9971e70fbf5ab888f2a851c765ea098d8ae68c81e1f4ce06e2046d91b6ea",
        }
    }

    var_str = json.dumps(variables, separators=(",", ":"))
    ext_str = json.dumps(extensions, separators=(",", ":"))

    full_url = f"{API_URL}?operationName=ExploreSearch&locale=en&currency={currency}&variables={var_str}&extensions={ext_str}"

    response = requests.get(full_url, headers=headers)
    response.raise_for_status()
    return response.json()


def parse_listings(data):
    """Parse raw API response into clean listing data."""
    listings = []

    ev3 = data.get("data", {}).get("dora", {}).get("exploreV3", {})
    metadata = ev3.get("metadata", {})
    geography = metadata.get("geography", {})
    pagination = metadata.get("paginationMetadata", {})

    for section in ev3.get("sections", []):
        if section.get("__typename") != "DoraExploreV3ListingsSection":
            continue

        for item in section.get("items", []):
            listing = item.get("listing", {})
            pricing = item.get("pricingQuote", {})

            price_struct = pricing.get("structuredStayDisplayPrice", {})
            primary = price_struct.get("primaryLine", {})

            total_price = primary.get("discountedPrice") or primary.get("price", "")
            original_price = primary.get("originalPrice", "")
            qualifier = primary.get("qualifier", "")

            price_num = None
            if total_price:
                try:
                    price_num = int("".join(c for c in total_price if c.isdigit()))
                except ValueError:
                    pass

            listings.append(
                {
                    "id": listing.get("id"),
                    "name": listing.get("name"),
                    "url": f"https://airbnb.com/rooms/{listing.get('id')}",
                    "bedrooms": listing.get("bedrooms"),
                    "bathrooms": listing.get("bathrooms"),
                    "beds": listing.get("beds"),
                    "rating": listing.get("avgRating"),
                    "reviews_count": listing.get("reviewsCount"),
                    "room_type": listing.get("roomType"),
                    "property_type": listing.get("propertyType"),
                    "person_capacity": listing.get("personCapacity"),
                    "is_superhost": listing.get("isSuperhost"),
                    "city": listing.get("city") or geography.get("city"),
                    "lat": listing.get("lat"),
                    "lng": listing.get("lng"),
                    "total_price": total_price,
                    "total_price_num": price_num,
                    "original_price": original_price,
                    "price_qualifier": qualifier,
                    "can_instant_book": pricing.get("canInstantBook"),
                }
            )

    return {
        "listings": listings,
        "total_count": pagination.get("totalCount"),
        "has_next_page": pagination.get("hasNextPage"),
        "location": geography.get("fullAddress"),
    }


def print_listings(result, fmt="table"):
    """Print listings in specified format."""
    listings = result["listings"]

    if fmt == "json":
        print(json.dumps(result, indent=2))
        return

    print(f"\n📍 {result['location']}")
    print(f"📊 Found {result['total_count']} total listings\n")
    print("=" * 90)

    sorted_listings = sorted(
        [l for l in listings if l["total_price_num"]],
        key=lambda x: x["total_price_num"],
    )

    for listing in sorted_listings:
        name = listing["name"][:50] + "..." if len(listing["name"]) > 50 else listing["name"]
        rating = f"⭐{listing['rating']}" if listing["rating"] else "No rating"
        superhost = "🏆" if listing["is_superhost"] else ""

        print(f"{name} {superhost}")
        print(f"  {listing['bedrooms']}BR/{listing['bathrooms']}BA | {rating} | {listing['reviews_count'] or 0} reviews")
        print(f"  💰 {listing['total_price']} {listing['price_qualifier']}")
        if listing["original_price"]:
            print(f"     (was {listing['original_price']})")
        print(f"  🔗 {listing['url']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Search Airbnb listings from the command line",
        prog="airbnb-search",
    )
    parser.add_argument("query", help='Search location (e.g., "Steamboat Springs, CO")')
    parser.add_argument("--checkin", "-i", help="Check-in date (YYYY-MM-DD)")
    parser.add_argument("--checkout", "-o", help="Check-out date (YYYY-MM-DD)")
    parser.add_argument("--min-price", type=int, help="Minimum price")
    parser.add_argument("--max-price", type=int, help="Maximum price")
    parser.add_argument("--min-bedrooms", type=int, help="Minimum bedrooms")
    parser.add_argument("--limit", type=int, default=50, help="Max results (default: 50)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--format", "-f", choices=["table", "json"], default="table",
        help="Output format (default: table)",
    )

    args = parser.parse_args()

    if args.json:
        args.format = "json"

    try:
        data = search_airbnb(
            query=args.query,
            checkin=args.checkin,
            checkout=args.checkout,
            min_price=args.min_price,
            max_price=args.max_price,
            min_bedrooms=args.min_bedrooms,
            items_per_page=args.limit,
        )
        result = parse_listings(data)
        print_listings(result, args.format)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
