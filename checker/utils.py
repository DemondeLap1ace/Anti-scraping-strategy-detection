from fake_useragent import UserAgent

def get_random_user_agent():
    ua = UserAgent()
    return ua.random
