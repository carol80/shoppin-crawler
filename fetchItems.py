import requests
from bs4 import BeautifulSoup
import time


def get_product_links(page_source):
    pass


def detect_pagination(page_source):
    pass


def get_product_urls(base_url:str, search_query:str, page_number:int=2):
    product_urls = []

    while page_number<3:
        url = base_url.format(search_query, page_number)
        headers = {
            "User-Agent": ""
        }
        
        response = requests.get(url, headers=headers)
        print(url)

        with open("./ajio.html", "wb+") as file:
            file.write(response.content)
        
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        if not products:
            print("No more products found.")
            break
        
        for product in products:
            link = product.h2.a['href']
            full_url = f"https://www.amazon.in{link}"
            product_urls.append(full_url)
        
        print(f"Page {page_number} processed. Found {len(products)} products.")
        page_number += 1
        time.sleep(2)

    return product_urls