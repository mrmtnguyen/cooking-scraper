# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper
from ._grouping_utils import group_ingredients


class HalfBakedHarvest(AbstractScraper):
    @classmethod
    def host(cls):
        return "halfbakedharvest.com"

    def author(self):
        return "halfbakedharvest"

    def ingredient_groups(self):
        return group_ingredients(
            self.ingredients(),
            self.soup,
            ".wprm-recipe-ingredient-group h4",
            ".wprm-recipe-ingredient",
        )
