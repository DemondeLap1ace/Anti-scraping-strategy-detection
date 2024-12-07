from website_checker import check_website  
from config import Config 

def main():
    check_website(Config.TEST_URL)

if __name__ == "__main__":
    main()
