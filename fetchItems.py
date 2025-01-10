import requests
from bs4 import BeautifulSoup
import time
from getProductLink import extract_clickable_elements, is_product_url


def write_products_to_file(products, filename="products.txt"):
    try:
        with open(filename, "a") as file:  # "a" for append mode
            file.writelines("\n".join(products))
        print(f"Content appended to '{filename}' successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def detect_pagination(buttons):
    pass


def detect_infinite_scroll(page_source):
    pass


def get_product_links(domain, page_source, keyword:str):
    products = []
    clickable_elements = extract_clickable_elements(domain, page_source, keyword.split())
    links = [obj["href"] for obj in clickable_elements if obj['type']=='link']
    buttons = [obj for obj in clickable_elements if obj['type']=='button']

    write_products_to_file(is_product_url(links))

    # if detect_pagination(buttons):
    #     # get_product_urls()
    #     pass


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