from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


ROLE_BUTTON_IDS = {
    "lane_baron": "topBtn",
    "lane_mid": "midBtn",
    "lane_jungle": "jungleBtn",
    "lane_dragon": "adcBtn",
    "lane_support": "supportBtn",
}


def fetch_champions_by_role(role_callback_data: str):
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    driver.get('https://jungler.gg/wild-rift-stats/')
    
    role_btn_id = ROLE_BUTTON_IDS[role_callback_data]
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, role_btn_id))).click()

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