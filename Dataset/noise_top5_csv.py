import pandas as pd

# Load Noise dataset (parsed from JSON)
noise_data = {
    "products": [
        {"asin": "B0DMDKTQCN", "title": "Smart Watch", "price": 7999, "rating": 4.0, "reviews_count": 18688, "sales_volume": "200+", "is_sponsored": True, "price_strikethrough": 10999, "category": "Smartwatch", "not_available": False},
        {"asin": "B0CQJWMMG7", "title": "True Wireless Earbuds", "price": 999, "rating": 4.1, "reviews_count": 8833, "sales_volume": "3K+", "is_sponsored": True, "price_strikethrough": 3499, "category": "Earbuds", "not_available": False},
        {"asin": "B0BJ72WZQ7", "title": "Smart Watch", "price": 1399, "rating": 4.0, "reviews_count": 17513, "sales_volume": "4K+", "is_sponsored": False, "price_strikethrough": 4999, "category": "Smartwatch", "not_available": False},
        {"asin": "B09Y5MK1KB", "title": "True Wireless Earbuds", "price": 0, "rating": 3.9, "reviews_count": 25968, "sales_volume": "2K+", "is_sponsored": False, "price_strikethrough": None, "category": "Earbuds", "not_available": True},
        {"asin": "B0D4QLT8WG", "title": "True Wireless Earbuds", "price": 1699, "rating": 4.0, "reviews_count": 4507, "sales_volume": "3K+", "is_sponsored": False, "price_strikethrough": 4999, "category": "Earbuds", "not_available": False},
        {"asin": "B0CY2377YW", "title": "Over-Ear Headphones", "price": 2399, "rating": 3.8, "reviews_count": 1611, "sales_volume": "1K+", "is_sponsored": False, "price_strikethrough": 5999, "category": "Headphones", "not_available": False},
        {"asin": "B0D25D74PL", "title": "True Wireless Earbuds", "price": 999, "rating": 3.8, "reviews_count": 4030, "sales_volume": "500+", "is_sponsored": False, "price_strikethrough": 2999, "category": "Earbuds", "not_available": False},
        {"asin": "B0DK979YJ7", "title": "True Wireless Earbuds", "price": 7999, "rating": 3.7, "reviews_count": 455, "sales_volume": "500+", "is_sponsored": False, "price_strikethrough": None, "category": "Earbuds", "not_available": False},
        {"asin": "B0DGV56J6G", "title": "Open Ear Earbuds", "price": 2699, "rating": 3.6, "reviews_count": 1435, "sales_volume": "500+", "is_sponsored": False, "price_strikethrough": 3999, "category": "Earbuds", "not_available": False},
        {"asin": "B0B1PX62WJ", "title": "On-Ear Headphones", "price": 1499, "rating": 3.5, "reviews_count": 3191, "sales_volume": "1K+", "is_sponsored": False, "price_strikethrough": 4999, "category": "Headphones", "not_available": False},
        {"asin": "B09Y5LL6P4", "title": "True Wireless Earbuds", "price": 799, "rating": 3.9, "reviews_count": 25968, "sales_volume": "1K+", "is_sponsored": False, "price_strikethrough": 3499, "category": "Earbuds", "not_available": False},
        {"asin": "B09Y5N4M7Z", "title": "True Wireless Earbuds", "price": 799, "rating": 3.9, "reviews_count": 25968, "sales_volume": "1K+", "is_sponsored": False, "price_strikethrough": 3499, "category": "Earbuds", "not_available": False},
        {"asin": "B0D4QNLF6Y", "title": "True Wireless Earbuds", "price": 1699, "rating": 4.0, "reviews_count": 4507, "sales_volume": "2K+", "is_sponsored": False, "price_strikethrough": 4999, "category": "Earbuds", "not_available": False},
        {"asin": "B0BW5RN77W", "title": "Smart Watch", "price": 1199, "rating": 4.0, "reviews_count": 4228, "sales_volume": "400+", "is_sponsored": False, "price_strikethrough": 6999, "category": "Smartwatch", "not_available": False},
        {"asin": "B0CQ4J4YFL", "title": "Smart Watch", "price": 1699, "rating": 4.0, "reviews_count": 17513, "sales_volume": "1K+", "is_sponsored": False, "price_strikethrough": 5999, "category": "Smartwatch", "not_available": False},
        {"asin": "B0B6BLTGTT", "title": "Smart Watch", "price": 1199, "rating": 4.0, "reviews_count": 16801, "sales_volume": "5K+", "is_sponsored": False, "price_strikethrough": 5999, "category": "Smartwatch", "not_available": False},
        {"asin": "B0BVR7PGQ7", "title": "Smart Watch", "price": 2299, "rating": 4.1, "reviews_count": 17535, "sales_volume": "1K+", "is_sponsored": False, "price_strikethrough": 7999, "category": "Smartwatch", "not_available": False}
    ]
}

# Create DataFrame
df = pd.DataFrame(noise_data["products"])

# Remove unavailable products
df = df[df["not_available"] != True]

# Convert sales_volume to numeric
def parse_sales_volume(volume):
    if pd.isna(volume):
        return 0
    volume = volume.replace("K+", "000").replace("+", "")
    if "K" in volume:
        return int(float(volume.replace("K", "")) * 1000)
    return int(volume)

df["sales_volume_numeric"] = df["sales_volume"].apply(parse_sales_volume)

# Calculate discount percentage
df["discount"] = df.apply(
    lambda x: ((x["price_strikethrough"] - x["price"]) / x["price_strikethrough"] * 100)
    if pd.notnull(x["price_strikethrough"]) and x["price"] > 0 else 0,
    axis=1
)

# Rank products by sales_volume_numeric, then rating, then reviews_count
df["rank_score"] = df["sales_volume_numeric"] * 100 + df["rating"] * 10 + df["reviews_count"] / 1000
top_5 = df.sort_values(by="rank_score", ascending=False).head(5)

# Select columns for CSV
top_5_csv = top_5[["asin", "category", "price", "rating", "reviews_count", "sales_volume_numeric", "discount"]]

# Save to CSV
top_5_csv.to_csv("noise_top5.csv", index=False)

print("CSV file 'noise_top5.csv' generated successfully.")
print("\nCSV Content Preview:")
print(top_5_csv.to_string(index=False))