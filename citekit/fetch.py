from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dateparser import parse

# from .citation import Citation


def fetch_data(url):
    data = {}
    url = url.strip()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    data["url"] = url
    parsed_url = urlparse(url)
    data["domain"] = parsed_url.netloc.replace("www.", "")

    data["title"] = get_title(soup).strip()
    data["author"] = get_author(soup).strip()
    data["published"] = get_published_date(soup).strip()

    return data


def parse_data(data):
    dt = parse(data["published"])
    if dt is not None:
        data["published"] = dt.year
    return data


def find_all(searches: list, soup):
    results = []
    for s in searches:
        results += soup.find_all(attrs=s)

    for res in results:
        res = res["content"] if "content" in str(res.keys) else res.text
        if res is not None:
            return res

    return ""


def get_title(soup):
    return soup.select("title")[0].text if soup.select("title") else ""


def get_author(soup):
    searches = [
        {"name": "author"},
        {"property": "article:author"},
        {"property": "author"},
        {"rel": "author"},
    ]

    return find_all(searches, soup)


def get_published_date(soup):
    searches = [
        {"name": "date"},
        {"property": "published_time"},
        {"name": "timestamp"},
        {"class": "submitted-date"},
        {"class": "posted-on"},
        {"class": "timestamp"},
        {"class": "date"},
    ]

    return find_all(searches, soup)
