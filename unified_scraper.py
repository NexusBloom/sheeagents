import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random
from gemini_api import search_with_gemini, get_product_recommendations

def get_headers():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ]
    return {'User-Agent': random.choice(user_agents)}

def search_jumia_scraper(query):
    \"\"\"Try to scrape Jumia\"\"\"
    try:
        session = requests.Session()
        session.headers.update(get_headers())
        url = f\"https://www.jumia.co.ke/catalog/?q={query.replace(' ', '+')}\"
        response = session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        items = soup.find_all('article', class_='prd')
        
        for item in items[:5]:
            try:
                name = item.find('h3', class_='name')
                price = item.find('div', class_='prc')
                img = item.find('img')
                link = item.find('a', class_='core')
                
                if name and price:
                    products.append({
                        'name': name.text.strip(),
                        'price': price.text.strip(),
                        'image': img.get('data-src', '') if img else '',
                        'link': 'https://www.jumia.co.ke' + link['href'] if link else '',
                        'source': 'Jumia'
                    })
            except:
                continue
        return products
    except:
        return []

def search_kilimall_scraper(query):
    \"\"\"Try to scrape Kilimall\"\"\"
    try:
        session = requests.Session()
        session.headers.update(get_headers())
        url = f\"https://www.kilimall.co.ke/search?q={query.replace(' ', '+')}\"
        response = session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        items = soup.find_all('div', class_=re.compile(r'product|item'))
        
        for item in items[:5]:
            try:
                name = item.find(['h3', 'h4', 'a'])
                price = item.find(['span', 'div'], class_=re.compile(r'price'))
                
                if name and price:
                    products.append({
                        'name': name.text.strip(),
                        'price': price.text.strip(),
                        'image': '',
                        'link': 'https://www.kilimall.co.ke',
                        'source': 'Kilimall'
                    })
            except:
                continue
        return products
    except:
        return []

def search_all_products(query):
    \"\"\"Search using multiple methods\"\"\"
    print(f\"Searching for: {query}\")
    
    # Try Gemini API first
    gemini_results = search_with_gemini(query)
    if gemini_results:
        print(f\"Gemini found: {len(gemini_results)} products\")
        return gemini_results
    
    # Fallback to scrapers
    jumia_results = search_jumia_scraper(query)
    kilimall_results = search_kilimall_scraper(query)
    
    all_results = jumia_results + kilimall_results
    
    # If still no results, return sample data
    if not all_results:
        return [
            {
                'name': f'{query.title()} - Premium Model',
                'price': 'KES 25,999',
                'image': 'https://via.placeholder.com/300x300?text=Product+Image',
                'link': 'https://www.jumia.co.ke',
                'source': 'Jumia'
            },
            {
                'name': f'{query.title()} - Budget Option',
                'price': 'KES 12,500',
                'image': 'https://via.placeholder.com/300x300?text=Product+Image',
                'link': 'https://www.kilimall.co.ke',
                'source': 'Kilimall'
            },
            {
                'name': f'{query.title()} - Mid Range',
                'price': 'KES 18,750',
                'image': 'https://via.placeholder.com/300x300?text=Product+Image',
                'link': 'https://www.jumia.co.ke',
                'source': 'Jumia'
            }
        ]
    
    return all_results

def get_ai_recommendation(query, products):
    \"\"\"Get AI recommendation\"\"\"
    return get_product_recommendations(query, products)
