# import json
# import random
# import time
# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from urllib.parse import urljoin
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import csv

# def scrape_facebook_marketplace(search_term):
#     # --- CONFIG ---
#     COOKIE_FILE = "fb_cookies.json"
#     SEARCH_TERM = search_term
#     BASE_URL = "https://www.facebook.com/marketplace"
#     SCROLL_PAUSE = (2, 5)  # min/max seconds between scrolls
#     MAX_SCROLLS = 5

#     # --- START BROWSER ---
#     options = uc.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
#     driver = uc.Chrome(options=options)

#     # --- LOAD FACEBOOK MAIN PAGE FIRST ---
#     driver.get("https://www.facebook.com")
#     time.sleep(3)

#     # --- LOAD COOKIES ---
#     with open(COOKIE_FILE, "r") as f:
#         cookies = json.load(f)

#     for cookie in cookies:
#         try:
#             selenium_cookie = {
#                 'name': cookie['name'],
#                 'value': cookie['value'],
#                 'domain': cookie['domain'],
#                 'path': cookie.get('path', '/'),
#                 'secure': cookie.get('secure', False),
#                 'httpOnly': cookie.get('httpOnly', False),
#             }
#             if 'expiry' in cookie:
#                 selenium_cookie['expiry'] = int(cookie['expiry'])
#             elif 'expirationDate' in cookie:
#                 selenium_cookie['expiry'] = int(cookie['expirationDate'])
#             driver.add_cookie(selenium_cookie)
#         except Exception as e:
#             print(f"Error adding cookie {cookie.get('name')}: {e}")

#     # --- NOW NAVIGATE TO MARKETPLACE ---
#     driver.get(BASE_URL)
#     time.sleep(5)


#     # --- REFRESH WITH LOGGED-IN SESSION ---
#     driver.get(BASE_URL)
#     time.sleep(5)

#     # --- SEARCH ---
#     wait = WebDriverWait(driver, 15)

#     # Close any popups if present
#     try:
#         close_btn = driver.find_element(By.XPATH, "//div[@aria-label='Close']")
#         close_btn.click()
#         time.sleep(1)
#     except:
#         pass

#     search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search Marketplace']")))
#     driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
#     time.sleep(1)
#     search_box.clear()
#     search_box.send_keys(SEARCH_TERM)
#     search_box.send_keys(Keys.RETURN)

#     # --- SCROLL ---
#     for _ in range(MAX_SCROLLS):
#         driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
#         time.sleep(random.uniform(*SCROLL_PAUSE))

#     # --- SCRAPE RESULTS ---
#     results = driver.find_elements(By.XPATH, "//a[contains(@href, '/marketplace/item/')]")

#     items = []
#     for r in results:
#         try:
#             spans = r.find_elements(By.XPATH, ".//span[contains(@dir,'auto')]")
#             price = None
#             title = None

#             for span in spans:
#                 text = span.text.strip()
#                 if not text:
#                     continue
#                 if '$' in text or 'CA$' in text:
#                     price = text
#                 elif not title:
#                     # First span that doesn't look like a price is title
#                     title = text

#             link = urljoin(BASE_URL, r.get_attribute("href"))

#             if title and price and link:
#                 items.append({"title": title, "price": price, "link": link.split('?')[0], "source": "Marketplace"})
#         except Exception:
#             continue


#     print(f"\nTotal items scraped from fb marketplace: {len(items)}")
#     driver.quit()
#     return items
