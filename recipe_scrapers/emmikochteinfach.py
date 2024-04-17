# mypy: allow-untyped-defs
from ._abstract import AbstractScraper


class EmmiKochtEinfach(AbstractScraper):
    @classmethod
    def host(cls):
        return "emmikochteinfach.de"

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

    def total_time(self):
        return self.schema.total_time()

    def cook_time(self):
        return self.schema.cook_time()

    def prep_time(self):
        return self.schema.prep_time()
