from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from tqdm import tqdm
import random
import json

BASE_URL = "https://www.camara.cl/diputados/detalle/gastosoperacionales.aspx"

def get_dip_page(dip_id): 
    return f"{BASE_URL}?prmID={dip_id}#ficha-diputados"

def extract_dip_data(driver, dip_id):
    driver.get( get_dip_page(dip_id) )

    dip_data = {}
    try:
        selector_xpath = '//*[@id="ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlMes"]'
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, selector_xpath))
        )
        month_selector = Select( element )
        month_selector.select_by_visible_text('mayo')

        # get table with data
        table_xpath = '//*[@id="ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_UpdatePanel1"]/div/div[2]/div[3]/table'
        expenses_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, table_xpath))
        )
        table_body = expenses_table.find_element(By.TAG_NAME, "tbody")
        table_rows = table_body.find_elements(By.TAG_NAME, "tr")

        # get different items
        for row in table_rows:
            col = row.find_elements(By.TAG_NAME, "td")
            item_total = col[1].text.strip().replace('.', '')
            dip_data[ col[0].text.strip() ] = int(item_total)

    
    except Exception as e:
        print( f"Error@Dip={dip_id}", e )

    return dip_data


if __name__ == '__main__':

    options = Options()
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--verbose")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    with open('diputades_index.json', 'r') as dip_index:
        dip_data = json.load(dip_index)

    for dip in tqdm(dip_data):
        dip_data[dip]['data'] = extract_dip_data( driver, dip )
        time_to_sleep = 2 + random.random() * 3
        driver.implicitly_wait( time_to_sleep )

    with open('diputades_data.json', 'w+') as dip_file:
        json.dump( dip_data, dip_file, ensure_ascii=False)

