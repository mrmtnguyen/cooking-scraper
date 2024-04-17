# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper
from ._grouping_utils import group_ingredients


class HalfBakedHarvest(AbstractScraper):
    @classmethod
    def host(cls):
        return "halfbakedharvest.com"

    def cook_time(self):
        return self.schema.cook_time()

    def prep_time(self):
        return self.schema.prep_time()

    def nutrients(self):
        return self.schema.nutrients()

    def ingredient_groups(self):
        return group_ingredients(
            self.ingredients(),
            self.soup,
            ".wprm-recipe-ingredient-group h4",
            ".wprm-recipe-ingredient",
        )

    def ratings(self):
        return self.schema.ratings()

    def description(self):
        return self.schema.description()
