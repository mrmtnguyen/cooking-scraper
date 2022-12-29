import unittest
from typing import Any, Iterator, Optional, Tuple


class ScraperTest(unittest.TestCase):

    maxDiff = None
    test_file_name: Optional[str] = None
    test_file_extension = "testhtml"
    scraper_class: Any

    @classmethod
    def expected_requests(cls) -> Iterator[str]:
        """
        Descriptions of the expected requests that the scraper-under-test will make, as
        tuples of: HTTP method, URL, path-to-content-file
        """
        filename = cls.test_file_name or cls.scraper_class.__name__.lower()
        yield f"tests/test_data/{filename}.{cls.test_file_extension}"

    @classmethod
    def setUpClass(cls):
        start_url = f"https://{cls.scraper_class.host()}/"
        for path in cls.expected_requests():
            with open(path, encoding="utf-8") as f:
                html = f.read()

        cls.harvester_class = cls.scraper_class(url=start_url, html=html)
