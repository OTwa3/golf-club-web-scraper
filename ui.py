import streamlit as st
import sqlite3
import pandas as pd

DB_FILE = 'scraped_data.db'

def run_query(query, params=()):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

st.set_page_config(page_title="Scraped Data Search", layout="wide")
st.title("Scraped Data Search")

# Filters
search = st.text_input("Search title contains:")
min_price = st.number_input("Min price", min_value=0.0, value=0.0, step=1.0)
max_price = st.number_input("Max price", min_value=0.0, value=9999.0, step=1.0)
source_filter = st.selectbox(
    "Source",
    ["All", "Marketplace", "GolfAvenue", "GlobalGolf", "JustGolfStuff"]
)
sort_by = st.selectbox("Sort by", ["price", "scraped_at"])
sort_order = st.radio("Order", ["Ascending", "Descending"])

if st.button("Search"):
    query = "SELECT * FROM items WHERE title LIKE ? AND price BETWEEN ? AND ?"
    params = [f"%{search}%", min_price, max_price]

    if source_filter != "All":
        query += " AND source = ?"
        params.append(source_filter)

    query += f" ORDER BY {sort_by} {'ASC' if sort_order == 'Ascending' else 'DESC'}"

    df = run_query(query, params)

    if not df.empty:
        # Make title clickable and drop link column
        df["title"] = df.apply(lambda row: f'<a href="{row["link"]}" target="_blank">{row["title"]}</a>', axis=1)
        df = df.drop(columns=["link"])

        # CSS for better spacing and scrollable table
        st.markdown("""
        <style>
            .table-container {
                overflow-x: auto;
                width: 100%;
            }
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                padding: 8px 12px;
                text-align: left;
            }
            th {
                background-color: #f0f0f0;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            a {
                color: #1a73e8;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
        """, unsafe_allow_html=True)

        html_table = df.to_html(escape=False, index=False)
        st.markdown(f'<div class="table-container">{html_table}</div>', unsafe_allow_html=True)
    else:
        st.warning("No results found.")

