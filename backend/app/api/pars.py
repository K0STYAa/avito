from bs4 import BeautifulSoup
import requests
import cfscrape


URL = 'https://www.avito.ru/'
HEADERS = {'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 \
    Safari/537.36", 'accept': '*/*'}
HOST = 'https://www.avito.ru'


def get_session():
    session = requests.Session()
    session.headers = {
        'Host': 'www.avito.ru',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; \
            x64; rv:69.0)   Gecko/20100101 Firefox/69.0',
        'Accept': '*/*'}
    return cfscrape.create_scraper(sess=session)


def get_html(url, params=None):
    session = get_session()
    r = session.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    count = soup.find('span', class_="page-title-count-1oJOc").get_text()
    count = "".join(count.split(" "))
    return count


def parse(reg: str, q: str):
    html = get_html(URL+reg+"?q="+q)
    if html.status_code == 200:
        return get_content(html.text)
    else:
        return "Error:", html.status_code


def get_content_top(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="iva-item-content-m2FiN")
    res = []
    for item in items:
        if len(res) >= 5:
            break
        tmp = item.find('div', class_="iva-item-titleStep-2bjuh")
        if tmp is None:
            continue
        price = item.find('span', class_="price-text-1HrJ_").get_text(strip=True)
        res.append({
            "link": HOST + tmp.find('a').get('href'),
            "price": price
        })

    return res


def parse_top(reg: str, q: str):
    html = get_html(URL+reg+"?q="+q)
    if html.status_code == 200:
        return get_content_top(html.text)
    else:
        return "Error:", html.status_code
