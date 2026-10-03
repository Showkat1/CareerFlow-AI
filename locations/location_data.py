
# CareerFlow AI location data
# Initial dataset for testing the hierarchical selector.

LOCATION_DATA = {
    "India": {
        "West Bengal": [
            "Kolkata",
            "Howrah",
            "Durgapur",
            "Siliguri",
        ],
        "Punjab": [
            "Ludhiana",
            "Mohali",
            "Amritsar",
            "Jalandhar",
            "Patiala",
        ],
        "Karnataka": [
            "Bengaluru",
            "Mysuru",
            "Mangaluru",
        ],
        "Maharashtra": [
            "Mumbai",
            "Pune",
            "Nagpur",
            "Nashik",
        ],
        "Telangana": [
            "Hyderabad",
            "Warangal",
        ],
        "Delhi": [
            "New Delhi",
        ],
    },
    "United States": {
        "California": [
            "San Francisco",
            "Los Angeles",
            "San Diego",
            "San Jose",
        ],
        "New York": [
            "New York City",
            "Buffalo",
            "Albany",
        ],
        "Texas": [
            "Austin",
            "Dallas",
            "Houston",
        ],
    },
    "United Kingdom": {
        "England": [
            "London",
            "Manchester",
            "Birmingham",
            "Leeds",
        ],
        "Scotland": [
            "Edinburgh",
            "Glasgow",
            "Aberdeen",
        ],
    },
}

SPECIAL_LOCATIONS = [
    "Remote",
    "Worldwide",
]


def get_countries():
    """Return available countries."""
    return sorted(LOCATION_DATA.keys())


def get_regions(country):
    """Return regions available for a country."""
    return sorted(LOCATION_DATA.get(country, {}).keys())


def get_cities(country, region):
    """Return cities available for a region."""
    return sorted(
        LOCATION_DATA.get(country, {}).get(region, [])
    )