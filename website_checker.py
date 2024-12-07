import requests 
from bs4 import BeautifulSoup
from checker.dynamic_checker import check_dynamic_content
from checker.captcha_checker import check_captcha_script
from checker.utils import get_random_user_agent
from checker.fingerprint_checker import check_browser_fingerprint
from config import Config
import time


def check_website(url):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    session = requests.Session()

    try:
        start_time = time.time()
        response = session.get(url, headers=headers)
        elapsed_time = time.time() - start_time

        print(f"HTTP响应状态: {response.status_code} - {response.reason}")
        print(f"请求响应时间: {elapsed_time:.2f}秒")

        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return

        # --- Response Headers ---
        print("\n--- Response Headers ---")
        print("| Header                       | Value                                                                                                                   |")
        print("|------------------------------|-------------------------------------------------------------------------------------------------------------------------|")
        for key, value in response.headers.items():
            print(f"| **{key}**                      | {value:<100} |")

        # --- 验证码检测 ---
        captcha_check = check_captcha_script(response.text)
        print(f"\n检测到验证码机制: {'是' if captcha_check else '否'}")

        # --- 动态内容检查 ---
        dynamic_content = check_dynamic_content(url)
        print(f"动态内容加载: {'是' if len(dynamic_content) > 500 else '否'}")
        print(f"动态内容（前100字符）：\n{dynamic_content[:100]}")

        # --- 浏览器指纹检测 ---
        fingerprint_check = check_browser_fingerprint(dynamic_content)
        print(f"检测到浏览器指纹机制: {'是' if fingerprint_check else '否'}")

        # --- Robots 标签检查 ---
        soup = BeautifulSoup(dynamic_content, 'html.parser')
        meta_tag = soup.find('meta', {'name': 'robots'})
        robots_check = 'noindex' in (meta_tag.get('content', '').lower() if meta_tag else '') or 'nofollow' in (meta_tag.get('content', '').lower() if meta_tag else '')
        print(f"Robots标签是否禁止抓取: {'是' if robots_check else '否'}")

        # --- Cookie 信息 ---
        print("\n--- Cookie 信息 ---")
        cookies = response.headers.get('Set-Cookie', '').split(';')
        print("| Cookie Name                  | Value                                                                                                                   |")
        print("|------------------------------|-------------------------------------------------------------------------------------------------------------------------|")
        for cookie in cookies:
            cookie_name, cookie_value = cookie.split('=', 1) if '=' in cookie else (cookie, 'N/A')
            print(f"| {cookie_name:<30} | {cookie_value:<100} |")

        if 'aliyungf_tc' in response.headers.get('Set-Cookie', ''):
            print(" ")

        with open('anti_scraping_report.txt', 'w') as f:
            f.write("检测结果：\n")
            f.write(f"HTTP响应状态: {response.status_code} - {response.reason}\n")
            f.write(f"请求响应时间: {elapsed_time:.2f}秒\n")

            f.write("\n--- Response Headers ---\n")
            f.write("| Header                       | Value                                                                                                                   |\n")
            f.write("|------------------------------|-------------------------------------------------------------------------------------------------------------------------|\n")
            for key, value in response.headers.items():
                f.write(f"| **{key}**                      | {value:<100} |\n")

            f.write(f"\n检测到验证码机制: {'是' if captcha_check else '否'}\n")

            f.write(f"\n动态内容加载: {'是' if len(dynamic_content) > 500 else '否'}\n")
            f.write(f"动态内容（前200字符）：\n{dynamic_content[:200]}\n")

            f.write(f"\n检测到浏览器指纹机制: {'是' if fingerprint_check else '否'}\n")

            f.write(f"\nRobots标签是否禁止抓取: {'是' if robots_check else '否'}\n")

            f.write("\n--- Cookie 信息 ---\n")
            f.write("| Cookie Name                  | Value                                                                                                                   |\n")
            f.write("|------------------------------|-------------------------------------------------------------------------------------------------------------------------|\n")
            for cookie in cookies:
                cookie_name, cookie_value = cookie.split('=', 1) if '=' in cookie else (cookie, 'N/A')
                f.write(f"| {cookie_name:<30} | {cookie_value:<100} |\n")

            if 'aliyungf_tc' in response.headers.get('Set-Cookie', ''):
                f.write("\n")

    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        with open('anti_scraping_report.txt', 'a') as f:
            f.write(f"请求发生错误: {e}\n")
