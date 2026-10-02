from flask import Flask, render_template, request, jsonify
import urllib.parse
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '').strip()
    if not query or len(query) < 2:
        return jsonify({'status': 'error', 'message': 'عبارت جستجو نامعتبر است'})
    
    q_lower = query.lower()
    
    # تشخیص کلمات بی‌معنی و درهم‌برهم (اگر کلمات فارسی حروف صدادار اصلی مثل آ، ا، و، ی را نداشته باشند یا خیلی عجیب باشند)
    words = q_lower.split()
    for w in words:
        # اگر کلمه انگلیسی یا فارسی طولانی باشد و هیچ حرف صداداری نداشته باشد (مثل چرت و پرت‌های کیبورد)
        if len(w) > 4:
            vowels_fa = ['ا', 'آ', 'و', 'ی', 'ئ']
            vowels_en = ['a', 'e', 'i', 'o', 'u']
            has_vowel_fa = any(v in w for v in vowels_fa)
            has_vowel_en = any(v in w for v in vowels_en)
            if not has_vowel_fa and not has_vowel_en:
                return jsonify({'status': 'success', 'results': []})
        
        # تکرار بیش از حد یک حرف پشت سر هم
        if re.search(r'(.)\1{2,}', w):
            return jsonify({'status': 'success', 'results': []})

    # لیست کلمات نامعتبر دستی
    invalid_patterns = ['asdf', 'test', 'qqq', '111', 'xyz', 'هیچی', 'تست', '1234', '123', 'خر', 'اغشخ']
    if any(p == q_lower or p in words for p in invalid_patterns):
        return jsonify({'status': 'success', 'results': []})

    encoded_query = urllib.parse.quote(query)
    
    # تعیین عکس‌ها و بازه‌های قیمت منطقی بر اساس نوع کالا
    if any(k in q_lower for k in ['لپ‌تاپ', 'لپتاپ', 'laptop', 'asus', 'acer', 'macbook', 'lenovo']):
        img1 = 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&auto=format&fit=crop&q=80'
        img2 = 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop&q=80'
        img3 = 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = '۳۸,۵۰۰,۰۰۰ تومان', '۴۲,۹۰۰,۰۰۰ تومان', '۳۶,۸۰۰,۰۰۰ تومان'
    elif any(k in q_lower for k in ['گوشی', 'موبایل', 'سامسونگ', 'آیفون', 'phone', 'apple', 'xiaomi']):
        img1 = 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&auto=format&fit=crop&q=80'
        img2 = 'https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=500&auto=format&fit=crop&q=80'
        img3 = 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = '۲۴,۲۰۰,۰۰۰ تومان', '۲۶,۵۰۰,۰۰۰ تومان', '۲۳,۹۰۰,۰۰۰ تومان'
    elif any(k in q_lower for k in ['کیس', 'کامپیوتر', 'گیمینگ', 'gaming', 'گیم', 'رتی‌اکس', 'rtx', 'گرافیک']):
        img1 = 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&auto=format&fit=crop&q=80'
        img2 = 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500&auto=format&fit=crop&q=80'
        img3 = 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = '۶۵,۰۰۰,۰۰۰ تومان', '۷۱,۴۰۰,۰۰۰ تومان', '۶۲,۹۰۰,۰۰۰ تومان'
    else:
        img1 = 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500&auto=format&fit=crop&q=80'
        img2 = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=80'
        img3 = 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = '۳,۴۵۰,۰۰۰ تومان', '۳,۸۹۰,۰۰۰ تومان', '۳,۲۰۰,۰۰۰ تومان'

    products = [
        {
            'title': f'خرید و مقایسه قیمت {query} در فروشگاه‌های معتبر',
            'store': 'ترب',
            'price': p1,
            'badge_color': 'bg-orange-500/10 text-orange-400 border-orange-500/20',
            'image': img1,
            'link': f"https://torob.com/search/?query={encoded_query}"
        },
        {
            'title': f'بررسی مشخصات و موجودی {query}',
            'store': 'دیجی‌کالا',
            'price': p2,
            'badge_color': 'bg-red-500/10 text-red-400 border-red-500/20',
            'image': img2,
            'link': f"https://www.digikala.com/search/?q={encoded_query}"
        },
        {
            'title': f'خرید آنلاین {query} با گارانتی اصلی',
            'store': 'تکنولایف',
            'price': p3,
            'badge_color': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
            'image': img3,
            'link': f"https://www.technolife.ir/product/list?search={encoded_query}"
        }
    ]

    return jsonify({'status': 'success', 'results': products})

if __name__ == '__main__':
    app.run(debug=True)