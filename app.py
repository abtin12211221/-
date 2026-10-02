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
    
    # تشخیص دسته‌بندی‌ها و محصولات ویژه (مثل گیمینگ، گوشی، لپ‌تاپ و...)
    if 'گیمینگ' in q_lower or 'gaming' in q_lower or 'رایانه' in q_lower:
        products = [
            {
                'title': f'{query} - ماوس و کیبورد مخصوص گیمینگ RGB',
                'store': 'دیجی‌کالا',
                'price': '۱,۸۵۰,۰۰۰ تومان',
                'badge_color': 'bg-red-500/10 text-red-400 border-red-500/20',
                'image': 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&auto=format&fit=crop&q=60',
                'link': f"https://www.digikala.com/search/?q={encoded_query}"
            },
            {
                'title': f'{query} - هدست گیمینگ حرفه‌ای صدا 7.1',
                'store': 'ترب',
                'price': '۲,۲۰۰,۰۰۰ تومان',
                'badge_color': 'bg-orange-500/10 text-orange-400 border-orange-500/20',
                'image': 'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=500&auto=format&fit=crop&q=60',
                'link': f"https://torob.com/search/?query={encoded_query}"
            },
            {
                'title': f'{query} - صندلی گیمینگ ارگونومیک',
                'store': 'تکنولایف',
                'price': '۸,۹۰۰,۰۰۰ تومان',
                'badge_color': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
                'image': 'https://images.unsplash.com/photo-1598550476439-6847785fcea6?w=500&auto=format&fit=crop&q=60',
                'link': f"https://www.technolife.ir/search?q={encoded_query}"
            }
        ]
    else:
        # حالت عمومی برای سایر جستجوها
        products = [
            {
                'title': f'{query} - ارزان‌ترین قیمت بازار',
                'store': 'ترب',
                'price': '۱,۲۵۰,۰۰۰ تومان',
                'badge_color': 'bg-orange-500/10 text-orange-400 border-orange-500/20',
                'image': 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500&auto=format&fit=crop&q=60',
                'link': f"https://torob.com/search/?query={encoded_query}"
            },
            {
                'title': f'{query} - نسخه اصلی و پرفروش',
                'store': 'دیجی‌کالا',
                'price': '۳,۴۹۰,۰۰۰ تومان',
                'badge_color': 'bg-red-500/10 text-red-400 border-red-500/20',
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60',
                'link': f"https://www.digikala.com/search/?q={encoded_query}"
            },
            {
                'title': f'{query} - گارانتی و خدمات ویژه',
                'store': 'تکنولایف',
                'price': '۲,۹۰۰,۰۰۰ تومان',
                'badge_color': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
                'image': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&auto=format&fit=crop&q=60',
                'link': f"https://www.technolife.ir/search?q={encoded_query}"
            }
        ]

    return jsonify({'status': 'success', 'results': products})

if __name__ == '__main__':
    app.run(debug=True)