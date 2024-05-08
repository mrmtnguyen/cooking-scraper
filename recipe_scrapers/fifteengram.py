# mypy: allow-untyped-defs

from ._abstract import AbstractScraper


class FifteenGram(AbstractScraper):
    @classmethod
    def host(cls):
        return "15gram.be"

    def canonical_url(self):
        return self.soup.find("meta", {"property": "og:url"}).get("content")

    def author(self):
        return "15gram"

    def title(self):
        return self.schema.title()

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    def image(self):
        return self.schema.image()

    def ingredients(self):
        return self.schema.ingredients()

    def instructions(self):
        return self.schema.instructions()

    def description(self):
        return self.schema.description()
