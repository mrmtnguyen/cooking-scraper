# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper


class Springlane(AbstractScraper):
    @classmethod
    def host(cls):
        return "springlane.de"
