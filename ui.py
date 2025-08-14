import streamlit as st
import pandas as pd
from utils import insert_items_bulk, setup_database, extract_lowest_price
from fb_marketplace_scraper import scrape_facebook_marketplace
from golfavenue_scraper import scrape_golfavenue
from globalgolf_scraper import scrape_globalgolf
from golfstuff_scraper import scrape_golfstuff


st.set_page_config(page_title="Golf Club Web Scraper", layout="wide")
st.title("Golf Club Web Scraper")


st.subheader("Select sources to scrape")
scrapers_to_run = {
    "Facebook Marketplace": st.checkbox("Facebook Marketplace", value=False),
    "GolfAvenue": st.checkbox("GolfAvenue", value=True),
    "GlobalGolf": st.checkbox("GlobalGolf", value=True),
    "JustGolfStuff": st.checkbox("JustGolfStuff", value=True)
}

st.subheader("Search parameters")
golf_search_term = st.selectbox("Club type", ["Drivers", "Fairway Woods", "Hybrids", "Irons", "Wedges", "Putters"])
brand_filter = st.text_input("Brand (optional)", value="")
hand_filter = st.selectbox("Hand Filter", ["All", "Left Hand", "Right Hand"])

# Facebook Search Term Only
fb_search_term = ""
if scrapers_to_run["Facebook Marketplace"]:
    fb_search_term = st.text_input("Facebook Marketplace Search", value="Driver LH")


# Search button
if st.button("Search"):
    with st.spinner("Scraping selected sources..."):
        all_items = []

        if scrapers_to_run["Facebook Marketplace"]:
            all_items += scrape_facebook_marketplace(fb_search_term, brand_filter=brand_filter)

        if scrapers_to_run["GolfAvenue"]:
            all_items += scrape_golfavenue(search_term=golf_search_term, hand_filter=hand_filter, brand_filter=brand_filter)

        if scrapers_to_run["GlobalGolf"]:
            all_items += scrape_globalgolf(search_term=golf_search_term, hand_filter=hand_filter, brand_filter=brand_filter)

        if scrapers_to_run["JustGolfStuff"]:
            all_items += scrape_golfstuff(search_term=golf_search_term, hand_filter=hand_filter, brand_filter=brand_filter)

        # Store results in session_state to persist across reruns
        st.session_state["all_items"] = all_items
        st.session_state["scrape_done"] = True

if st.session_state.get("scrape_done"):
    all_items = st.session_state.get("all_items", [])

    # Display table
    if all_items:
        st.success(f"Scraped {len(all_items)} items successfully!")

        df = pd.DataFrame(all_items)

        # Price conversion
        df["price_numeric"] = df["price"].apply(extract_lowest_price)
        df["price"] = df["price_numeric"].apply(lambda x: f"${x:,.2f} CAD" if pd.notnull(x) else "")

        sort_by = st.selectbox("Sort by", ["price", "title"])
        sort_order = st.radio("Order", ["Ascending", "Descending"])
        ascending = sort_order == "Ascending"

        if sort_by == "price":
            df = df.sort_values(by="price_numeric", ascending=ascending)
        else:
            df = df.sort_values(by="title", ascending=ascending)

        # Price formatting
        df["price"] = df["price_numeric"].apply(lambda x: f"${x:,.2f} CAD" if pd.notnull(x) else "")
        df = df.drop(columns=["price_numeric"])

        # Merge title and link
        df["title"] = df.apply(lambda row: f'<a href="{row["link"]}" target="_blank">{row["title"]}</a>', axis=1)
        df = df.drop(columns=["link"])

        st.markdown("""
        <style>
            .table-container {overflow-x: auto; width: 100%;}
            table {border-collapse: collapse; width: 100%;}
            th, td {padding: 8px 12px; text-align: left;}
            th {background-color: #f0f0f0;}
            tr:nth-child(even) {background-color: #f9f9f9;}
            a {color: #1a73e8; text-decoration: none;}
            a:hover {text-decoration: underline;}
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="table-container">{df.to_html(escape=False, index=False)}</div>', unsafe_allow_html=True)
    else:
        st.warning("No items found - please ensure your search filters are correct.")