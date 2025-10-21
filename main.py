import concurrent.futures
import logging
from scrapers.specific_scraper import TechBlogScraper
from utils.database_manager import DatabaseManager


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


SITES_TO_SCRAPE = [
    # Premium laptops (high price range)
    "https://www.amazon.in/s?k=buy+macbook+on+amazon&adgrpid=166537001972&gad_source=1&hvadid=697202032748&hvdev=c&hvlocphy=9180061&hvnetw=g&hvqmt=e&hvrand=13585009150502058614&hvtargid=kwd-938130254607&hydadcr=24541_2265439&mcid=0acd501f55c7361e974005b67fc100d1&tag=googinhydr1-21&ref=pd_sl_3s357vlti2_e",
    
    # Wireless headphones (mid-low price range)
    "https://www.amazon.in/s?k=wireless+headphones&crid=2R5IXZKুুමුතුකුමුන්&sprefix=wireless+headphones%2Caps%2C197&ref=nb_sb_noss_1",
    
    # Mechanical keyboards (mid price range)
    "https://www.amazon.in/s?k=mechanical+keyboard&crid=1WVQHJ0P9H3Z6&sprefix=mechanical+keyboard%2Caps%2C193&ref=nb_sb_noss_1",
    
    # Gaming mouse (low-mid price range)
    "https://www.amazon.in/s?k=gaming+mouse&crid=22UZ5S5A42ZPY&sprefix=gaming+mouse%2Caps%2C193&ref=nb_sb_noss_1",
    
    # Monitors (varied price range)
    "https://www.amazon.in/s?k=monitor&crid=36TDZTLIJ5TH4&sprefix=monitor%2Caps%2C198&ref=nb_sb_noss_1",
]


def scrape_site(url: str) -> dict:
    """Instantiate and run a scraper for a single URL and return the results."""
    scraper = TechBlogScraper(url)
    data = scraper.scrape()
    return {"url": url, "data": data}


def run_scrapers() -> None:
    """Run all scrapers concurrently and store results in the database."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(scrape_site, url): url for url in SITES_TO_SCRAPE}

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                # Persist results
                with DatabaseManager() as db:
                    db.insert_data(result["data"], result["url"])
            except Exception as exc:  # pragma: no cover - runtime exception handling
                logging.error(f"{url} generated an exception: {exc}")


if __name__ == "__main__":
    # Ensure database schema exists
    with DatabaseManager() as db:
        db.setup_database()

    # Execute scraping
    run_scrapers()
    logging.info("Scraping process finished.")
