# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper


class ClosetCooking(AbstractScraper):
    @classmethod
    def host(cls):
        return "closetcooking.com"

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()
