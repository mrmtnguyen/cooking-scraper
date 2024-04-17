# mypy: allow-untyped-defs

from ._abstract import AbstractScraper


class Epicurious(AbstractScraper):
    @classmethod
    def host(cls):
        return "epicurious.com"

    def author(self):
        return self.soup.find("a", {"itemprop": "author"}).get_text()

    def ratings(self):
        return self.schema.ratings()
