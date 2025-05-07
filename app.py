import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
import logging

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройки браузера (чтобы не открывалось окно)
options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/chromium"
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Запуск ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://jungler.gg/wild-rift-stats/')

# Ждём, пока страница загрузится
time.sleep(5)

# Получаем HTML уже с выполненным JavaScript
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Закрываем браузер
driver.quit()

# Теперь ищем данные в soup
champion_data_top_lane = soup.find_all('tr')  #  ищем по классу

print(f"Найдено строк: {len(champion_data_top_lane)}")
for champion in champion_data_top_lane[:5]:  # выводим 5 строк для проверки
    print(champion.text.strip())


champions = []
for champion in champion_data_top_lane:
    if champion.find('span') == None:
        continue
    elif champion.find('td') == None:
        continue
    else: name = champion.find('span').text.strip()
    win_rate = champion.find('td', class_='stats-table-data stats-active').text.strip()
    champions.append({'name': name, 'win_rate': win_rate})

def get_win_rate(champion_name):
    try:
        name = next(item for item in champions if item["name"] == champion_name).get('name')
        win_rate = next(item for item in champions if item["name"] == champion_name).get('win_rate')
        return f"{name}: Win Rate = {win_rate}"
    except Exception as e:
        return f"An error occurred: {e}"
    return "Champion not found."

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in champions]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери чемпиона:", reply_markup=reply_markup)

# Обработка нажатия на кнопку
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    champion_name = query.data
    win_rate_info = get_win_rate(champion_name)
    await query.edit_message_text(text=win_rate_info)

# Запуск бота
if name == '__main__':
    TOKEN = os.getenv("TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print('Бот запущен')
    app.run_polling()



