from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from tqdm import tqdm
import json

INDEX_URL = 'https://www.camara.cl/diputados/diputados.aspx#mostrarDiputados'

options = Options()
options.add_argument("--window-size=1920x1080")
options.add_argument("--verbose")
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)


driver.get( INDEX_URL )

# get index page with all codes
dip_data = {}

try:
    index_xpath = '//*[@id="ContentPlaceHolder1_ContentPlaceHolder1_pnlDiputadosLista"]'
    dip_table = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, index_xpath))
        )
    diputades = dip_table.find_elements(By.TAG_NAME, "article")

    for dip in tqdm(diputades, desc='Index'):
        dip_name = dip.find_element(By.TAG_NAME, 'h4').text
        dip_info = dip.find_elements(By.TAG_NAME, 'p')
        dip_district, dip_party = dip_info[0].text, dip_info[1].text.replace("Partido: ", "")

        dip_id = dip.find_element(By.TAG_NAME, 'a').get_attribute('href').split('=')[-1]

        dip_img = dip.find_element(By.TAG_NAME, 'img').get_attribute('src')

        dip_data[ dip_id ] = { 
            'name': dip_name,
            'district': dip_district,
            'party': dip_party,
            'image': dip_img
        }

except Exception as e:
    print( e )

with open('diputades_index.json', 'w+') as dip_file:
    json.dump( dip_data, dip_file, ensure_ascii=False)
print("Done!")

