# mypy: allow-untyped-defs

from ._abstract import AbstractScraper


class TheModernProper(AbstractScraper):
    @classmethod
    def host(cls):
        return "themodernproper.com"

    def cuisine(self):
        return self.schema.cuisine()

    def description(self):
        return self.schema.description()
