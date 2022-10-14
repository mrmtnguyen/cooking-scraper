# mypy: allow-untyped-defs

from recipe_scrapers.weightwatchers import Weightwatchers
from tests import ScraperTest


class TestWeightwatchersScraper(ScraperTest):

    scraper_class = Weightwatchers

    def test_host(self):
        self.assertEqual("weightwatchers.de", self.harvester_class.host())

    def test_author(self):
        self.assertEqual("WeightWatchers", self.harvester_class.author())

    def test_title(self):
        self.assertEqual(self.harvester_class.title(), "Würstchengulasch mit Nudeln")

    def test_category(self):
        self.assertEqual("WeightWatchers", self.harvester_class.category())

    def test_total_time(self):
        self.assertEqual(25, self.harvester_class.total_time())

    def test_cook_time(self):
        self.assertEqual(0, self.harvester_class.cook_time())

    def test_prep_time(self):
        self.assertEqual(25, self.harvester_class.prep_time())

    def test_yields(self):
        self.assertEqual("2 servings", self.harvester_class.yields())

    # def test_image(self):
    #    self.assertEqual(None, self.harvester_class.image())

    # def test_ingredients(self):
    #    self.assertEqual(None, self.harvester_class.ingredients())

    # def test_instructions(self):
    #    self.assertEqual(None, self.harvester_class.instructions())

    # def test_ratings(self):
    #    self.assertEqual(None, self.harvester_class.ratings())

    # def test_cuisine(self):
    #    self.assertEqual(None, self.harvester_class.cuisine())

    def test_description(self):
        self.assertEqual(
            "18 Uhr und alle haben Hunger? Dann koche rasch das Würstchengulasch und alle sind happy.",
            self.harvester_class.description(),
        )

    def test_difficulty(self):
        self.assertEqual("Leicht", self.harvester_class.difficulty())