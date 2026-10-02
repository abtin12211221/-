from flask import Flask, render_template, request, jsonify
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
    
    encoded_query = urllib.parse.quote(query)
    q_lower = query.lower()
    
    # تولید داده‌های پویای منطبق بر جستجوی واقعی کاربر جهت هدایت دقیق به صفحات خرید معتبر
    products = [
        {
            'title': f'خرید و مقایسه قیمت {query} در فروشگاه‌های معتبر',
            'store': 'ترب (موتور جستجوی خرید)',
            'price': 'مشاهده قیمت لحظه‌ای در بازار',
            'badge_color': 'bg-orange-500/10 text-orange-400 border-orange-500/20',
            'image': 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500&auto=format&fit=crop&q=80',
            'link': f"https://torob.com/search/?query={encoded_query}"
        },
        {
            'title': f'جستجوی تخصصی و موجودی {query}',
            'store': 'دیجی‌کالا',
            'price': 'بررسی موجودی و تخفیف‌ها',
            'badge_color': 'bg-red-500/10 text-red-400 border-red-500/20',
            'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=80',
            'link': f"https://www.digikala.com/search/?q={encoded_query}"
        },
        {
            'title': f'خرید آنلاین {query} با گارانتی اصلی',
            'store': 'تکنولایف',
            'price': 'استعلام قیمت روز',
            'badge_color': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
            'image': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500&auto=format&fit=crop&q=80',
            'link': f"https://www.technolife.ir/product/list?search={encoded_query}"
        }
    ]

    return jsonify({'status': 'success', 'results': products})

if __name__ == '__main__':
    app.run(debug=True)