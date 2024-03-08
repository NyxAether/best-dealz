from pytest import fixture

from best_dealz.idealo import Article, Idealo


@fixture
def idealo() -> Idealo:
    return Idealo()


def test_get_products(idealo: Idealo) -> None:
    articles = idealo.get_products("iphone")
    assert len(articles) > 0
    assert "iphone" in articles[0].title.lower()
    assert articles[0].price > 0

def test_get_minimal_price(idealo: Idealo,monkeypatch) -> None:
    def patch_get_products(self, search_terms: str) -> list[Article]:
        return [
            Article(
                title="iphone",
                price=300,
            ),
            Article(
                title="iphone",
                price=100,
            ),
            Article(
                title="iphone",
                price=200,
            )
        ]
    monkeypatch.setattr(Idealo, "get_products", patch_get_products)
    assert idealo.get_minimal_price("iphone") == 100
