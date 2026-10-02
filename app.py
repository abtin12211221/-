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
            
            # جستجوی کارت محصولات در ساختار جدید دیجی‌کالا
            items = soup.select('div.product-list_ProductList__item__LpMY3, article, div[data-product-id]')
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
                    
                    # استخراج عنوان دقیق محصول
                    title_elem = item.find('h3') or item.find('h4') or item.select_one('div[data-testid="title"]') or item.find('span', string=True)
                    title = title_elem.get_text(strip=True) if title_elem else f"محصول {query}"
                    
                    # استخراج تصویر با کیفیت
                    img_elem = item.find('img')
                    image = ""
                    if img_elem:
                        image = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('srcset', '').split(' ')[0]
                    if not image or 'http' not in image:
                        image = "https://via.placeholder.com/200"
                    
                    # استخراج قیمت دقیق از ساختار جدید دیجی‌کالا
                    price = "موجود در سایت"
                    price_container = item.select_one('div[data-testid="price-final"]') or item.select_one('span[data-testid="price"]')
                    if price_container:
                        price = price_container.get_text(strip=True)
                    else:
                        # جستجوی متن حاوی تومان به عنوان پشتیبان
                        price_elem = item.find(string=lambda t: t and 'تومان' in t)
                        if price_elem:
                            price = str(price_elem).strip()
                    
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
        
        # اگر به هر دلیلی آیتمی استخراج نشد، لینک مستقیم جستجو قرار می‌گیرد
        if not products:
            fallback_url = f"https://www.digikala.com/search/?q={encoded_query}"
            products.append({
                'title': f'نتایج جستجوی "{query}" در دیجی‌کالا',
                'store': 'دیجی‌کالا',
                'price': 'مشاهده قیمت و خرید',
                'image': 'https://via.placeholder.com/200',
                'link': fallback_url
            })
            
        return jsonify({'status': 'success', 'results': products})
        
    except Exception as e:
        fallback_url = f"https://www.digikala.com/search/?q={urllib.parse.quote(query)}"
        return jsonify({
            'status': 'success',
            'results': [{
                'title': f'مشاهده نتایج جستجوی "{query}" در دیجی‌کالا',
                'store': 'دیجی‌کالا',
                'price': 'مشاهده در سایت',
                'image': 'https://via.placeholder.com/200',
                'link': fallback_url
            }]
        })

if __name__ == '__main__':
    app.run(debug=True)