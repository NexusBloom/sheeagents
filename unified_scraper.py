import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random

def get_headers():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ]
    return {
        'User-Agent': random.choice(user_agents)
    }

def search_all_products(query):
    # Return sample data for now
    return [
        {
            'name': query + ' - Sample from Jumia',
            'price': 'KES 15,999',
            'image': '',
            'link': 'https://www.jumia.co.ke',
            'source': 'Jumia'
        },
        {
            'name': query + ' - Sample from Kilimall',
            'price': 'KES 12,500',
            'image': '',
            'link': 'https://www.kilimall.co.ke',
            'source': 'Kilimall'
        }
    ]