import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random
from gemini_api import search_with_gemini, get_product_recommendations

def search_all_products(query):
    """Search products using Gemini AI or fallback to sample data"""
    print("Searching for: " + query)
    
    # Try Gemini API first
    gemini_results = search_with_gemini(query)
    if gemini_results and len(gemini_results) > 0:
        print("Gemini AI found " + str(len(gemini_results)) + " products")
        return gemini_results
    
    # Fallback to realistic sample data
    print("Using sample data (Add GEMINI_API_KEY to .env for live results)")
    
    samples = {
        "phone": [
            {"name": "Samsung Galaxy A54 5G", "price": "KES 42,999", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"},
            {"name": "iPhone 13 128GB", "price": "KES 89,999", "image": "", "link": "https://www.kilimall.co.ke", "source": "Kilimall"},
            {"name": "Xiaomi Redmi Note 12", "price": "KES 23,499", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"}
        ],
        "laptop": [
            {"name": "HP 250 G8 Laptop", "price": "KES 45,999", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"},
            {"name": "Lenovo IdeaPad 3", "price": "KES 38,500", "image": "", "link": "https://www.kilimall.co.ke", "source": "Kilimall"},
            {"name": "Dell Inspiron 15", "price": "KES 52,999", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"}
        ],
        "tv": [
            {"name": "Samsung 43 Smart TV", "price": "KES 34,999", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"},
            {"name": "LG 32 LED TV", "price": "KES 19,500", "image": "", "link": "https://www.kilimall.co.ke", "source": "Kilimall"},
            {"name": "Hisense 40 Smart TV", "price": "KES 28,999", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"}
        ],
        "headphones": [
            {"name": "Sony WH-CH520", "price": "KES 8,499", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"},
            {"name": "JBL Tune 760NC", "price": "KES 12,999", "image": "", "link": "https://www.kilimall.co.ke", "source": "Kilimall"},
            {"name": "Boat Rockerz 450", "price": "KES 3,499", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"}
        ]
    }
    
    # Return samples for known categories or generic samples
    if query.lower() in samples:
        return samples[query.lower()]
    else:
        return [
            {"name": query.title() + " - Premium Model", "price": "KES 25,999", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"},
            {"name": query.title() + " - Standard Model", "price": "KES 15,500", "image": "", "link": "https://www.kilimall.co.ke", "source": "Kilimall"},
            {"name": query.title() + " - Budget Model", "price": "KES 8,999", "image": "", "link": "https://www.jumia.co.ke", "source": "Jumia"}
        ]

def get_ai_recommendation(query, products):
    """Get AI recommendation for products"""
    return get_product_recommendations(query, products)
