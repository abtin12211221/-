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
    
    # لینک‌های دقیق‌تر برای جلوگیری از باز شدن صفحه عمومی سرچ بی‌کیفیت
    products = [
        # --- دیجی‌کالا (لینک به صفحه نتایج با مرتب‌سازی پرفروش‌ترین‌ها برای دقت بیشتر) ---
        {
            'title': f'{query} - مدل اقتصادی و پرفروش',
            'store': 'دیجی‌کالا',
            'price': '۲,۴۵۰,۰۰۰ تومان',
            'badge_color': 'bg-red-500/10 text-red-400 border-red-500/20',
            'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60',
            'link': f"https://www.digikala.com/search/?q={encoded_query}&sort=4"
        },
        {
            'title': f'{query} - نسخه اصلی با گارانتی معتبر',
            'store': 'دیجی‌کالا',
            'price': '۴,۸۹۰,۰۰۰ تومان',
            'badge_color': 'bg-red-500/10 text-red-400 border-red-500/20',
            'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60',
            'link': f"https://www.digikala.com/search/?q={encoded_query}&sort=7"
        },
        
        # --- ترب ---
        {
            'title': f'{query} - ارزان‌ترین قیمت بازار',
            'store': 'ترب',
            'price': '۲,۱۰۰,۰۰۰ تومان',
            'badge_color': 'bg-orange-500/10 text-orange-400 border-orange-500/20',
            'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&auto=format&fit=crop&q=60',
            'link': f"https://torob.com/search/?query={encoded_query}"
        },
        {
            'title': f'{query} - پیشنهاد ویژه فروشندگان',
            'store': 'ترب',
            'price': '۳,۶۵۰,۰۰۰ تومان',
            'badge_color': 'bg-orange-500/10 text-orange-400 border-orange-500/20',
            'image': 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500&auto=format&fit=crop&q=60',
            'link': f"https://torob.com/search/?query={encoded_query}"
        },

        # --- تکنولایف ---
        {
            'title': f'{query} - نسخه استاندارد بازار',
            'store': 'تکنولایف',
            'price': '۳,۹۹۰,۰۰۰ تومان',
            'badge_color': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
            'image': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&auto=format&fit=crop&q=60',
            'link': f"https://www.technolife.ir/product/list?search={encoded_query}"
        }
    ]

    return jsonify({'status': 'success', 'results': products})

if __name__ == '__main__':
    app.run(debug=True)