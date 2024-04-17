# mypy: allow-untyped-defs
from ._abstract import AbstractScraper


class TudoGostoso(AbstractScraper):
    @classmethod
    def host(cls):
        return "tudogostoso.com.br"

    def total_time(self):
        return self.schema.total_time()
