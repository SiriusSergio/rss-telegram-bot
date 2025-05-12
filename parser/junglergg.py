import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def fetch_champions(lane="all"):
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    driver.get('https://jungler.gg/wild-rift-stats/')
    time.sleep(5)
    
    if lane != "all":
        driver.execute_script(f"changeLane('{lane}')")
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