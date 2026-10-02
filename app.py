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
    
    # ۱. لیست سیاه جامع برای کلمات رکیک و ناسزا
    bad_words = [
        'مادرجنده', 'مادر جنده', 'جنده', 'کیر', 'کونی', 'کون', 'پاره', 'لاشی', 
        'كس', 'کص', 'کصکش', 'کسکش', 'کس', 'کص', 'دس', 'داش', 'سگ', 'خر',
        'جندع', 'کصده', 'کسده', 'لاشخور', 'منگل', 'امل', 'اغشخ'
    ]
    
    q_clean_all = q_lower.replace(' ', '').replace('‌', '').replace('_', '').replace('-', '')
    for bw in bad_words:
        bw_clean = bw.replace(' ', '').replace('‌‌', '')
        if bw_clean in q_clean_all or bw in q_lower:
            return jsonify({'status': 'success', 'results': []})

    words = q_lower.split()
    for w in words:
        w_clean = w.replace('‌', '').strip()
        if w_clean in bad_words:
            return jsonify({'status': 'success', 'results': []})
            
        # فیلتر هوشمند تشخیص کیبوردکوبی و متون درهم‌برهم رندوم
        consonants = re.findall(r'[بقجحخدذرزژسشصضطظعغفقکگلمنوهی]', w)
        vowels = re.findall(r'[آأإؤئءاوي]', w)
        if len(w) >= 5 and (len(consonants) / len(w) > 0.85 or len(w) > 6 and len(vowels) == 0):
            return jsonify({'status': 'success', 'results': []})
            
        if re.search(r'(.)\1{2,}', w):
            return jsonify({'status': 'success', 'results': []})
            
        if 'غق' in w or 'بزغ' in w or 'لتب' in w or 'زغ' in w:
            return jsonify({'status': 'success', 'results': []})

    invalid_patterns = ['asdf', 'test', 'qqq', '111', 'xyz', 'هیچی', 'تست', '1234', '123', 'غلتبز']
    if any(p == q_lower or p in words for p in invalid_patterns):
        return jsonify({'status': 'success', 'results': []})

    encoded_query = urllib.parse.quote(query)
    
    # ۲. تعیین عکس‌ها و بازه‌های قیمت واقعی (به شکل بازه: از ... تا ... تومان) بر اساس نوع محصول
    if any(k in q_lower for k in ['فرش', 'قالی', 'گلیم', 'موکت', 'پادری']):
        img1 = 'https://images.unsplash.com/photo-1600121848594-d8644e57abab?w=500&auto=format&fit=crop&q=80'
        img2 = 'https://images.unsplash.com/photo-1579656381226-5fc0f0100c3b?w=500&auto=format&fit=crop&q=80'
        img3 = 'https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۳,۸۰۰,۰۰۰ تا ۴,۹۰۰,۰۰۰ تومان', 'از ۴,۲۰۰,۰۰۰ تا ۵,۶۰۰,۰۰۰ تومان', 'از ۳,۵۰۰,۰۰۰ تا ۴,۲۰۰,۰۰۰ تومان'
    elif any(k in q_lower for k in ['لپ‌تاپ', 'لپتاپ', 'laptop', 'asus', 'acer', 'macbook', 'lenovo']):
        img1 = 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&auto=format&fit=crop&q=80'
        img2 = 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop&q=80'
        img3 = 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۳۵,۰۰۰,۰۰۰ تا ۴۲,۰۰۰,۰۰۰ تومان', 'از ۳۸,۰۰۰,۰۰۰ تا ۴۶,۰۰۰,۰۰۰ تومان', 'از ۳۲,۰۰۰,۰۰۰ تا ۳۹,۰۰۰,۰۰۰ تومان'
    elif any(k in q_lower for k in ['گوشی', 'موبایل', 'سامسونگ', 'آیفون', 'phone', 'apple', 'xiaomi']):
        img1 = 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&auto=format&fit=crop&q=80'
        img2 = 'https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=500&auto=format&fit=crop&q=80'
        img3 = 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۲۲,۰۰۰,۰۰۰ تا ۲۸,۰۰۰,۰۰۰ تومان', 'از ۲۵,۰۰۰,۰۰۰ تا ۳۱,۰۰۰,۰۰۰ تومان', 'از ۲۰,۰۰۰,۰۰۰ تا ۲۶,۰۰۰,۰۰۰ تومان'
    elif any(k in q_lower for k in ['کیس', 'کامپیوتر', 'گیمینگ', 'gaming', 'گیم', 'رتی‌اکس', 'rtx', 'گرافیک', 'مادربرد']):
        img1 = 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&auto=format&fit=crop&q=80'
        img2 = 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500&auto=format&fit=crop&q=80'
        img3 = 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۶۰,۰۰۰,۰۰۰ تا ۷۵,۰۰۰,۰۰۰ تومان', 'از ۶۸,۰۰۰,۰۰۰ تا ۸۲,۰۰۰,۰۰۰ تومان', 'از ۵۵,۰۰۰,۰۰۰ تا ۷۰,۰۰۰,۰۰۰ تومان'
    elif any(k in q_lower for k in ['کفش', 'کتونی', 'لباس', 'پیراهن', 'شلوار', 'پوشاک']):
        img1 = 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&auto=format&fit=crop&q=80'
        img2 = 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&auto=format&fit=crop&q=80'
        img3 = 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۹۰۰,۰۰۰ تا ۱,۴۰۰,۰۰۰ تومان', 'از ۱,۲۰۰,۰۰۰ تا ۱,۹۰۰,۰۰۰ تومان', 'از ۷۵۰,۰۰۰ تا ۱,۱۰۰,۰۰۰ تومان'
    else:
        img1 = 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=80'
        img2 = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=80'
        img3 = 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۷,۰۰۰,۰۰۰ تا ۹,۵۰۰,۰۰۰ تومان', 'از ۸,۲۰۰,۰۰۰ تا ۱۰,۸۰۰,۰۰۰ تومان', 'از ۶,۵۰۰,۰۰۰ تا ۸,۸۰۰,۰۰۰ تومان'

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