# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper


class CdKitchen(AbstractScraper):
    @classmethod
    def host(cls):
        return "cdkitchen.com"

    def yields(self):
        return self.schema.yields()
