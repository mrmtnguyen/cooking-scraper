# mypy: allow-untyped-defs

from ._abstract import AbstractScraper
from ._utils import normalize_string


class Yummly(AbstractScraper):
    @classmethod
    def host(cls):
        return "yummly.com"

    def title(self):
        return self.schema.title()

    def author(self):
        return self.schema.author()

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    def ingredients(self):
        return self.schema.ingredients()

    def instructions(self):
        instructions = self.soup.findAll("li", attrs={"class": "prep-step"})
        return (
            "\n".join(normalize_string(instr.get_text()) for instr in instructions)
            if instructions
            else None
        )
