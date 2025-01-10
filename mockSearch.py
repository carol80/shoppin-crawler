import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options



def search_keyword_using_selenium(url, keyword):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Find the search input element using XPath with placeholder containing "Search"
    try:
        # time.sleep(30)
        search_box = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Search')]")
    except:
        print("Search box not found.")
        driver.quit()
        return

    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)
    driver.quit()
