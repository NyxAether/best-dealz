import re
from statistics import mean

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, HttpUrl


class NoArticleFound(Exception):
    pass


class Article(BaseModel):
    title: str
    price: float = Field(ge=0.0)
    url: HttpUrl

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Article):
            return NotImplemented
        return self.url == other.url

    def __float__(self) -> float:
        return self.price


class Idealo:
    def __init__(self, search_terms: str) -> None:
        self.adress = "https://www.idealo.fr"
        self.search_adress = self.adress + "/prechcat.html"
        self.search_terms = search_terms.lower()
        self._articles = None

    @property
    def search_uri(self) -> str:
        return self.search_adress + "?q=" + self.search_terms

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
        price_pattern = re.compile(r"(\d[\d\s,]*\d)")
        r = session.get(uri, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        articles_html = soup.find_all("div", class_="offerList-item")
        articles: list[Article] = []
        terms_list = self.search_terms.split()
        for article in articles_html:
            title = article.find(
                "div", class_="offerList-item-description-title"
            ).text.strip()
            title_lower = title.lower()
            url = self.adress + article.find("a")["href"]
            price_text = price_pattern.search(
                article.find("div", class_="offerList-item-priceMin").text
            )
            if price_text:
                price = float(re.sub(r"\s", "", price_text.group(0).replace(",", ".")))
            else:
                raise ValueError("No price found")
            if all([term in title_lower for term in terms_list]):
                articles.append(Article(title=title, url=url, price=price))

        return articles

    def get_min_price_article(self) -> Article:
        articles = self.get_products()
        if len(articles) == 0:
            raise NoArticleFound(f"No article found for {self.search_terms}")
        return min(articles, key=lambda article: article.price)

    def get_mean_price_article(self) -> float:
        articles = self.get_products()
        if len(articles) == 0:
            raise NoArticleFound(f"No article found for {self.search_terms}")
        return mean([article.price for article in articles])

    def reset(self) -> None:
        """Reset articles to None, so the next call to get_products will fetch data"""
        self._articles = None
