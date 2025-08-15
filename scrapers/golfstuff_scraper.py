import requests
from bs4 import BeautifulSoup

# TODO: Fix scraping logic, currently not scraping all the results/correct results

def scrape_golfstuff(search_term, hand_filter="All", brand_filter=""):

    if search_term.lower() == "fairway woods":
        search_term = "woods"

    BASE_URL = f"https://justgolfstuff.ca/collections/{search_term.replace(' ', '+')}"

    # Build query params
    params = {}
    if hand_filter != "All":
        params["pf_opt_hand"] = hand_filter.replace(' ', '+')
    if brand_filter:
        params["pf_t_brand"] = brand_filter.replace(' ', '+')
        params["pf_t_brand_and_condition"] = "true"

    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(BASE_URL, params=params, headers=headers)
    if resp.status_code != 200:
        print(f"Failed to fetch page: {resp.url} with error {resp.status_code}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    items = []

    print(f"Fetching URL: {resp.url}")

    products = soup.select("div.product-item")
    for prod in products:
        try:

            title_elem = prod.select_one("a.product-item__title")
            price_elem = prod.select_one("span.price--highlight") or prod.select_one("span.price--regular")
            if not title_elem or not price_elem:
                continue

            title = title_elem.text.strip()

            # Check if brand_filter is in the title, if not skip
            if brand_filter and brand_filter.lower() not in title.lower():
                continue

            price = price_elem.text.strip()
            link = title_elem["href"]
            if link.startswith("/"):
                link = "https://justgolfstuff.ca" + link

            items.append({
                "title": title,
                "price": price,
                "link": link,
                "source": "JustGolfStuff"
            })
        except Exception:
            continue

    print(f"Total visible items scraped from Just Golf Stuff: {len(items)}")
    return items