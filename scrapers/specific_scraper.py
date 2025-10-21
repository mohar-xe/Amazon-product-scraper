import logging
import re
from bs4 import BeautifulSoup
import requests

from .base_scraper import BaseScraper


class TechBlogScraper(BaseScraper):
    """Amazon product listing scraper (works for Amazon search result pages)."""
    
    def __init__(self, url: str):
        super().__init__(url)
        # Use a realistic User-Agent to avoid being blocked by Amazon
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

    def scrape(self):
        logging.info(f"Scraping Amazon search page: {self.url}")
        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Could not fetch {self.url}: {e}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        scraped_data = []

        # Amazon product listings are typically in divs with attribute data-component-type="s-search-result"
        products = soup.find_all("div", {"data-component-type": "s-search-result"})

        for product in products:
            # Extract product title (h2 > span)
            title_h2 = product.select_one("h2")
            if title_h2:
                title_span = title_h2.select_one("span")
                title = title_span.get_text(strip=True) if title_span else "N/A"
            else:
                title = "N/A"

            # Extract price (Amazon has multiple price formats; we try the common ones)
            price = 0.0
            price_whole = product.select_one("span.a-price-whole")
            price_fraction = product.select_one("span.a-price-fraction")
            
            if price_whole:
                # Clean and parse (Amazon uses comma as thousands separator in India)
                price_str = price_whole.get_text(strip=True).replace(",", "").replace(".", "")
                if price_fraction:
                    frac = price_fraction.get_text(strip=True)
                    price_str = price_str + "." + frac
                try:
                    price = float(price_str)
                except ValueError:
                    pass

            # Extract rating (optional)
            rating_elem = product.select_one("span.a-icon-alt")
            rating = rating_elem.get_text(strip=True) if rating_elem else "N/A"

            # Extract image URL (optional)
            img_elem = product.select_one("img.s-image")
            image_url = img_elem.get("src") if img_elem else "N/A"

            # Only add if we found at least a title
            if title != "N/A":
                scraped_data.append({
                    "name": title,
                    "price": price,
                    "rating": rating,
                    "image_url": image_url,
                })

        logging.info(f"Found {len(scraped_data)} products from {self.url}")
        return scraped_data



