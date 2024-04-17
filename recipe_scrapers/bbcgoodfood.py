# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper
from ._grouping_utils import group_ingredients


class BBCGoodFood(AbstractScraper):
    @classmethod
    def host(cls):
        return "bbcgoodfood.com"

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    def ingredient_groups(self):
        return group_ingredients(
            self.ingredients(),
            self.soup,
            ".recipe__ingredients h3",
            ".recipe__ingredients li",
        )

    def description(self):
        return self.schema.description()
