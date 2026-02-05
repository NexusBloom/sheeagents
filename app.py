import streamlit as st
import sys
from pathlib import Path

# Add project root to path
current_file = Path(__file__).resolve()
project_root = current_file.parent
sys.path.insert(0, str(project_root))

import re
from unified_scraper import search_all_products, get_ai_recommendation

# Page config
st.set_page_config(page_title="ShopSavvy AI", page_icon="🛒", layout="wide")

def clean_query(raw):
    if not raw:
        return ""
    query = raw.strip()
    for word in ["in jumia", "from jumia", "on jumia", "jumia",
                 "in kilimall", "from kilimall", "on kilimall", "kilimall"]:
        query = re.sub(word, "", query, flags=re.IGNORECASE)
    query = " ".join(query.split())
    return query if query else raw.strip()

@st.cache_data(ttl=300)
def get_products(query, min_p, max_p):
    if not query:
        return []
    try:
        all_p = search_all_products(query)
        # Filter by price if possible
        filtered = []
        for p in all_p:
            price_str = p.get("price", "0")
            nums = re.findall(r"[\d,]+", price_str)
            if nums:
                price_num = int(nums[0].replace(",", ""))
                if min_p <= price_num <= max_p:
                    p["price_num"] = price_num
                    filtered.append(p)
        return filtered
    except Exception as e:
        st.error(f"Error: {e}")
        return []

def show_product(p, rank):
    with st.container():
        c1, c2, c3 = st.columns([1, 3, 1])
        with c1:
            img_url = p.get("image", "")
            if img_url and img_url.startswith("http"):
                st.image(img_url, width=120)
            else:
                initial = p.get("name", "X")[0].upper()
                bg = "#fff3e0" if p.get("source") == "Jumia" else "#e8f5e9"
                st.markdown(f"<div style='width:120px;height:120px;background:{bg};display:flex;align-items:center;justify-content:center;font-size:40px;border-radius:8px;'>{initial}</div>", unsafe_allow_html=True)

        with c2:
            st.markdown(f"**{p['name']}**")
            source = p.get("source", "")
            if source == "Jumia":
                st.markdown(":orange[**Jumia**]")
            else:
                st.markdown(":green[**Kilimall**]")

            price = p.get("price", "N/A")
            st.markdown(f"**{price}**")
            
            link = p.get("link", "")
            if link:
                st.markdown(f"[View on {source}]({link})")

        with c3:
            st.markdown(f"#{rank}")
            st.caption("AI Match" if rank <= 3 else "")

# UI
st.title("🛒 ShopSavvy AI")
st.write("Compare prices across Jumia and Kilimall Kenya")

# Search
query = st.text_input("What are you looking for?", "")

col1, col2 = st.columns([3, 1])
with col1:
    min_price = st.number_input("Min Price (KES)", 0, 1000000, 0)
with col2:
    max_price = st.number_input("Max Price (KES)", 0, 1000000, 100000)

search = st.button("🔍 Search", use_container_width=True, type="primary")

if search and query:
    with st.spinner(f"Searching for: {query}..."):
        clean_q = clean_query(query)
        products = get_products(clean_q, min_price, max_price)
        
        if products:
            st.success(f"Found {len(products)} products!")
            
            for idx, product in enumerate(products[:10]):
                show_product(product, idx + 1)
                st.divider()
            
            # AI Recommendation
            st.subheader("🤖 AI Recommendation")
            with st.spinner("Analyzing..."):
                rec = get_ai_recommendation(clean_q, products)
                st.info(rec)
        else:
            st.error("No products found! Try different search terms or price range.")

elif search and not query:
    st.warning("Please enter a search term")
