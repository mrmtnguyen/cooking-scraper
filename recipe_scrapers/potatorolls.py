# mypy: allow-untyped-defs

import warnings

from ._abstract import AbstractScraper
from ._grouping_utils import group_ingredients
from ._utils import get_yields, normalize_string


class PotatoRolls(AbstractScraper):
    @classmethod
    def host(cls):
        return "potatorolls.com"

    def author(self):
        return "Martin's Famous Potato Rolls and Bread"

    def ingredients(self):
        ingredient_blocks = self.soup.select(
            'div[itemprop="ingredients recipeIngredient"] .ingredient p'
        )
        ingredients = [
            normalize_string(ingredient.get_text())
            for ingredient in ingredient_blocks
            if not ingredient.find("strong")
        ]

        return ingredients

    def ingredient_groups(self):
        return group_ingredients(
            self.ingredients(),
            self.soup,
            "div.ingredient > div > p > strong > em",
            "div.ingredient > div > p:not(:has(strong))",
        )

    def instructions(self):
        instructions = self.soup.select('div[itemprop="recipeInstructions"] p')

        return "\n".join(
            [normalize_string(instruction.get_text()) for instruction in instructions]
        )

    def language(self):
        msg = (
            f"{self.host()} appears to write language metadata into HTML DOCTYPE "
            "declaration instead of the top-level 'html' element or elsewhere. "
            "Please let us know if it becomes available in a standard location, "
            "and then we can try to retrieve it dynamically."
        )
        warnings.warn(msg)
        return "en-US"

    def yields(self):
        serve_element = self.soup.find(
            "p", string=lambda text: text.startswith("Serves:")
        )
        if serve_element:
            serves = serve_element.text.split(":")[-1].strip()
            return get_yields(serves)
