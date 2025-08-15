# ⛳ Golf Club Web Scraper

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

Golf Club Web Scraper is a web application that searches and aggregates **used golf club listings** from multiple online retailers.  
It helps golfers quickly compare golf club prices, filter by specs, and find the best deals.

https://github.com/user-attachments/assets/f8c74d2e-dd6b-4bee-b30a-b22e2d2f288b

---

## ✨ Features
- **Scrape multiple golf stores**:
  - Golf Avenue
  - Global Golf
  - Just Golf Stuff
  - Facebook Marketplace (WIP)
- **Smart Filters**:
  - Club Type (Drivers, Irons, Putters, etc.)
  - Brand (Callaway, TaylorMade, Ping, etc.)
  - Hand Orientation (Left, Right, All)
- **Automatic multi-page scraping**
- **Price range handling** (takes lowest price for sorting)
- **Clickable results** linking directly to product pages
- **Session storage** for quick navigation

---

## 📦 Installation

### Requirements
- Python **3.9+**
- `pip`

### Setup
```bash
# Clone the repository
git clone https://github.com/<your-username>/golf-scraper.git
cd golf-scraper

# (Optional but recommended) Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```


## 🚀 Usage
### Run the Streamlit app:
```bash
streamlit run scraper_ui.py
```
Then:
Select which websites to scrape
Enter search parameters (club type, brand, hand orientation)
Click Search
View and sort results, click titles to visit product pages

## 🛠 Future Features / Roadmap
 - Add more golf retailers (2nd Swing, Golf Galaxy, PGA Tour Superstore)
 - Export results to CSV/Excel
 - Email alerts for new deals
 - Advanced filters (loft, shaft flex, condition)
 - Mobile-friendly UI improvements
 - Save searches for quick access
 - Public deployment with analytics

## 🤝 Contributing
- Contributions are welcome!
- Fork the repo
- Create a branch (git checkout -b feature-name)
- Commit changes
- Submit a Pull Request

## ⚠️ Notes & Limitations
- Web scrapers are delicate and may break if a website updates its structure
- Please submit an issue if you notice missing or incorrect data

## 📜 License
- This project is licensed under the MIT License.

## Support
- 💡 If you found this project helpful, give it a ⭐ on GitHub to help more golfers find it!


