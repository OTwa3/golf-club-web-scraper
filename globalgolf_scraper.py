import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

def scrape_globalgolf(search_term):
    BASE_URL = "https://www.globalgolf.ca/search/clubs/?dxt=1&"
    search_url = f"{BASE_URL}term={search_term.replace(' ', '+')}"


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
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.catprod.s-fit.con")))
    except:
        print("No products found or page took too long to load.")
        driver.quit()
        return []

    products = driver.find_elements(By.CSS_SELECTOR, "div.catprod.s-fit.con")

    items = []
    for prod in products:
        try:
            title_elem = prod.find_element(By.CSS_SELECTOR, "h3")
            used_price_elem = prod.find_element(By.CSS_SELECTOR, "button.price span:last-of-type")
            brand_elem = prod.find_element(By.CSS_SELECTOR, "div.mrg-10")
            link_elem = prod.find_element(By.CSS_SELECTOR, "a.gllrylnk")
            title = title_elem.text.strip()
            price = used_price_elem.text.strip()
            brand = brand_elem.text.strip()

            items.append({
                "title": brand + " " + title,
                "price": price,
                "link": link_elem.get_attribute("href"),
                "source": "GlobalGolf"
            })
        except Exception:
            continue

    driver.quit()
    print(f"\nTotal items scraped from GlobalGolf: {len(items)}")
    return items
