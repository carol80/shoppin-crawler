import threading
import itertools
from mockSearch import search_keyword_using_selenium

searchValue = ["Keyboard mouse"]
websites = [
    "https://www.amazon.in",
    "https://www.flipkart.com",
    "https://www.ajio.com",
    "https://www.walmart.com",
    "https://www.ebay.com",
    "https://www.aliexpress.com"
]


searchItems = [searchVal.split() for searchVal in searchValue]
keyword = " ".join(list(itertools.chain.from_iterable(searchItems)))

threads = []
for url in websites:
    search_keyword_using_selenium(url, keyword)