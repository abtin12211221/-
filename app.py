@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'status': 'error', 'message': 'عبارت جستجو خالی است'})

    products = []
    try:
        url = f"https://www.digikala.com/search/?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        
        response = requests.get(url, headers=headers, timeout=12)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # جستجوی عمومی‌تر برای کارت‌های محصولات در دیجی‌کالا
            items = soup.select('article, div.product-card, div[data-product-id]')
            
            if not items:
                # اگر با سلکتورهای بالا پیدا نکرد، تمام تگ‌های لینک که ساختار محصول دارند را پیدا کن
                items = soup.find_all('a', href=lambda href: href and '/product/dkp-' in href)

            for item in items[:12]:
                try:
                    # اگر الگو لینک مستقیم بود
                    if item.name == 'a':
                        link_elem = item
                    else:
                        link_elem = item.find('a', href=True)

                    raw_link = link_elem['href'] if link_elem else ""
                    if not raw_link or '/product/dkp-' not in raw_link:
                        continue
                        
                    link = f"https://www.digikala.com{raw_link}" if raw_link.startswith('/') else raw_link

                    # استخراج عنوان
                    title_elem = item.find('h3') or item.find('h4') or item.select_text = item.select_one('div[data-testid="title"]')
                    title = title_elem.get_text(strip=True) if title_elem else "محصول دیجی‌کالا"

                    # استخراج عکس
                    img_elem = item.find('img')
                    image = img_elem.get('src') or img_elem.get('data-src') if img_elem else "https://via.placeholder.com/200"

                    # استخراج قیمت
                    price_elem = item.select_one('span[data-testid="price"]') or item.find(string=lambda t: t and 'تومان' in t)
                    price = price_elem.get_text(strip=True) if price_elem else "موجود در سایت"
                    if hasattr(price_elem, 'parent') and not price_elem.parent.name == 'span':
                        price = price_elem.strip()

                    # جلوگیری از تکراری شدن محصولات در لیست
                    if not any(p['link'] == link for p in products):
                        products.append({
                            'title': title,
                            'store': 'دیجی‌کالا',
                            'price': price,
                            'image': image,
                            'link': link
                        })
                except Exception as e:
                    continue

        return jsonify({'status': 'success', 'results': products})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})