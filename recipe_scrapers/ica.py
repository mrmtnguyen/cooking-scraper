# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper


class Ica(AbstractScraper):
    @classmethod
    def host(cls):
        return "ica.se"

    def category(self):
        return self.schema.category()

    def yields(self):
        return self.schema.yields()

    def ratings(self):
        return self.schema.ratings()

    def cuisine(self):
        return self.schema.cuisine()

    def description(self):
        return self.schema.description()

    def nutrients(self):
        return self.schema.nutrients()
