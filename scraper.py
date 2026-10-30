import os
import time
import sqlite3
import requests

IMAGE_FOLDER = "arzoonjou_images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def run_scraper(search_keyword="سفره پاک کن"):
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys

        chrome_options = Options()
        chrome_options.debugger_address = "127.0.0.1:9222"
        driver = webdriver.Chrome(options=chrome_options)
        
        print(f"Step 1: Searching for '{search_keyword}' on Digikala to get product name...")
        
        # ۱. رفتن به دیجی‌کالا و جستجوی محصول
        driver.get("https://www.digikala.com")
        time.sleep(2)

        product_name = ""
        try:
            search_inputs = driver.find_elements(By.TAG_NAME, "input")
            for inp in search_inputs:
                placeholder = inp.get_attribute("placeholder") or ""
                if "جستجو" in placeholder:
                    inp.clear()
                    inp.send_keys(search_keyword)
                    inp.send_keys(Keys.RETURN)
                    time.sleep(3)
                    break
            
            # استخراج نام اولین محصول پیدا شده در دیجی‌کالا
            titles = driver.find_elements(By.TAG_NAME, "h3") + driver.find_elements(By.CSS_SELECTOR, "h2")
            for t in titles:
                text = t.text.strip()
                if len(text) > 5:
                    product_name = text
                    break

            if not product_name:
                product_name = search_keyword

            print(f"Product name found: {product_name}")

            # ۲. رفتن به پنل افیلو برای استخراج لینک اختصاصی بر اساس نام پیدا شده
            print("Step 2: Going to Affilio to find links and prices...")
            driver.get("https://publisher.affilio.ir/affiliate-links/select-products")
            time.sleep(3)

            # جستجوی نام محصول در افیلو
            aff_inputs = driver.find_elements(By.TAG_NAME, "input")
            for inp in aff_inputs:
                placeholder = inp.get_attribute("placeholder") or ""
                if "جستجو" in placeholder or "محصول" in placeholder:
                    inp.clear()
                    inp.send_keys(product_name)
                    inp.send_keys(Keys.RETURN)
                    time.sleep(3)
                    break

            time.sleep(2)
            valid_cards = driver.find_elements(By.CSS_SELECTOR, "div.bg-white, div[class*='card']")
            filtered_cards = [c for c in valid_cards if len(c.find_elements(By.TAG_NAME, "img")) > 0 and "تومان" in c.text]

            if not filtered_cards:
                filtered_cards = driver.find_elements(By.CSS_SELECTOR, ".grid > div")

            if not filtered_cards:
                print("No products found in Affilio for this name.")
                return

            conn = sqlite3.connect("arzoonjou.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products")
            conn.commit()

            # استخراج اطلاعات و لینک مجزا برای هر آیتم
            for index, card in enumerate(filtered_cards[:3]):
                try:
                    text_lines = [line.strip() for line in card.text.split('\n') if line.strip()]
                    title = product_name
                    price = "تماس بگیرید"

                    # استخراج قیمت
                    try:
                        price_elements = card.find_elements(By.XPATH, ".//*[contains(text(), 'تومان')]")
                        if price_elements:
                            price = price_elements[0].text.strip()
                    except:
                        pass

                    if price == "تماس بگیرید":
                        for line in text_lines:
                            if "تومان" in line:
                                price = line
                                break

                    img_url = ""
                    try:
                        img = card.find_element(By.TAG_NAME, "img")
                        img_url = img.get_attribute("src") or img.get_attribute("data-src")
                    except:
                        pass

                    # کلیک روی کارت و گرفتن لینک اختصاصی افیلیت
                    aff_link = "https://publisher.affilio.ir/affiliate-links/select-products"
                    try:
                        driver.execute_script("arguments[0].click();", card)
                        time.sleep(1.2)

                        buttons = driver.find_elements(By.TAG_NAME, "button")
                        for btn in buttons:
                            if "کپی لینک" in btn.text:
                                driver.execute_script("arguments[0].click();", btn)
                                time.sleep(0.4)
                                break

                        inputs = driver.find_elements(By.TAG_NAME, "input")
                        for inp in inputs:
                            val = inp.get_attribute("value")
                            if val and "http" in val and "select-products" not in val and len(val) > 25:
                                aff_link = val
                                break
                    except:
                        pass

                    img_path = ""
                    if img_url and img_url.startswith("http"):
                        try:
                            img_data = requests.get(img_url, timeout=4).content
                            safe_title = "".join([c for c in title if c.isalnum()][:10]) or f"p_{index}"
                            img_path = f"{IMAGE_FOLDER}/{safe_title}_{index}.jpg"
                            with open(img_path, "wb") as f:
                                f.write(img_data)
                        except:
                            pass

                    cursor.execute(
                        "INSERT INTO products (title, price, image_path, affiliate_link) VALUES (?, ?, ?, ?)",
                        (title, price, img_path, aff_link)
                    )
                    conn.commit()
                except:
                    continue

            conn.close()
            print("Process completed successfully!")

        except Exception as e:
            print(f"Error: {e}")

    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    run_scraper("سفره پاک کن")