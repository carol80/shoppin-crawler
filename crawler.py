import threading
import multiprocessing
import itertools
from mockSearch import search_keyword_using_selenium
from fetchItems import write_products_to_JSON

searchValue = ["jacket", "shirt"]
websites = [
    # "https://www.amazon.in",
    "https://www.flipkart.com",
    # "https://www.ajio.com",
    # "https://www.ebay.com",
    # "https://www.bewakoof.com",
    # "https://www.myntra.com",
    # "https://www.nykaa.com",
    # "https://www.meesho.com",
    # "https://www.firstcry.com",
    # "https://www.tatacliq.com"
]
threading_active=False
multiprocessing_active=True
products_with_domains = dict()


searchItems = [searchVal.split() for searchVal in searchValue]
keyword = " ".join(list(itertools.chain.from_iterable(searchItems)))


if threading_active:
    threads = []
    for url in websites:
        try:
            t = threading.Thread(target=search_keyword_using_selenium, args=(url, keyword, products_with_domains))
            threads.append(t)
            t.start()
        except Exception:
            print(Exception)

    for t in threads:
        t.join()

elif multiprocessing_active:
    manager = multiprocessing.Manager()
    products_with_domains = manager.dict()
    processes = []
    pool = multiprocessing.Pool(processes=4)

    for url in websites:
        pool.apply_async(search_keyword_using_selenium, args=(url, keyword, products_with_domains))
    
    pool.close()
    pool.join()

    products_with_domains = dict(products_with_domains)

else:
    for url in websites:
        try:
            search_keyword_using_selenium(url, keyword, products_with_domains)
        except Exception as e:
            print(repr(e))

write_products_to_JSON(products_with_domains)