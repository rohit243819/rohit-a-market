from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path
from urllib.parse import quote

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "rohit_hub.db"


# =========================================================
# CATEGORIES
# =========================================================

CATEGORIES = [
    "Fashion",
    "Electronics",
    "Home",
    "Beauty",
    "Sports",
    "Grocery",
    "Footwear",
    "Bags",
    "Watches",
    "Accessories"
]


# =========================================================
# 20 PRODUCTS PER CATEGORY
# =========================================================

PRODUCTS = {

    "Fashion": [
        "Classic T-Shirt",
        "Slim Fit Shirt",
        "Casual Shirt",
        "Polo T-Shirt",
        "Formal Shirt",
        "Cotton Kurta",
        "Denim Jacket",
        "Hoodie",
        "Chinos",
        "Cargo Pants",
        "Track Pants",
        "Formal Trousers",
        "Linen Shirt",
        "Graphic T-Shirt",
        "Sweatshirt",
        "Casual Shorts",
        "Denim Shirt",
        "Bomber Jacket",
        "Traditional Kurta",
        "Premium Blazer"
    ],

    "Electronics": [
        "Wireless Earbuds",
        "Bluetooth Speaker",
        "Smartphone",
        "Smartphone Stand",
        "Power Bank",
        "USB-C Cable",
        "Wireless Mouse",
        "Mechanical Keyboard",
        "Laptop Stand",
        "Webcam",
        "Smart LED Bulb",
        "USB Hub",
        "Fast Charger",
        "Gaming Mouse",
        "Gaming Keyboard",
        "Smart Plug",
        "Tablet",
        "Computer Headphones",
        "Portable SSD",
        "Bluetooth Headphones"
    ],

    "Home": [
        "Table Lamp",
        "Wall Clock",
        "Cushion Set",
        "Bedsheet",
        "Pillow Set",
        "Curtains",
        "Storage Box",
        "Laundry Basket",
        "Floor Mat",
        "Kitchen Organizer",
        "Water Bottle",
        "Coffee Mug",
        "Dinner Set",
        "Non Stick Pan",
        "Frying Pan",
        "Glass Set",
        "Serving Tray",
        "Plant Pot",
        "Photo Frame",
        "Desk Organizer"
    ],

    "Beauty": [
        "Face Wash",
        "Moisturizer",
        "Sunscreen",
        "Lip Balm",
        "Face Serum",
        "Body Lotion",
        "Shampoo",
        "Conditioner",
        "Hair Oil",
        "Perfume",
        "Deodorant",
        "Body Wash",
        "Hand Cream",
        "Face Mask",
        "Makeup Brush Set",
        "Compact Powder",
        "Lipstick",
        "Kajal",
        "Nail Polish",
        "Grooming Kit"
    ],

    "Sports": [
        "Running T-Shirt",
        "Running Shorts",
        "Training Shorts",
        "Sports Leggings",
        "Gym Vest",
        "Compression Tights",
        "Track Jacket",
        "Sports Bra",
        "Training Pants",
        "Cycling Jersey",
        "Football Jersey",
        "Basketball Shorts",
        "Yoga Pants",
        "Yoga Top",
        "Running Jacket",
        "Sports Socks",
        "Gym Gloves",
        "Resistance Bands",
        "Sports Cap",
        "Training Hoodie"
    ],

    "Grocery": [
        "Basmati Rice",
        "Wheat Flour",
        "Toor Dal",
        "Moong Dal",
        "Chana Dal",
        "Sugar",
        "Salt",
        "Tea",
        "Coffee",
        "Cooking Oil",
        "Biscuits",
        "Corn Flakes",
        "Oats",
        "Pasta",
        "Noodles",
        "Tomato Ketchup",
        "Peanut Butter",
        "Honey",
        "Dry Fruits",
        "Spices Combo"
    ],

    "Footwear": [
        "Running Shoes",
        "Casual Sneakers",
        "Formal Shoes",
        "Walking Shoes",
        "Sports Shoes",
        "Canvas Shoes",
        "Loafers",
        "Sandals",
        "Flip Flops",
        "Training Shoes",
        "Trekking Shoes",
        "Slip-On Sneakers",
        "Chelsea Boots",
        "Ankle Boots",
        "Ethnic Juttis",
        "Heels",
        "Wedge Sandals",
        "Ballet Flats",
        "Kids Sneakers",
        "House Slippers"
    ],

    "Bags": [
        "Laptop Backpack",
        "Travel Backpack",
        "College Backpack",
        "Tote Bag",
        "Sling Bag",
        "Crossbody Bag",
        "Duffel Bag",
        "Gym Bag",
        "Messenger Bag",
        "Office Bag",
        "Leather Wallet",
        "Card Holder",
        "Travel Pouch",
        "Makeup Bag",
        "School Backpack",
        "Cabin Trolley",
        "Travel Duffle",
        "Mini Backpack",
        "Laptop Sleeve",
        "Waist Bag"
    ],

    "Watches": [
        "Classic Analog Watch",
        "Minimal Watch",
        "Chronograph Watch",
        "Sports Watch",
        "Leather Strap Watch",
        "Mesh Strap Watch",
        "Digital Watch",
        "Smart Watch",
        "Dress Watch",
        "Casual Watch",
        "Automatic Watch",
        "Quartz Watch",
        "Kids Watch",
        "Women's Watch",
        "Men's Watch",
        "Dual Time Watch",
        "Pilot Watch",
        "Diver Style Watch",
        "Fitness Watch",
        "Premium Watch"
    ],

    "Accessories": [
        "Sunglasses",
        "Leather Belt",
        "Baseball Cap",
        "Wallet",
        "Keychain",
        "Phone Case",
        "Laptop Sleeve",
        "Travel Organizer",
        "Passport Holder",
        "Card Holder",
        "Scarf",
        "Tie",
        "Bow Tie",
        "Hair Band",
        "Hair Clips",
        "Bracelet",
        "Necklace",
        "Earrings",
        "Ring",
        "Gift Set"
    ]
}


# =========================================================
# PRICES
# =========================================================

BASE_PRICES = {
    "Fashion": 699,
    "Electronics": 999,
    "Home": 299,
    "Beauty": 249,
    "Sports": 499,
    "Grocery": 99,
    "Footwear": 799,
    "Bags": 599,
    "Watches": 999,
    "Accessories": 199
}


# =========================================================
# CATEGORY IMAGES
# =========================================================

CATEGORY_IMAGES = {
    "Fashion": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=700&q=80",
    "Electronics": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=700&q=80",
    "Home": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=700&q=80",
    "Beauty": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=700&q=80",
    "Sports": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=700&q=80",
    "Grocery": "https://images.unsplash.com/photo-1542838132-92c53300491e?w=700&q=80",
    "Footwear": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700&q=80",
    "Bags": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=700&q=80",
    "Watches": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=700&q=80",
    "Accessories": "https://images.unsplash.com/photo-1523779917675-b6ed3a42a561?w=700&q=80"
}


# =========================================================
# DATABASE
# =========================================================

def get_db():

    connection = sqlite3.connect(DB_FILE)

    connection.row_factory = sqlite3.Row

    return connection


def create_products():

    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS products (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            category TEXT NOT NULL,

            price INTEGER NOT NULL,

            rating REAL NOT NULL,

            image TEXT NOT NULL,

            google_url TEXT NOT NULL

        )
    """)

    count = connection.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    if count == 0:

        for category in CATEGORIES:

            base_price = BASE_PRICES[category]

            for number, name in enumerate(
                PRODUCTS[category],
                start=1
            ):

                price = (
                    base_price
                    + ((number * 137) % 1800)
                )

                rating = round(
                    4.0 + ((number * 7) % 10) / 10,
                    1
                )

                search_query = quote(
                    f"{name} {category}"
                )

                google_url = (
                    "https://www.google.com/search"
                    "?tbm=isch&q="
                    + search_query
                )

                image_url = (
                    CATEGORY_IMAGES[category]
                )

                connection.execute(
                    """
                    INSERT INTO products
                    (
                        name,
                        category,
                        price,
                        rating,
                        image,
                        google_url
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        name,
                        category,
                        price,
                        rating,
                        image_url,
                        google_url
                    )
                )

    connection.commit()

    connection.close()


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        categories=CATEGORIES
    )


# =========================================================
# PRODUCTS API
# =========================================================

@app.route("/api/products")
def products_api():

    category = request.args.get(
        "category",
        ""
    )

    search = request.args.get(
        "search",
        ""
    ).strip()


    connection = get_db()


    query = """
        SELECT *
        FROM products
        WHERE 1=1
    """


    parameters = []


    if category:

        query += """
            AND category = ?
        """

        parameters.append(
            category
        )


    if search:

        query += """
            AND (
                name LIKE ?
                OR category LIKE ?
            )
        """

        search_value = (
            "%" +
            search +
            "%"
        )

        parameters.append(
            search_value
        )

        parameters.append(
            search_value
        )


    query += """
        ORDER BY id
    """


    products = connection.execute(
        query,
        parameters
    ).fetchall()


    connection.close()


    return jsonify([
        dict(product)
        for product in products
    ])


# =========================================================
# CHECKOUT
# =========================================================

@app.route("/checkout")
def checkout():

    return render_template(
        "checkout.html"
    )


# =========================================================
# PAYMENT
# =========================================================

@app.route("/payment")
def payment():

    return render_template(
        "payment.html"
    )


# =========================================================
# SUCCESS
# =========================================================

@app.route("/order-success")
def order_success():

    return render_template(
        "order_success.html"
    )


# =========================================================
# START
# =========================================================

# if __name__ == "__main__":
#
#     create_products()
#
#     app.run(
#         debug=True
#     )

if __name__ == "__main__":

    create_products()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )