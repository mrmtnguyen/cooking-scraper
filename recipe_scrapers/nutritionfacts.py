# mypy: allow-untyped-defs

from ._abstract import AbstractScraper
from ._grouping_utils import group_ingredients


class NutritionFacts(AbstractScraper):
    @classmethod
    def host(cls):
        return "nutritionfacts.org"

    def title(self):
        return self.schema.title()

    def category(self):
        return self.schema.category()

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

    def description(self):
        return self.schema.description()
