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
    
    # لیست پیشرفته معتبرترین فروشگاه‌ها با لینک‌های مستقیم و اطلاعات جامع
    stores_data = [
        {
            'name': 'دیجی‌کالا',
            'category': 'بزرگترین فروشگاه آنلاین ایران',
            'badge_color': 'bg-red-500/10 text-red-400 border-red-500/20',
            'url': f"https://www.digikala.com/search/?q={encoded_query}",
            'logo': '🛒'
        },
        {
            'name': 'ترب',
            'category': 'موتور مقایسه قیمت بازار',
            'badge_color': 'bg-orange-500/10 text-orange-400 border-orange-500/20',
            'url': f"https://torob.com/search/?query={encoded_query}",
            'logo': '⚖️'
        },
        {
            'name': 'ایمالز',
            'category': 'مرجع قیمت‌گذاری فروشندگان',
            'badge_color': 'bg-blue-500/10 text-blue-400 border-blue-500/20',
            'url': f"https://emalls.ir/مشخصات_{encoded_query}",
            'logo': '📊'
        },
        {
            'name': 'تکنولایف',
            'category': 'متخصص کالای دیجیتال و موبایل',
            'badge_color': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
            'url': f"https://www.technolife.ir/product/list?search={encoded_query}",
            'logo': '📱'
        },
        {
            'name': 'باسلام',
            'category': 'بازار اجتماعی و محصولات سنتی',
            'badge_color': 'bg-amber-500/10 text-amber-400 border-amber-500/20',
            'url': f"https://basalam.com/search?q={encoded_query}",
            'logo': '🧶'
        }
    ]

    results = []
    for store in stores_data:
        results.append({
            'title': f'نتایج جستجوی "{query}" در {store["name"]}',
            'store': store['name'],
            'category': store['category'],
            'badge_color': store['badge_color'],
            'logo': store['logo'],
            'price_text': 'بررسی قیمت لحظه‌ای و خرید',
            'link': store['url']
        })

    return jsonify({'status': 'success', 'results': results})

if __name__ == '__main__':
    app.run(debug=True)