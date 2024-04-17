# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper


class EthanChlebowski(AbstractScraper):
    @classmethod
    def host(cls):
        return "ethanchlebowski.com"

    def category(self):
        return self.schema.category()

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    def ratings(self):
        return None

    def cuisine(self):
        return None

    def description(self):
        return self.soup.head.find("meta", {"property": "og:description"})["content"]
