import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

def scrape_golfavenue(search_term):
    BASE_URL = "https://www.golfavenue.ca/en/search"
    search_url = f"{BASE_URL}?q={search_term.replace(' ', '+')}"
    
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
    
    driver = uc.Chrome(options=options)
    driver.get(search_url)

    wait = WebDriverWait(driver, 20)

    # Filter results to left-handed dexterity
    left_handed_checkbox = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(text(), 'Left-Handed')]")
    ))

    left_handed_checkbox.click()

    # Open product type dropdown
    dropdown_trigger = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.main-filter-laps-product-type[data-role='trigger']")
    ))
    dropdown_trigger.click()


    # Filter results to driver
    driver_checkbox = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(text(), 'Driver')]")
    ))

    driver_checkbox.click()

    # Wait for product tiles to load
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-item, div.product-tile")))
    except:
        print("No products found or page took too long to load.")
        driver.quit()
        return []
    
    wait = WebDriverWait(driver, 2)
    
    products = driver.find_elements(By.CSS_SELECTOR, "div.product-item, div.product-tile")

    # Extract product information
    items = []
    products = driver.find_elements(By.CSS_SELECTOR, "div.item.product")
    for prod in products:
        try:
            title_elem = prod.find_element(By.CSS_SELECTOR, "strong.product-item-name a")
            price_elem = prod.find_element(By.CSS_SELECTOR, "span.price-wrapper span.price")
            link = title_elem.get_attribute("href")
            title = title_elem.text.strip()
            price = price_elem.text.strip()
            items.append({
                "title": title,
                "price": price,
                "link": link,
                "source": "GolfAvenue"
            })
        except Exception:
            continue
    
    driver.quit()
    print(f"\nTotal items scraped from GolfAvenue: {len(items)}")
    return items