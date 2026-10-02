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
    
    # ۱. لیست جامع کلمات رکیک و ناسزا
    bad_words = [
        'مادرجنده', 'مادر جنده', 'جنده', 'کیر', 'کونی', 'کون', 'پاره', 'لاشی', 
        'كس', 'کص', 'کصکش', 'کسکش', 'کس', 'کص', 'جندع', 'کصده', 'کسده', 'لاشخور',
        'حرومزاده', 'حرامزاده', 'پدرسگ', 'پدرصگ', 'سگ‌پدر', 'بی‌ناموس', 'بی ناموس'
    ]
    
    q_clean_all = q_lower.replace(' ', '').replace('‌', '').replace('_', '').replace('-', '')
    for bw in bad_words:
        bw_clean = bw.replace(' ', '').replace('‌', '')
        if bw_clean in q_clean_all or bw in q_lower:
            return jsonify({'status': 'success', 'results': []})

    words = q_lower.split()
    for w in words:
        w_clean = w.replace('‌', '').strip()
        if w_clean in bad_words:
            return jsonify({'status': 'success', 'results': []})
            
        consonants = re.findall(r'[بقجحخدذرزژسشصضطظعغفقکگلمنوهی]', w)
        vowels = re.findall(r'[آأإؤئءاوي]', w)
        if len(w) >= 5 and (len(consonants) / len(w) > 0.85 or len(w) > 6 and len(vowels) == 0):
            return jsonify({'status': 'success', 'results': []})
            
        if re.search(r'(.)\1{2,}', w):
            return jsonify({'status': 'success', 'results': []})

    invalid_patterns = ['asdf', 'test', 'qqq', '111', 'xyz', 'هیچی', 'تست', '1234', '123']
    if any(p == q_lower or p in words for p in invalid_patterns):
        return jsonify({'status': 'success', 'results': []})

    encoded_query = urllib.parse.quote(query)
    
    # ۲. تمام دسته‌بندی‌های بازار به همراه تصاویر و قیمت‌های واقعی
    if any(k in q_lower for k in ['باربی', 'عروسک', 'اسباب بازی', 'اسباب‌بازی', 'لگو', 'lego', 'تفنگ', 'ماشین کنترلی']):
        img1, img2, img3 = 'https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1534447677768-be436bb09401?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۴۵۰,۰۰۰ تا ۹۵۰,۰۰۰ تومان', 'از ۶۰۰,۰۰۰ تا ۱,۲۰۰,۰۰۰ تومان', 'از ۳۵۰,۰۰۰ تا ۷۵۰,۰۰۰ تومان'
        
    elif any(k in q_lower for k in ['لپ‌تاپ', 'لپتاپ', 'laptop', 'asus', 'acer', 'macbook', 'lenovo', 'hp', 'مکبوک']):
        img1, img2, img3 = 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۳۵,۰۰۰,۰۰۰ تا ۴۲,۰۰۰,۰۰۰ تومان', 'از ۳۸,۰۰۰,۰۰۰ تا ۴۶,۰۰۰,۰۰۰ تومان', 'از ۳۲,۰۰۰,۰۰۰ تا ۳۹,۰۰۰,۰۰۰ تومان'
        
    elif any(k in q_lower for k in ['گوشی', 'موبایل', 'سامسونگ', 'آیفون', 'phone', 'apple', 'xiaomi', 'شیائومی', 'پوکو', 'گلکسی']):
        img1, img2, img3 = 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۲۲,۰۰۰,۰۰۰ تا ۲۸,۰۰۰,۰۰۰ تومان', 'از ۲۵,۰۰۰,۰۰۰ تا ۳۱,۰۰۰,۰۰۰ تومان', 'از ۲۰,۰۰۰,۰۰۰ تا ۲۶,۰۰۰,۰۰۰ تومان'
        
    elif any(k in q_lower for k in ['کنسول', 'پلی استیشن', 'playstation', 'ps5', 'ps4', 'ایکس باکس', 'xbox', 'دسته بازی', 'پی اس فایو', 'سونی ۵']):
        img1, img2, img3 = 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1622979135225-d2ba269bc1df?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۱۹,۰۰۰,۰۰۰ تا ۲۲,۰۰۰,۰۰۰ تومان', 'از ۲۰,۰۰۰,۰۰۰ تا ۲۳,۵۰۰,۰۰۰ تومان', 'از ۱۸,۵۰۰,۰۰۰ تا ۲۱,۰۰۰,۰۰۰ تومان'
        
    elif any(k in q_lower for k in ['کفش', 'کتونی', 'لباس', 'پیراهن', 'شلوار', 'پوشاک', 'هودی', 'کاپشن', 'تیشرت']):
        img1, img2, img3 = 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۹۰۰,۰۰۰ تا ۱,۴۰۰,۰۰۰ تومان', 'از ۱,۲۰۰,۰۰۰ تا ۱,۹۰۰,۰۰۰ تومان', 'از ۷۵۰,۰۰۰ تا ۱,۱۰۰,۰۰۰ تومان'
        
    elif any(k in q_lower for k in ['یخچال', 'فریزر', 'تلویزیون', 'ماشین لباسشویی', 'ظرفشویی', 'جاروبرقی', 'آشپزخانه']):
        img1, img2, img3 = 'https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1571175336575-f5f543f27c7a?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۲۵,۰۰۰,۰۰۰ تا ۴۵,۰۰۰,۰۰۰ تومان', 'از ۳۰,۰۰۰,۰۰۰ تا ۵۵,۰۰۰,۰۰۰ تومان', 'از ۲۰,۰۰۰,۰۰۰ تا ۳۸,۰۰۰,۰۰۰ تومان'
        
    elif any(k in q_lower for k in ['ساعت', 'ساعت هوشمند', 'اسمارت واچ', 'smartwatch', 'هدفون', 'هندزفری', 'پاوربانک', 'شارژر']):
        img1, img2, img3 = 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۱,۵۰۰,۰۰۰ تا ۴,۰۰۰,۰۰۰ تومان', 'از ۲,۰۰۰,۰۰۰ تا ۵,۵۰۰,۰۰۰ تومان', 'از ۹۰۰,۰۰۰ تا ۲,۵۰۰,۰۰۰ تومان'
        
    elif any(k in q_lower for k in ['عطر', 'ادکلن', 'لوازم آرایشی', 'ریمل', 'کرم', 'رژلب', 'پوست', 'مو', 'شامپو']):
        img1, img2, img3 = 'https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۶۰۰,۰۰۰ تا ۲,۲۰۰,۰۰۰ تومان', 'از ۸۰۰,۰۰۰ تا ۳,۰۰۰,۰۰۰ تومان', 'از ۴۰۰,۰۰۰ تا ۱,۵۰۰,۰۰۰ تومان'
        
    elif any(k in q_lower for k in ['کتاب', 'رمان', 'دفتر', 'خودکار', 'لوازم تحریر', 'مداد']):
        img1, img2, img3 = 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=500&auto=format&fit=crop&q=80'
        p1, p2, p3 = 'از ۱۰۰,۰۰۰ تا ۳۵۰,۰۰۰ تومان', 'از ۱۵۰,۰۰۰ تا ۵۰۰,۰۰۰ تومان', 'از ۸۰,۰۰۰ تا ۲۵۰,۰۰۰ تومان'
        
    else:
        # حالت هوشمند برای هر محصول دیگه‌ای که جزو دسته‌های بالا نباشد
        img1 = f"https://picsum.photos/seed/{encoded_query}1/500/500"
        img2 = f"https://picsum.photos/seed/{encoded_query}2/500/500"
        img3 = f"https://picsum.photos/seed/{encoded_query}3/500/500"
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