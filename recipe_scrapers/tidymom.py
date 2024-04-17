# mypy: allow-untyped-defs

from ._abstract import AbstractScraper
from ._grouping_utils import group_ingredients


class TidyMom(AbstractScraper):
    @classmethod
    def host(cls):
        return "tidymom.net"

    def category(self):
        return self.schema.category()

    def ingredient_groups(self):
        return group_ingredients(
            self.ingredients(),
            self.soup,
            ".mv-create-ingredients h4",
            ".mv-create-ingredients li",
        )

    def cuisine(self):
        return self.schema.cuisine()
