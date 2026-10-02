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
    
    # استخراج مستقیم محصولات از دیجی‌کالا
    try:
        url = f"https://www.digikala.com/search/?q={encoded_query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        response = requests.get(url, headers=headers, timeout=8)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # جستجو برای پیدا کردن کارت‌های محصولات بر اساس لینک صفحه محصول (dkp)
            product_links = soup.find_all('a', href=lambda href: href and '/product/dkp-' in href)
            
            seen_links = set()
            for a_tag in product_links:
                try:
                    raw_link = a_tag.get('href', '')
                    if not raw_link or '/product/dkp-' not in raw_link:
                        continue
                    
                    link = f"https://www.digikala.com{raw_link}" if raw_link.startswith('/') else raw_link
                    if link in seen_links:
                        continue
                    seen_links.add(link)
                    
                    # پیدا کردن بلوک والد کالا برای استخراج عکس، عنوان و قیمت
                    parent_card = a_tag.find_parent('article') or a_tag.find_parent('div', class_=lambda c: c and ('product' in c.lower() or 'card' in c.lower())) or a_tag
                    
                    # استخراج عنوان محصول
                    title_elem = parent_card.find('h3') or parent_card.find('h4') or parent_card.find('p') or a_tag
                    title = title_elem.get_text(strip=True) if title_elem else f"محصول {query}"
                    if len(title) < 3: # اگر متن تگ لینک خیلی کوتاه بود، از عنوان داخل تگ جستجو می‌کنیم
                        title = a_tag.get_text(strip=True) or f"محصول {query}"
                    
                    # استخراج عکس با کیفیت کالا
                    img_elem = parent_card.find('img')
                    image = ""
                    if img_elem:
                        image = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('srcset', '').split(' ')[0]
                    if not image or 'http' not in image:
                        image = "https://via.placeholder.com/200?text=No+Image"
                    
                    # استخراج قیمت کالا
                    price = "موجود در سایت"
                    price_elem = parent_card.find(string=lambda t: t and 'تومان' in t)
                    if price_elem:
                        price = str(price_elem).strip()
                    
                    products.append({
                        'title': title[:80] + ('...' if len(title) > 80 else ''),
                        'store': 'دیجی‌کالا',
                        'price': price,
                        'image': image,
                        'link': link
                    })
                    
                    if len(products) >= 8: # محدودیت به ۸ محصول برتر برای سرعت بیشتر
                        break
                except Exception:
                    continue
        
        # اگر به هر دلیلی محصولی پیدا نشد، لینک جستجوی کلی قرار داده شود
        if not products:
            fallback_url = f"https://www.digikala.com/search/?q={encoded_query}"
            products.append({
                'title': f'نتایج جستجوی "{query}" در دیجی‌کالا',
                'store': 'دیجی‌کالا',
                'price': 'مشاهده قیمت و خرید',
                'image': 'https://via.placeholder.com/200?text=Digikala',
                'link': fallback_url
            })
            
        return jsonify({'status': 'success', 'results': products})
        
    except Exception as e:
        fallback_url = f"https://www.digikala.com/search/?q={encoded_query}"
        return jsonify({
            'status': 'success',
            'results': [{
                'title': f'مشاهده نتایج جستجوی "{query}" در دیجی‌کالا',
                'store': 'دیجی‌کالا',
                'price': 'مشاهده در سایت',
                'image': 'https://via.placeholder.com/200?text=Digikala',
                'link': fallback_url
            }]
        })

if __name__ == '__main__':
    app.run(debug=True)