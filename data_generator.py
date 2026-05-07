#EDA Project

# Step 1: Import libraries
import pandas as pd 
import numpy as np
import random 
from faker import Faker
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Initialize Faker for generating fake data
fake = Faker()

# Step 2: Define base lists

categories = {
    "Electronics":    ["Smartphone", "Laptop", "Tablet", 
                       "Earbuds", "Smartwatch", "Charger"],
    "Fashion":        ["T-Shirt", "Jeans", "Kurti", 
                       "Sneakers", "Saree", "Jacket"],
    "Home & Kitchen": ["Mixer Grinder", "Pressure Cooker", 
                       "Bedsheet", "Curtains", "Air Fryer"],
    "Books":          ["Fiction Novel", "Self-Help Book", 
                       "Textbook", "Comic Book", "Biography"],
    "Beauty":         ["Face Wash", "Moisturiser", "Lipstick", 
                       "Sunscreen", "Hair Oil"],
    "Sports":         ["Yoga Mat", "Dumbbells", "Cricket Bat", 
                       "Badminton Racket", "Skipping Rope"],
    "Grocery":        ["Organic Rice", "Olive Oil", 
                       "Protein Powder", "Green Tea", "Dry Fruits"],
    "Toys":           ["LEGO Set", "Remote Car", "Barbie Doll", 
                       "Board Game", "Puzzle"],
}

# Intentional messiness in payment & delivery
payment_methods = ["Credit Card", "Debit Card", "UPI", 
                   "Net Banking", "Cash on Delivery",
                   "credit card", "upi", "COD", "Debit card"]

order_statuses = ["Delivered", "Shipped", "Cancelled", 
                  "Returned", "Pending"]

# Carriers mapped to country
carrier_map = {
    "India":     ["BlueDart", "Delhivery", "DTDC", "Ekart", "FedEx"],
    "USA":       ["FedEx", "UPS", "USPS", "DHL"],
    "UK":        ["Royal Mail", "DHL", "Parcelforce", "Evri"],
    "Australia": ["Australia Post", "DHL", "StarTrack", "Couriers Please"],
    "Canada":    ["Canada Post", "FedEx", "UPS", "Purolator"],
    "UAE":       ["Aramex", "DHL", "FedEx", "Emirates Post"],
}

# Warehouse mapped to country
warehouse_map = {
    "India":     ["Mumbai Hub", "Delhi Hub", "Bengaluru Hub", "Kolkata Hub", "Chennai Hub"],
    "USA":       ["New York Hub", "Los Angeles Hub", "Texas Hub"],
    "UK":        ["London Hub", "Manchester Hub"],
    "Australia": ["Sydney Hub", "Melbourne Hub"],
    "Canada":    ["Toronto Hub", "Vancouver Hub"],
    "UAE":       ["Dubai Hub", "Abu Dhabi Hub"],
}

loyalty_tiers = ["Bronze", "Silver", "Gold", "Platinum"]

sentiments = ["Positive", "Neutral", "Negative", None]


# Messy gender values intentionally
gender_pool = ["Male", "Female", "male", "female", 
               "M", "F", "Other"]


express_delivery = ["Yes", "No", "yes", "no"]  
# inconsistency

# Step 3:Generate dataset
STATES_CITIES = {
    # India
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
    "Karnataka":   ["Bengaluru", "Mysuru", "Hubli", "Mangaluru"],
    "Tamil Nadu":  ["Chennai", "Coimbatore", "Madurai", "Salem"],
    "Delhi":       ["New Delhi", "Dwarka", "Rohini", "Saket"],
    # USA
    "California":  ["Los Angeles", "San Francisco", "San Diego", "Sacramento"],
    "New York":    ["New York City", "Buffalo", "Albany", "Syracuse"],
    "Texas":       ["Houston", "Dallas", "Austin", "San Antonio"],
    # UK
    "England":     ["London", "Manchester", "Birmingham", "Liverpool"],
    "Scotland":    ["Edinburgh", "Glasgow", "Aberdeen", "Dundee"],
    # Australia
    "New South Wales": ["Sydney", "Newcastle", "Wollongong", "Canberra"],
    "Victoria":        ["Melbourne", "Geelong", "Ballarat", "Bendigo"],
    # Canada
    "Ontario":          ["Toronto", "Ottawa", "Hamilton", "London"],
    "British Columbia": ["Vancouver", "Victoria", "Kelowna", "Surrey"],
    # UAE
    "Dubai":     ["Downtown Dubai", "Deira", "Bur Dubai", "Jumeirah"],
    "Abu Dhabi": ["Al Ain", "Khalifa City", "Musaffah", "Yas Island"],
}

# Every state mapped to correct country
country_map = {
    # India
    "Maharashtra": "India",
    "Karnataka":   "India",
    "Tamil Nadu":  "India",
    "Delhi":       "India",
    # USA
    "California":  "USA",
    "New York":    "USA",
    "Texas":       "USA",
    # UK
    "England":     "UK",
    "Scotland":    "UK",
    # Australia
    "New South Wales": "Australia",
    "Victoria":        "Australia",
    # Canada
    "Ontario":          "Canada",
    "British Columbia": "Canada",
    # UAE
    "Dubai":     "UAE",
    "Abu Dhabi": "UAE",
}

records = []  # Empty list to store all rows

for i in range(1100):  # 1100 fake orders

    # Customer Info
    order_id      = f"ORD{100000 + i}"
    customer_name = fake.name()
    customer_id   = f"CUST{random.randint(1000, 9999)}"
    age           = random.randint(18, 65)
    gender        = random.choice(gender_pool)
    email         = fake.email()

    # Location
    state   = random.choice(list(STATES_CITIES.keys()))
    city    = random.choice(STATES_CITIES[state])
    country = country_map[state]       
    pincode = random.randint(100000, 999999)

    # Order Info
    order_date    = fake.date_between(start_date='-2y', end_date='today')
    delivery_days = random.randint(1, 15)
    delivery_date = order_date + pd.Timedelta(days=delivery_days)
    order_status  = random.choice(order_statuses)
    if order_status in ["Cancelled", "Pending"]:
        delivery_date = None

    category     = random.choice(list(categories.keys()))
    product_name = random.choice(categories[category])
    quantity     = random.randint(1, 10)

    # Financial
    unit_price = round(random.uniform(50, 80000), 2)
    if random.random() < 0.03:  # outliers
        unit_price = round(random.uniform(200000, 500000), 2)
    discount    = random.choice([0, 5, 10, 15, 20, 25, 30, None])
    total_price = round(unit_price * quantity * (1 - (discount or 0) / 100), 2)
    payment_method = random.choice(payment_methods)

    # Delivery — all matched to country ✅
    shipping_carrier = random.choice(carrier_map[country])
    express          = random.choice(express_delivery)
    warehouse        = random.choice(warehouse_map[country])

    # Feedback
    rating           = round(random.uniform(1, 5), 1) if random.random() > 0.20 else None
    sentiment        = random.choice(sentiments)
    return_requested = random.choice(["Yes", "No"])
    loyalty_tier     = random.choice(loyalty_tiers)

    # Append row as a dictionary
    records.append({
        "order_id":              order_id,
        "customer_id":           customer_id,
        "customer_name":         customer_name,
        "age":                   age,
        "gender":                gender,
        "email":                 email,
        "city":                  city,
        "state":                 state,
        "pincode":               pincode,
        "country":               country,
        "order_date":            order_date,
        "delivery_date":         delivery_date,
        "order_status":          order_status,
        "product_category":      category,
        "product_name":          product_name,
        "quantity":              quantity,
        "unit_price":            unit_price,
        "total_price":           total_price,
        "discount_%":            discount,
        "payment_method":        payment_method,
        "shipping_carrier":      shipping_carrier,
        "delivery_days":         delivery_days,
        "express_delivery":      express,
        "warehouse_location":    warehouse,
        "rating":                rating,
        "review_sentiment":      sentiment,
        "return_requested":      return_requested,
        "customer_loyalty_tier": loyalty_tier,
    })

# Step 4: Create dataframe and save to csv

df = pd.DataFrame(records)
df = pd.concat([df, df.sample(n=50, random_state=7)], ignore_index=True)
try:
    df.to_csv("Ecommerce_orders.csv", index=False)
    print("✅ Dataset generated successfully! file saved as 'Ecommerce_orders.csv'")
except PermissionError:
    print("⚠️ Please close the file 'Ecommerce_orders.csv' if it's open in Excel or Power BI, and try again.")
    