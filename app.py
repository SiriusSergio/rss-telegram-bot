import os
import logging
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Парсинг чемпионов
def fetch_champions():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    driver.get('https://jungler.gg/wild-rift-stats/')
    time.sleep(5)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    champion_rows = soup.find_all('tr')

    champions = []
    for row in champion_rows:
        name_span = row.find('span')
        winrate_td = row.find('td', class_='stats-table-data stats-active')
        if name_span and winrate_td:
            name = name_span.text.strip()
            win_rate = winrate_td.text.strip()
            champions.append({'name': name, 'win_rate': win_rate})
    return champions

champions = fetch_champions()

# Функция получения винрейта
def get_win_rate(champion_name):
    for champ in champions:
        if champ['name'] == champion_name:
            return f"{champ['name']}: Win Rate = {champ['win_rate']}"
    return "Champion not found."

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(champ['name'], callback_data=champ['name'])] for champ in champions[:20]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери чемпиона:", reply_markup=reply_markup)

# Обработка кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    win_rate_info = get_win_rate(query.data)
    await query.edit_message_text(text=win_rate_info)

# Запуск бота
if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    logger.info("Бот запущен")
    app.run_polling()
