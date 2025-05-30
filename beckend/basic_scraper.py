import requests
from bs4 import BeautifulSoup
import time
import random
from sites import extract_amazon, extract_bestbuy, extract_walmart, extract_newegg

def fetch_html_requests(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.text
    except Exception as e:
        return None

def fetch_html_selenium(url):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    options = Options()
    options.headless = True
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(random.uniform(2, 5))
        driver.delete_all_cookies()
        time.sleep(random.uniform(1, 2))
        scrolls = random.randint(1,3)
        for _ in range(scrolls):
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(random.uniform(1, 2))
        time.sleep(random.uniform(2, 4))
        html = driver.page_source
        return html
    except Exception as e:
        return None
    finally:
        driver.quit()

def scrape(site, query, use_selenium=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    if site == "amazon":
        url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
    elif site == "walmart":
        url = f"https://www.walmart.com/search/?query={query.replace(' ', '%20')}"
    elif site == "bestbuy":
        url = f"https://www.bestbuy.com/site/searchpage.jsp?st={query.replace(' ', '+')}"
    elif site == "newegg":
        url = f"https://www.newegg.com/p/pl?d={query.replace(' ', '+')}"
    else:
        return {"error": "Site not supported"}

    if use_selenium:
        html = fetch_html_selenium(url)
    else:
        html = fetch_html_requests(url, headers)

    if not html:
        return {"error": "Failed to fetch page"}

    soup = BeautifulSoup(html, "html.parser")

    # בדיקה בסיסית לקאפצ'ה
    if "captcha" in soup.text.lower() or "are you human" in soup.text.lower():
        return {"error": "Blocked by captcha"}

    # שליחה לניתוח לפי האתר
    if site == "amazon":
        return extract_amazon(soup)
    elif site == "walmart":
        return extract_walmart(soup)
    elif site == "bestbuy":
        return extract_bestbuy(soup)
    elif site == "newegg":
        return extract_newegg(soup)
    else:
        return {"error": "Site not supported"}

if __name__ == "__main__":
    print(scrape("amazon", "Lenovo Tab P12-2024", use_selenium=True))
    print(scrape("walmart", "iPhone", use_selenium=False))
    print(scrape("bestbuy", "Samsung TV", use_selenium=True))
    print(scrape("newegg", "RTX 3070", use_selenium=False))
