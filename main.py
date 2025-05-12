import logging 
from bot import create_bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app = create_bot()
    logger.info("Бот запущен")
    app.run_polling()