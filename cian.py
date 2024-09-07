import random
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


# CHROME_DRIVER_PATH = './win64/chromedriver-win64'
CHROME_DRIVER_PATH = './chromedriver-mac-arm64/chromedriver'

def start_driver():
    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver
url = "https://spb.cian.ru/"

driver = start_driver()
driver.get(url)

choose_area = driver.find_element(By.CLASS_NAME, "_025a50318d--input-wrapper--fsQWA" )
choose_area.click()
area_input = driver.find_element(By.XPATH, "//*[@id='geo-suggest-input']")
area_input.send_keys("Санкт-Петербург, Петроградский район")
area_input.send_keys(Keys.ENTER)
# search_button = driver.find_element(By.CLASS_NAME, "_025a50318d--button--ljPOU")
search_button = driver.find_element(By.XPATH, '//*[@id="frontend-mainpage"]/section/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div[3]/span/span[2]/a')
search_button.click()

## Вариант 0
# next_button = driver.find_element(By.XPATH, '//*[@id="frontend-serp"]/div/div[5]/div[1]/nav/')
# while next_button is not '//*[@id="frontend-serp"]/div/div[5]/div[1]/nav':
#     pass


# Вариант 1
links_list = []
parsed_text = []

for page_number in range(1, 4):
    url = f'https://spb.cian.ru/cat.php?deal_type=sale&district%5B0%5D=138&engine_version=2&offer_type=flat&p={page_number}&room1=1&room2=1'
    driver.get(url)

    # elements = driver.find_elements(By.CLASS_NAME, "_93444fe79c--container--Povoi_93444fe79c--cont--OzgVc")
    elements = driver.find_elements(By.CLASS_NAME, "_93444fe79c--container--Povoi")

    links = [card.find_element(By.CLASS_NAME, "_93444fe79c--media--9P6wN").get_attribute("href") for card in elements]
    links_list.extend(links)

    for link in links_list:
        print(link)
        driver.get(link)

        main_info = driver.find_element(By.CLASS_NAME, "a10a3f92e9--container--u51hg").text
        price = driver.find_element(By.CLASS_NAME, "a10a3f92e9--amount--ON6i1").text
        price_for_m2 = driver.find_element(By.CLASS_NAME, "a10a3f92e9--item--iWTsg").text
        location = driver.find_element(By.CLASS_NAME, "a10a3f92e9--address-line--GRDTb").text
        subway = driver.find_element(By.CLASS_NAME, "a10a3f92e9--undergrounds--sGE99").text
        # try:
        #     developer = driver.find_element(By.CLASS_NAME, "a10a3f92e9--name-container--enElO").text
        # except NoSuchElementException:
        #     developer = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--logo--QGiT1').text

        parsed_text.append({
            "link": link,
            "main_info": main_info,
            "price": price,
            "price_for_m2": price_for_m2,
            "location": location,
            "subway": subway,
            # "developer": developer
        })
        time.sleep(random.uniform(1, 3))

# Вариант 2
for page_number in range(37):
    button = driver.find_element(By.XPATH, '//*[@id="frontend-serp"]/div/div[5]/div[1]/nav/a')
    button.click()

df = pd.DataFrame(parsed_text)
df['price_m2'] = [metro.split('\n')[1] for metro in df.price_for_m2]

df.to_excel('cian_output.xlsx')
