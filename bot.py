import os
import requests
from bs4 import BeautifulSoup
import time

TOKEN = '8858034230:AAEnzS-eEgErUnHOh3GGxAi5lQ6XIgEgWzk'
CHAT_ID = '8283299548'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7'
}

URLS = [
    'https://www.jumia.com.eg/ar/mlp-mens-clothing/',
    'https://www.jumia.com.eg/ar/womens-clothing/',
    'https://www.jumia.com.eg/ar/category-fashion-deals/'
]

sent_products = set()

def check_jumia_fashion():
    for url in URLS:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('article', class_='prd')

            for item in products:
                link_tag = item.find('a', class_='core')
                name_tag = item.find('h3', class_='name')
                price_tag = item.find('div', class_='prc')
                old_price_tag = item.find('div', class_='old')

                if not name_tag or not price_tag or not link_tag or not old_price_tag:
                    continue

                product_url = 'https://www.jumia.com.eg' + link_tag['href']
                
                if product_url in sent_products:
                    continue

                name = name_tag.text.strip()
                current_price = float(price_tag.text.replace('EGP', '').replace(',', '').strip())
                old_price = float(old_price_tag.text.replace('EGP', '').replace(',', '').strip())

                if old_price > current_price:
                    discount = ((old_price - current_price) / old_price) * 100
                else:
                    discount = 0

                if discount >= 65:
                    send_telegram(name, current_price, old_price, discount, product_url)
                    sent_products.add(product_url)

        except Exception as e:
            print(f"خطأ: {e}")

def send_telegram(name, current, old, discount, link):
    msg = (
        f"🚨 **حقّق اللقطة! خصم قوي على ملابس جوميا**\n\n"
        f"💵 **السعر الحالي:** EGP {current:,.2f}\n"
        f"💸 **السعر السابق:** EGP {old:,.2f}\n"
        f"📉 **نسبة الخصم:** {discount:.1f}%\n\n"
        f"📌 **المنتج:** {name}\n"
        f"🔗 [اضغط هنا للشراء فوراً]({link})"
    )
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(api_url, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})

if __name__ == '__main__':
    print("البوت يعمل الآن...")
    while True:
        check_jumia_fashion()
        time.sleep(180)
