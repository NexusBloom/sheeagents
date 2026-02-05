import requests
from bs4 import BeautifulSoup
import re

def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }

def extract_jumia_products(search_query):
    url = f\"https://www.jumia.co.ke/catalog/?q={search_query.replace(' ', '+')}\"
    
    try:
        r = requests.get(url, headers=get_headers(), timeout=30)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        products = []
        items = soup.find_all('article', {'class': 'prd'})
        
        for item in items[:15]:
            try:
                name_elem = item.find('h3', {'class': 'name'})
                name = name_elem.text.strip() if name_elem else 'No name'
                
                price_elem = item.find('div', {'class': 'prc'})
                price = price_elem.text.strip() if price_elem else 'N/A'
                
                img_elem = item.find('img')
                image = img_elem.get('data-src') if img_elem else None
                
                link_elem = item.find('a', {'class': 'core'})
                link = 'https://www.jumia.co.ke' + link_elem['href'] if link_elem else url
                
                if name != 'No name':
                    products.append({
                        'name': name,
                        'price': price,
                        'image': image,
                        'link': link,
                        'source': 'Jumia'
                    })
            except:
                continue
                
        return products
    except Exception as e:
        print(f\"Jumia error: {e}\")
        return []
