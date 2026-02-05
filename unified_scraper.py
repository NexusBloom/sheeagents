import requests
from bs4 import BeautifulSoup
import re
import json

def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }

def search_kilimall(query):
    \"\"\"Search Kilimall Kenya\"\"\"
    url = f\"https://www.kilimall.co.ke/search?q={query.replace(' ', '+')}&page=1&perPage=20\"
    
    try:
        session = requests.Session()
        # First get the page to establish session
        r = session.get(url, headers=get_headers(), timeout=30)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        products = []
        
        # Try to find product data in script tags (JSON)
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'window.__INITIAL_STATE__' in script.string:
                try:
                    json_str = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', script.string, re.DOTALL)
                    if json_str:
                        data = json.loads(json_str.group(1))
                        # Extract products from JSON structure
                        if 'products' in data:
                            for item in data['products'][:10]:
                                products.append({
                                    'name': item.get('name', 'Unknown'),
                                    'price': f\"KES {item.get('price', 'N/A')}\",
                                    'image': item.get('image', ''),
                                    'link': f\"https://www.kilimall.co.ke/product/{item.get('id', '')}\",
                                    'source': 'Kilimall'
                                })
                            return products
                except:
                    pass
        
        # Fallback to HTML parsing
        items = soup.find_all(['div', 'article'], class_=re.compile(r'product|item|goods', re.I))
        
        for item in items[:10]:
            try:
                # Name
                name_elem = item.find(['h3', 'h4', 'h2', 'a'], class_=re.compile(r'name|title', re.I))
                name = name_elem.get_text(strip=True) if name_elem else 'Unknown'
                
                # Price
                price_elem = item.find(['span', 'div', 'p'], class_=re.compile(r'price|prc', re.I))
                price = price_elem.get_text(strip=True) if price_elem else 'N/A'
                
                # Image
                img = item.find('img')
                image = ''
                if img:
                    image = img.get('data-src') or img.get('data-original') or img.get('src', '')
                    if image.startswith('//'):
                        image = 'https:' + image
                    elif image.startswith('/'):
                        image = 'https://www.kilimall.co.ke' + image
                
                # Link
                link_elem = item.find('a', href=True)
                link = 'https://www.kilimall.co.ke' + link_elem['href'] if link_elem and link_elem['href'].startswith('/') else link_elem['href'] if link_elem else url
                
                if name and name != 'Unknown':
                    products.append({
                        'name': name,
                        'price': price,
                        'image': image,
                        'link': link,
                        'source': 'Kilimall'
                    })
            except Exception as e:
                continue
        
        return products
        
    except Exception as e:
        print(f\"Kilimall error: {e}\")
        return []

def search_jumia(query):
    \"\"\"Search Jumia Kenya\"\"\"
    url = f\"https://www.jumia.co.ke/catalog/?q={query.replace(' ', '+')}\"
    
    try:
        r = requests.get(url, headers=get_headers(), timeout=30)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        products = []
        
        # Jumia uses specific article tags
        items = soup.find_all('article', {'class': 'prd _fb col c-prd'})
        
        if not items:
            items = soup.find_all('article', class_=re.compile(r'prd|product', re.I))
        
        for item in items[:10]:
            try:
                # Name
                name_elem = item.find('h3', {'class': 'name'})
                if not name_elem:
                    name_elem = item.find(['h3', 'div'], class_=re.compile(r'name|title', re.I))
                name = name_elem.get_text(strip=True) if name_elem else 'Unknown'
                
                # Price
                price_elem = item.find('div', {'class': 'prc'})
                if not price_elem:
                    price_elem = item.find(['div', 'span'], class_=re.compile(r'price|prc', re.I))
                price = price_elem.get_text(strip=True) if price_elem else 'N/A'
                
                # Image
                img = item.find('img')
                image = ''
                if img:
                    image = img.get('data-src') or img.get('src', '')
                    if image.startswith('//'):
                        image = 'https:' + image
                
                # Link
                link_elem = item.find('a', {'class': 'core'})
                if not link_elem:
                    link_elem = item.find('a', href=True)
                link = 'https://www.jumia.co.ke' + link_elem['href'] if link_elem and link_elem['href'].startswith('/') else link_elem['href'] if link_elem else url
                
                if name and name != 'Unknown':
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

def search_all_products(query):
    \"\"\"Search both platforms\"\"\"
    kilimall_results = search_kilimall(query)
    jumia_results = search_jumia(query)
    
    all_results = kilimall_results + jumia_results
    
    # Try to sort by price
    def get_price_num(price_str):
        nums = re.findall(r'[\d,]+', str(price_str))
        return int(nums[0].replace(',', '')) if nums else 999999
    
    all_results.sort(key=lambda x: get_price_num(x['price']))
    
    return all_results

# Test
if __name__ == \"__main__\":
    results = search_all_products(\"headphones\")
    print(f\"Found {len(results)} products\")
    for p in results[:5]:
        print(f\"{p['source']}: {p['name'][:40]}... - {p['price']}\")
