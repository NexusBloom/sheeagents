import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random

def get_headers():
    \"\"\"Rotate user agents to avoid blocking\"\"\"
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
    ]
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }

def search_jumia_api(query):
    \"\"\"Try Jumia API first\"\"\"
    try:
        # Jumia search API
        url = f\"https://www.jumia.co.ke/catalog/?q={query.replace(' ', '+')}&page=1\"
        
        session = requests.Session()
        session.headers.update(get_headers())
        
        # Add cookies to seem more human
        session.cookies.set('country', 'KE')
        session.cookies.set('currency', 'KES')
        
        response = session.get(url, timeout=30, allow_redirects=True)
        
        if response.status_code != 200:
            print(f\"Jumia returned status {response.status_code}\")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        
        # Multiple selectors for product containers
        selectors = [
            'article.prd._fb.col.c-prd',
            'article.prd',
            '[data-sku]',
            '.-paxs .row .c-prd'
        ]
        
        items = []
        for selector in selectors:
            items = soup.select(selector)
            if items:
                print(f\"Jumia: Found {len(items)} items with selector: {selector}\")
                break
        
        for item in items[:15]:
            try:
                # Name
                name_elem = item.select_one('h3.name, .title, div.name')
                name = name_elem.get_text(strip=True) if name_elem else None
                
                # Price
                price_elem = item.select_one('div.prc, .price, [data-price]')
                price = price_elem.get_text(strip=True) if price_elem else None
                
                # Image
                img_elem = item.select_one('img')
                image = ''
                if img_elem:
                    image = img_elem.get('data-src') or img_elem.get('src', '')
                    if image.startswith('//'):
                        image = 'https:' + image
                
                # Link
                link_elem = item.select_one('a.core[href], a[href]')
                link = ''
                if link_elem and link_elem.get('href'):
                    href = link_elem['href']
                    link = 'https://www.jumia.co.ke' + href if href.startswith('/') else href
                
                if name and price:
                    products.append({
                        'name': name,
                        'price': price,
                        'image': image,
                        'link': link,
                        'source': 'Jumia'
                    })
            except Exception as e:
                continue
        
        return products
        
    except Exception as e:
        print(f\"Jumia error: {e}\")
        return []

def search_kilimall_api(query):
    \"\"\"Try Kilimall API\"\"\"
    try:
        # Try multiple Kilimall endpoints
        endpoints = [
            f\"https://www.kilimall.co.ke/api/search?q={query}&page=1&perPage=20\",
            f\"https://www.kilimall.co.ke/api/v2/search?keyword={query}&page=1&size=20\"
        ]
        
        session = requests.Session()
        session.headers.update(get_headers())
        session.headers.update({
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        })
        
        for url in endpoints:
            try:
                response = session.get(url, timeout=30)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        products = []
                        
                        # Handle different API response structures
                        items = []
                        if 'data' in data and 'products' in data['data']:
                            items = data['data']['products']
                        elif 'data' in data and 'list' in data['data']:
                            items = data['data']['list']
                        elif 'products' in data:
                            items = data['products']
                        
                        for item in items[:15]:
                            try:
                                name = item.get('name') or item.get('title', 'Unknown')
                                price = item.get('price', 'N/A')
                                if isinstance(price, (int, float)):
                                    price = f\"KES {price}\"
                                
                                image = item.get('image') or item.get('thumbnail', '')
                                slug = item.get('slug') or item.get('id', '')
                                link = f\"https://www.kilimall.co.ke/product/{slug}\" if slug else ''
                                
                                products.append({
                                    'name': name,
                                    'price': price,
                                    'image': image,
                                    'link': link,
                                    'source': 'Kilimall'
                                })
                            except:
                                continue
                        
                        if products:
                            print(f\"Kilimall API success: {len(products)} products\")
                            return products
                    except:
                        continue
            except:
                continue
        
        # Fallback to HTML scraping
        return search_kilimall_html(query, session)
        
    except Exception as e:
        print(f\"Kilimall API error: {e}\")
        return []

def search_kilimall_html(query, session=None):
    \"\"\"Fallback HTML scraping for Kilimall\"\"\"
    try:
        if not session:
            session = requests.Session()
            session.headers.update(get_headers())
        
        url = f\"https://www.kilimall.co.ke/search?q={query.replace(' ', '+')}\"
        response = session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        
        # Try multiple selectors
        selectors = [
            'div.product-item',
            'div.goods-item',
            '.product-list .item',
            '[data-product-id]',
            '.search-result-item'
        ]
        
        items = []
        for selector in selectors:
            items = soup.select(selector)
            if items:
                print(f\"Kilimall HTML: Found {len(items)} items with {selector}\")
                break
        
        for item in items[:15]:
            try:
                name_elem = item.select_one('h3, h4, .product-name, .goods-name, a[title]')
                name = name_elem.get_text(strip=True) or name_elem.get('title', 'Unknown') if name_elem else 'Unknown'
                
                price_elem = item.select_one('.price, .goods-price, [class*=\"price\"]')
                price = price_elem.get_text(strip=True) if price_elem else 'N/A'
                
                img_elem = item.select_one('img')
                image = ''
                if img_elem:
                    image = img_elem.get('data-src') or img_elem.get('data-original') or img_elem.get('src', '')
                    if image.startswith('//'):
                        image = 'https:' + image
                
                link_elem = item.select_one('a[href]')
                link = ''
                if link_elem and link_elem.get('href'):
                    href = link_elem['href']
                    link = 'https://www.kilimall.co.ke' + href if href.startswith('/') else href
                
                if name != 'Unknown':
                    products.append({
                        'name': name,
                        'price': price,
                        'image': image,
                        'link': link,
                        'source': 'Kilimall'
                    })
            except:
                continue
        
        return products
        
    except Exception as e:
        print(f\"Kilimall HTML error: {e}\")
        return []

def search_all_products(query):
    \"\"\"Search both platforms\"\"\"
    print(f\"Searching for: {query}\")
    
    # Search Jumia
    jumia_results = search_jumia_api(query)
    print(f\"Jumia found: {len(jumia_results)} products\")
    
    time.sleep(random.uniform(1, 2))  # Random delay
    
    # Search Kilimall
    kilimall_results = search_kilimall_api(query)
    print(f\"Kilimall found: {len(kilimall_results)} products\")
    
    all_results = jumia_results + kilimall_results
    
    # Sort by price
    def get_price_num(price_str):
        nums = re.findall(r'[\d,]+', str(price_str))
        return int(nums[0].replace(',', '')) if nums else 999999
    
    all_results.sort(key=lambda x: get_price_num(x['price']))
    
    return all_results

# Test
if __name__ == \"__main__\":
    results = search_all_products(\"iphone\")
    print(f\"\\nTotal: {len(results)} products\")
    for p in results[:5]:
        print(f\"{p['source']}: {p['name'][:40]} - {p['price']}\")
