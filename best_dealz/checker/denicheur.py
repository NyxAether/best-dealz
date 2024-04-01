import re
from unicodedata import normalize

import requests
from bs4 import BeautifulSoup

from best_dealz.checker.pricechecker import Article, PriceChecker


class Denicheur(PriceChecker):
    def __init__(self, search_terms: str) -> None:
        super().__init__(search_terms)
        self.adress = "https://ledenicheur.fr"
        self._search_adress = self.adress
        self._search_terms = search_terms.lower()
        self._articles = None

    @property
    def search_uri(self) -> str:
        return self._search_adress + f"/search?search={self._search_terms}"

    def get_products(self) -> list[Article]:
        if self._articles is not None:
            return self._articles
        uri = self.search_uri
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) "
                    "Gecko/20100101 Firefox/123.0"
                ),
                "Accept": (
                    "text/html,application/xhtml+xml,application/xml;"
                    "q=0.9,image/avif,image/webp,*/*;q=0.8"
                ),
                "Accept-Language": "fr-FR,en-US;q=0.7,en;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
            }
        )
        r = session.get(uri, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        articles_html = soup.find_all(attrs={"data-test": "ProductGridCard"})
        articles: list[Article] = []
        terms_list = self._search_terms.split()
        price_pattern = re.compile(r"(\d[\d\s]*,\d+)")
        for article in articles_html:
            title = article.find(attrs={"data-test": "ProductName"}).text.strip()
            title_lower = title.lower()
            card_link = article.find("a",attrs={"data-test": "InternalLink"})
            if card_link is None:
                continue
            url = self.adress + card_link["href"]
            price_element= card_link.select("div > div > div > div > span")
            if len(price_element) == 0:
                continue
            price_match = price_pattern.search(
                # normalize is used to remove unicode space \xa0
                normalize("NFKD", card_link.select("div > div > div > div > span")[-1].text)
            )
            if price_match:
                price = float(price_match.group(0).replace(",", ".").replace(" ", ""))
            else:
                raise ValueError("No price found")
            if all(term in title_lower for term in terms_list):
                articles.append(Article(title=title, price=price, url=url))
        self._articles = articles
        return articles

