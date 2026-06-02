import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# Config
stores = {
    1: "Astoria",
    2: "Hell's Kitchen",
    3: "Lower Manhattan"
}

product_catalog = [
    ("Coffee", "Brewed Coffee", "House Blend"),
    ("Coffee", "Brewed Coffee", "Dark Roast"),
    ("Coffee", "Brewed Coffee", "Ethiopian Single Origin"),
    ("Coffee", "Espresso", "Double Shot"),
    ("Coffee", "Espresso", "Ristretto"),
    ("Coffee", "Latte", "Vanilla Latte"),
    ("Coffee", "Latte", "Oat Milk Latte"),
    ("Coffee", "Cappuccino", "Classic Cappuccino"),
    ("Coffee", "Cold Brew", "Nitro Cold Brew"),
    ("Coffee", "Cold Brew", "Classic Cold Brew"),
    ("Tea", "Brewed Tea", "English Breakfast"),
    ("Tea", "Brewed Tea", "Green Tea"),
    ("Tea", "Chai", "Masala Chai Latte"),
    ("Bakery", "Pastry", "Butter Croissant"),
    ("Bakery", "Pastry", "Almond Croissant"),
    ("Bakery", "Muffin", "Blueberry Muffin"),
    ("Bakery", "Muffin", "Chocolate Chip Muffin"),
    ("Drinking Chocolate", "Hot Chocolate", "Classic Dark"),
    ("Drinking Chocolate", "Hot Chocolate", "Spiced Mocha"),
    ("Packaged Chocolate", "Retail Bar", "72% Dark"),
    ("Coffee Beans", "Retail Bag", "Ethiopian 250g"),
    ("Coffee Beans", "Retail Bag", "Colombian 250g"),
]

unit_prices = {
    "Brewed Coffee": 3.50,
    "Espresso": 2.75,
    "Latte": 5.25,
    "Cappuccino": 4.75,
    "Cold Brew": 5.50,
    "Brewed Tea": 3.00,
    "Chai": 4.50,
    "Pastry": 4.25,
    "Muffin": 3.75,
    "Hot Chocolate": 4.50,
    "Retail Bar": 6.00,
    "Retail Bag": 14.00,
}

def hour_weight(hour, store_id):
    # Different patterns per store
    base = [0.1, 0.05, 0.02, 0.01, 0.01, 0.02, 0.5, 2.5, 3.5, 2.8, 2.0, 1.8,
            1.5, 1.2, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.15]
    if store_id == 2:  # Hell's Kitchen - stronger evening
        evening_boost = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0.3, 0.5, 0.4, 0.3, 0.2, 0.1, 0, 0]
        return base[hour] + evening_boost[hour]
    elif store_id == 3:  # Lower Manhattan - stronger morning rush
        morning_boost = [0, 0, 0, 0, 0, 0, 0, 0.5, 1.0, 0.5, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        return base[hour] + morning_boost[hour]
    return base[hour]

def day_weight(dow):
    # 0=Mon, 6=Sun
    weights = [1.0, 1.0, 1.1, 1.0, 1.2, 0.9, 0.8]
    return weights[dow]

records = []
transaction_id = 1
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 6, 30)

current_date = start_date
while current_date <= end_date:
    dow = current_date.weekday()
    for store_id, store_location in stores.items():
        # Base transactions per day per store
        base_txns = int(np.random.normal(180, 20) * day_weight(dow))
        base_txns = max(80, base_txns)

        hour_weights = [hour_weight(h, store_id) for h in range(24)]
        hour_probs = np.array(hour_weights) / sum(hour_weights)

        hours_chosen = np.random.choice(range(24), size=base_txns, p=hour_probs)

        for hour in hours_chosen:
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            t = f"{hour:02d}:{minute:02d}:{second:02d}"

            product = random.choice(product_catalog)
            p_cat, p_type, p_detail = product
            price = unit_prices[p_type] * random.uniform(0.95, 1.05)
            price = round(price, 2)
            qty = np.random.choice([1, 2, 3], p=[0.75, 0.20, 0.05])
            pid = product_catalog.index(product) + 1

            records.append({
                "transaction_id": transaction_id,
                "year": 2025,
                "transaction_date": current_date.strftime("%Y-%m-%d"),
                "transaction_time": t,
                "transaction_qty": qty,
                "unit_price": price,
                "store_id": store_id,
                "store_location": store_location,
                "product_id": pid,
                "product_category": p_cat,
                "product_type": p_type,
                "product_detail": p_detail,
            })
            transaction_id += 1

    current_date += timedelta(days=1)

df = pd.DataFrame(records)
df.to_csv("/home/claude/afficionado_coffee_sales.csv", index=False)
print(f"Dataset generated: {len(df)} rows")
print(df.head())
print(df.dtypes)
