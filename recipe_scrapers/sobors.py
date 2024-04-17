# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper


class SoBors(AbstractScraper):
    @classmethod
    def host(cls):
        return "sobors.hu"

    def title(self):
        return self.schema.title()

    def description(self):
        return self.schema.description()

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    def prep_time(self):
        return self.schema.prep_time()

    def cook_time(self):
        return self.schema.cook_time()
