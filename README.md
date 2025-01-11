# shoppin-crawler
A Web Crawler that creates a DB of all the products with given keywords in a given list of e-commerce websites.


## Approach Implemented
1. Selenium wrapper to find the Search bar (discovering the products)
    * Intuition: Every E-commerce website has a searchbox and entering a keyword takes us to the products-list page
    * We can find the searchbox with the help of a conditional Xpath that identifies it based on the [placeholder, name, value, label, aria-label] having values [Search, Find, Shop for, etc..]
    * We can do this with the help of selenium, and just navigate to discovering the product page 

2. Card Detection - Get the clickable elements & check if it is a valid product link
    * Intuition: Almost every website has cards to display the content which when clicked, takes us to the product page.
    * Here we have 2 approaches, 
        * <b>(Not Implemented)</b> one where we perform a pattern identification and find all the cards (which could be really slow & challenging) 
        * the second approach, where we fetch all the clickable elements on that page and verifying if it could be a potential product link.
            * if the link or the text(label) has the keywords searched by the user.
            * check if the product link fits in the compiled generic product-regexes (the regex used is a very generic bt still effective way to eliminate the non-product links.)
            * url correction: hrefs we get from these elements are mostly encoded & may not have the domain along with it(just the redirect url) 

3. Edge Cases
    * Infinite scroll: Since we are using selenium, we can still control the browser and the activity that goes on the browser, so we scroll to the bottom of the page and wait for some time to get the dynamically loaded content.
        * we fetch the page source before and after the scrolling to compare if there's any new content appended to the page
        * If the page sources dont match, it can be derived that there could be dynamic data that's loaded to the page.
        * Since comparing the 2 page sources could be time consuming, we compare the hashcode of both the page-sources.(using hashlib) 
        * Instead of going to the depth of the infinite scroll, we have set the `depth_for_infinite_scroll=5`. To go to more depth, change this.
    * <b>(Not Implemented)</b> Pagination: we can do it using 2 ways
        * Either identify the "Next Page" element using a conditional Xpath and navigate further
        * determine the "Next Page" link from the hrefs & check if that link fits into a compiled page-regexes (mostly when pagination is present, there's params in the url like "page=" or "_pgn", etc)

4. Parallel Processing
    * Threading: set `threading_active` to use this feature. It opens every E-commerce website in a seperate thread and continues processing.
    * Multiprocessing(Works better): set `multiprocessing_active` to use this feature. It opens every E-commerce website as seperate sub-process and continues processing further. To curate the data from all of these subprocesses, we have used a shared variable with Manager()

5. TODOs
    - Integrate saucelabs or browserstack: Currently all the browsers are launched locally limiting the no. of parallel instances. (So integrating it with a cloud provider could speed up the process).
    - Discover the search-url and make API calls to fetch the page-source instead of using selenium. Could be faster.
    - Enhance the product and pagination finding regexes.
    - in most of the websites, we have captcha, or "not a robot verification": look for ways to bypass that.
    - Integrate Celery or have a redis/rabbitmq queue: Since each of these tasks are time consuming, we can add each website as a task. This way, it could help us scale the crawler to take in more load.


### Prerequisite

* Python
* Flask (If we want to convert it to an API wrapper)
* Selenium (For launching the e-commerce websites)

### Installing

* Clone the repository.
* create a virtualenv
* `pip install -r requirements.txt`
* `python crawler.py`

## Deployment

<b>(Not Implemented due to time constraints)</b> Can we deployed to Render or Netlify

## Output

Websites used: <br>
[
    "https://www.amazon.in",
    "https://www.flipkart.com",
    "https://www.ajio.com",
    "https://www.ebay.com",
    "https://www.bewakoof.com",
    "https://www.myntra.com",
    "https://www.nykaa.com",
    "https://www.firstcry.com",
    "https://www.tatacliq.com",
]
<br><br>
keywords:<br> ["black", "jacket"]

* products.json
* products.txt