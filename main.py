from fastapi import FastAPI

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/pills/{name_pill}")
def read_name(name_pill: str):
    return {'link': parcePill(name_pill)}



def parcePill(query):
    # Настройки для работы с Chrome
    chrome_options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Открыть сайт
        driver.get("https://grls.rosminzdrav.ru/GRLS.aspx")

        # Явное ожидание для текстового поля
        text_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_plate_txtTorg"))
        )
        text_field.send_keys(query)

        # Явное ожидание для кнопки
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_plate_bSeek"))
        )
        submit_button.click()

        # Явное ожидание для строк таблицы
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.hi_sys.poi"))
        )

        if rows:
            rows[0].click()  # Клик по первой строке
        else:
            raise Exception("No rows found")

        # Явное ожидание для кнопки "Показать инструкции"
        instructions_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "instructionsCaller"))
        )
        instructions_button.click()

        # Явное ожидание для ссылки
        link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[target='_blank']"))
        )
        pdf_url = link.get_attribute("href")

        return pdf_url

    finally:
        # Закрыть драйвер
        driver.quit()





