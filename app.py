from flask import Flask, render_template, request

app = Flask(__name__)

GLOBAL_PRODUCTS_DATABASE = [
    {
        "id": 1,
        "name": "Apple iPhone 15 Pro Max",
        "category": "موبایل",
        "use_case": "عکاسی حرفه‌ای، گیمینگ، پردازش سنگین",
        "image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=500&auto=format&fit=crop&q=60",
        "countries": {
            "USA": {
                "currency": "$",
                "currency_name": "دلار",
                "price_prediction": "📉 پیش‌بینی هوش مصنوعی: نزدیک رویداد بعدی اپل، قیمت حدود ۵۰ دلار کاهش می‌یابد.",
                "used_price": 950,
                "stores": [
                    {"name": "Amazon US", "price": 1199, "shipping": 0, "trusted": True},
                    {"name": "Best Buy", "price": 1199, "shipping": 15, "trusted": True},
                    {"name": "eBay (Refurbished)", "price": 999, "shipping": 10, "trusted": True}
                ]
            },
            "UAE": {
                "currency": "AED",
                "currency_name": "درهم",
                "price_prediction": "🔥 فرصت عالی: معافیت مالیاتی فصلی در دبی، بهترین زمان خرید!",
                "used_price": 3600,
                "stores": [
                    {"name": "Amazon AE", "price": 4399, "shipping": 0, "trusted": True},
                    {"name": "Noon", "price": 4350, "shipping": 20, "trusted": True},
                    {"name": "Sharaf DG", "price": 4499, "shipping": 0, "trusted": True}
                ]
            },
            "Iran": {
                "currency": "تومان",
                "currency_name": "تومان",
                "price_prediction": "📈 پیش‌بینی هوش مصنوعی: قیمت نوسان محدود دارد؛ خرید در این هفته منطقی است.",
                "used_price": 62000000,
                "stores": [
                    {"name": "دیجی‌کالا", "price": 74500000, "shipping": 60000, "trusted": True},
                    {"name": "تکنولایف", "price": 73900000, "shipping": 0, "trusted": True},
                    {"name": "کالایاب", "price": 75000000, "shipping": 0, "trusted": True}
                ]
            }
        }
    }
]

@app.route("/", methods=["GET", "POST"])
def index():
    search_query = ""
    selected_country = "Iran"
    matched_product = None
    country_data = None
    ai_advice = ""
    
    if request.method == "POST":
        search_query = request.form.get("query", "").strip()
        selected_country = request.form.get("country", "Iran").strip()
        
        if search_query:
            for prod in GLOBAL_PRODUCTS_DATABASE:
                if search_query.lower() in prod["name"].lower() or search_query in prod["category"]:
                    matched_product = prod.copy()
                    break
            
            if matched_product and selected_country in matched_product["countries"]:
                country_data = matched_product["countries"][selected_country]
                for store in country_data["stores"]:
                    store["total_price"] = store["price"] + store["shipping"]
                country_data["stores"] = sorted(country_data["stores"], key=lambda x: x["total_price"])
                for i, store in enumerate(country_data["stores"]):
                    store["is_cheapest"] = (i == 0)
                ai_advice = f"تحلیل هوش مصنوعی برای بازار {selected_country}: این کالا برای کاربرد «{matched_product['use_case']}» مناسب است. قیمت مدل دست‌دوم تمیز در این منطقه حدود {format(country_data['used_price'], ',')} {country_data['currency_name']} است."

    return render_template("index.html", 
                           product=matched_product, 
                           country_data=country_data, 
                           query=search_query, 
                           selected_country=selected_country,
                           ai_advice=ai_advice)

if __name__ == "__main__":
    app.run(debug=True)
    