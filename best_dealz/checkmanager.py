import sys

from best_dealz.checker.pricechecker import NoArticleFound, PriceChecker
from best_dealz.smtp2go import SMTP2GO, Email


class CheckManager:
    def __init__(self, price_checker: PriceChecker, mailer: SMTP2GO) -> None:
        self._price_checker = price_checker
        self._mailer = mailer

    def check_min_price(self, threshold: float) -> None:
        try:
            min_price_article = self._price_checker.get_min_price_article()
            mean_price = self._price_checker.get_mean_price_article()
            if min_price_article.price < threshold:
                search_tems = self._price_checker.search_terms
                subject = f"{search_tems} at {min_price_article.price} €"
                body = (
                    f"""Article "{min_price_article.title}" is at """
                    f"""{min_price_article.price} €\n"""
                    f"Average price for {search_tems} is {mean_price:.2f} €\n"
                    f"See article at {min_price_article.url}\n"
                    f"Search url : {self._price_checker.search_uri}"
                )
                self._mailer.send_email(Email(subject=subject, text_body=body))
                print(
                    f"Email sent\n"
                    f"Best price for {search_tems} is {min_price_article.price} €"
                )
        except NoArticleFound:
            print(
                f"Checker {self._price_checker.__class__.__name__} "
                "did not find an article.\n"
                f"No article found.\n"
                f"Search terms : {self._price_checker.search_terms}",
                file=sys.stderr,
            )
