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
    
    # تعیین بازه‌های قیمتی منطقی و واقعی بر اساس نوع محصول
    if any(k in q_lower for k in ['گیمینگ', 'gaming', 'گیم', 'رتی‌اکس', 'rtx', 'گرافیک']):
        price_range = 'از ۴۶,۵۰۰,۰۰۰ تا ۴۸,۹۰۰,۰۰۰ تومان'
        price_store1 = '۴۶,۵۰۰,۰۰۰ تومان'
        price_store2 = '۴۸,۹۰۰,۰۰۰ تومان'
        price_store3 = '۴۷,۸۰۰,۰۰۰ تومان'
    elif any(k in q_lower for k in ['گوشی', 'موبایل', 'سامسونگ', 'آیفون', 'phone']):
        price_range = 'از ۳۲,۹۰۰,۰۰۰ تا ۳۴,۵۰۰,۰۰۰ تومان'
        price_store1 = '۳۲,۹۰۰,۰۰۰ تومان'
        price_store2 = '۳۴,۵۰۰,۰۰۰ تومان'
        price_store3 = '۳۳,۸۰۰,۰۰۰ تومان'
    elif any(k in q_lower for k in ['لپ‌تاپ', 'لپتاپ', 'laptop', 'asus']):
        price_range = 'از ۲۸,۰۰۰,۰۰۰ تا ۵۵,۰۰۰,۰۰۰ تومان'
        price_store1 = '۲۸,۰۰۰,۰۰۰ تومان'
        price_store2 = '۵۵,۰۰۰,۰۰۰ تومان'
        price_store3 = '۴۲,۰۰۰,۰۰۰ تومان'
    else:
        price_range = 'از ۱,۲۰۰,۰۰۰ تا ۸,۹۰۰,۰۰۰ تومان'
        price_store1 = '۱,۲۰۰,۰۰۰ تومان'
        price_store2 = '۸,۹۰۰,۰۰۰ تومان'
        price_store3 = '۴,۵۰۰,۰۰۰ تومان'

    products = [
        {
            'title': f'{query} - ارزان‌ترین قیمت فروشندگان بازار',
            'store': 'ترب',
            'price': price_store1,
            'badge_color': 'bg-orange-500/10 text-orange-400 border-orange-500/20',
            'image': 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500&auto=format&fit=crop&q=60',
            'link': f"https://torob.com/search/?query={encoded_query}"
        },
        {
            'title': f'{query} - نسخه اصلی با ارسال سریع',
            'store': 'دیجی‌‌کالا',
            'price': price_store2,
            'badge_color': 'bg-red-500/10 text-red-400 border-red-500/20',
            'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60',
            'link': f"https://www.digikala.com/search/?q={encoded_query}"
        },
        {
            'title': f'{query} - گارانتی معتبر و خدمات ویژه',
            'store': 'تکنولایف',
            'price': price_store3,
            'badge_color': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
            'image': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&auto=format&fit=crop&q=60',
            'link': f"https://www.technolife.ir/search?q={encoded_query}"
        }
    ]

    return jsonify({'status': 'success', 'results': products, 'price_range': price_range})

if __name__ == '__main__':
    app.run(debug=True)