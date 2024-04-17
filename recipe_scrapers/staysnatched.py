# mypy: allow-untyped-defs

from ._abstract import AbstractScraper


class StaySnatched(AbstractScraper):
    @classmethod
    def host(cls):
        return "staysnatched.com"

    def author(self):
        author_element = self.soup.find(
            "div",
            {
                "class": "wprm-recipe-block-container wprm-recipe-block-container-columns wprm-block-text-normal wprm-recipe-author-container"
            },
        )
        return author_element.find("a").get_text() if author_element else "Unknown"

    def category(self):
        return self.schema.category()

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    def ratings(self):
        return self.schema.ratings()

    def cuisine(self):
        return self.schema.cuisine()

    def description(self):
        return self.schema.description()
