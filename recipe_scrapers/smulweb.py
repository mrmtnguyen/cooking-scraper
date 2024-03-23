# mypy: allow-untyped-defs

import re

from ._abstract import AbstractScraper


class Smulweb(AbstractScraper):
    instruction_delimiter = re.compile(r"(\.|\))\s*([A-Z])")

    @classmethod
    def host(cls):
        return "smulweb.nl"

    def instructions(self):
        schema_instructions = self.schema.instructions()
        return self.instruction_delimiter.sub(r"\1\n\2", schema_instructions)


    def description(self):
        return self.schema.description()
