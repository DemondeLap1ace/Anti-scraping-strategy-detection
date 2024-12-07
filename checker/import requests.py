import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

def check_website(url):

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    session = requests.Session()
    try:
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Response status code: {response.status_code}")
            if response.status_code == 403:
                print("可能被禁止访问，IP或User-Agent被拦截")
            elif response.status_code == 429:
                print("请求过于频繁，可能触发了访问频率限制")
            return

        print("\nResponse Headers:")
        for key, value in response.headers.items():
            print(f"{key}: {value}")

        if 'captcha' in response.text.lower() or 'verify' in response.text.lower() or 'recaptcha' in response.text.lower() or 'hcaptcha' in response.text.lower():
            print("网站可能有验证码机制")

        dynamic_source = check_dynamic_content(url)
        print("动态内容分析完成")

        soup = BeautifulSoup(dynamic_source, 'html.parser')

        meta_tag = soup.find('meta', {'name': 'robots'})
        if meta_tag and ('noindex' in meta_tag.get('content', '').lower() or 'nofollow' in meta_tag.get('content', '').lower()):
            print("网站设置了robots标签，可能不允许爬虫抓取")

        scripts = soup.find_all('script')
        if scripts:
            print("网站中包含JavaScript脚本，可能依赖JavaScript加载内容")

        print("\n开始模拟请求频率检测...")

        for i in range(5):
            time.sleep(0.5)  
            response = session.get(url, headers=headers)
            if response.status_code == 429:
                print("检测到频率限制：状态码429")
                break
            print(f"请求 {i+1}: 成功")


        print("\n模拟用户行为分析：检查JS动态内容和Cookies")
        print(f"初次请求的Cookies: {session.cookies}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

def check_dynamic_content(url):
    driver = webdriver.Chrome()  
    driver.get(url)

    time.sleep(5)

    scroll_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(1, 4): 
        driver.execute_script(f"window.scrollTo(0, {scroll_height * i / 4});")
        time.sleep(2)

    try:
        clickable_elements = driver.find_elements(By.TAG_NAME, "a") 
        if clickable_elements:
            clickable_elements[0].click()  
            time.sleep(3)
    except Exception as e:
        print(f"点击元素失败: {e}")

    try:
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.END)  
        time.sleep(1)
    except Exception as e:
        print(f"键盘输入模拟失败: {e}")

    page_source = driver.page_source

    driver.quit()

    return page_source


check_website(url)
