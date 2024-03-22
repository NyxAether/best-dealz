import time
from pathlib import Path

import click

from best_dealz.idealo import Idealo
from best_dealz.paths import Paths
from best_dealz.smtp2go import SMTP2GO, Email


class Notifications:
    def __init__(self, search_terms: str, threshold: float) -> None:
        self.search_terms = search_terms
        self.threshold = threshold
        self.dealz = Idealo(search_terms)
        self.paths = Paths(Path.cwd())
        self.emailer = SMTP2GO(self.paths.config)

    def loop(self, timer: int = 60, timer_after_email: int = 1800) -> None:
        """Check prices every 60 seconds. If price is below threshold, send an email
        and wait for 30 minutes before checking again.

        Args:
            timer (int, optional): timer in seconds to check prices. Defaults to 60.
            timer_after_email (int, optional): timer in seconds to wait
                                after sending an email. Defaults to 1800.
        """
        while True:
            self.dealz.reset()
            time.sleep(timer)
            click.echo(f"Checking prices for {self.search_terms}...")
            best_article = self.dealz.get_min_price_article()
            click.echo(f"Best price is {best_article.price} €")
            if best_article.price < self.threshold:
                click.echo(
                    f"Article {best_article.title} is below {self.threshold} €.\n"
                    f"Current price is {best_article.price} € :\n"
                    f"{best_article.url}"
                )
                new_email = Email(
                    subject=f"Article {best_article.title} is below {self.threshold} €",
                    text_body=f"Current price is {best_article.price} € :\n"
                    f"{best_article.url}",
                )
                self.emailer.send_email(new_email)
                time.sleep(timer_after_email)
