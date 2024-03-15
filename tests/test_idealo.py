from pydantic_core import Url
from pytest import MonkeyPatch, fixture

from best_dealz.idealo import Article, Idealo


@fixture
def idealo() -> Idealo:
    return Idealo()


def test_get_products(idealo: Idealo) -> None:
    articles = idealo.get_products("iphone")
    assert len(articles) > 0
    assert "iphone" in articles[0].title.lower()
    assert articles[0].price > 0


def test_get_min_price_article(idealo: Idealo, monkeypatch: MonkeyPatch) -> None:
    def patch_get_products(self: Idealo, search_terms: str) -> list[Article]:
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
    assert idealo.get_min_price_article("iphone").price == 100
