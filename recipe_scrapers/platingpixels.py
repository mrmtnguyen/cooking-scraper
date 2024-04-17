# mypy: allow-untyped-defs

from ._abstract import AbstractScraper
from ._grouping_utils import group_ingredients


class PlatingPixels(AbstractScraper):
    @classmethod
    def host(cls):
        return "platingpixels.com"

    def author(self):
        author_tag = self.soup.find("strong", string="Author:")
        if author_tag and author_tag.next_sibling:
            return author_tag.next_sibling.strip()
        return "Plating Pixels"

    def title(self):
        return self.schema.title()

    def category(self):
        return self.schema.category()

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    def ingredient_groups(self):
        return group_ingredients(
            self.ingredients(),
            self.soup,
            "h4.wprm-recipe-ingredient-group-name",
            "li.wprm-recipe-ingredient",
        )

    def ratings(self):
        return self.schema.ratings()

    def cuisine(self):
        return self.schema.cuisine()

    def description(self):
        return self.schema.description()
