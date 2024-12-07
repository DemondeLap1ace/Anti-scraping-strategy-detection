# 文件：checker/fingerprint_checker.py

def check_browser_fingerprint(response_text):

    fingerprint_indicators = [
        'navigator.language',  
        'navigator.userAgent',  
        'navigator.platform',  
        'navigator.screen',    
        'navigator.hardwareConcurrency',  
    ]
    
    for indicator in fingerprint_indicators:
        if indicator in response_text:
            return True
    
    return False
