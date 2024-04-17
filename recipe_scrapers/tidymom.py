# mypy: allow-untyped-defs

from ._abstract import AbstractScraper
from ._grouping_utils import group_ingredients


class TidyMom(AbstractScraper):
    @classmethod
    def host(cls):
        return "tidymom.net"

    def category(self):
        return self.schema.category()

    def yields(self):
        return self.schema.yields()

    def ingredient_groups(self):
        return group_ingredients(
            self.ingredients(),
            self.soup,
            ".mv-create-ingredients h4",
            ".mv-create-ingredients li",
        )

    def cuisine(self):
        return self.schema.cuisine()

    def description(self):
        return self.schema.description()
