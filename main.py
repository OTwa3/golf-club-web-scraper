from fb_marketplace_scraper import scrape_facebook_marketplace
from golfavenue_scraper import scrape_golfavenue
from globalgolf_scraper import scrape_globalgolf
from golfstuff_scraper import scrape_golfstuff
from utils import insert_items_bulk, setup_database

setup_database()

all_items = []

# all_items += scrape_facebook_marketplace("Driver LH")
all_items += scrape_golfavenue("Drivers", "Left Hand", "Callaway")
all_items += scrape_globalgolf("Drivers", "Left Hand", "Callaway")
all_items += scrape_golfstuff("Drivers", "Left Hand", "Callaway")


insert_items_bulk(all_items)
print(f"Inserted {len(all_items)} items into the database.")
