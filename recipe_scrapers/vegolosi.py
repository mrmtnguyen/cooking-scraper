# mypy: allow-untyped-defs

from ._abstract import AbstractScraper


class Vegolosi(AbstractScraper):
    @classmethod
    def host(cls):
        return "vegolosi.it"

    def title(self):
        return self.soup.h1.get_text().strip()

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    def ratings(self):
        return self.schema.ratings()
