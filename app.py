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
    
    # لیست کامل فروشگاه‌ها با اطلاعات هماهنگ برای نمایش به صورت کارت‌های شیک
    products = [
        {
            'title': f'جستجوی "{query}" در دیجی‌کالا',
            'store': 'دیجی‌کالا',
            'price': 'مشاهده قیمت روز و خرید',
            'image': 'https://www.digikala.com/statics/img/svg/digikala.svg',
            'link': f"https://www.digikala.com/search/?q={encoded_query}"
        },
        {
            'title': f'مقایسه قیمت "{query}" در ترب',
            'store': 'ترب',
            'price': 'مقایسه فروشندگان بازار',
            'image': 'https://torob.com/static/images/torob_logo.svg',
            'link': f"https://torob.com/search/?query={encoded_query}"
        },
        {
            'title': f'بررسی و قیمت "{query}" در ایمالز',
            'store': 'ایمالز',
            'price': 'مشاهده لیست فروشندگان',
            'image': 'https://emalls.ir/Content/Design/images/emalls-logo.png',
            'link': f"https://emalls.ir/مشخصات_{encoded_query}"
        },
        {
            'title': f'خرید "{query}" از تکنولایف',
            'store': 'تکنولایف',
            'price': 'بررسی تخصصی و خرید',
            'image': 'https://www.technolife.ir/image/static/technolife-logo.svg',
            'link': f"https://www.technolife.ir/product/list?search={encoded_query}"
        },
        {
            'title': f'خرید "{query}" از باسلام',
            'store': 'باسلام',
            'price': 'مشاهده محصولات بازار اجتماعی',
            'image': 'https://basalam.com/images/basalam-logo.png',
            'link': f"https://basalam.com/search?q={encoded_query}"
        }
    ]

    return jsonify({'status': 'success', 'results': products})

if __name__ == '__main__':
    app.run(debug=True)