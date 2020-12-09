from bs4 import BeautifulSoup
import requests
import cfscrape


URL = 'https://www.avito.ru/'
HEADERS = {'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 \
    Safari/537.36", 'accept': '*/*'}


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
    #  reg = input() | mordoviya | moskva | simferopol | rossiya
    #  q = input() | fifa | лыжи+беговые | книга
    html = get_html(URL+reg+"?q="+q)
    if html.status_code == 200:
        count = get_content(html.text)
        return count
    else:
        return "Error:", html.status_code
