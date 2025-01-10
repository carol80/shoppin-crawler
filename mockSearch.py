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
from fetchItems import get_product_links


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
        print("Search box not found.", url)
        driver.quit()
        return

    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

    page_source = driver.page_source
    get_product_links(domain=url, page_source=page_source, keyword=keyword)

    # if pagination is there, do something

    driver.quit()



def initialize_chrome_driver_instance():
	# logger.info(f"{Colors.CYAN}Initializing{Colors.END}{Colors.YELLOW} chrome-driver{Colors.END} {Colors.CYAN}   'webdriver_instance' for web-automation via chrome...{Colors.END}")
	service = ChromeService(executable_path="./driver/chromedriver")

	chrome_options = webdriver.ChromeOptions()
	chrome_options.headless = False  # Set to False if you want to see the browser while running
	# chrome_options.add_experimental_option("debuggerAddress", debugger_address)
	chrome_options.add_argument("--auto-open-devtools-for-tabs")
	chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

	driver_instance = webdriver.Chrome(service=service, options=chrome_options)

	# Enable network logging
	driver_instance.execute_cdp_cmd('Network.enable', {})

	# logger.info(f"{Colors.GREEN}Successfully initialized webdriver_instance:{Colors.END}")
	# logger.info(f"{Colors.MAGENTA} {driver_instance} {Colors.END}")
	# logger.info(f"{Colors.BLUE}Returning;{Colors.END} {Colors.YELLOW}driver_instance{Colors.END}")
	# logger.info(f"{Colors.CYAN}-{Colors.END}{Colors.CYAN} driver_instance:{Colors.END} {Colors.YELLOW}{driver_instance}{Colors.END}")

	# Print a blank line to the terminal
	print("")
	return driver_instance


def intercept_traffic_check_log_auth(driver_instance):
    driver_instance.get("https://amazon.in")
    time.sleep(5)
    intercepted_traffic_object = driver_instance.get_log("performance")
    #print(intercepted_traffic_object)

    return intercepted_traffic_object

# print(intercept_traffic_check_log_auth(initialize_chrome_driver_instance()))



def track_network_calls(url, search_term):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    service = ChromeService(executable_path="./driver/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    # Enable Network and Runtime domains
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Runtime.enable", {})

    network_logs = []

    def process_network_event(params):
        if "Network.requestWillBeSent" in params["method"]:
            request = params["params"]["request"]
            network_logs.append({
                "type": "request",
                "url": request["url"],
                "method": request["method"],
                "headers": request.get("headers", {})
            })
        elif "Network.responseReceived" in params["method"]:
            response = params["params"]["response"]
            network_logs.append({
                "type": "response",
                "url": response["url"],
                "status": response["status"],
                "headers": response.get("headers", {})
            })

    # Override the original `send` method
    original_execute = driver.execute

    def execute(driver_command, params=None):
        result = original_execute(driver_command, params)
        if driver_command == 'executeCdpCommand':
            process_network_event(params)
        return result

    driver.execute = execute

    try:
        if "amazon.in" in url:
            search_box = driver.find_element(By.ID, "twotabsearchtextbox")
        elif "ajio.com" in url:
            search_box = driver.find_element(By.CLASS_NAME, "ajio-search-bar")
        else:
            print("Website not supported")
            return []

        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

    except Exception as e:
        print(f"Error during search: {e}")
        driver.quit()
        return []

    driver.quit()
    return network_logs


def track_network_calls(url, search_term):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    service = ChromeService(executable_path="./driver/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    # Enable Network and Runtime domains
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Runtime.enable", {})

    network_logs = []

    def get_network_logs():
        logs = driver.execute_cdp_cmd("Network.getResponseBody", {})
        return logs

    try:
        if "amazon.in" in url:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
            )
        elif "ajio.com" in url:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ajio-search-bar"))
            )
        else:
            print("Website not supported")
            return []

        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='s-main-slot s-result-list s-search-results sg-row']")))

        # Capture logs after page load
        network_entries = driver.execute_cdp_cmd("Network.getResponseBody", {})
        print(network_entries)
        for entry in network_entries:
            if "Network.requestWillBeSent" in entry:
                request = entry['params']['request']
                network_logs.append({
                    "type": "request",
                    "url": request["url"],
                    "method": request["method"],
                    "headers": request.get("headers", {})
                })
            if "Network.responseReceived" in entry:
                response = entry['params']['response']
                network_logs.append({
                    "type": "response",
                    "url": response["url"],
                    "status": response["status"],
                    "headers": response.get("headers", {})
                })

    except Exception as e:
        print(f"Error during search or log capture: {e}")
        driver.quit()
        return []

    driver.quit()
    return network_logs