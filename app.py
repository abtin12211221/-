import os
import sqlite3
from flask import Flask, render_template_string, request, send_from_directory

app = Flask(__name__)

# پوشه تصاویر
IMAGE_FOLDER = "arzoonjou_images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# قالب HTML زیبا با ظاهر نارنجی و مدرن
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ارزون‌جو | تخفیف‌های ناب افیلیت</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Vazirmatn', sans-serif; background-color: #f8fafc; }
    </style>
</head>
<body class="bg-slate-50 min-h-screen">
    <!-- هدر سایت -->
    <header class="bg-orange-500 text-white shadow-md py-4 px-6 mb-8">
        <div class="container mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
            <h1 class="text-2xl font-bold tracking-wide">🔥 ارزون‌جو (تخفیف‌های ویژه)</h1>
            <form method="GET" action="/" class="flex w-full md:w-1/3">
                <input type="text" name="q" value="{{ search_query }}" placeholder="جستجوی محصول..." class="w-full px-4 py-2 rounded-r-lg text-slate-800 bg-white focus:outline-none">
                <button type="submit" class="bg-slate-900 px-5 py-2 rounded-l-lg hover:bg-slate-800 transition">بگرد</button>
            </form>
        </div>
    </header>

    <!-- محتوای اصلی -->
    <main class="container mx-auto px-4 pb-12">
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {% for product in products %}
            <div class="bg-white rounded-xl shadow-sm hover:shadow-md transition overflow-hidden border border-slate-100 flex flex-col justify-between">
                <div>
                    {% if product[3] %}
                    <img src="/{{ product[3] }}" alt="{{ product[1] }}" class="w-full h-48 object-cover">
                    {% else %}
                    <div class="w-full h-48 bg-slate-200 flex items-center justify-center text-slate-400">بدون تصویر</div>
                    {% endif %}
                    <div class="p-4">
                        <h2 class="font-bold text-slate-800 text-sm line-clamp-2 mb-2">{{ product[1] }}</h2>
                        <p class="text-orange-600 font-bold text-base mb-4">{{ product[2] }}</p>
                    </div>
                </div>
                <div class="p-4 pt-0">
                    <a href="{{ product[4] }}" target="_blank" class="block w-full text-center bg-orange-500 hover:bg-orange-600 text-white py-2 rounded-lg font-bold transition">خرید مستقیم</a>
                </div>
            </div>
            {% else %}
            <div class="col-span-full text-center py-16 text-slate-400">
                <p class="text-lg">محصولی یافت نشد. لطفاً اسکرپر را اجرا کنید.</p>
            </div>
            {% endfor %}
        </div>
    </main>
</body>
</html>
"""

def get_db():
    conn = sqlite3.connect("arzoonjou.db")
    return conn

@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    conn = get_db()
    cursor = conn.cursor()
    
    if query:
        cursor.execute("SELECT id, title, price, image_path, affiliate_link FROM products WHERE title LIKE ?", (f"%{query}%",))
    else:
        cursor.execute("SELECT id, title, price, image_path, affiliate_link FROM products")
        
    products = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, products=products, search_query=query)

@app.route(f"/{IMAGE_FOLDER}/<path:filename>")
def downloaded_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    