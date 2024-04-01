from pathlib import Path

import click

from best_dealz.checker.denicheur import Denicheur
from best_dealz.checker.idealo import Idealo
from best_dealz.checker.pricechecker import NoArticleFound, PriceChecker
from best_dealz.checkmanager import CheckManager
from best_dealz.paths import Paths
from best_dealz.smtp2go import SMTP2GO


@click.group(help="Find price on idealo")
def main() -> None:
    pass


@click.command(help="Get current minimal price for a product")
@click.argument("search_terms")
def min_price(search_terms: str) -> None:
    try:
        dealz = Idealo(search_terms)
        print_min_price(dealz)
        denicheur = Denicheur(search_terms)
        print_min_price(denicheur)

    except NoArticleFound as e:
        click.echo(e)


@click.command(help="Alert if article is below threshold")
@click.argument("search_terms")
@click.argument("threshold")
def alert_below(
    search_terms: str,
    threshold: str,
) -> None:
    """Alert if article is below threshold

    Args:
        search_terms (str): Search terms use for the deal search.
            Can be multiple searches if separated by comma
        threshold (float | int): Threshold below which an email is sent.
            Can be multiple thresholds if separated by comma
    """
    if "," in str(search_terms):
        search_terms_list = search_terms.split(",")
        threshold_list = threshold.split(",")
    else:
        search_terms_list = [search_terms]
        threshold_list = [threshold]

    paths = Paths(Path.cwd())
    emailer = SMTP2GO(paths.config)
    for search_term, thresh in zip(search_terms_list, threshold_list):
        try:
            dealz = Idealo(search_term)
            checker = CheckManager(dealz, emailer)
            checker.check_min_price(float(thresh))
            denicheur = Denicheur(search_term)
            checker = CheckManager(denicheur, emailer)
            checker.check_min_price(float(thresh))
        except ValueError as e:
            click.echo(e)


main.add_command(min_price)
main.add_command(alert_below)


def print_min_price(checker: PriceChecker) -> None:
    min_price_article = checker.get_min_price_article()
    mean_price = checker.get_mean_price_article()
    print(
        f"Average price for {checker.search_terms} is {mean_price:.2f} € :\n"
        f"Best price for {checker.search_terms} is {min_price_article.price} € :\n"
        f"Best article : {min_price_article.url}\n"
        f"Search : {checker.search_uri}"
    )


if __name__ == "__main__":
    main()
