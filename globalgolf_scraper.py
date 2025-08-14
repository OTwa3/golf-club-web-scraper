import requests
from bs4 import BeautifulSoup
import time

BRAND_MAP = {
    "taylormade": 27,
    "callaway": 4,
    "cleveland": 6,
    "mizuno": 13,
    "ping": 20,
    "cobra": 7,
    "titleist": 29,
    "krank": 486,
    "srixon": 25,
    "xxio": 1051,
    "pxg" : 1130
}

def get_brand_id(brand_name):
    if not brand_name:
        return None
    return BRAND_MAP.get(brand_name.lower())

def scrape_globalgolf(search_term, hand_filter="All", brand_filter=""):
    BASE_URL = "https://www.globalgolf.ca/search/clubs/"
    page = 1
    all_items = []
    seen_urls = set()
    headers = {"User-Agent": "Mozilla/5.0"}

    while True:
        params = {"term": search_term, "pg": page}

        # Hand filter
        if hand_filter.lower() == "left hand":
            params["dxt"] = "1"
        elif hand_filter.lower() == "right hand":
            params["dxt"] = "2"

        # Brand filter
        brand_id = get_brand_id(brand_filter)
        if brand_id:
            params["bid"] = str(brand_id)

        resp = requests.get(BASE_URL, params=params, headers=headers)
        if resp.status_code != 200:
            print(f"Failed to fetch page {page}")
            break

        print(f"Fetching URL: {resp.url}")
        soup = BeautifulSoup(resp.text, "html.parser")
        products = soup.select("div.catprod.s-fit.con")
        if not products:
            print(f"No more products found on page {page}. Ending scrape.")
            break

        new_items_count = 0
        for prod in products:
            try:
                title_elem = prod.select_one("h3")
                price_elem = prod.select_one("button.price span:last-of-type")
                brand_elem = prod.select_one("div.mrg-10")
                link_elem = prod.select_one("a.gllrylnk")

                if not title_elem or not price_elem or not brand_elem or not link_elem:
                    continue

                title = f"{brand_elem.text.strip()} {title_elem.text.strip()}"
                price = price_elem.text.strip()
                link = link_elem["href"]

                if link in seen_urls:
                    print("Detected previously seen product. Ending scrape.")
                    return all_items
                seen_urls.add(link)
                new_items_count += 1

                all_items.append({
                    "title": title,
                    "price": price,
                    "link": link,
                    "source": "GlobalGolf"
                })
            except Exception:
                continue

        print(f"Page {page}: {new_items_count} new items scraped.")
        page += 1
        time.sleep(1)

    print(f"Total items scraped from GlobalGolf: {len(all_items)}")
    return all_items
