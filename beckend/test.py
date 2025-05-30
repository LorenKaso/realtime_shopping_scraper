from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
from bs4 import BeautifulSoup

def human_behavior_scrape_amazon(query):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    options = Options()
    options.headless = False  # רואה את הדפדפן! (להפוך ל-True אם לא רוצים לראות)
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    try:
        url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
        driver.get(url)
        time.sleep(random.uniform(2, 5))
        driver.delete_all_cookies()
        time.sleep(random.uniform(1, 2))
        scroll_times = random.randint(1, 3)
        for _ in range(scroll_times):
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(random.uniform(1, 2))
        time.sleep(random.uniform(2, 4))
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # בדיקה אם נחסמנו ע"י קאפצ’ה
        if "captcha" in soup.text.lower() or "are you human" in soup.text.lower():
            print("Blocked by captcha!")
            return {"error": "Blocked by captcha"}

        item = soup.select_one('.s-result-item[data-component-type="s-search-result"]')
        if item:
            print(item.prettify())
        else:
            print("No item found!")

        if not item:
            print("No item found.")
            return {"error": "No item found"}

        title = item.select_one('h2 a span')
        price_whole = item.select_one('.a-price-whole')
        price_fraction = item.select_one('.a-price-fraction')
        price = (price_whole.text.strip() if price_whole else '') + ('.' + price_fraction.text.strip() if price_fraction else '')
        rating = item.select_one('.a-icon-alt')
        reviews = item.select_one('.a-size-base')
        print("Title:", title.text.strip() if title else '')
        print("Price:", price.strip('.'))
        print("Rating:", rating.text.strip() if rating else '')
        print("Reviews:", reviews.text.strip() if reviews else '')
        return {
            "title": title.text.strip() if title else '',
            "price": price.strip('.'),
            "rating": rating.text.strip() if rating else '',
            "reviews": reviews.text.strip() if reviews else ''
        }

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}
    finally:
        driver.quit()

if __name__ == "__main__":
    # כאן תרשמי מוצר לבדיקה, לדוגמה:
    result = human_behavior_scrape_amazon("Lenovo Tab P12-2024")
    print(result)
