import requests
from bs4 import BeautifulSoup
import re

def extract_product_image(product_element):
    """Extract image URL from product element"""
    img = product_element.find("img")
    if not img:
        return None
    
    # Check common image attributes in order of preference
    for attr in ["data-src", "data-original", "src", "data-lazy-src"]:
        if img.get(attr):
            url = img[attr]
            # Make sure it's a full URL
            if url.startswith('//'):
                return 'https:' + url
            elif url.startswith('/'):
                return 'https://www.kilimall.co.ke' + url
            return url
    
    return None

def scrape_kilimall_products(url):
    """Scrape products from Kilimall with images"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(r.content, "html5lib")
        
        products = []
        product_containers = soup.find_all("div", class_=re.compile(r"product|item|goods"))
        
        for product in product_containers[:20]:  # Limit to 20 products
            # Extract product name
            name_elem = product.find(["h3", "h2", "h4", "a", "div"], class_=re.compile(r"name|title"))
            name = name_elem.get_text(strip=True) if name_elem else "Unknown Product"
            
            # Extract price
            price_elem = product.find(["span", "div", "p"], class_=re.compile(r"price|cost"))
            price = price_elem.get_text(strip=True) if price_elem else "Price not available"
            
            # Extract image
            image_url = extract_product_image(product)
            
            # Only add if we have at least name and image
            if name and image_url:
                products.append({
                    "name": name,
                    "price": price,
                    "image": image_url,
                    "source": "Kilimall"
                })
        
        return products
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

# Test if run directly
if __name__ == "__main__":
    url = "https://www.kilimall.co.ke/search?q=phone"
    products = scrape_kilimall_products(url)
    print(f"Found {len(products)} products")
    for p in products[:3]:
        print(f"\nName: {p['name']}")
        print(f"Price: {p['price']}")
        print(f"Image: {p['image'][:80]}...")
