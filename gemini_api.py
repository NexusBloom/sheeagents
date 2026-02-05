import google.generativeai as genai
import os
import json
import re

def setup_gemini():
    \"\"\"Setup Gemini API with key from environment\"\"\"
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return None
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def search_with_gemini(query, platform=\"both\"):
    \"\"\"Use Gemini to search and structure product data\"\"\"
    model = setup_gemini()
    if not model:
        return []
    
    prompt = f\"\"\"Search for \"{query}\" on {platform} e-commerce sites in Kenya.
    Return a JSON array of 5-10 products with this exact structure:
    [
      {{
        \"name\": \"Product Name\",
        \"price\": \"KES X,XXX\",
        \"image\": \"https://example.com/image.jpg\",
        \"link\": \"https://www.jumia.co.ke/product-link\",
        \"source\": \"Jumia\"
      }}
    ]
    Make prices realistic for Kenyan market. Include both Jumia and Kilimall sources.\"\"\"
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        
        # Extract JSON from response
        json_match = re.search(r'\[.*\]', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        print(f\"Gemini error: {e}\")
    
    return []

def get_product_recommendations(query, products):
    \"\"\"Get AI recommendations for products\"\"\"
    model = setup_gemini()
    if not model or not products:
        return \"No recommendations available\"
    
    product_summary = json.dumps(products[:5], indent=2)
    
    prompt = f\"\"\"Based on these products for \"{query}\":
    {product_summary}
    
    Provide a brief recommendation (2-3 sentences) on which product offers the best value.\"\"\"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return \"Unable to generate recommendation\"
