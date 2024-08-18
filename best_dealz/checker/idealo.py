import re

import requests
from bs4 import BeautifulSoup

from best_dealz.checker.pricechecker import Article, PriceChecker


class Idealo(PriceChecker):
    def __init__(self, search_terms: str) -> None:
        super().__init__(search_terms)
        self.adress = "https://www.idealo.fr"
        self._search_adress = self.adress + "/prechcat.html"
        self._search_terms = search_terms.lower()
        self._articles = None

    @property
    def search_uri(self) -> str:
        return self._search_adress + "?q=" + self._search_terms

    def get_products(self) -> list[Article]:
        if self._articles is not None:
            return self._articles
        uri = self.search_uri
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; "
                    "rv:129.0) Gecko/20100101 Firefox/129.0"
                ),
                "Accept": (
                    "text/html,application/xhtml+xml,application/xml;"
                    "q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;"
                    "q=0.8"
                ),
                "Accept-Language": "fr-FR,en-US;q=0.7,en;q=0.3",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Sec-GPC": "1",
                "Priority": "u=0, i",
            }
        )
        price_pattern = re.compile(r"(\d[\d\s,]*\d)")
        r = session.get(uri, timeout=60)
        if r.status_code != 200:
            raise ValueError(
                f"Error while getting products: {r.status_code}"
                f"\nUri tested is {uri}"
                f"\nResponse: {r.text}"
            )
        soup = BeautifulSoup(r.text, "html.parser")
        articles_html = soup.find_all(
            "div", attrs={"class": re.compile("sr-resultList__item")}
        )
        articles: list[Article] = []
        terms_list = self._search_terms.split()
        for article in articles_html:
            title = article.find(
                "div", attrs={"class": re.compile(r"sr-productSummary__title")}
            ).text.strip()
            title_lower = title.lower()
            if article.find("a") is None:
                continue
            url = article.find("a")["href"]
            price_text = price_pattern.search(
                article.find(
                    "div", attrs={"class": re.compile(r"detailedPriceInfo__price")}
                ).text
            )
            if price_text:
                price = float(re.sub(r"\s", "", price_text.group(0).replace(",", ".")))
            else:
                raise ValueError("No price found")
            if all([term in title_lower for term in terms_list]):
                articles.append(Article(title=title, url=url, price=price))
        self._articles = articles
        return articles
