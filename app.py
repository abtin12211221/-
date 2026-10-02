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
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.digikala.com/search/?q={encoded_query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('article, div.product-card, div[data-product-id]')
            
            if not items:
                items = soup.find_all('a', href=lambda href: href and '/product/dkp-' in href)

            for item in items[:12]:
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
                    title = title_elem.get_text(strip=True) if title_elem else f"محصول مرتبط با {query}"

                    img_elem = item.find('img')
                    image = img_elem.get('src') or img_elem.get('data-src') if img_elem else "https://via.placeholder.com/200"

                    price_elem = item.select_one('span[data-testid="price"]') or item.find(string=lambda t: t and 'تومان' in t)
                    price = price_elem.get_text(strip=True) if hasattr(price_elem, 'get_text') else "مشاهده قیمت در سایت"

                    if not any(p['link'] == link for p in products):
                        products.append({
                            'title': title,
                            'store': 'دیجی‌کالا',
                            'price': price,
                            'image': image,
                            'link': link
                        })
                except Exception:
                    continue

        # اگر به هر دلیلی اسکرپر محصولی پیدا نکرد، برای جلوگیری از ارور، صفحه جستجوی مستقیم دیجی‌کالا رو برمی‌گردونه
        if not products:
            products.append({
                'title': f'نتایج جستجوی "{query}" در دیجی‌کالا',
                'store': 'دیجی‌کالا',
                'price': 'کلیک کنید',
                'image': 'https://via.placeholder.com/200',
                'link': url
            })

        return jsonify({'status': 'success', 'results': products})
    
    except Exception as e:
        # حتی در صورت بروز خطای سرور هم لینک مستقیم رو به کاربر میدیم تا کارش راه بیفته
        fallback_url = f"https://www.digikala.com/search/?q={urllib.parse.quote(query)}"
        return jsonify({
            'status': 'success', 
            'results': [{
                'title': f'مشاهده نتایج جستجوی "{query}" در دیجی‌کالا',
                'store': 'دیجی‌کالا',
                'price': 'مشاهده',
                'image': 'https://via.placeholder.com/200',
                'link': fallback_url
            }]
        })

if __name__ == '__main__':
    app.run(debug=True)