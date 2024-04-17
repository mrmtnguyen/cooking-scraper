# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper


class VegRecipesOfIndia(AbstractScraper):
    @classmethod
    def host(cls):
        return "vegrecipesofindia.com"

    def yields(self):
        return self.schema.yields()

    def ratings(self):
        return self.schema.ratings()
