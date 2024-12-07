import re

def check_captcha_script(html):
    captcha_keywords = ['hcaptcha', 'g-recaptcha', 'protected by Cloudflare', 'captcha', 'recaptcha']
    
    for keyword in captcha_keywords:
        if keyword.lower() in html.lower():
            return True

    iframe_pattern = re.compile(r'<iframe[^>]*src="([^"]*)"', re.IGNORECASE)
    if iframe_pattern.search(html):
        iframe_sources = iframe_pattern.findall(html)
        for src in iframe_sources:
            if 'captcha' in src.lower():
                return True

    script_pattern = re.compile(r'<script[^>]*src="([^"]*)"', re.IGNORECASE)
    if script_pattern.search(html):
        scripts = script_pattern.findall(html)
        for script in scripts:
            if 'captcha' in script.lower() or 'recaptcha' in script.lower():
                return True
    
    return False
