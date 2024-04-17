# mypy: allow-untyped-defs

from ._abstract import AbstractScraper


class FineDiningLovers(AbstractScraper):
    @classmethod
    def host(cls):
        return "finedininglovers.com"

    def yields(self):
        return self.schema.yields()
