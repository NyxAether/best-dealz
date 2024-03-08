import re

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field


class Article(BaseModel):
    title: str
    price: float = Field(ge=0.0)


class Idealo:
    def __init__(self) -> None:
        self.adress = "https://www.idealo.fr/prechcat.html"

    def get_products(self, search_terms: str) -> list[Article]:
        uri = self.adress + "?q=" + search_terms
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
        price_pattern = re.compile(r"([\d,]+)")
        r = session.get(uri, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        articles_html = soup.find_all("div", class_="offerList-item")
        articles: list[Article] = []
        for article in articles_html:
            title = article.find(
                "div", class_="offerList-item-description-title"
            ).text.strip()
            price_text = price_pattern.search(
                article.find("div", class_="offerList-item-priceMin").text
            )
            if price_text:
                price = float(price_text.group(0).replace(",", "."))
            else:
                raise ValueError("No price found")
            articles.append(Article(title=title, price=price))

        return articles

    def get_minimal_price(self, search_terms: str) -> float:
        articles = self.get_products(search_terms)
        return min([article.price for article in articles])
