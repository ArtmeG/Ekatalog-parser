from aiogram import types, executor, Dispatcher, Bot
from bs4 import BeautifulSoup
import requests
from Key import my_key


bot = Bot(my_key)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def user_welcome(message: types.message):
    await bot.send_message(message.chat.id, """Hi! I'm bot that helps you find products quickly 
    <b><a href="https://ek.ua/ua/">E Katalog</a></b>
    я отправлю тебе товар, введи в поле его название...""",
                           parse_mode='html', disable_web_page_preview=0)


@dp.message_handler(content_types=['text'])
async def parser(message: types.message):
    url = 'https://ek.ua/ek-list.php?search_=' + message.text
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    main_url = 'https://ek.ua/ua'

    all_links = soup.find_all('a', class_='model-short-title')
    for item in all_links:
        url = main_url + item['href']
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        name = soup.select('.page-title')
        name = name[0].text

        price = soup.select('.desc-big-price')
        price = price[0].text

        img = soup.select('.img200 > img')
        img = img[0]['src']

        await bot.send_photo(message.chat.id, img, caption="<b>" + name + "</b>\n<i>" +
            price + f"</i>\n<a href='{url}'>Ссылка на сайт</a>", parse_mode='html')


executor.start_polling(dp)
