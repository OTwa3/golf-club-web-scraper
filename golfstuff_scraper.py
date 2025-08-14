import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

def scrape_golfstuff(search_term):
    BASE_URL = "https://justgolfstuff.ca/collections/drivers?pf_opt_hand=Left+Hand"
    #search_url = f"{BASE_URL}?term={search_term.replace(' ', '+')}"
    search_url = BASE_URL

    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")

    driver = uc.Chrome(options=options)
    driver.get(search_url)

    wait = WebDriverWait(driver, 15)

    # Close any popups if present
    try:
        close_btn = driver.find_element(By.XPATH, "//div[@aria-label='Close']")
        close_btn.click()
        time.sleep(1)
    except:
        pass
    

    # Wait for product tiles to load
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-item")))
    except:
        print("No products found or page took too long to load.")
        driver.quit()
        return []

    products = driver.find_elements(By.CSS_SELECTOR, "div.product-item")

    items = []
    for prod in products:
        try:
            # Title and link
            title_elem = prod.find_element(By.CSS_SELECTOR, "a.product-item__title")
            link = title_elem.get_attribute("href")
            title = title_elem.text.strip()

            # Price (take sale price if available)
            try:
                price_elem = prod.find_element(By.CSS_SELECTOR, "span.price--highlight")
            except:
                price_elem = prod.find_element(By.CSS_SELECTOR, "span.price--regular")
            price = price_elem.text.strip()

            items.append({
                "title": title,
                "price": price,
                "link": "https://justgolfstuff.ca" + link if link.startswith("/") else link,
                "source": "JustGolfStuff"
            })
        except Exception:
            continue

    driver.quit()
    print(f"\nTotal items scraped from Just Golf Stuff: {len(items)}")
    return items

