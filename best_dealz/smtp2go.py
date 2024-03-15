import sys
from pathlib import Path

import requests
import yaml
from pydantic import BaseModel


class EmailConfig(BaseModel):
    sender: str
    to: list[str]
    api_key: str


class Email(BaseModel):
    subject: str
    text_body: str


class SMTP2GO:
    def __init__(self, config_path: Path) -> None:
        self._config = EmailConfig(**yaml.safe_load(config_path.read_text()))
        self._api_url = "https://api.smtp2go.com/v3/email/send"

    def send_email(self, email: Email) -> None:
        response = requests.post(
            self._api_url, json=self._config.model_dump() | email.model_dump()
        )
        if response.status_code != 200:
            print(f"Error while sending email: {response.text}", file=sys.stderr)
