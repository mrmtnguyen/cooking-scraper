# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper
from ._grouping_utils import group_ingredients


class RainbowPlantLife(AbstractScraper):
    @classmethod
    def host(cls):
        return "rainbowplantlife.com"

    def yields(self):
        return self.schema.yields()

    def ingredient_groups(self):
        return group_ingredients(
            self.ingredients(),
            self.soup,
            ".wprm-recipe-ingredient-group h4",
            ".wprm-recipe-ingredient",
        )

    def ratings(self):
        return self.schema.ratings()
