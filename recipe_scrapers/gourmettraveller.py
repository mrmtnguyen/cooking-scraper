# mypy: allow-untyped-defs

import re

from ._abstract import AbstractScraper
from ._grouping_utils import group_ingredients
from ._utils import normalize_string


class GourmetTraveller(AbstractScraper):
    @classmethod
    def host(cls):
        return "gourmettraveller.com.au"

    def author(self):
        return self.schema.author()

    def title(self):
        return self.schema.title()

    def category(self):
        recipe_category_span = self.soup.find(
            "span", {"class": "related-tags__label"}, text=re.compile("Recipe Course")
        )
        if not recipe_category_span:
            return None
        value = recipe_category_span.find_next_sibling("span")
        return normalize_string(value.text)

    def total_time(self):
        return self.schema.total_time()

    def prep_time(self):
        return self.schema.prep_time()

    def cook_time(self):
        return self.schema.cook_time()

    def yields(self):
        return self.schema.yields()

    def image(self):
        return self.schema.image()

    def ingredients(self):
        group_heading_divs = self.soup.find_all(
            "div", {"class": "recipe-ingredients__title"}
        )
        group_headings = [
            normalize_string(group_heading_div.text)
            for group_heading_div in group_heading_divs
        ]

        # The group headings are also included in the ingredients in the schema
        # Remove the group headings from the ingredients
        ingredients = filter(
            lambda ingredient: ingredient not in group_headings,
            self.schema.ingredients(),
        )

        return list(ingredients)

    def instructions(self):
        return self.schema.instructions()

    def ratings(self):
        return self.schema.ratings()

    def cuisine(self):
        return self.schema.cuisine()

    def description(self):
        return self.schema.description()

    def ingredient_groups(self):
        return group_ingredients(
            self.ingredients(),
            self.soup,
            ".recipe-ingredients__title",
            ".recipe-ingredients__item",
        )
