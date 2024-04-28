import re
import unittest
from typing import List

from recipe_scrapers import SCRAPERS

SEPARATOR = "Scrapers available for:"


def get_documented_scrapers() -> List[str]:
    documented_scrapers = []
    with open("README.rst") as f:
        found = False
        for line in f:
            if line.strip() == SEPARATOR:
                found = True
                next(f)  # Skip the underline
            elif found and line.strip():
                match = re.search(r"^- `http(?:s)?:\/\/(?:www.)?([^\s\/]+)", line)
                if not match:
                    break

                domain = match.group(1)

                documented_scrapers.append(domain)

    return documented_scrapers


class TestReadme(unittest.TestCase):

    def test_includes(self):
        documented_scrapers = get_documented_scrapers()

        for scraper in SCRAPERS:
            match = re.search(r"(?:www.)?(.*)", scraper)
            domain = match.group(1)
            # If this test is failing, the scraper has not been added to the list in README.rst
            self.assertIn(domain, documented_scrapers)
