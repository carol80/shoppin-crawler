import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse, parse_qsl, urljoin


def handle_redirects(domain, href:str):
    if not href: 
        return None
    if href.startswith("https://") or href.startswith("http://"):
        return href
    
    href=unquote(href)
    parsed_url = urlparse(href)
    query_params = dict(parse_qsl(parsed_url.query))
    redirect_url = query_params.get("url")
    

    if redirect_url:
        if redirect_url.startswith(domain):
            return redirect_url
        else:
            return urljoin(domain, redirect_url)
    else:
        return urljoin(domain, href)
    



def extract_clickable_elements(domain, HTMLPage, keywords):
    soup = BeautifulSoup(HTMLPage, 'html.parser')

    clickable_elements = []
    ss={}

    # Extract links
    for link in soup.find_all('a'):
        href = link.get('href')
        text = link.text.strip()
        
        try:
            if any((key in text.lower()) or (key in href.lower()) for key in keywords) and text not in ss:
                href = handle_redirects(domain, href)
                if href:
                    clickable_elements.append({'type': 'link', 'text': text, 'href': href})
                    ss[text] = href
        except Exception as e:
            print(repr(e))

    # print(soup.find_all('a'))
    # print("------------------------------------------------------------------------------------------------------------------")
    # print(clickable_elements)
    
    # # Extract buttons
    # for button in soup.find_all(['button', 'input']):
    #     text = button.text.strip() if button.name == 'button' else button.get('value', '').strip()
    #     clickable_elements.append({'type': 'button', 'text': text})

    return clickable_elements
