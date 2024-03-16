from pathlib import Path

import click

from best_dealz.idealo import Idealo
from best_dealz.notifications import Notifications
from best_dealz.paths import Paths
from best_dealz.smtp2go import SMTP2GO, Email


@click.group(help="Find price on idealo")
def main() -> None:
    pass


@click.command(help="Get current minimal price for a product")
@click.argument("search_terms")
def min_price(search_terms: str) -> None:
    dealz = Idealo()
    best_article = dealz.get_min_price_article(search_terms)
    click.echo(
        f"Best price for {search_terms} is {best_article.price} € :\n"
        f"{best_article.url}"
    )


@click.command(help="Alert if article is below threshold")
@click.argument("search_terms")
@click.argument("threshold", type=float)
@click.option(
    "--timer", default=60, help="Timer in seconds to check prices. Defaults to 60"
)
@click.option(
    "--timer-after-email", default=1800, help="Timer in seconds to wait after sending an email. Defaults to 1800"
)
def alert_below(search_terms: str, threshold: float | int, timer: int = 60, timer_after_email: int = 1800) -> None:
    Notifications(search_terms, threshold).loop(timer, timer_after_email)


if __name__ == "__main__":
    main()

main.add_command(min_price)
main.add_command(alert_below)
