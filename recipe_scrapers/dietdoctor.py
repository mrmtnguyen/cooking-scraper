# mypy: allow-untyped-defs

from ._abstract import AbstractScraper
from ._utils import normalize_string


class DietDoctor(AbstractScraper):
    @classmethod
    def host(cls):
        return "dietdoctor.com"

    def author(self):
        return self.schema.author()

    def title(self):
        return self.schema.title()

    def category(self):
        return self.schema.category()

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    def image(self):
        return self.schema.image()

    def ingredients(self):
        return self.schema.ingredients()

    def instructions(self):
        instructions = self.soup.select(
            "ol.recipe-steps-list li.recipe-steps-item div.recipe-steps-item-text"
        )

        return "\n".join(
            [normalize_string(instruction.get_text()) for instruction in instructions]
        )

    def ratings(self):
        return self.schema.ratings()

    def cuisine(self):
        return self.schema.cuisine()

    def description(self):
        return self.schema.description()
