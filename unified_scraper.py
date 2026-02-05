
from gemini_api import search_with_gemini, get_product_recommendations

def search_all_products(query):
    """Return sample products"""
    samples = {
        "phone": [
            {"name": "Samsung Galaxy A54", "price": "KES 42,999", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"},
            {"name": "iPhone 13", "price": "KES 89,999", "image": "", "link": "https://www.kilimall.co.ke", "source": "Kilimall"}
        ],
        "laptop": [
            {"name": "HP Laptop", "price": "KES 45,999", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"},
            {"name": "Lenovo Laptop", "price": "KES 38,500", "image": "", "link": "https://www.kilimall.co.ke", "source": "Kilimall"}
        ],
        "tv": [
            {"name": "Samsung TV", "price": "KES 34,999", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"},
            {"name": "LG TV", "price": "KES 19,500", "image": "", "link": "https://www.kilimall.co.ke", "source": "Kilimall"}
        ],
        "headphones": [
            {"name": "Sony Headphones", "price": "KES 8,499", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"},
            {"name": "JBL Headphones", "price": "KES 12,999", "image": "", "link": "https://www.kilimall.co.ke", "source": "Kilimall"}
        ]
    }
    
    query_lower = query.lower()
    if query_lower in samples:
        return samples[query_lower]
    else:
        return [
            {"name": query + " - Premium", "price": "KES 25,999", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"},
            {"name": query + " - Budget", "price": "KES 12,500", "image": "", "link": "https://www.kilimall.co.ke", "source": "Kilimall"}
        ]

def get_ai_recommendation(query, products):
    return get_product_recommendations(query, products)
