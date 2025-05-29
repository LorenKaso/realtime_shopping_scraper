import requests
from bs4 import BeautifulSoup

def scrape(site, query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    # 1. Walmart
    if site == "walmart":
        url = f"https://www.walmart.com/search/?query={query.replace(' ', '%20')}"
        response = requests.get(url, headers=headers)
        print("Status code:", response.status_code)
        print(response.text[:400])
        soup = BeautifulSoup(response.text, "html.parser")
        item = soup.select_one('div[data-item-id]')
        if not item:
            return {"error": "No item found"}
        title = item.select_one('a span')
        price = item.select_one('span[data-automation-id="product-price"]')
        rating = item.select_one('span[aria-label*="out of 5 Stars"]')
        reviews = item.select_one('span[class*="stars-reviews-count"]')
        return {
            "title": title.text.strip() if title else '',
            "price": price.text.strip() if price else '',
            "rating": rating.text.strip() if rating else '',
            "reviews": reviews.text.strip() if reviews else ''
        }

    # 2. Newegg
    elif site == "newegg":
        url = f"https://www.newegg.com/p/pl?d={query.replace(' ', '+')}"
        response = requests.get(url, headers=headers)
        print("Status code:", response.status_code)
        print(response.text[:400])
        soup = BeautifulSoup(response.text, "html.parser")
        item = soup.select_one('.item-cell')
        if not item:
            return {"error": "No item found"}
        title = item.select_one('.item-title')
        price = item.select_one('.price-current strong')
        rating = item.select_one('.item-rating .rating')
        reviews = item.select_one('.item-rating-num')
        return {
            "title": title.text.strip() if title else '',
            "price": price.text.strip() if price else '',
            "rating": rating['aria-label'] if rating and rating.has_attr('aria-label') else '',
            "reviews": reviews.text.strip('()') if reviews else ''
        }

    # 3. BestBuy
    elif site == "bestbuy":
        url = f"https://www.bestbuy.com/site/searchpage.jsp?st={query.replace(' ', '+')}"
        response = requests.get(url, headers=headers)
        print("Status code:", response.status_code)
        print(response.text[:400])
        soup = BeautifulSoup(response.text, "html.parser")
        item = soup.select_one('.sku-item')
        if not item:
            return {"error": "No item found"}
        title = item.select_one('.sku-header > a')
        price = item.select_one('.priceView-customer-price span')
        rating = item.select_one('.c-reviews-v4')
        reviews = item.select_one('.c-reviews-v4 span')
        return {
            "title": title.text.strip() if title else '',
            "price": price.text.strip() if price else '',
            "rating": rating.text.strip() if rating else '',
            "reviews": reviews.text.strip() if reviews else ''
        }

    # 4. Amazon
    elif site == "amazon":
        url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
        response = requests.get(url, headers=headers)
        print("Status code:", response.status_code)
        print(response.text[:400])
        soup = BeautifulSoup(response.text, "html.parser")
        item = soup.select_one('.s-result-item[data-component-type="s-search-result"]')
        if not item:
            return {"error": "No item found"}
        title = item.select_one('h2 a span')
        price_whole = item.select_one('.a-price-whole')
        price_fraction = item.select_one('.a-price-fraction')
        price = (price_whole.text.strip() if price_whole else '') + ('.' + price_fraction.text.strip() if price_fraction else '')
        rating = item.select_one('.a-icon-alt')
        reviews = item.select_one('.a-size-base')
        return {
            "title": title.text.strip() if title else '',
            "price": price.strip('.'),  # תסירי נקודה בודדת בסוף אם אין חלק עשרוני
            "rating": rating.text.strip() if rating else '',
            "reviews": reviews.text.strip() if reviews else ''
        }

    else:
        return {"error": "site not supported"}
