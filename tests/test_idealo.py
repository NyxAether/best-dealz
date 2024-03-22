import pytest
from pydantic_core import Url
from pytest import MonkeyPatch, fixture

from best_dealz.idealo import Article, Idealo, NoArticleFound


@fixture
def idealo() -> Idealo:
    return Idealo("iphone")


def test_get_products(idealo: Idealo) -> None:
    articles = idealo.get_products()
    assert len(articles) > 0
    assert "iphone" in articles[0].title.lower()
    assert articles[0].price > 0


def test_get_min_price_article(idealo: Idealo, monkeypatch: MonkeyPatch) -> None:
    def patch_get_products(self: Idealo) -> list[Article]:
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

    monkeypatch.setattr(Idealo, "get_products", patch_get_products)
    assert idealo.get_min_price_article().price == 100
    monkeypatch.setattr(Idealo, "get_products", lambda self: [])
    with pytest.raises(NoArticleFound):
        idealo.get_min_price_article()


def test_get_mean_price_article(idealo: Idealo, monkeypatch: MonkeyPatch) -> None:
    def patch_get_products(self: Idealo) -> list[Article]:
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

    monkeypatch.setattr(Idealo, "get_products", patch_get_products)
    assert idealo.get_mean_price_article() == 200
    monkeypatch.setattr(Idealo, "get_products", lambda self: [])
    with pytest.raises(NoArticleFound):
        idealo.get_mean_price_article()


def test_search_uri(idealo: Idealo) -> None:
    assert idealo.search_uri == "https://www.idealo.fr/prechcat.html?q=iphone"
