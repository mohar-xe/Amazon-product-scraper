# Amazon Product Scraper & Analytics Dashboard

A Python web scraping application that collects product data from Amazon India and displays it in a beautiful vintage-styled analytics dashboard.

## Features

- **Multi-Category Scraping**: Scrapes 5 product categories (Laptops, Headphones, Keyboards, Gaming Mice, Monitors)
- **Concurrent Scraping**: Uses ThreadPoolExecutor for fast parallel scraping
- **SQLite Database**: Stores product data with name, price, rating, image URL, and timestamp
- **Beautiful Dashboard**: Flask web app with vintage notebook aesthetic
- **Rich Analytics**: 
  - 4 stat cards (total products, avg/min/max prices)
  - Bar chart (average price by category)
  - Pie chart (product distribution)
  - Histogram (price distribution)
  - Data table with all products

## Tech Stack

- **Python 3.x**
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP client
- **Flask** - Web framework
- **Pandas** - Data manipulation
- **Matplotlib & Seaborn** - Data visualization
- **SQLite3** - Database

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mohar-xe/Amazon-product-scraper.git
cd web_scraper
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start (Single Command)
```bash
./run.sh
```

This script will:
1. Run the scraper to collect ~110 products from Amazon
2. Start the Flask dashboard at http://127.0.0.1:5000/

### Manual Run

**Run scraper only:**
```bash
python main.py
```

**Run dashboard only:**
```bash
python web/app.py
```

Then open http://127.0.0.1:5000/ in your browser.

## Project Structure

```
web_scraper/
├── main.py                 # Main scraping orchestration
├── requirements.txt        # Python dependencies
├── run.sh                 # Convenience script to run everything
├── scrapers/
│   ├── base_scraper.py    # Abstract base scraper class
│   └── specific_scraper.py # Amazon product scraper implementation
├── utils/
│   └── database_manager.py # SQLite database context manager
└── web/
    ├── app.py             # Flask application
    ├── static/
    │   └── style.css      # Additional styles (if needed)
    └── templates/
        └── index.html     # Dashboard HTML template
```

## Data Collected

For each product:
- Product name
- Price (₹)
- Rating
- Image URL
- Source URL
- Scraped timestamp

## Dashboard Features

- **Vintage Aesthetic**: Beige/brown color palette with notebook-style design
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Stats**: Live calculations from database
- **Visual Analytics**: Multiple chart types for data insights
- **Clean Tables**: Top 50 products displayed with full details

## Notes

- Scraper uses realistic browser headers to avoid detection
- Concurrent scraping with 5 workers for optimal performance
- Data persists in `data.db` SQLite database
- Charts use vintage color palette matching the dashboard theme

## License

MIT License - Feel free to use and modify!
