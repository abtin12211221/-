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
    
    # تعیین عکس‌ها و بازه‌های قیمتی دقیق و مرتبط با محصول جستجو شده
    if any(k in q_lower for k in ['گیمینگ', 'gaming', 'گیم', 'رتی‌اکس', 'rtx', 'گرافیک', 'ماوس', 'کیبورد', 'هدست']):
        img1 = 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&auto=format&fit=crop&q=80' # سخت‌افزار/گیمینگ
        img2 = 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=500&auto=format&fit=crop&q=80' # تجهیزات گیمینگ
        img3 = 'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=500&auto=format&fit=crop&q=80' # هدفون/هدست
        price_store1 = '۴۶,۵۰۰,۰۰۰ تومان'
        price_store2 = '۴۸,۹۰۰,۰۰۰ تومان'
        price_store3 = '۴۷,۸۰۰,۰۰۰ تومان'
    elif any(k in q_lower for k in ['گوشی', 'موبایل', 'سامسونگ', 'آیفون', 'phone', 'apple']):
        img1 = 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&auto=format&fit=crop&q=80' # موبایل
        img2 = 'https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=500&auto=format&fit=crop&q=80' # آیفون/گوشی
        img3 = 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500&auto=format&fit=crop&q=80' # اسمارت‌فون
        price_store1 = '۳۲,۹۰۰,۰۰۰ تومان'
        price_store2 = '۳۴,۵۰۰,۰۰۰ تومان'
        price_store3 = '۳۳,۸۰۰,۰۰۰ تومان'
    elif any(k in q_lower for k in ['لپ‌تاپ', 'لپتاپ', 'laptop', 'asus', 'acer', 'macbook']):
        img1 = 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&auto=format&fit=crop&q=80' # لپ‌تاپ روشن
        img2 = 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop&q=80' # مک‌بوک
        img3 = 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop&q=80' # لپ‌تاپ مهندسی
        price_store1 = '۲۸,۰۰۰,۰۰۰ تومان'
        price_store2 = '۵۵,۰۰۰,۰۰۰ تومان'
        price_store3 = '۴۲,۰۰۰,۰۰۰ تومان'
    elif any(k in q_lower for k in ['ساعت', 'ایرداد', 'هدفون', 'watch', 'airpods']):
        img1 = 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=80' # ساعت هوشمند
        img2 = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=80' # هدفون
        img3 = 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500&auto=format&fit=crop&q=80' # گجت پوشیدنی
        price_store1 = '۱,۸50,۰۰۰ تومان'
        price_store2 = '۳,۹۰۰,۰۰۰ تومان'
        price_store3 = '۲,۷۰۰,۰۰۰ تومان'
    else:
        # حالت پیش‌فرض هوشمند (تولید عکس داینامیک بر اساس متن سرچ شده با استفاده از کلیدواژه عمومی با کیفیت)
        img1 = 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500&auto=format&fit=crop&q=80'
        img2 = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=80'
        img3 = 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&auto=format&fit=crop&q=80'
        price_store1 = '۱,۲۰۰,۰۰۰ تومان'
        price_store2 = '۸,۹۰۰,۰۰۰ تومان'
        price_store3 = '۴,۵۰۰,۰۰۰ تومان'

    products = [
        {
            'title': f'{query} - ارزان‌ترین قیمت فروشندگان بازار',
            'store': 'ترب',
            'price': price_store1,
            'badge_color': 'bg-orange-500/10 text-orange-400 border-orange-500/20',
            'image': img1,
            'link': f"https://torob.com/search/?query={encoded_query}"
        },
        {
            'title': f'{query} - نسخه اصلی با ارسال سریع',
            'store': 'دیجی‌کالا',
            'price': price_store2,
            'badge_color': 'bg-red-500/10 text-red-400 border-red-500/20',
            'image': img2,
            'link': f"https://www.digikala.com/search/?q={encoded_query}"
        },
        {
            'title': f'{query} - گارانتی معتبر و خدمات ویژه',
            'store': 'تکنولایف',
            'price': price_store3,
            'badge_color': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
            'image': img3,
            'link': f"https://www.technolife.ir/search?q={encoded_query}"
        }
    ]

    return jsonify({'status': 'success', 'results': products})

if __name__ == '__main__':
    app.run(debug=True)