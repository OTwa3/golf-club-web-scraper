import requests
from bs4 import BeautifulSoup

def scrape_golfavenue(search_term, hand_filter="All", brand_filter=""):
    """
    Scrape GolfAvenue products using generated search URL.
    """
    BASE_URL = "https://www.golfavenue.ca/en/search"

    # Build URL path
    brand_term = brand_filter.replace(" ", "").lower() if brand_filter else ""
    search_term_clean = search_term.replace(" ", "").lower()
    hand_term = ""
    if hand_filter.lower() == "left hand":
        hand_term = "left-handed"
    elif hand_filter.lower() == "right hand":
        hand_term = "right-handed"

    path = f"{search_term_clean}"

    if (brand_term):
        path += f"/{brand_term}"
    if hand_term:
        path += f"/{hand_term}"

    url = f"{BASE_URL}/{path}?q={search_term.replace(' ', '+')}"
    print(f"Fetching URL: {url}")

    # Get page content
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print("Failed to fetch page")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    items = []

    # Find product tiles
    products = soup.select("div.product-item, div.product-tile")
    for prod in products:
        try:
            title_elem = prod.select_one("strong.product-item-name a")
            price_elem = prod.select_one("span.price-wrapper span.price")
            if not title_elem or not price_elem:
                continue

            title = title_elem.text.strip()
            link = title_elem["href"]
            price = price_elem.text.strip()

            items.append({
                "title": title,
                "price": price,
                "link": link,
                "source": "GolfAvenue"
            })
        except Exception:
            continue

    print(f"Total items scraped from GolfAvenue: {len(items)}")
    return items
