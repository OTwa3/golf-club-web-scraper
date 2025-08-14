import requests
from bs4 import BeautifulSoup
import time

# TODO: Fix scraping logic, currently not scraping all the results/correct results

def scrape_golfavenue(search_term, hand_filter="All", brand_filter=""):
    BASE_URL = "https://www.golfavenue.ca/en/search"

    if search_term.lower() == "irons":
        search_term = "individual-irons"
    elif search_term.lower() == "fairway woods":
        search_term = "fairway-woods"

    # Clean search terms
    brand_term = brand_filter.replace(" ", "").lower() if brand_filter else ""
    search_term_clean = search_term.replace(" ", "").lower()
    hand_term = ""
    if hand_filter.lower() == "left hand":
        hand_term = "left-handed"
    elif hand_filter.lower() == "right hand":
        hand_term = "right-handed"

    path = f"{search_term_clean}"
    if brand_term:
        path += f"/{brand_term}"
    if hand_term:
        path += f"/{hand_term}"

    all_items = []
    seen_urls = set()
    page = 1
    headers = {"User-Agent": "Mozilla/5.0"}

    while True:
        if page == 1:
            url = f"{BASE_URL}/{path}?q={search_term.replace(' ', '+')}"
        else:
            url = f"{BASE_URL}/{path}/page/{page}?q={search_term.replace(' ', '+')}"

        print(f"Fetching URL: {url}")
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Failed to fetch page {page}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        products = soup.select("div.product-item, div.product-tile")
        if not products:
            print(f"No more products found on page {page}. Ending scrape.")
            break

        new_items_count = 0
        for prod in products:
            try:
                title_elem = prod.select_one("strong.product-item-name a")
                price_elem = prod.select_one("span.price-wrapper span.price")
                if not title_elem or not price_elem:
                    continue

                title = title_elem.text.strip()
                link = title_elem["href"]
                price = price_elem.text.strip()

                # Stop if URL already seen
                if link in seen_urls:
                    print("Detected previously seen product. Ending scrape.")
                    return all_items
                seen_urls.add(link)
                new_items_count += 1

                all_items.append({
                    "title": title,
                    "price": price,
                    "link": link,
                    "source": "GolfAvenue"
                })
            except Exception:
                continue

        print(f"Page {page}: {new_items_count} new items scraped.")
        page += 1
        time.sleep(1)

    print(f"Total items scraped from GolfAvenue: {len(all_items)}")
    return all_items
