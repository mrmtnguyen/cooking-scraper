from ._abstract import AbstractScraper
from ._utils import normalize_string


class BongEats(AbstractScraper):
    @classmethod
    def host(cls):
        return "bongeats.com"


    def prep_time(self):
        return self.schema.prep_time()

    def cook_time(self):
        return self.schema.cook_time()


    def ingredients(self):
        ingredients_div = self.soup.find(
            "div",
            class_="recipe-ingredients",
        )
        ingredients = ingredients_div.findAll("li")
        return [normalize_string(ingredient.get_text()) for ingredient in ingredients]

    def instructions(self):
        instructions_div = self.soup.find(
            "div",
            class_="recipe-process",
        )
        instructions = instructions_div.findAll("li")
        return "\n".join(
            [normalize_string(instruction.get_text()) for instruction in instructions]
        )
