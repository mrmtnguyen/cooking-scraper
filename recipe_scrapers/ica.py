# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper


class Ica(AbstractScraper):
    @classmethod
    def host(cls):
        return "ica.se"

    def cuisine(self):
        return self.schema.cuisine()

    def description(self):
        return self.schema.description()
