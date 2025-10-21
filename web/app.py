import os
import logging
import sqlite3
import io
import base64
import re

from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Set vintage notebook style with beige/brown colors
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Georgia', 'Times New Roman']

# Create custom beige/brown color palette
vintage_colors = ['#8b6f47', '#b8860b', '#d4a574', '#a0522d', '#cd853f', '#daa520']
vintage_cmap = LinearSegmentedColormap.from_list('vintage', 
    ['#8b6f47', '#b8860b', '#d4a574', '#daa520'])

app = Flask(__name__)


# Database path relative to this file
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data.db")


def extract_category_from_url(url):
	"""Extract product category from Amazon URL for better labeling."""
	if 'macbook' in url.lower():
		return 'Laptops'
	elif 'headphone' in url.lower():
		return 'Headphones'
	elif 'keyboard' in url.lower():
		return 'Keyboards'
	elif 'mouse' in url.lower():
		return 'Gaming Mice'
	elif 'monitor' in url.lower():
		return 'Monitors'
	else:
		# Try to extract from k= parameter
		match = re.search(r'[?&]k=([^&]+)', url)
		if match:
			return match.group(1).replace('+', ' ')[:20]
		return 'Other'


@app.route("/")
def index():
	try:
		conn = sqlite3.connect(DB_PATH)
		# Use pandas to easily read SQL query into a DataFrame
		df = pd.read_sql_query(
			"SELECT * FROM products ORDER BY scraped_at DESC", conn
		)
		conn.close()
	except Exception as e:
		logging.exception("Error connecting to database or reading data")
		return f"Error connecting to database or reading data: {e}", 500

	if df.empty:
		return render_template("index.html", table="<p>No data available. Run the scraper first.</p>", 
		                       plot_url_bar="", plot_url_pie="", plot_url_dist="",
		                       total_products=0, avg_price=0, max_price=0, min_price=0)

	# Add category labels
	df['category'] = df['source_url'].apply(extract_category_from_url)

	# Calculate stats
	total_products = len(df)
	avg_price = df[df['price'] > 0]['price'].mean() if len(df[df['price'] > 0]) > 0 else 0
	max_price = df['price'].max()
	min_price = df[df['price'] > 0]['price'].min() if len(df[df['price'] > 0]) > 0 else 0

	# --- Chart 1: Average Price by Category (Bar Chart) ---
	fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='#fefbf3')
	ax1.set_facecolor('#faf6f0')
	if "price" in df.columns and "category" in df.columns:
		category_prices = df[df['price'] > 0].groupby("category")["price"].mean().sort_values(ascending=False)
		bars = category_prices.plot(kind="bar", ax=ax1, color=vintage_colors[:len(category_prices)], 
		                            edgecolor='#5d4e37', linewidth=1.5)
		ax1.set_title("Average Price by Category", fontsize=16, fontweight='bold', 
		             pad=20, color='#3e2723', family='serif')
		ax1.set_ylabel("Average Price (₹)", fontsize=12, fontweight='bold', color='#5d4e37')
		ax1.set_xlabel("Category", fontsize=12, fontweight='bold', color='#5d4e37')
		ax1.grid(axis='y', alpha=0.3, linestyle='--', color='#8b6f47')
		ax1.tick_params(colors='#5d4e37')
		plt.xticks(rotation=45, ha="right")
		
		# Add value labels on bars
		for i, v in enumerate(category_prices):
			ax1.text(i, v + max(category_prices) * 0.02, f'₹{v:,.0f}', 
			        ha='center', va='bottom', fontsize=10, fontweight='bold', color='#5d4e37')
		
		plt.tight_layout()

	img1 = io.BytesIO()
	fig1.savefig(img1, format="png", dpi=100, bbox_inches='tight')
	img1.seek(0)
	plot_url_bar = base64.b64encode(img1.getvalue()).decode()
	plt.close(fig1)

	# --- Chart 2: Product Count by Category (Pie Chart) ---
	fig2, ax2 = plt.subplots(figsize=(8, 8), facecolor='#fefbf3')
	category_counts = df.groupby("category").size()
	wedges, texts, autotexts = ax2.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%',
	                                     colors=vintage_colors[:len(category_counts)], startangle=90, 
	                                     textprops={'fontsize': 11, 'fontweight': 'bold', 'color': '#3e2723'},
	                                     wedgeprops={'edgecolor': '#5d4e37', 'linewidth': 1.5})
	ax2.set_title("Product Distribution by Category", fontsize=16, fontweight='bold', 
	             pad=20, color='#3e2723', family='serif')
	
	# Enhance text
	for autotext in autotexts:
		autotext.set_color('#fefbf3')
		autotext.set_fontweight('bold')
	
	plt.tight_layout()

	img2 = io.BytesIO()
	fig2.savefig(img2, format="png", dpi=100, bbox_inches='tight')
	img2.seek(0)
	plot_url_pie = base64.b64encode(img2.getvalue()).decode()
	plt.close(fig2)

	# --- Chart 3: Price Distribution (Histogram) ---
	fig3, ax3 = plt.subplots(figsize=(10, 5), facecolor='#fefbf3')
	ax3.set_facecolor('#faf6f0')
	df_with_price = df[df['price'] > 0]
	if not df_with_price.empty:
		ax3.hist(df_with_price['price'], bins=20, color='#b8860b', edgecolor='#5d4e37', 
		        linewidth=1.5, alpha=0.8)
		ax3.set_title("Price Distribution", fontsize=16, fontweight='bold', 
		             pad=20, color='#3e2723', family='serif')
		ax3.set_xlabel("Price (₹)", fontsize=12, fontweight='bold', color='#5d4e37')
		ax3.set_ylabel("Number of Products", fontsize=12, fontweight='bold', color='#5d4e37')
		ax3.grid(axis='y', alpha=0.3, linestyle='--', color='#8b6f47')
		ax3.tick_params(colors='#5d4e37')
		plt.tight_layout()

	img3 = io.BytesIO()
	fig3.savefig(img3, format="png", dpi=100, bbox_inches='tight')
	img3.seek(0)
	plot_url_dist = base64.b64encode(img3.getvalue()).decode()
	plt.close(fig3)

	# Convert DataFrame to HTML table (top 50 for performance)
	table_html = df.head(50)[['name', 'price', 'rating', 'category', 'scraped_at']].to_html(
		classes="data", index=False, escape=False
	)

	return render_template("index.html", 
	                       table=table_html, 
	                       plot_url_bar=plot_url_bar,
	                       plot_url_pie=plot_url_pie,
	                       plot_url_dist=plot_url_dist,
	                       total_products=total_products,
	                       avg_price=avg_price,
	                       max_price=max_price,
	                       min_price=min_price)


if __name__ == "__main__":
	app.run(debug=True)