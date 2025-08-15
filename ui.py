import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import extract_lowest_price
from golfavenue_scraper import scrape_golfavenue
from globalgolf_scraper import scrape_globalgolf
from golfstuff_scraper import scrape_golfstuff

st.set_page_config(page_title="Golf Club Price Compare", layout="wide")
st.title("Golf Club Price Compare")

# --- SOURCE SELECTION ---
st.subheader("Data Sources")
col1, col2, col3 = st.columns(3)
with col1:
    golfavenue_on = st.checkbox("GolfAvenue", value=True)
    globalgolf_on = st.checkbox("GlobalGolf", value=True)
    golfstuff_on = st.checkbox("JustGolfStuff", value=True)
    
# --- SEARCH PARAMETERS ---
st.subheader("Search Filters")
col1, col2, col3 = st.columns([1,1,1])
with col1:
    golf_search_term = st.selectbox("Club Type", ["Drivers", "Fairway Woods", "Hybrids", "Irons", "Wedges", "Putters"])
with col2:
    brand_filter = st.text_input("Brand (optional)")
with col3:
    hand_filter = st.selectbox("Hand", ["All", "Left Hand", "Right Hand"])

# --- SEARCH BUTTON ---
if st.button("Search Clubs", use_container_width=True):
    all_items = []
    progress_placeholder = st.empty()
    progress_bar = progress_placeholder.progress(0)

    scrapers = [
        ("GolfAvenue", golfavenue_on, scrape_golfavenue),
        ("GlobalGolf", globalgolf_on, scrape_globalgolf),
        ("JustGolfStuff", golfstuff_on, scrape_golfstuff)
    ]

    active_scrapers = [(name, func) for name, on, func in scrapers if on]
    total_scrapers = len(active_scrapers)
    completed_scrapers = 0

    def run_scraper(name, func):
        # Run scraper and return results
        return func(golf_search_term, hand_filter, brand_filter)

    with st.spinner("Scraping selected sources..."):
        with ThreadPoolExecutor(max_workers=total_scrapers) as executor:
            future_to_name = {executor.submit(run_scraper, name, func): name for name, func in active_scrapers}
            for future in as_completed(future_to_name):
                items = future.result()
                all_items += items
                completed_scrapers += 1
                progress_bar.progress(completed_scrapers / total_scrapers)

    progress_placeholder.empty()  # remove progress bar

    st.session_state["all_items"] = all_items
    st.session_state["scrape_done"] = True

# --- RESULTS ---
if st.session_state.get("scrape_done"):
    all_items = st.session_state.get("all_items", [])
    if all_items:
        st.success(f"✅ Found {len(all_items)} items")
        df = pd.DataFrame(all_items)
        df["price_numeric"] = df["price"].apply(extract_lowest_price)

        # Filter & sort
        with st.expander("Filter & Sort Results", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                local_search = st.text_input("Search in Titles").strip().lower()
            with col2:
                sort_by = st.selectbox("Sort by", ["price", "title", "source"])
            with col3:
                ascending = st.radio("Order", ["Ascending", "Descending"]) == "Ascending"

        if local_search:
            df = df[df["title"].str.lower().str.contains(local_search)]

        if sort_by == "price":
            df = df.sort_values(by="price_numeric", ascending=ascending)
        else:
            df = df.sort_values(by=sort_by, ascending=ascending)

        df["price"] = df["price_numeric"].apply(lambda x: f"${x:,.2f} CAD" if pd.notnull(x) else "")
        df = df.drop(columns=["price_numeric"])
        df["title"] = df.apply(lambda r: f'<a href="{r["link"]}" target="_blank">{r["title"]}</a>', axis=1)
        df = df.drop(columns=["link"])

        st.markdown("""
        <style>
        .table-container {overflow-x: auto; width: 100%;}
        table {border-collapse: collapse; width: 100%;}
        th, td {padding: 8px 12px; text-align: left !important;}
        
        /* Table header */
        th {background-color: #4a4a4a; color: #fff;}
        
        /* Table rows: alternate subtle shading that works in dark mode */
        tr:nth-child(even) {background-color: rgba(255, 255, 255, 0.05);}
        tr:nth-child(odd) {background-color: rgba(255, 255, 255, 0.02);}
        
        /* Links */
        a {color: #1a73e8; text-decoration: none;}
        a:hover {text-decoration: underline;}
        </style>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="table-container">{df.to_html(escape=False, index=False)}</div>', unsafe_allow_html=True)
    else:
        st.warning("No items found - try different filters.")
