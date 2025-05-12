import logging
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

ROLE_BUTTON_IDS = {
    "lane_baron": "topBtn",
    "lane_mid": "midBtn",
    "lane_jungle": "jungleBtn",
    "lane_adc": "adcBtn",
    "lane_support": "supportBtn",
}


def fetch_champions_by_role(role: str):
    logger.info(f"Запрашиваем чемпионов для роли: {role}")
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    driver.get('https://jungler.gg/wild-rift-stats/')
    

    try:
        btn_id = ROLE_TO_BUTTON_ID.get(role)
        if not btn_id:
            logger.error(f"Неизвестная роль: {role}")
            return []

        # Ждём появления и скроллим к кнопке
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, btn_id))
        )
        driver.execute_script("arguments\[0\].scrollIntoView(true);", element)
        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, btn_id))
        ).click()

        logger.info(f"Клик по кнопке роли {role} выполнен")

        # Даём странице отрисовать новую таблицу
        time.sleep(4)

        # Сохраняем HTML для отладки
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

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
        logger.info(f"Найдено чемпионов: {len(champions)}")
        return champions

    except Exception as e:
        logger.exception(f"Ошибка при парсинге данных для роли {role}: {e}")
        return []

    finally:
        driver.quit()