# mypy: allow-untyped-defs

from ._abstract import AbstractScraper


class AberleHome(AbstractScraper):
    @classmethod
    def host(cls):
        return "aberlehome.com"

    def category(self):
        return self.schema.category()

    def ratings(self):
        return self.schema.ratings()

    def cuisine(self):
        return self.schema.cuisine()

    def description(self):
        return self.schema.description()
