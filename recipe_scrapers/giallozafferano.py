# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper


class GialloZafferano(AbstractScraper):
    @classmethod
    def host(cls):
        return "ricette.giallozafferano.it"

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    def ratings(self):
        return self.schema.ratings()
