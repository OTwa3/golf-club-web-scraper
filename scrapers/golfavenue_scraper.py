import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import math

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

    headers = {"User-Agent": "Mozilla/5.0"}
    all_items = []
    seen_urls = set()

    # ---------- helper to scrape a single page ----------
    def scrape_page(page):
        url = (
            f"{BASE_URL}/{path}?q={search_term.replace(' ', '+')}"
            if page == 1
            else f"{BASE_URL}/{path}/page/{page}?q={search_term.replace(' ', '+')}"
        )

        print(f"Scraping page {page}: {url}")

        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Failed to fetch page {page}")
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        products = soup.select("div.product-item, div.product-tile")
        page_items = []

        for prod in products:
            try:
                title_elem = prod.select_one("strong.product-item-name a")
                price_elem = prod.select_one("span.price-wrapper span.price")
                if not title_elem or not price_elem:
                    continue

                title = title_elem.text.strip()
                link = title_elem["href"]
                price = price_elem.text.strip()

                if link in seen_urls:
                    continue

                seen_urls.add(link)
                page_items.append({
                    "title": title,
                    "price": price,
                    "link": link,
                    "source": "GolfAvenue"
                })
            except Exception:
                continue

        print(f"Page {page}: {len(page_items)} items scraped.")
        return page_items

       # ---------- fetch first page (to get total count) ----------
    first_page = scrape_page(1)
    all_items.extend(first_page)

    # find total results from toolbar-number
    try:
        soup_first = BeautifulSoup(
            requests.get(f"{BASE_URL}/{path}?q={search_term.replace(' ', '+')}", headers=headers).text,
            "html.parser"
        )
        number_elems = soup_first.select("span.toolbar-number")

        if not number_elems:
            total_results = len(first_page)
        elif len(number_elems) == 1:
            total_results = int(number_elems[0].text.strip())
        else:
            total_results = int(number_elems[-1].text.strip())

    except Exception:
        total_results = len(first_page)

    total_pages = math.ceil(total_results / 30)
    print(f"Total results: {total_results} → {total_pages} pages")


    # ---------- scrape remaining pages in parallel ----------
    if total_pages > 1:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(scrape_page, p) for p in range(2, total_pages + 1)]
            for future in as_completed(futures):
                all_items.extend(future.result())

    print(f"Total items scraped from GolfAvenue: {len(all_items)}")
    return all_items
