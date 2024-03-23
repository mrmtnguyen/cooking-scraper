# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper


class TheExpertGuides(AbstractScraper):
    @classmethod
    def host(cls):
        return "theexpertguides.com"

    def prep_time(self):
        return self.schema.prep_time()

    def cook_time(self):
        return self.schema.cook_time()


    def description(self):
        return self.schema.description()
