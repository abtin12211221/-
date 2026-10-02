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
    
    # لیست جامع و بسیار کامل کلمات رکیک، ناسزا و توهین‌آمیز
    bad_words = [
        'جنده', 'مادرجنده', 'مادر جنده', 'کیر', 'کونی', 'کون', 'لاشی', 
        'کص', 'کس', 'کصکش', 'کسکش', 'جندع', 'کصده', 'کسده', 'لاشخور',
        'حرومزاده', 'حرامزاده', 'پدرسگ', 'پدرصگ', 'سگ‌پدر', 'بی‌ناموس',
        'بی ناموس', 'منگل', 'احمق', 'خر', 'جاکش', 'Dande', 'kos', 'kir',
        'kooni', 'lashii', 'koskesh', 'haroomzade', 'haramzade'
    ]
    
    # پاکسازی متن از فاصله و کاراکترهای اضافی برای جلوگیری از دور زدن فیلتر
    q_clean_all = q_lower.replace(' ', '').replace('‌', '').replace('_', '').replace('-', '')
    for bw in bad_words:
        bw_clean = bw.replace(' ', '').replace('‌', '')
        if bw_clean in q_clean_all or bw.lower() in q_lower:
            return jsonify({'status': 'success', 'results': []})

    words = q_lower.split()
    for w in words:
        w_clean = w.replace('‌', '').strip()
        if w_clean in bad_words:
            return jsonify({'status': 'success', 'results': []})
            
        # فیلتر هوشمند کیبوردکوبی و حروف رندوم بی‌‌معنی
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
    
    # تولید عکس‌ها و لینک‌های هوشمند داینامیک برای هر محصولی که سرچ شود
    img_url_1 = f"https://picsum.photos/seed/{encoded_query}1/500/500"
    img_url_2 = f"https://picsum.photos/seed/{encoded_query}2/500/500"
    img_url_3 = f"https://picsum.photos/seed/{encoded_query}3/500/500"

    products = [
        {
            'title': f'جستجوی قیمت لحظه‌ای "{query}" در بازار',
            'store': 'ترب',
            'price': 'مشاهده نرخ‌های آنلاین و مقایسه فروشندگان',
            'badge_color': 'bg-orange-500/10 text-orange-400 border-orange-500/20',
            'image': img_url_1,
            'link': f"https://torob.com/search/?query={encoded_query}"
        },
        {
            'title': f'بررسی مشخصات و موجودی "{query}"',
            'store': 'دیجی‌کالا',
            'price': 'استعلام آخرین قیمت و نظرات کاربران',
            'badge_color': 'bg-red-500/10 text-red-400 border-red-500/20',
            'image': img_url_2,
            'link': f"https://www.digikala.com/search/?q={encoded_query}"
        },
        {
            'title': f'خرید آنلاین "{query}" با ضمانت',
            'store': 'تکنولایف',
            'price': 'بررسی شرایط فروش و ارسال فوری',
            'badge_color': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
            'image': img_url_3,
            'link': f"https://www.technolife.ir/product/list?search={encoded_query}"
        }
    ]

    return jsonify({'status': 'success', 'results': products})

if __name__ == '__main__':
    app.run(debug=True)