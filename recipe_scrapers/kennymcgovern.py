# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper
from ._utils import normalize_string


class KennyMcGovern(AbstractScraper):
    @classmethod
    def host(cls):
        return "kennymcgovern.com"

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    def instructions(self):
        instructions = self.soup.findAll(
            "div", {"class": "wprm-recipe-instruction-text"}
        )

        return "\n".join(
            [normalize_string(instruction.get_text()) for instruction in instructions]
        )
