from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def check_dynamic_content(url, max_scrolls=4, wait_time=5):

    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu") 
    chrome_options.add_argument("--no-sandbox")  

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)


        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )


        scroll_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(1, max_scrolls + 1):

            driver.execute_script(f"window.scrollTo(0, {scroll_height * i / (max_scrolls + 1)});")
            time.sleep(2)

        page_source = driver.page_source
        return page_source

    except Exception as e:
        print(f"页面加载出错: {e}")
        return None

    finally:
        driver.quit()


