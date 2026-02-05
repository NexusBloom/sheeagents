
import os
import json
import re

# Dummy functions that return empty/safe results
def setup_gemini():
    return None

def search_with_gemini(query, platform="both"):
    """Return empty list - API not configured"""
    return []

def get_product_recommendations(query, products):
    """Return message - API not configured"""
    return "Configure GEMINI_API_KEY in Streamlit Cloud secrets for AI recommendations"
