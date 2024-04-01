import pytest
from pydantic_core import Url
from pytest import MonkeyPatch, fixture

from best_dealz.checker.denicheur import Denicheur
from best_dealz.checker.pricechecker import Article, NoArticleFound


@fixture
def denicheur() -> Denicheur:
    return Denicheur("iphone")


def test_get_products(denicheur: Denicheur) -> None:
    articles = denicheur.get_products()
    assert len(articles) > 0
    assert "iphone" in articles[0].title.lower()
    assert articles[0].price > 0


def test_get_min_price_article(denicheur: Denicheur, monkeypatch: MonkeyPatch) -> None:
    def patch_get_products(self: Denicheur) -> list[Article]:
        return [
            Article(
                title="iphone",
                url=Url("https://fake.com"),
                price=300,
            ),
            Article(
                title="iphone",
                url=Url("https://fake.com"),
                price=100,
            ),
            Article(
                title="iphone",
                url=Url("https://fake.com"),
                price=200,
            ),
        ]

    monkeypatch.setattr(Denicheur, "get_products", patch_get_products)
    assert denicheur.get_min_price_article().price == 100
    monkeypatch.setattr(Denicheur, "get_products", lambda self: [])
    with pytest.raises(NoArticleFound):
        denicheur.get_min_price_article()


def test_get_mean_price_article(denicheur: Denicheur, monkeypatch: MonkeyPatch) -> None:
    def patch_get_products(self: Denicheur) -> list[Article]:
        return [
            Article(
                title="iphone",
                url=Url("https://fake.com"),
                price=300,
            ),
            Article(
                title="iphone",
                url=Url("https://fake.com"),
                price=100,
            ),
            Article(
                title="iphone",
                url=Url("https://fake.com"),
                price=200,
            ),
        ]

    monkeypatch.setattr(Denicheur, "get_products", patch_get_products)
    assert denicheur.get_mean_price_article() == 200
    monkeypatch.setattr(Denicheur, "get_products", lambda self: [])
    with pytest.raises(NoArticleFound):
        denicheur.get_mean_price_article()


def test_search_uri(denicheur: Denicheur) -> None:
    assert denicheur.search_uri == "https://ledenicheur.fr/search?search=iphone"
