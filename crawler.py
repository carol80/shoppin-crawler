import threading
import multiprocessing
import itertools
from mockSearch import search_keyword_using_selenium

searchValue = ["jacket", "shirt"]
websites = [
    # "https://www.amazon.in",
    # "https://www.flipkart.com",
    "https://www.ajio.com",
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


searchItems = [searchVal.split() for searchVal in searchValue]
keyword = " ".join(list(itertools.chain.from_iterable(searchItems)))


if threading_active:
    threads = []
    for url in websites:
        try:
            t = threading.Thread(target=search_keyword_using_selenium, args=(url, keyword, ))
            threads.append(t)
            t.start()
        except Exception:
            print(Exception)

    for t in threads:
        t.join()

elif multiprocessing_active:
    processes = []
    pool = multiprocessing.Pool(processes=4)

    for url in websites:
        pool.apply_async(search_keyword_using_selenium, args=(url, keyword, ))
    
    pool.close()
    pool.join()

else:
    for url in websites:
        try:
            search_keyword_using_selenium(url, keyword)
        except Exception as e:
            print(repr(e))