def extract_amazon(soup):
    item = soup.select_one('.s-result-item[data-component-type="s-search-result"]')
    if not item:
        return {"error": "No item found"}

    title = None
    for sel in [
        'a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal h2 span',
        'h2 a span',
        '.a-size-medium.a-color-base.a-text-normal'
    ]:
        tag = item.select_one(sel)
        if tag and tag.text.strip():
            title = tag.text.strip()
            break

    price = None
    for sel in ['span.a-offscreen', '.a-price-whole', '.price-characteristic', '.a-price-fraction']:
        tag = item.select_one(sel)
        if tag and tag.text.strip():
            price = tag.text.strip().replace('$', '').replace('..', '.').strip('.')
            break

    rating = None
    for sel in ['span.a-icon-alt', '.a-icon-star-small', '.a-icon-star']:
        tag = item.select_one(sel)
        if tag and tag.text.strip():
            rating = tag.text.strip()
            break

    reviews = None
    for sel in ['span.a-size-base.s-underline-text', '.a-size-small .a-link-normal', '.a-size-small.a-link-normal']:
        tag = item.select_one(sel)
        if tag and tag.text.strip():
            reviews = tag.text.strip()
            break

    image = None
    img_tag = item.select_one('img.s-image')
    if img_tag:
        image = img_tag.get('src')

    return {
        "title": title or "",
        "price": price or "",
        "rating": rating or "",
        "reviews": reviews or "",
        "image": image or ""
    }


def extract_walmart(soup):
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


def extract_bestbuy(soup):
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


def extract_newegg(soup):
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
