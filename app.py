from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib.parse

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
    encoded_query = urllib.parse.quote(query)
    
    # ۱. جستجو و استخراج هوشمند از دیجی‌کالا
    try:
        url = f"https://www.digikala.com/search/?q={encoded_query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        response = requests.get(url, headers=headers, timeout=6)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('div.product-list_ProductList__item__LpMY3, article, div[data-product-id]')
            if not items:
                items = soup.find_all('a', href=lambda href: href and '/product/dkp-' in href)
            
            for item in items[:4]:
                try:
                    if item.name == 'a':
                        link_elem = item
                    else:
                        link_elem = item.find('a', href=True)
                    raw_link = link_elem['href'] if link_elem else ""
                    if not raw_link or '/product/dkp-' not in raw_link:
                        continue
                    link = f"https://www.digikala.com{raw_link}" if raw_link.startswith('/') else raw_link
                    
                    title_elem = item.find('h3') or item.find('h4') or item.select_one('div[data-testid="title"]')
                    title = title_elem.get_text(strip=True) if title_elem else f"محصول {query}"
                    
                    img_elem = item.find('img')
                    image = ""
                    if img_elem:
                        image = img_elem.get('src') or img_elem.get('data-src') or ""
                    if not image or 'http' not in image:
                        image = "https://via.placeholder.com/200"
                    
                    price_container = item.select_one('div[data-testid="price-final"]') or item.select_one('span[data-testid="price"]')
                    price = price_container.get_text(strip=True) if price_container else "مشاهده قیمت"
                    
                    products.append({
                        'title': title,
                        'store': 'دیجی‌کالا',
                        'price': price,
                        'image': image,
                        'link': link
                    })
                except Exception:
                    continue
    except Exception:
        pass

    # ۲. افزودن نتایج مستقیم برای تمام سایت‌های مرجع بازار (ترب، ایمالز، تکنولایف، باسلام)
    all_stores = [
        {
            'name': 'ترب',
            'url': f"https://torob.com/search/?query={encoded_query}",
            'image': 'https://via.placeholder.com/200?text=Torob'
        },
        {
            'name': 'ایمالز',
            'url': f"https://emalls.ir/مشخصات_{encoded_query}",
            'image': 'https://via.placeholder.com/200?text=Emalls'
        },
        {
            'name': 'تکنولایف',
            'url': f"https://www.technolife.ir/product/list?search={encoded_query}",
            'image': 'https://via.placeholder.com/200?text=Technolife'
        },
        {
            'name': 'باسلام',
            'url': f"https://basalam.com/search?q={encoded_query}",
            'image': 'https://via.placeholder.com/200?text=Basalam'
        },
        {
            'name': 'دیجی‌کالا',
            'url': f"https://www.digikala.com/search/?q={encoded_query}",
            'image': 'https://via.placeholder.com/200?text=Digikala'
        }
    ]

    for store in all_stores:
        products.append({
            'title': f'جستجوی کامل و مقایسه قیمت "{query}" در {store["name"]}',
            'store': store['name'],
            'price': 'مشاهده لیست قیمت‌ها',
            'image': store['image'],
            'link': store['url']
        })

    return jsonify({'status': 'success', 'results': products})

if __name__ == '__main__':
    app.run(debug=True)