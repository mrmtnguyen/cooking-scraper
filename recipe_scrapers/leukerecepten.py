# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper


class Leukerecepten(AbstractScraper):
    @classmethod
    def host(cls):
        return "leukerecepten.nl"

    def category(self):
        return self.schema.category()

    def ratings(self):
        return self.schema.ratings()

    def cuisine(self):
        return self.schema.cuisine()

    def description(self):
        return self.schema.description()
