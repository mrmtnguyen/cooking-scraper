# mypy: allow-untyped-defs

from ._abstract import AbstractScraper


class EatLiveRun(AbstractScraper):
    @classmethod
    def host(cls):
        return "eatliverun.com"

    def site_name(self):
        return "Eat, Live, Run"

    def title(self):
        return self.schema.title()

    def category(self):
        return self.schema.category()

    def yields(self):
        return self.schema.yields()
