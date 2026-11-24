
import random

from db.session import SessionLocal, engine
from db.models import Base, Product, Review, CompetitorPrice


# Category-wise product catalogue
products = {
    "clothing": [
        ("Men's Cotton T-Shirt", 699, "cotton, regular fit, breathable"),
        ("Women's Denim Jeans", 1499, "denim, slim fit, stretchable"),
        ("Men's Running Jacket", 1999, "polyester, lightweight, water resistant"),
        ("Women's Summer Dress", 1299, "floral, cotton, casual wear"),
        ("Unisex Hoodie", 1599, "fleece, warm, adjustable hood"),
        ("Sports Shoes", 2499, "mesh, lightweight, cushioned sole"),
        ("Formal Shirt", 1199, "cotton blend, slim fit, wrinkle resistant"),
        ("Leather Wallet", 899, "genuine leather, compact, multiple slots"),
    ],

    "electronics": [
        ("Wireless Earbuds X1", 2999, "wireless, noise cancellation, long battery"),
        ("Smart Watch S2", 4999, "fitness tracking, AMOLED, waterproof"),
        ("Gaming Mouse G5", 1499, "RGB, ergonomic, programmable buttons"),
        ("Laptop Stand Pro", 1999, "aluminium, adjustable, lightweight"),
        ("Bluetooth Speaker B3", 3499, "portable, waterproof, stereo sound"),
        ("Mechanical Keyboard K2", 3999, "RGB, mechanical switches, USB-C"),
        ("Power Bank 20000mAh", 1799, "fast charging, portable, high capacity"),
        ("HD Webcam C1", 2299, "1080p, autofocus, noise reduction"),
    ],

    "food": [
        ("Organic Almonds 500g", 599, "organic, protein rich, unsalted"),
        ("Dark Chocolate 70%", 249, "70% cocoa, antioxidant rich, vegetarian"),
        ("Peanut Butter 1kg", 399, "high protein, no added sugar, creamy"),
        ("Green Tea Pack", 299, "natural, antioxidant rich, caffeine"),
        ("Organic Honey 500g", 449, "natural, unprocessed, pure"),
        ("Rolled Oats 1kg", 199, "whole grain, high fibre, healthy"),
        ("Protein Granola 500g", 499, "high protein, nuts, whole grain"),
        ("Cold Pressed Coconut Oil", 349, "natural, cold pressed, multipurpose"),
    ]
}


# Category-specific review data
review_data = {
    "clothing": {
        "positive": [
            "great fabric quality",
            "comfortable fitting",
            "excellent stitching",
            "good value for money",
            "looks stylish",
            "perfect size and fit"
        ],
        "negative": [
            "poor fabric quality",
            "size was incorrect",
            "colour faded after washing",
            "stitching came apart",
            "not worth the price",
            "delivery was delayed"
        ]
    },

    "electronics": {
        "positive": [
            "excellent performance",
            "great battery life",
            "amazing build quality",
            "easy to set up",
            "works perfectly",
            "worth the price"
        ],
        "negative": [
            "battery drains quickly",
            "stopped working after a month",
            "bluetooth keeps disconnecting",
            "poor build quality",
            "overheating issue",
            "not worth the price"
        ]
    },

    "food": {
        "positive": [
            "great taste and quality",
            "fresh and delicious",
            "good packaging",
            "excellent nutritional value",
            "worth the price",
            "good product quality"
        ],
        "negative": [
            "poor taste",
            "product was not fresh",
            "packaging was damaged",
            "quality was disappointing",
            "quantity was less than expected",
            "near expiry product received"
        ]
    }
}


competitors = ["CompA", "CompB", "CompC"]

Base.metadata.create_all(engine)

with SessionLocal() as session:

    for category, category_products in products.items():

        for name, price, features in category_products:

            product = Product(
                name=name,
                category=category,
                base_price=price,
                features=features
            )

            session.add(product)
            session.flush()  # Generate product ID

            # Generate 30 random reviews per product
            for _ in range(30):

                positive = random.random() < 0.6

                review_list = review_data[category]

                review_text = (
                    random.choice(
                        review_list["positive"]
                        if positive
                        else review_list["negative"]
                    )
                    + ". "
                    + random.choice(
                        review_list["positive"]
                        if positive
                        else review_list["negative"]
                    )
                )

                rating = (
                    random.randint(4, 5)
                    if positive
                    else random.randint(1, 3)
                )

                session.add(
                    Review(
                        product_id=product.id,
                        rating=rating,
                        text=review_text
                    )
                )

            # Generate competitor prices
            for competitor in competitors:

                competitor_price = round(
                    price * random.uniform(0.85, 1.15), 2
                )

                session.add(
                    CompetitorPrice(
                        product_id=product.id,
                        competitor_name=competitor,
                        price=competitor_price
                    )
                )

    session.commit()

print("E-commerce sample data generated successfully!")
