from abc import ABC, abstractmethod

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


class PriceChecker(ABC):
    def __init__(self, search_terms: str) -> None:
        self._search_terms = search_terms.lower()
        self._articles: None | list[Article] = None

    @property
    def search_terms(self) -> str:
        return self._search_terms

    @property
    @abstractmethod
    def search_uri(self) -> str:
        pass

    @abstractmethod
    def get_products(self) -> list[Article]:
        pass

    @abstractmethod
    def get_min_price_article(self) -> Article:
        pass

    @abstractmethod
    def get_mean_price_article(self) -> float:
        pass

    def reset(self) -> None:
        """Reset articles to None, so the next call to get_products will fetch data"""
        self._articles = None
