import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Бот работает! Сейчас проверим Selenium.")

    # Настройка Selenium
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://jungler.gg/wild-rift-stats/")
        await update.message.reply_text("Selenium успешно запустился и открыл сайт!")
        driver.quit()
    except Exception as e:
        await update.message.reply_text(f"Ошибка при запуске Selenium: {e}")

def main():
    import os
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("Не задан BOT_TOKEN в переменных окружения")
    
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == '__main__':
    main()
