import streamlit as st
from fb_marketplace_scraper import scrape_facebook_marketplace
from golfavenue_scraper import scrape_golfavenue
from globalgolf_scraper import scrape_globalgolf
from golfstuff_scraper import scrape_golfstuff
from utils import insert_items_bulk, setup_database

# --- Streamlit Page Config ---
st.set_page_config(page_title="Golf Scraper Controller", layout="wide")
st.title("Golf Scraper Controller")

setup_database()

# --- Scraper selection ---
st.subheader("Select scrapers to run")
scrapers_to_run = {
    "Facebook Marketplace": st.checkbox("Facebook Marketplace", value=True),
    "GolfAvenue": st.checkbox("GolfAvenue", value=True),
    "GlobalGolf": st.checkbox("GlobalGolf", value=True),
    "JustGolfStuff": st.checkbox("JustGolfStuff", value=True)
}

# --- Search terms and filters ---
st.subheader("Search terms & filters")
search_terms = {}
brand_filters = {}
hand_filters = {}

if scrapers_to_run["Facebook Marketplace"]:
    search_terms["Facebook Marketplace"] = st.text_input("Facebook Marketplace Search", value="Driver LH")
    brand_filters["Facebook Marketplace"] = st.text_input("Facebook Marketplace Brand", value="")

if scrapers_to_run["GolfAvenue"]:
    search_terms["GolfAvenue"] = st.text_input("GolfAvenue Search", value="Driver")
    hand_filters["GolfAvenue"] = st.selectbox("Hand Filter (GolfAvenue)", ["All", "Left Hand", "Right Hand"])
    brand_filters["GolfAvenue"] = st.text_input("GolfAvenue Brand", value="")

if scrapers_to_run["GlobalGolf"]:
    search_terms["GlobalGolf"] = st.text_input("GlobalGolf Search", value="Driver")
    hand_filters["GlobalGolf"] = st.selectbox("Hand Filter (GlobalGolf)", ["All", "Left Hand", "Right Hand"])
    brand_filters["GlobalGolf"] = st.text_input("GlobalGolf Brand", value="")

if scrapers_to_run["JustGolfStuff"]:
    search_terms["JustGolfStuff"] = st.text_input("JustGolfStuff Search", value="Driver")
    hand_filters["JustGolfStuff"] = st.selectbox("Hand Filter (JustGolfStuff)", ["All", "Left Hand", "Right Hand"])
    brand_filters["JustGolfStuff"] = st.text_input("JustGolfStuff Brand", value="")

# --- Run Button ---
if st.button("Run Selected Scrapers"):
    all_items = []

    if scrapers_to_run["Facebook Marketplace"]:
        all_items += scrape_facebook_marketplace(
            search_terms["Facebook Marketplace"], 
            brand_filter=brand_filters["Facebook Marketplace"]
        )

    if scrapers_to_run["GolfAvenue"]:
        all_items += scrape_golfavenue(
            search_terms["GolfAvenue"], 
            hand_filter=hand_filters["GolfAvenue"], 
            brand_filter=brand_filters["GolfAvenue"]
        )

    if scrapers_to_run["GlobalGolf"]:
        all_items += scrape_globalgolf(
            search_terms["GlobalGolf"], 
            hand_filter=hand_filters["GlobalGolf"], 
            brand_filter=brand_filters["GlobalGolf"]
        )

    if scrapers_to_run["JustGolfStuff"]:
        all_items += scrape_golfstuff(
            search_terms["JustGolfStuff"], 
            hand_filter=hand_filters["JustGolfStuff"], 
            brand_filter=brand_filters["JustGolfStuff"]
        )

    if all_items:
        insert_items_bulk(all_items)
        st.success(f"Inserted {len(all_items)} items into the database.")
    else:
        st.warning("No items scraped.")
