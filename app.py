from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'status': 'error', 'message': 'عبارت جستجو خالی است'})

    products = []
    try:
        # جستجو مستقیماً در دیجی‌کالا (همکاران افیلیو)
        url = f"https://www.digikala.com/search/?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # استخراج کارت محصولات دیجی‌کالا
            # ساختار کلاس‌های دیجی‌کالا رو برای محصولات پوشش می‌دیم
            items = soup.select('div.product-card, div[data-product-id]')
            
            for item in items[:12]:  # محدود کردن به 12 محصول برتر
                try:
                    # پیدا کردن عنوان
                    title_elem = item.select_text = item.find('h3') or item.select_one('.text-body-1')
                    title = title_elem.get_text(strip=True) if title_elem else "محصول دیجی‌کالا"
                    
                    # پیدا کردن لینک محصول
                    link_elem = item.find('a', href=True)
                    raw_link = link_elem['href'] if link_elem else "#"
                    if raw_link.startswith('/'):
                        link = f"https://www.digikala.com{raw_link}"
                    else:
                        link = raw_link

                    # پیدا کردن عکس محصول
                    img_elem = item.find('img')
                    image = img_elem.get('src') or img_elem.get('data-src') if img_elem else "https://via.placeholder.com/200"

                    # پیدا کردن قیمت
                    price_elem = item.select_one('.text-h5, span[data-testid="price"]')
                    price = price_elem.get_text(strip=True) if price_elem else "تماس بگیرید"

                    products.append({
                        'title': title,
                        'store': 'دیجی‌کالا (افیلیو)',
                        'price': price,
                        'image': image,
                        'link': link  # لینک مستقیم بدون پسوند اضافه افیلیو
                    })
                except Exception as e:
                    continue

        return jsonify({'status': 'success', 'results': products})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)