# mypy: allow-untyped-defs
from ._abstract import AbstractScraper


class EmmiKochtEinfach(AbstractScraper):
    @classmethod
    def host(cls):
        return "emmikochteinfach.de"



    def cook_time(self):
        return self.schema.cook_time()

    def prep_time(self):
        return self.schema.prep_time()
