from pathlib import Path

import click

from best_dealz.idealo import Idealo
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
def alert_below(search_terms: str, threshold: float | int) -> None:
    dealz = Idealo()
    paths = Paths(Path.cwd())
    emailer = SMTP2GO(paths.config)
    best_article = dealz.get_min_price_article(search_terms)
    if best_article.price < threshold:
        click.echo(
            f"Article {best_article.title} is below {threshold} €.\n"
            f"Current price is {best_article.price} € :\n"
            f"{best_article.url}"
        )
        new_email = Email(
            subject=f"Article {best_article.title} is below {threshold} €",
            text_body=f"Current price is {best_article.price} € :\n{best_article.url}",
        )
        emailer.send_email(new_email)


if __name__ == "__main__":
    main()

main.add_command(min_price)
main.add_command(alert_below)
